import ast
import os
import sys
import json
from datetime import datetime

error_messages = []
error_data = []  # List to hold error data for JSON output
error_messages.append("Error Checking:")

def check_syntax(file_path):
    try:
        # Read the Python script
        with open(file_path, "r") as file:
            content = file.read()
        # Try to parse the script using ast.parse
        ast.parse(content)

    except IndentationError as e:
        error_msg = {
            "file_path": file_path,
            "line": e.lineno,
            "msg": f"Indentation error: {e.msg}"
        }
        error_data.append(error_msg)

    except SyntaxError as e:
        error_msg = {
            "file_path": file_path,
            "line": e.lineno,
            "msg": f"Syntax error: {e.msg}"
        }
        error_data.append(error_msg)

def check_syntax_in_directory(directory_path, output_path):
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        # Check for Python files
        if filename.endswith(".py"):
            
            file_path = os.path.join(directory_path, filename)
            print(file_path)
            check_syntax(file_path)

    # Write errors to a JSON file if there are any
    if error_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_path, f"{vhp_module}_syntax_errors_{timestamp}.json")
        with open(output_file, "w") as f:
            json.dump(error_data, f, indent=4)  # Write error data as JSON
            print(f"Errors logged to {output_file}")
    else:
        print("No error found..")

# Example usage

txt_folder = f"D:/docker/app_konversi/input/vhp-serverless/image/src/output/log"
py_folder = "D:/docker/app_konversi/input/vhp-serverless/image/src/output/converted2"
vhp_module = ""

if len(sys.argv) > 1:
    param = sys.argv[1]  # The parameter will be the second argument
    print(f"Received parameter: {param}")
    vhp_module = param
else:
    print("No parameter received.")

check_syntax_in_directory(py_folder, output_path=txt_folder)
