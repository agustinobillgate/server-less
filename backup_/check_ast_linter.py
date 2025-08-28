import ast
import os
import sys
import tokenize
import builtins
import datetime
from io import BytesIO
from typing import List, Dict, Set, Optional
from dataclasses import dataclass

# ===== Settings =====
folder_py = "../functions_py"   # change to ".." to scan the whole repo
output_dir = "./output/ast/"
output_file = "lint_report_ALL.txt"
separator = "\n" + "=" * 100 + "\n"

os.makedirs(output_dir, exist_ok=True)
combined_output_path = os.path.join(output_dir, output_file)


# ===== Helpers =====
@dataclass
class LintMessage:
    code: str      # e.g. "E111", "F821"
    msg: str       # human readable
    line: int
    col: int

    def __str__(self):
        return f"{self.line}:{self.col} {self.code} {self.msg}"


NOW = lambda: datetime.datetime.now().isoformat(timespec="seconds")
BUILTIN_NAMES = set(dir(builtins))
IGNORED_UNUSED = {"_", "__", "self", "cls"}

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ===== Indentation / token checks =====
def token_lint(src: str) -> List[LintMessage]:
    """
    - Detect TabError/SyntaxError during tokenization
    - Mixed indentation: lines with both leading tabs and spaces in the file
    """
    msgs: List[LintMessage] = []
    try:
        # Try tokenizing to surface TabError early
        list(tokenize.tokenize(BytesIO(src.encode("utf-8")).readline))
    except tokenize.TokenError as e:
        # TokenError usually carries (msg, (line, col))
        text = e.args[0]
        if len(e.args) > 1 and isinstance(e.args[1], tuple):
            line, col = e.args[1][:2]
        else:
            line, col = (1, 0)
        # Use E999 to mimic flake8 "SyntaxError-like" bucket
        msgs.append(LintMessage("E999", f"Tokenization error: {text}", line, col))
        return msgs
    except IndentationError as e:
        msgs.append(LintMessage("E111", f"Indentation error: {e.msg}", e.lineno or 1, (e.offset or 0)))
        return msgs
    except TabError as e:
        msgs.append(LintMessage("E101", f"Tab error: {e}", 1, 0))
        return msgs

    # Mixed indentation detector: warn if the file has both tabs and spaces at line starts
    has_tab_indent = False
    has_space_indent = False
    for i, line in enumerate(src.splitlines(), start=1):
        if not line.strip():
            continue
        # Leading whitespace only
        leading = line[: len(line) - len(line.lstrip())]
        if not leading:
            continue
        if "\t" in leading:
            has_tab_indent = True
        if leading and all(ch == " " for ch in leading):
            has_space_indent = True

    if has_tab_indent and has_space_indent:
        msgs.append(LintMessage("E101", "Mixed indentation (tabs and spaces)", 1, 0))

    return msgs


# ===== Scope model for variable analysis =====
class Scope:
    def __init__(self, kind: str, parent: Optional["Scope"] = None):
        self.kind = kind
        self.parent = parent
        self.assigned: Set[str] = set()
        self.used: Set[str] = set()
        self.params: Set[str] = set()
        self.globals: Set[str] = set()
        self.nonlocals: Set[str] = set()
        self.imported: Set[str] = set()
        # First definition line for better messages
        self.first_def_line: Dict[str, int] = {}

    def root(self) -> "Scope":
        s = self
        while s.parent:
            s = s.parent
        return s

    def resolve_has(self, name: str) -> bool:
        if name in self.globals:
            r = self.root()
            return (name in r.assigned) or (name in r.params) or (name in r.imported)
        if name in self.nonlocals:
            p = self.parent
            while p and p.kind == "module":
                p = p.parent
            if p:
                return (name in p.assigned) or (name in p.params) or (name in p.imported) or p.resolve_has(name)
            return False

        if name in self.assigned or name in self.params or name in self.imported:
            return True
        return self.parent.resolve_has(name) if self.parent else False


