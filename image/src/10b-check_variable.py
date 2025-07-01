import ast, os, sys

class VariableVisitor(ast.NodeVisitor):
    def __init__(self, ignore_list):
        self.defined_variables = set()
        self.undeclared_variables = {}
        self.ignore_list = set(ignore_list)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_variables.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Skip checking if the variable is in the ignore list
        if isinstance(node.ctx, ast.Load) and node.id not in self.defined_variables and node.id not in self.ignore_list:
            if node.id not in self.undeclared_variables:
                self.undeclared_variables[node.id] = []
            self.undeclared_variables[node.id].append(node.lineno)

def find_undeclared_variables(filename, ignore_list):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)

    visitor = VariableVisitor(ignore_list)
    visitor.visit(tree)

    return visitor.undeclared_variables

def get_ignore_list(file_path):
    """Reads the ignore list from a text file."""
    with open(file_path, 'r') as file:
        ignore_list = [line.strip() for line in file if line.strip()]
    return ignore_list

if __name__ == "__main__":
    # List of variables to ignore
    if len(sys.argv) <= 1:
        print("No arguments were passed.")
    else:
        arg1 = sys.argv[1]
        ignore_list = ['buffer_copy', 
                    'local_storage', 
                    'int', 'to_string', 'generate_output',
                    'create_model_like', 
                    'func', 'str', 'bool', 'date'
                    ]  # Add any variables you want to ignore

        
        # filename = f'D:/docker/pixcdk/image/src/functions/mk_po_btn_val_chg_currencybl.py'  # hk_ooo_remove_selected_data_webbl, main_gl_mi_reportbl
        folder_py = f"D:/docker/pixcdk/image/src/functions"
        filename = f"{folder_py}/{arg1}"  # hk_ooo_remove_selected_data_webbl, main_gl_mi_reportbl
        file_py = os.path.basename(filename)
        ignore_list_path = f"D:/docker/pixcdk/image/src/output/qc/kw/keywords_{file_py}.txt"
        ignore_list = ignore_list + get_ignore_list(ignore_list_path)
        undeclared_vars = find_undeclared_variables(filename, ignore_list)

        if undeclared_vars:
            print("Undeclared variables:\n--------------------------")
            for var, lines in undeclared_vars.items():
                if var not in ignore_list:
                    print(f"{var}: lines {', '.join(map(str, lines))}")
        else:
            print("No undeclared variables found.")
