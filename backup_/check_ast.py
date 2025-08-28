import ast
import os
import time
from typing import List, Dict
# from analyze_loops import analyze_file
from datetime import datetime
import datetime

class SQLAlchemyAnalyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.queries = []
        self.total_lines = self.get_line_count()

    def get_line_count(self):
        """Get the total number of lines in the file."""
        with open(self.filename, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def visit_Call(self, node):
        """Analyze function calls for SQLAlchemy queries."""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "query":  # Detect session.query(Model)
                table = self.get_node_name(node.args[0]) if node.args else "unknown"
                filters = []
                final_method = None

                parent = node
                while isinstance(parent, ast.Attribute):  # Check for chained calls
                    if parent.attr in {"filter", "filter_by"}:  # Extract filters
                        filters.extend(self.extract_filters(parent))
                    elif parent.attr in {"all", "first", "one"}:  # Extract query type
                        final_method = parent.attr
                    parent = parent.value if isinstance(parent, ast.Attribute) else None

                self.queries.append({
                    "table": table,
                    "filters": filters,
                    "query_type": final_method or "unknown",
                    "line": node.lineno
                })

        self.generic_visit(node)

    def extract_filters(self, node):
        """Extract filter conditions from SQLAlchemy filter() calls."""
        if isinstance(node, ast.Call):
            return [self.get_filter_expr(arg) for arg in node.args]
        return []

    def get_filter_expr(self, node):
        """Convert a filter condition AST node into a readable expression."""
        if isinstance(node, ast.Compare):  # e.g., User.id == 1
            left = self.get_node_name(node.left)
            op = self.get_operator(node.ops[0])
            right = self.get_node_name(node.comparators[0])
            return f"{left} {op} {right}"
        return "unknown"

    def get_operator(self, op):
        """Map AST comparison operators to symbols."""
        operators = {
            ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<", ast.LtE: "<=",
            ast.Gt: ">", ast.GtE: ">=", ast.In: "IN", ast.NotIn: "NOT IN"
        }
        return operators.get(type(op), "?")

    def get_node_name(self, node):
        """Extracts a readable name from AST nodes."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):  # e.g., User.id
            return f"{self.get_node_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return "unknown"

    def analyze(self):
        """Parse the file and analyze queries."""
        with open(self.filename, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        self.visit(tree)

        output = [f"File: {self.filename}"]
        output.append(f"Total Lines: {self.total_lines}")
        output.append("Database Queries Found:\n" + "-"*40)

        for query in self.queries:
            output.append(
                f"Line {query['line']}: Query on {query['table']}, "
                f"Filters: {', '.join(query['filters']) if query['filters'] else 'None'}, "
                f"Method: {query['query_type']}"
            )

        return "\n".join(output)

def analyze_sqlalchemy_queries(filename):
    analyzer = SQLAlchemyAnalyzer(filename)
    result = analyzer.analyze()
    
    output_dir = "output/ast"
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = f"query_analysis_{os.path.basename(filename)}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Analysis saved to {output_path}")

class LoopVisitor(ast.NodeVisitor):
    def __init__(self):
        self.loops = []
        self.current_function = None
        self.outputs = []
        self.depth = 0
        
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function

    def visit_Assign(self, node):
        # Look for assignments with get_output calls
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'get_output':
            args = []
            for arg in node.value.args:
                if isinstance(arg, ast.Call):
                    args.append(ast.unparse(arg))
            
            self.outputs.append({
                'function': self.current_function,
                'line': node.lineno,
                'type': 'call',
                'args': args,
                'targets': [ast.unparse(target) for target in node.targets]
            })
        self.generic_visit(node)

    def visit_For(self, node):
        self.depth += 1
        
        # Find any get_output calls inside this loop's body
        output_calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Assign) and isinstance(child.value, ast.Call):
                if isinstance(child.value.func, ast.Name) and child.value.func.id == 'get_output':
                    args = []
                    for arg in child.value.args:
                        if isinstance(arg, ast.Call):
                            args.append(ast.unparse(arg))
                    
                    output_calls.append({
                        'line': child.lineno,
                        'args': args,
                        'targets': [ast.unparse(target) for target in child.targets]
                    })
        
        loop_type = "standard"
        if isinstance(node.iter, ast.Call):
            if hasattr(node.iter.func, 'attr') and node.iter.func.attr == 'query':
                loop_type = "database_query"
            elif isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'query':
                loop_type = "query_function"
            elif hasattr(node.iter.func, 'attr') and node.iter.func.attr == 'all':
                loop_type = "database_all"
        elif isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
            loop_type = "range"
            
        loop_info = {
            'type': loop_type,
            'line': node.lineno,
            'function': self.current_function,
            'target': ast.unparse(node.target),
            'iter': ast.unparse(node.iter),
            'body_length': len(node.body),
            'has_break': any(isinstance(n, ast.Break) for n in ast.walk(node)),
            'has_continue': any(isinstance(n, ast.Continue) for n in ast.walk(node)),
            'depth': self.depth,
            'output_calls': output_calls  # Add output calls to loop info
        }
        self.loops.append(loop_info)
        self.generic_visit(node)
        self.depth -= 1

def analyze_file(file_path: str) -> tuple[List[Dict], List[Dict]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tree = ast.parse(content)
    visitor = LoopVisitor()
    visitor.visit(tree)
    return visitor.loops, visitor.outputs

def write_analysis_to_file(loops: List[Dict], outputs: List[Dict], input_file: str, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Loop and Output Function Analysis\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"File: {input_file}\n")
        f.write("=" * 80 + "\n\n")
        
        current_function = None
        for loop in loops:
            if loop['function'] != current_function:
                if current_function is not None:
                    f.write("\n")
                current_function = loop['function']
                f.write(f"Function: {current_function}\n")
                f.write("=" * 50 + "\n")
            
            indent = "    " * loop['depth']
            f.write(f"{indent}└─ Loop_{loop['depth']} (line {loop['line']}) - {loop['type']}\n")
            f.write(f"{indent}   ├─ Target: {loop['target']}\n")
            f.write(f"{indent}   ├─ Iterator: {loop['iter']}\n")
            
            # Add get_output calls inside the loop information
            if loop['output_calls']:
                for call in loop['output_calls']:
                    f.write(f"{indent}   ├─ get_output() at line {call['line']}:\n")
                    f.write(f"{indent}   │  --get_output ")
                    for arg in call['args']:
                        f.write(f"'{arg}'\n{indent}   │  ")
                    f.write(f"Assigns to: {', '.join(call['targets'])}\n")
            
            f.write("\n")
        
        f.write("\nSummary:\n")
        f.write(f"Total loops: {len(loops)}\n")
        f.write(f"Total get_output calls: {len(outputs)}\n")
        
        # Count by loop type
        loop_types = {}
        for loop in loops:
            loop_types[loop['type']] = loop_types.get(loop['type'], 0) + 1
        
        f.write("\nLoop types found:\n")
        for type_name, count in loop_types.items():
            f.write(f"- {type_name}: {count}\n")

# # Main execution
# script_path = "../functions_py/supply_hinlist_btn_go_1_webbl.py"
# output_dir = "./output/ast/"
# os.makedirs(output_dir, exist_ok=True)

# # Get the script name without extension and create output filename
# script_name = os.path.splitext(os.path.basename(script_path))[0]
# output_path = os.path.join(output_dir, f"loop_analysis_{script_name}.txt")

# if os.path.exists(script_path):
#     try:
#         loops, outputs = analyze_file(script_path)
#         write_analysis_to_file(loops, outputs, script_path, output_path)
#         print(f"Analysis completed. Results written to {output_path}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
# else:
#     print(f"File not found: {script_path}")

# # Remove duplicate script_path assignment
# analyze_sqlalchemy_queries(script_path)


# ========= Settings =========
folder_py = "../functions_py"   # change to ".." if you want to scan the whole repo root
output_dir = "./output/ast/"
combined_filename = "loop_analysis_ALL.txt"
separator = "\n" + "="*100 + "\n"

os.makedirs(output_dir, exist_ok=True)
combined_output_path = os.path.join(output_dir, combined_filename)

def safe_str(obj):
    """Make best-effort string without blowing up on weird objects."""
    try:
        return str(obj)
    except Exception:
        try:
            return repr(obj)
        except Exception:
            return "<unprintable>"

def analyze_single_file(file_path):
    """
    Calls user-provided analysis helpers if available:
      - analyze_file(file_path) -> (loops, outputs)
      - analyze_sqlalchemy_queries(file_path) -> any
    Returns a string section to append to the consolidated report.
    """
    lines = []
    header = [
        separator,
        f"FILE: {file_path}",
        f"ANALYZED AT: {datetime.datetime.now().isoformat(timespec='seconds')}",
        "-"*100
    ]
    lines.extend(header)

    # 1) Loop & output analysis
    try:
        loops, outputs = analyze_file(file_path)  # expects your existing function
        lines.append("Loop Analysis (raw):")
        lines.append(safe_str(loops))
        lines.append("")
        lines.append("Outputs (raw):")
        lines.append(safe_str(outputs))
    except NameError:
        lines.append("WARN: analyze_file() is not defined in this runtime.")
    except Exception as e:
        lines.append(f"ERROR running analyze_file(): {e}")

    lines.append("-"*100)

    # 2) SQLAlchemy query analysis (optional)
    try:
        result = analyze_sqlalchemy_queries(file_path)  # expects your existing function
        lines.append("SQLAlchemy Query Analysis (raw):")
        lines.append(safe_str(result))
    except NameError:
        lines.append("NOTE: analyze_sqlalchemy_queries() not defined; skipping.")
    except Exception as e:
        lines.append(f"ERROR running analyze_sqlalchemy_queries(): {e}")

    lines.append(separator)
    return "\n".join(lines)

def iter_py_files(root_dir):
    """Yield absolute paths of .py files under root_dir, recursively."""
    for base, _, files in os.walk(root_dir):
        for fname in files:
            if fname.lower().endswith(".py"):
                yield os.path.join(base, fname)

def main():
    # Prepare report header
    with open(combined_output_path, "w", encoding="utf-8") as f:
        f.write(f"Consolidated Loop & Query Analysis Report\n")
        f.write(f"Root scanned: {os.path.abspath(folder_py)}\n")
        f.write(f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
        f.write(separator)

    # Walk and analyze each .py
    count = 0
    for py_path in iter_py_files(folder_py):
        section = analyze_single_file(py_path)
        with open(combined_output_path, "a", encoding="utf-8") as f:
            f.write(section)
        count += 1

    # Tail note
    with open(combined_output_path, "a", encoding="utf-8") as f:
        f.write(f"\nAnalyzed {count} Python file(s).\n")

    print(f"Analysis completed. Results written to {combined_output_path}")

if __name__ == "__main__":
    main()