class VarLinter(ast.NodeVisitor):
    """
    Emits VSCode-like red-underlines:
      - F821 undefined name
      - F401 imported but unused
      - F841 local variable assigned but never used
      - ARG001 duplicate function arg names
      - A001 builtin shadowed by assignment/def
    """
    def __init__(self):
        self.scope = Scope("module", None)
        self.messages: List[LintMessage] = []
        # remember duplicate args per function
        self._arg_seen_stack: List[Set[str]] = []

    def push(self, kind: str):
        self.scope = Scope(kind, self.scope)
        self._arg_seen_stack.append(set())

    def pop(self):
        self._arg_seen_stack.pop()
        self.scope = self.scope.parent  # type: ignore

    # ---- helpers ----
    def add(self, code: str, msg: str, node: ast.AST, col_bias: int = 0):
        line = getattr(node, "lineno", 1)
        col = max(0, getattr(node, "col_offset", 0) + col_bias)
        self.messages.append(LintMessage(code, msg, line, col))

    def mark_assign(self, name: str, node: ast.AST):
        self.scope.assigned.add(name)
        self.scope.first_def_line.setdefault(name, getattr(node, "lineno", 0))
        if name in BUILTIN_NAMES:
            self.add("A001", f"Variable '{name}' shadows a Python builtin", node)

    def mark_import(self, name: str, node: ast.AST):
        self.scope.imported.add(name)
        self.scope.first_def_line.setdefault(name, getattr(node, "lineno", 0))
        if name in BUILTIN_NAMES:
            self.add("A001", f"Import '{name}' shadows a Python builtin", node)

    def mark_used(self, name: str, node: ast.AST):
        if name in IGNORED_UNUSED:
            return
        self.scope.used.add(name)
        if (name not in BUILTIN_NAMES) and (not self.scope.resolve_has(name)):
            self.add("F821", f"Undefined name '{name}'", node)

    # ---- nodes ----
    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store):
            self.mark_assign(node.id, node)
        elif isinstance(node.ctx, ast.Load):
            self.mark_used(node.id, node)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            asname = alias.asname or alias.name.split(".")[0]
            self.mark_import(asname, node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "__future__":
            return
        for alias in node.names:
            if alias.name == "*":
                # can't safely analyze star imports; skip but warn
                self.add("F406", "Star import; name resolution may be incorrect", node)
                continue
            asname = alias.asname or alias.name
            self.mark_import(asname, node)

    def _collect_args(self, args: ast.arguments, where: ast.AST):
        seen = self._arg_seen_stack[-1]
        all_args = list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs)
        if args.vararg:
            all_args.append(args.vararg)
        if args.kwarg:
            all_args.append(args.kwarg)

        for a in all_args:
            name = a.arg
            if name in seen:
                self.add("ARG001", f"Duplicate function argument '{name}'", a)
            seen.add(name)
            self.scope.params.add(name)
            self.scope.first_def_line.setdefault(name, getattr(a, "lineno", 0))
            if name in BUILTIN_NAMES:
                self.add("A001", f"Parameter '{name}' shadows a Python builtin", a)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # function name bound in outer scope
        self.mark_assign(node.name, node)
        # enter function
        self.push("function")
        self._collect_args(node.args, node)
        self.generic_visit(node)
        self._report_unused_locals()
        self.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.mark_assign(node.name, node)
        self.push("class")
        self.generic_visit(node)
        self.pop()

    def visit_Global(self, node: ast.Global):
        for n in node.names:
            self.scope.globals.add(n)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for n in node.names:
            self.scope.nonlocals.add(n)

    # comprehensions are their own scope in Py3
    def _visit_comp_scope(self, node: ast.AST):
        self.push("comprehension")
        self.generic_visit(node)
        self._report_unused_locals()
        self.pop()

    def visit_ListComp(self, node: ast.ListComp): self._visit_comp_scope(node)
    def visit_SetComp(self, node: ast.SetComp): self._visit_comp_scope(node)
    def visit_DictComp(self, node: ast.DictComp): self._visit_comp_scope(node)
    def visit_GeneratorExp(self, node: ast.GeneratorExp): self._visit_comp_scope(node)

    # ---- after-scope checks ----
    def _report_unused_locals(self):
        unused = (self.scope.assigned | self.scope.params | self.scope.imported) - self.scope.used - IGNORED_UNUSED
        for name in sorted(unused):
            line = self.scope.first_def_line.get(name, 1)
            if name in self.scope.imported:
                self.messages.append(LintMessage("F401", f"'{name}' imported but unused", line, 0))
            elif name in self.scope.params:
                self.messages.append(LintMessage("F841", f"Parameter '{name}' assigned but never used", line, 0))
            else:
                self.messages.append(LintMessage("F841", f"Local variable '{name}' assigned but never used", line, 0))


def lint_variables(tree: ast.AST) -> List[LintMessage]:
    v = VarLinter()
    v.visit(tree)
    return v.messages


# ===== File lint pipeline =====
def lint_file(path: str) -> List[LintMessage]:
    msgs: List[LintMessage] = []
    try:
        src = read_text(path)
    except Exception as e:
        msgs.append(LintMessage("E000", f"Could not read file: {e}", 1, 0))
        return msgs

    # 1) token-level (indent/mixed)
    msgs.extend(token_lint(src))
    # If tokenization/indent error exists, further parsing will likely fail noisily; still try parse
    if any(m.code in {"E111", "E101", "E999"} for m in msgs):
        # continue to parse anyway; parser can give sharper location for real SyntaxError
        pass

    # 2) AST parse
    try:
        tree = ast.parse(src, filename=path)
    except IndentationError as e:
        msgs.append(LintMessage("E111", f"Indentation error: {e.msg}", e.lineno or 1, (e.offset or 0)))
        return msgs
    except TabError as e:
        msgs.append(LintMessage("E101", f"Tab error: {e}", 1, 0))
        return msgs
    except SyntaxError as e:
        msgs.append(LintMessage("E999", f"SyntaxError: {e.msg}", e.lineno or 1, (e.offset or 0)))
        return msgs

    # 3) Variable analysis
    msgs.extend(lint_variables(tree))
    # Sort messages by (line, col, code)
    msgs.sort(key=lambda m: (m.line, m.col, m.code))
    return msgs


# ===== Directory walk & report =====
def iter_py_files(root_dir: str):
    for base, _, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith(".py"):
                yield os.path.join(base, fname)

def write_report_for_file(path: str) -> str:
    rel = os.path.relpath(path, start=folder_py)
    header = [
        separator,
        f"FILE: {path}",
        f"RELATIVE: {rel}",
        f"ANALYZED AT: {NOW()}",
        "-" * 100
    ]
    msgs = lint_file(path)
    if not msgs:
        body = ["No issues found."]
    else:
        body = [str(m) for m in msgs]
    return "\n".join(header + body + [separator])

def main():
    with open(combined_output_path, "w", encoding="utf-8") as f:
        f.write("Python Indentation & Variable Lint Report\n")
        f.write(f"Root scanned: {os.path.abspath(folder_py)}\n")
        f.write(f"Generated: {NOW()}\n")
        f.write(separator)

    count = 0
    for py in iter_py_files(folder_py):
        section = write_report_for_file(py)
        with open(combined_output_path, "a", encoding="utf-8") as f:
            f.write(section)
        count += 1

    with open(combined_output_path, "a", encoding="utf-8") as f:
        f.write(f"\nAnalyzed {count} file(s).\n")

    print(f"Done. Report -> {combined_output_path}")

if __name__ == "__main__":
    main()
