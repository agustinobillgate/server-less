import os
import ast
import datetime

# ========= Settings =========
folder_py = "../functions_py"   # set to ".." to scan the whole project
output_dir = "./output/ast/"
os.makedirs(output_dir, exist_ok=True)

parse_errors_path = os.path.join(output_dir, "parse_errors.txt")
time_calc_report_path = os.path.join(output_dir, "time_calc_usages.txt")

# ========= Helpers =========
def norm(p: str) -> str:
    return os.path.normpath(os.path.abspath(p))

def iter_py_files(root):
    root = norm(root)
    for base, _, files in os.walk(root):
        for fname in files:
            if fname.lower().endswith(".py"):
                yield norm(os.path.join(base, fname))

# ========= Safe parse =========
def safe_parse_file(path: str):
    """Try parsing Python source. Return error info dict if failed; else None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        ast.parse(src, filename=path)
        return None  # OK
    except (SyntaxError, IndentationError, TabError) as e:
        try:
            src_lines = open(path, "r", encoding="utf-8").read().splitlines()
        except Exception:
            src_lines = []
        lineno = getattr(e, "lineno", 0) or 0
        offset = getattr(e, "offset", 0) or 0
        line_text = src_lines[lineno - 1] if 1 <= lineno <= len(src_lines) else ""
        return {
            "file": norm(path),
            "type": e.__class__.__name__,
            "msg": getattr(e, "msg", str(e)),
            "lineno": lineno,
            "offset": offset,
            "line_text": line_text,
        }
    except Exception as e:
        return {
            "file": norm(path),
            "type": "UnexpectedError",
            "msg": str(e),
            "lineno": 0,
            "offset": 0,
            "line_text": "",
        }

def format_parse_error(err: dict) -> str:
    caret_col = max(0, err["offset"] - 1)
    caret_line = (" " * caret_col + "^") if err["line_text"] else ""
    header = f"{err['file']}:{err['lineno']}:{err['offset']} {err['type']}: {err['msg']}"
    return "\n".join([header, err["line_text"], caret_line, "=" * 100])

# ========= Time range usage finder =========
class TimeCalcFinder(ast.NodeVisitor):
    """
    Detect common date range / timedelta patterns:
      - datetime.timedelta(...), or from-import 'timedelta(...)'
      - pandas.date_range(...), or from-import 'date_range(...)'
      - pandas DateOffset(...) and offsets (MonthEnd, BDay, etc.), via alias or from-import
      - dateutil.relativedelta.relativedelta(...), or from-import 'relativedelta(...)'
      - NEW: Generic calls to 'timedelta' and string literals containing 'timedelta'
    """
    PANDAS_OFFSETS = {
        "DateOffset", "BDay", "BusinessDay", "CBMonthEnd", "CBMonthBegin",
        "Day", "Hour", "Minute", "Second", "Milli", "Micro", "Nano",
        "MonthBegin", "MonthEnd", "BMonthBegin", "BMonthEnd",
        "QuarterBegin", "QuarterEnd", "YearBegin", "YearEnd", "FY5253",
        "Week", "WeekOfMonth", "LastDayOfMonth"
    }

    def __init__(self):
        super().__init__()
        # Module aliases
        self.datetime_aliases = set()    # e.g., {"datetime", "dt"}
        self.pandas_aliases = set()      # e.g., {"pandas", "pd"}

        # Directly imported callables / classes (for bare-name calls)
        self.timedelta_names = set()         # {"timedelta", "td"...}
        self.date_range_names = set()        # {"date_range", "dr"...}
        self.offset_names = set()            # {"DateOffset", "MonthEnd", ...}
        self.relativedelta_names = set()     # {"relativedelta", "rd"...}

        self.findings = []  # list[(line, desc, preview)]
        self._src_lines = []

    def set_source(self, src_text: str):
        self._src_lines = src_text.splitlines()

    def _line_text(self, node):
        ln = getattr(node, "lineno", 0)
        if 1 <= ln <= len(self._src_lines):
            return self._src_lines[ln - 1].rstrip("\n")
        return ""

    # --- imports ---
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            mod = alias.name
            asname = alias.asname or mod
            base = asname.split(".")[0]
            if mod == "datetime":
                self.datetime_aliases.add(base)
            elif mod == "pandas":
                self.pandas_aliases.add(base)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "datetime":
            for alias in node.names:
                if alias.name == "timedelta":
                    self.timedelta_names.add(alias.asname or "timedelta")
        elif node.module == "pandas":
            for alias in node.names:
                if alias.name == "date_range":
                    self.date_range_names.add(alias.asname or "date_range")
                if alias.name in self.PANDAS_OFFSETS:
                    self.offset_names.add(alias.asname or alias.name)
        elif node.module and node.module.startswith("pandas.tseries.offsets"):
            for alias in node.names:
                self.offset_names.add(alias.asname or alias.name)
        elif node.module == "dateutil.relativedelta":
            for alias in node.names:
                if alias.name == "relativedelta":
                    self.relativedelta_names.add(alias.asname or "relativedelta")
        self.generic_visit(node)

    # --- strings ---
    def visit_Constant(self, node: ast.Constant):
        # NEW: Find string literals that contain 'timedelta'
        if isinstance(node.value, str) and 'timedelta' in node.value.lower():
            self._add(node, "String literal containing 'timedelta'")
        self.generic_visit(node)

    # --- calls ---
    def visit_Call(self, node: ast.Call):
        func = node.func
        
        # A) Handle direct name calls like `timedelta(...)` or `date_range(...)`
        if isinstance(func, ast.Name):
            func_id = func.id
            # 1. Imported timedelta
            if func_id in self.timedelta_names:
                self._add(node, f"timedelta(...) from datetime import: {func_id}")
            # 2. NEW: Generic timedelta call (unverified source)
            elif func_id == 'timedelta':
                self._add(node, f"Generic call to function named 'timedelta': {func_id}(...)")
            # 3. Pandas date_range
            elif func_id in self.date_range_names:
                self._add(node, f"date_range(...) call: {func_id}")
            # 4. Pandas offsets
            elif func_id in self.offset_names:
                self._add(node, f"pandas offset call: {func_id}(...)")
            # 5. dateutil relativedelta
            elif func_id in self.relativedelta_names:
                self._add(node, f"relativedelta(...) call: {func_id}")

        # B) Handle attribute calls like `dt.timedelta(...)` or `pd.date_range(...)`
        if isinstance(func, ast.Attribute):
            attr_name = func.attr
            # 1. datetime.timedelta
            if attr_name == 'timedelta':
                base = self._attr_base_name(func)
                if base in self.datetime_aliases or base == "datetime":
                    self._add(node, f"datetime.timedelta(...) call: {self._call_name(func)}")
                # NEW: Generic attribute call (unverified source)
                else:
                    self._add(node, f"Generic attribute call to '.timedelta': {self._call_name(func)}(...)")
            # 2. pandas.date_range
            elif attr_name == 'date_range':
                base = self._attr_base_name(func)
                if base in self.pandas_aliases or base == "pandas":
                    self._add(node, f"pandas.date_range(...) call: {self._call_name(func)}")
            # 3. pandas.DateOffset
            elif attr_name == 'DateOffset':
                base = self._attr_base_name(func)
                if base in self.pandas_aliases or base == "pandas":
                    self._add(node, f"pandas.DateOffset(...) call: {self._call_name(func)}")
            # 4. dateutil.relativedelta
            elif attr_name == 'relativedelta':
                self._add(node, f"dateutil.relativedelta.relativedelta(...) call: {self._call_name(func)}")

        self.generic_visit(node)

    # --- helpers ---
    def _attr_base_name(self, attr: ast.Attribute) -> str:
        obj = attr.value
        while isinstance(obj, ast.Attribute):
            obj = obj.value
        return obj.id if isinstance(obj, ast.Name) else ""

    def _call_name(self, func) -> str:
        if isinstance(func, ast.Name):
            return func.id
        parts = []
        cur = func
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        parts.reverse()
        return ".".join(parts) if parts else type(func).__name__

    def _add(self, node: ast.AST, desc: str):
        ln = getattr(node, "lineno", 0)
        self.findings.append((ln, desc, self._line_text(node)))

def find_time_usages(py_path: str):
    try:
        with open(py_path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src, filename=py_path)
    except Exception:
        return []  # parse errors handled elsewhere
    finder = TimeCalcFinder()
    finder.set_source(src)
    finder.visit(tree)
    return finder.findings

# ========= Main =========
def main():
    all_files = list(iter_py_files(folder_py))
    print(f"Scanning {len(all_files)} Python files under {norm(folder_py)}")

    # Pass 1: parse errors
    parse_errors = []
    for pyfile in all_files:
        err = safe_parse_file(pyfile)
        if err:
            parse_errors.append(err)

    if parse_errors:
        with open(parse_errors_path, "w", encoding="utf-8") as out:
            out.write(f"AST Parse Errors Report\nGenerated: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
            out.write("=" * 100 + "\n")
            for e in parse_errors:
                out.write(format_parse_error(e) + "\n")
        print(f"Found {len(parse_errors)} file(s) with parse errors. -> {parse_errors_path}")
    else:
        print("No parse errors found.")

    error_files = {e["file"] for e in parse_errors}

    # Pass 2: time calc usages (only on files that parsed OK)
    time_hits = {}  # file -> list[(line, desc, preview)]
    for pyfile in all_files:
        if norm(pyfile) in error_files:
            continue
        hits = find_time_usages(pyfile)
        if hits:
            time_hits[pyfile] = hits

    if time_hits:
        with open(time_calc_report_path, "w", encoding="utf-8") as out:
            out.write(f"Time Range / Timedelta Usage Report\nGenerated: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
            out.write("=" * 100 + "\n")
            for path, items in sorted(time_hits.items()):
                out.write(f"FILE: {path}\n")
                for ln, desc, preview in items:
                    out.write(f"  {ln}: {desc}\n")
                    if preview:
                        out.write(f"      {preview}\n")
                out.write("-" * 100 + "\n")
        print(f"Found time-range logic in {len(time_hits)} file(s). -> {time_calc_report_path}")
    else:
        print("No timedelta/date_range/relativedelta usages found.")

    print(f"Done. Scanned: {len(all_files)} file(s). OK for time-scan: {len(all_files) - len(error_files)} file(s).")

if __name__ == "__main__":
    main()