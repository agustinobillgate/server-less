import os
import ast
import datetime


folder_py = "../functions_py"
output_dir = "./output/ast/"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "parse_errors.txt")

def safe_parse_file(path: str):
    """Try parsing Python source. Return error info dict if failed."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        ast.parse(src, filename=path)
        return None  # OK
    except (NameError, TypeError, IndexError, ValueError) as e:
        # Collect extra context to make a good, VS Code–like message
        try:
            with open(path, "r", encoding="utf-8") as f:
                src_for_line = f.read().splitlines()
        except Exception:
            src_for_line = []

        lineno = getattr(e, "lineno", None) or 0
        offset = getattr(e, "offset", None) or 0
        line_text = src_for_line[lineno - 1] if 1 <= lineno <= len(src_for_line) else ""
        return {
            "file": path,
            "type": e.__class__.__name__,
            "msg": getattr(e, "msg", str(e)),
            "lineno": lineno,
            "offset": offset,
            "line_text": line_text,
        }
    except (SyntaxError, IndentationError, TabError) as e:
        try:
            src_lines = open(path, "r", encoding="utf-8").read().splitlines()
        except Exception:
            src_lines = []
        lineno = getattr(e, "lineno", 0) or 0
        offset = getattr(e, "offset", 0) or 0
        line_text = src_lines[lineno - 1] if 1 <= lineno <= len(src_lines) else ""
        return {
            "file": path,
            "type": e.__class__.__name__,
            "msg": getattr(e, "msg", str(e)),
            "lineno": lineno,
            "offset": offset,
            "line_text": line_text,
        }
    except Exception as e:
        return {
            "file": path,
            "type": "UnexpectedError",
            "msg": str(e),
            "lineno": 0,
            "offset": 0,
            "line_text": "",
        }

def format_error_block(path: str, err: dict) -> str:
    """
    Pretty print parse error with file:line:col, message,
    the problematic line, and a caret under the column.
    """
    line = err.get("lineno", 0)
    col = err.get("offset", 0)
    typ = err.get("type", "Error")
    msg = err.get("message", "")
    text = err.get("line_text", "")

    caret_col = max(0, col - 1)  # convert to 0-based for spacing
    caret_line = (" " * caret_col) + "^" if text else ""

    header = f"{path}:{line}:{col} {typ}: {msg}"
    snippet = text if text else "<no line available>"
    return "\n".join([header, snippet, caret_line])
def format_error(err: dict) -> str:
    caret_col = max(0, err["offset"] - 1)
    caret_line = (" " * caret_col + "^") if err["line_text"] else ""
    header = f"{err['file']}:{err['lineno']}:{err['offset']} {err['type']}: {err['msg']}"
    return "\n".join([header, err["line_text"], caret_line, "=" * 100])

def iter_py_files(root):
    for base, _, files in os.walk(root):
        for fname in files:
            if fname.endswith(".py"):
                yield os.path.join(base, fname)

def main():
    errors = []
    for pyfile in iter_py_files(folder_py):
        err = safe_parse_file(pyfile)
        if err:
            errors.append(err)

    if errors:
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(f"AST Parse Errors Report\nGenerated: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
            out.write("=" * 100 + "\n")
            for e in errors:
                out.write(format_error(e) + "\n")
        print(f"Found {len(errors)} file(s) with errors. Report written to {output_path}")
    else:
        print("No parse errors found.")

if __name__ == "__main__":
    main()