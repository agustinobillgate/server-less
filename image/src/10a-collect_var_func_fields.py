import ast, os, pkgutil, sys

combine_keyword = []
args_list = []
function_defs = []
wildcard_functions = []
variable_names = []
model_imports = []
model_fields = {}
create_model = []
def parse_python_file(file_path):

    try: # baca undeclare variable
        def visit_FunctionDef(node, defined_variables, current_function_params, undeclared_variables):
            # Collect parameters for the current function
            current_function_params.update(arg.arg for arg in node.args.args)
            for child in node.body:
                visit(child, defined_variables, current_function_params, undeclared_variables)
            current_function_params.clear()  # Clear after visiting the function

        def visit_Assign(node, defined_variables, undeclared_variables):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined_variables.add(target.id)
            # Visit the value of the assignment
            for value in ast.iter_child_nodes(node):
                visit(value, defined_variables, set(), undeclared_variables)

        def visit_Name(node, defined_variables, current_function_params, undeclared_variables):
            if isinstance(node.ctx, ast.Load) and node.id not in defined_variables:
                if node.id not in current_function_params:
                    if node.id not in undeclared_variables:
                        undeclared_variables[node.id] = []
                    undeclared_variables[node.id].append(node.lineno)

        def visit(node, defined_variables, current_function_params, undeclared_variables):
            if isinstance(node, ast.FunctionDef):
                visit_FunctionDef(node, defined_variables, current_function_params, undeclared_variables)
            elif isinstance(node, ast.Assign):
                visit_Assign(node, defined_variables, undeclared_variables)
            elif isinstance(node, ast.Name):
                visit_Name(node, defined_variables, current_function_params, undeclared_variables)
            else:
                for child in ast.iter_child_nodes(node):
                    visit(child, defined_variables, current_function_params, undeclared_variables)

        def find_undeclared_variables(file_path):
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read(), filename=file_path)

            defined_variables = set()
            undeclared_variables = {}
            current_function_params = set()
            
            visit(tree, defined_variables, current_function_params, undeclared_variables)
            
            return undeclared_variables
        
    except SyntaxError as e:
        print(f"Error: Syntax error in the file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}") 

    # ----------------------------------------
    try: # baca data yang ada/dikenal
        with open(file_path, "r") as file:
            code = file.read()

        # Parse the code into an AST
        tree = ast.parse(code)
        
        def find_functions_in_module(module_name):
            
            # Get the module path
            module = pkgutil.find_loader(module_name)
            if module is None:
                print(f"Module {module_name} not found.")
                
            # Load the module source code
            module_path = module.get_filename()
            if module_path.endswith('.py'):
                with open(module_path, 'r') as f:
                    source = f.read()

                # Parse the source code into an AST
                tree = ast.parse(source)

                # Find all function definitions in the module
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        wildcard_functions.append(node.name)

        def find_function_defs(node):
            if isinstance(node, ast.FunctionDef):
                function_defs.append(node.name)  # Capture function name
            for child in ast.iter_child_nodes(node):
                find_function_defs(child)
      
        def find_function_arguments(node):
            # Function to recursively find FunctionDef nodes
            def visit(node):
                if isinstance(node, ast.FunctionDef):
                    # Collect argument names for the current function
                    args_list.extend(arg.arg for arg in node.args.args)
                # Visit child nodes
                for child in ast.iter_child_nodes(node):
                    visit(child)

            visit(node)
        
        def find_variable_assignments(node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_names.append(target.id)  # Capture variable name
            for child in ast.iter_child_nodes(node):
                find_variable_assignments(child)

        def find_model_imports(node):
            # Function to recursively find ImportFrom nodes for 'models'
            def visit(node):
                if isinstance(node, ast.ImportFrom) and node.module == 'models':
                    model_imports.extend(alias.name for alias in node.names)
                # Visit child nodes
                for child in ast.iter_child_nodes(node):
                    visit(child)

            visit(node)
            
        #----------------------------------------------
        # collect table & field
        #----------------------------------------------
        
        def get_table_fields(file_path):
            fields = set()
            
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read(), filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for body_item in node.body:
                        if isinstance(body_item, ast.Assign):
                            for target in body_item.targets:
                                if isinstance(target, ast.Name):
                                    if (target.id).startswith('__') & (target.id).endswith('__'):
                                        pass
                                    else:
                                        fields.add(target.id)

            return fields

        def visit_model(node, model_fields):
            if isinstance(node, ast.ImportFrom) and node.module == 'models':
                for alias in node.names:
                    if alias.name in model_fields:
                        model_fields[alias.name] = set()  # Initialize set for fields

            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id in model_fields:
                    model_fields[node.value.id].add(node.attr)

            for child in ast.iter_child_nodes(node):
                visit_model(child, model_fields)

        def find_model_fields(model_name, file_path, models_directory):
            

            # Find table.py and extract fields
            for filename in os.listdir(models_directory):
                # print(filename, model_name)
                filemodel_name = f"{model_name}.py"
                if filename.endswith('.py') and filename == filemodel_name.lower():
                    full_path = os.path.join(models_directory, filename)
                    model_fields['table'] = get_table_fields(full_path)

            # Parse the target file to find field accesses
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read(), filename=file_path)

            visit_model(tree, model_fields)

        #----------------------------------------------
        # get model_like
        def find_assignments_with_create_model_like(node):
            
            if isinstance(node, ast.Assign):
                # Check if the right-hand side is a call to `create_model_like`
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    if node.value.func.id == 'create_model_like':
                        # Collect variables on the left-hand side of the assignment
                        for target in node.targets:
                            if isinstance(target, ast.Tuple):
                                # If it's a tuple, collect all variables
                                for elt in target.elts:
                                    if isinstance(elt, ast.Name):
                                        create_model.append(elt.id)
                            elif isinstance(target, ast.Name):
                                # Single variable assignment
                                create_model.append(target.id)
            
            for child in ast.iter_child_nodes(node):
                try:
                    create_model.extend(find_assignments_with_create_model_like(child))
                except Exception as e:
                    print({e})


        #----------------------------------------------

        undeclared_vars = find_undeclared_variables(file_path)
        if undeclared_vars:
            print("==Undeclared variables:")
            for var, lines in undeclared_vars.items():
                print(f"{var}: lines {', '.join(map(str, lines))}")
        else:
            print("==No undeclared variables found.")
        
        #-------------------------------------------------
        find_functions_in_module('functions.additional_functions')
        find_assignments_with_create_model_like(tree)
        find_function_defs(tree)
        find_function_arguments(tree)
        find_model_imports(tree)
        find_variable_assignments(tree)
        #-------------------------------------------------
        print("\n==Functions in 'functions.additional_functions':")
        for func in wildcard_functions:
            combine_keyword.append(func)
            print(func)

        print("\n==Create Model Like':")
        for cm in create_model:
            combine_keyword.append(cm)
            print(cm)
        # Print all variable names found
        print("\n==Variable Assignments:")
        for var in set(variable_names):  # Use set to avoid duplicates
            combine_keyword.append(var)
            print(var)

        print("\n==Function Definitions:")
        for func in function_defs:
            combine_keyword.append(func)
            print(func)

        print("\n==Function Arguments:")
        for arg in set(args_list):  # Use set to avoid duplicates
            combine_keyword.append(arg)
            print(arg)

        print("\n==Models Table:")
        for model in set(model_imports):  # Use set to avoid duplicates
           
            model_name = model
            combine_keyword.append(model_name)
            #-----------------------------------------------------
            # Collect table-field
            #-----------------------------------------------------
            # model_name = "Brief"
            find_model_fields(model_name, file_path, models_directory)

            list_table_fields = []
            for model, fields in model_fields.items():
                for f in fields:
                    list_table_fields.append(f"{model_name}.{f}")
                
            for tf in list_table_fields:
                combine_keyword.append(tf)
                print(tf)
            #-----------------------------------------------------
            
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except SyntaxError as e:
        print(f"Error: Syntax error in the file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Param: {pyfile} {recid} arguments were passed.")
    else:
        arg1 = sys.argv[1]
        recid = sys.argv[2]
        # file_path = f"D:/docker/pixcdk/image/src/functions/mk_po_btn_val_chg_currencybl.py"  # hk_ooo_remove_selected_data_webbl, load_ratecode1bl .py filename, main_gl_mi_reportbl
        file_path = f"D:/docker/pixcdk/image/src/functions"
        models_directory = "D:/docker/pixcdk/image/src/models"
        file_py = arg1
        file_all_keyword = f"D:/docker/pixcdk/image/src/output/qc/kw/keywords_{file_py}.txt"

        file_to_process = f"{file_path}/{file_py}"
        parse_python_file(file_to_process)

        with open(file_all_keyword, 'w') as output_file_all:
            for kw in combine_keyword:
                output_file_all.write(f"{kw}\n")

    
