import os, re, importlib
from functions.additional_functions import *
import sqlalchemy as sa
from fuzzywuzzy import process


import_line = []
table_import_list = []
table_field_list = {}
table_field_def_value_list = {}
dataclass_field_list = {}

incomplete_var_names = {}

py_vars = []

main_func_vars = []
main_func_params = []
main_func_param_names = []
main_func_return = []
body_main_func_line = []

inner_func_vars = []
inner_func_params = []
inner_func_return = []
body_inner_func_line = []


curr_inner_func_vars = []
curr_inner_func_params = []
curr_inner_func_param_names = []
curr_inner_func_return = []
curr_body_inner_func_line = []
curr_func_name = ""

inner_functions = []
all_vars = {}
curr_vars = []
curr_input_params = []
curr_output_params = []
curr_body = []

curr_lines = ""
line_case = []

def_dataclass = []
data_class_objects = []
data_class_list = []
buffer_list = {}
curr_buffer_list = {}

return_main_func_object = []

temp_table_and_db_loop_line = []

import_file_list = []

curr_file_name = ""

curr_case_var = ""
first_case = False

add_indentation = 0

check_if_do_statement = False
if_without_do = False
if_level = 0
if_inside_if = False

multiple_lines = False

converted = False

is_assign = False
assign_str = ""
if_then_assign = False

debug_flag = False

prev_clean_curr_line = ""

curr_line_case = []
curr_temp_table_line = 0
curr_temp_table_name = ""
delete_curr_temp_table_flag = False

num_vars_include_file = 0
include_file_flag = False

preprocesor_pos = 0

db_tables = os.listdir("models/")
db_tables = [table_name.replace(".py","") for table_name in db_tables 
             if re.match(r".*\.py",table_name, re.IGNORECASE) and not re.match(r"^_.*",table_name, re.IGNORECASE)\
             and table_name != "base.py"]


def create_table_field_list():
    global db_tables, table_field_list

    type_map = {
            sa.Integer: "int",
            sa.String: "str",
            sa.Float: "decimal",
            sa.Boolean: "bool",
            sa.Date: "date",
            sa.DateTime: "datetime",
            sa.Text: "str",
            sa.Numeric: "decimal",
            sa.LargeBinary: "bytes"
        }   

    for table_name in db_tables:
        model = getattr(importlib.import_module("models." + table_name),convert_to_class_name(table_name))
        table_field_list[table_name] = {}
        table_field_def_value_list[table_name] = {}
        for column in model.__table__.columns:

            if isinstance(column.type, sa.ARRAY):
                inner_type = column.type.item_type
                converted_type = "[" + type_map.get(type(inner_type)) + "]"

            else:
                converted_type = type_map.get(type(column.type))    
            table_field_list[table_name][column.name] = converted_type
            
            if column.default:

                table_field_def_value_list[table_name][column.name] = column.default.arg

def reset_variables():
    global import_line, table_import_list, py_vars, dataclass_field_list
    global main_func_vars, main_func_params, main_func_return, body_main_func_line, buffer_list
    global inner_func_vars, inner_func_params, inner_func_return, body_inner_func_line
    global curr_inner_func_vars, curr_inner_func_params, curr_inner_func_return, curr_body_inner_func_line, curr_func_name
    global inner_functions, incomplete_var_names
    global curr_vars, curr_input_params, curr_output_params, curr_body, all_vars
    global curr_lines, line_case, prev_clean_curr_line
    global def_dataclass, return_main_func_object, curr_buffer_list
    global curr_case_var, first_case, add_indentation, check_if_do_statement, if_without_do
    global multiple_lines, converted, is_assign, if_then_assign, data_class_objects, data_class_list, temp_table_and_db_loop_line
    global curr_temp_table_line, curr_temp_table_name, curr_line_case, delete_curr_temp_table_flag
    global num_vars_include_file, include_file_flag

    data_class_objects = []
    data_class_list = []
    dataclass_field_list = {}

    py_vars = []

    import_line = []
    table_import_list = []
    incomplete_var_names = {}

    main_func_vars = []
    main_func_params = []
    main_func_return = []
    body_main_func_line = []

    inner_func_vars = []
    inner_func_params = []
    inner_func_return = []
    body_inner_func_line = []


    curr_inner_func_vars = []
    curr_inner_func_params = []
    curr_inner_func_return = []
    curr_body_inner_func_line = []
    curr_func_name = ""

    inner_functions = []

    curr_vars = []
    curr_input_params = []
    curr_output_params = []
    curr_body = []

    all_vars = {}

    curr_lines = ""
    line_case = []

    def_dataclass = []
    buffer_list = {}
    curr_buffer_list = {}

    return_main_func_object = []

    curr_case_var = ""
    first_case = False

    add_indentation = 0

    check_if_do_statement = False
    if_without_do = False

    multiple_lines = False

    converted = False

    is_assign = False
    if_then_assign = False

    curr_lines = ""
    prev_clean_curr_line = ""

    curr_line_case = []
    curr_temp_table_line = 0
    curr_temp_table_name = ""
    delete_curr_temp_table_flag = False

    num_vars_include_file = 0
    include_file_flag = False


import re


def replace_incomplete_variable_names(code, var_mapping):
    """
    Replace incomplete variable names with complete ones based on provided mapping.
    
    :param code: The code in which replacements should be made.
    :param var_mapping: A dictionary where the key is the incomplete variable name and the value is the complete variable name.
    :return: Code with replaced variable names.
    """

    def replacer(match):
        word = match.group(0)
        return var_mapping.get(word, word)

    # Make a pattern that matches any of the keys in var_mapping, surrounded by word boundaries
    pattern = r'\b(?:' + '|'.join(re.escape(key) for key in var_mapping.keys()) + r')\b'
    
    return re.sub(pattern, replacer, code)


def canonicalize_variables(code, var_list):
    # Create a dictionary to map the lowercase version of each variable name to its canonical version
    var_map = {var.lower(): var for var in var_list}

    # Create a regex pattern to match variable names that are similar (ignoring case) to those in var_list
    pattern = r'\b(' + '|'.join(re.escape(var) for var in var_map.keys()) + r')\b'

    # Replace matched variables with their canonical versions from the var_map
    def repl(match):
        if match.group(1) != '':
            return var_map[match.group(1).lower()]

    return re.sub(pattern, repl, code, flags=re.IGNORECASE)



def replace_matches_condition(match, is_db_query=False):
    left_operand = match.group(1)
    regex_str = match.group(2)

    # Transform ABL regex into SQL regex
    def transform_to_sql_regex(abl_regex):
        special_chars = r"^$+?[]\|()"
        adjusted_regex = (abl_regex.replace("~.", "{dot}")
                                   .replace("~*", "{asterisk}")
                                   .replace("~~", "{tilde}")
                                   .replace("~", "{esc}"))
        adjusted_regex = ''.join(f'\\{char}' if char in special_chars else char for char in adjusted_regex)
        adjusted_regex = (adjusted_regex.replace("*", ".*")
                                        .replace("{esc}", "\\")
                                        .replace("{dot}", "\\.")
                                        .replace("{asterisk}", "\\*")
                                        .replace("{tilde}", "~"))
        return adjusted_regex

    # Identify if the matched regex_str starts with "(" (indicating a complex expression)
    if regex_str.startswith("(") and regex_str.endswith(")"):
        # Remove the outer parenthesis
        inner_expression = regex_str[1:-1]
        
        # Split by "+" to handle individual segments
        segments = inner_expression.split("+")
        transformed_segments = []
        for segment in segments:
            segment = segment.strip()  # Remove potential whitespace
            # Check if this segment is a string (starts and ends with ")
            if segment.startswith('"') and segment.endswith('"') :
                segment_content = segment[1:-1]  # Remove the quotes
                transformed_content = transform_to_sql_regex(segment_content)
                transformed_segments.append(f'"{transformed_content}"')
            
            else:
                # If not a string, append as-is
                transformed_segments.append(segment)
        
        adjusted_regex = " + ".join(transformed_segments)
    else:
        adjusted_regex = transform_to_sql_regex(regex_str)
    
    # Formulate the final converted expression
    if is_db_query:
        return f'{left_operand}.op("~")({adjusted_regex})'
    else:
        update_import("import re")
        # Handle array-like access in the left operand
        if '[' in left_operand and ']' in left_operand:
            left_operand = f'{left_operand.split("[")[0]}[{left_operand.split("[")[1]}'
        
        return f're.match({adjusted_regex},{left_operand})'


# def adjust_match_conditions(code, is_db_query=False):
#     pattern = r"""
#     (
#         (?:\w+\([^\)]+\))   # Matches a function-like expression, e.g., entry(...)
#         |                   # OR
#         (?:[\w\-_]+(?:\.\w+)*)  # Matches attribute access, e.g., object.attribute or just a variable
#     )
#     \s+MATCHES\s+           # The MATCHES keyword
#     (
#         (?:\([^)]+\))      # Matches a parenthesis expression, e.g., (some_var)
#         |                  # OR
#         "([^"]*)"          # Matches a double-quoted string
#         |                  # OR
#         \w+                # Matches a variable
#     )
#     """
#     return re.sub(pattern, lambda m: replace_matches_condition(m, is_db_query), code, flags=re.VERBOSE)
def adjust_match_conditions(code, is_db_query=False):
    pattern = r"""
    (
        (?:\w+\([^\)]+\))   # Matches a function-like expression, e.g., entry(...)
        |                   # OR
        (?:[\w\-_]+(?:\.\w+)*(?:\[\d+\])?)  # Matches attribute access, e.g., object.attribute or array access, e.g., array[0]
    )
    \s+MATCHES\s+           # The MATCHES keyword
    (
        (?:\([^)]+\))      # Matches a parenthesis expression, e.g., (some_var)
        |                  # OR
        "([^"]*)"          # Matches a double-quoted string
        |                  # OR
        \w+                # Matches a variable
    )
    """
    return re.sub(pattern, lambda m: replace_matches_condition(m, is_db_query), code, flags=re.VERBOSE)



def condense_newlines(text):
    return re.sub(r'\n{3,}', '\n\n', text)

def replace_with_clear(code):
    # pattern = r"^FOR EACH ([\w-]+) :\s*DELETE \1\.\s*END\.$"    
    pattern = r"FOR EACH ([\w-]+)\s?:\s*(DELETE|delete) \1\.\s*END\."    
    replacement = r"\1_list.clear()"
    # print(re.findall(pattern,code,flags=re.DOTALL))
    return re.sub(pattern, replacement, code, flags=re.DOTALL)


def transform_equal_signs(code):
    # Find assignment and ignore comparisons
    assignment_pattern = r'(?<=\w)\s*=\s*(?![=>])'

    # Split the code by the assignment
    parts = re.split(assignment_pattern, code, maxsplit=1)

    # If we don't find an assignment or there's only one part, return the original code
    if len(parts) <= 1:
        return code

    # In the right side of the assignment (after the split), replace single equals with double equals for comparison
    parts[1] = re.sub(r'(?<![<>!=])=\s*(?!\s*=)', ' == ', parts[1])

    # Join the parts back together
    return ' = '.join(parts).replace("  "," ")

def adjust_function_arg(code, function_name, param_index):
    occurrences = [m.start() for m in re.finditer(function_name, code)]
    
    for occ in occurrences:
        stack = []
        comma_count = 0
        index = occ
        
        while index < len(code):  # Make sure we don't go out of bounds
            char = code[index]
            
            if char == '(':
                stack.append('(')
            elif char == ')' and stack:
                stack.pop()
            elif char == ',' and len(stack) == 1:  # Ensure we're at the top level of our target function
                comma_count += 1
            
            # If we're at the correct parameter index:
            if len(stack) == 1 and comma_count == param_index - 1:
                start_index = index + 1
                
                # Skip any whitespace after comma
                while start_index < len(code) and code[start_index].isspace():
                    start_index += 1
                    
                end_index = start_index

                if code[start_index].isdigit():
                    while end_index < len(code) and code[end_index].isdigit():
                        end_index += 1
                else:
                    while end_index < len(code) and (code[end_index] not in ',)' or len(stack) > 1):
                        if code[end_index] == '(':
                            stack.append('(')
                        elif code[end_index] == ')':
                            stack.pop()
                        end_index += 1

                param_value = code[start_index:end_index]

                if param_value.isdigit():
                    original_number = int(param_value)
                    adjusted_number = original_number - 1
                    code = code[:start_index] + str(adjusted_number) + code[end_index:]
                else:  
                    code = code[:end_index] + " - 1" + code[end_index:]
                
                break  # Exit the loop once we've adjusted the parameter
                
            index += 1

    return code

def decrement_array_indices(code):
    # Define a regex pattern to find content within square brackets
    pattern = r'\[(.*?)\]'

    # This function will be used to replace matches with decremented index
    def replace(match):
        index = match.group(1)
        
        # Check if the index is an integer
        if index.isdigit():
            return f"[{int(index) - 1}]"
        else:
            return f"[{index} - 1]"

    # Use sub method to find all patterns and replace them
    return re.sub(pattern, replace, code)

def convert_variable_names(code):
    # First replace variables with underscores "_" to double underscores "__"
    code = re.sub(r'(\b\w*)_(\w*\b)', lambda m: m.group(0).replace("_", "__"), code)

    # Then replace hyphens "-" with underscores "_"
    code = re.sub(r'(\b\w*)-(\w*\b)', r'\1_\2', code)

    return code


def replace_char_in_strings(code, char, replace_with):
    def replacer(match):
        # This function is called for every string match.
        # It replaces commas with "{comma}".
        return match.group(0).replace(char, replace_with)

    # The regex pattern finds all string literals
    pattern = r"\'[^\']*\'|\"[^\"]*\""
    return re.sub(pattern, replacer, code)

def remove_multiple_chars(content,char):

    content = content.strip()  # the while loop will leave a trailing space, 
                    # so the trailing whitespace must be dealt with
                    # before or after the while loop
    while char + char in content:
        content = content.replace(char + char , char)

    return content


def remove_abl_comments(code):
    result = []
    i = 0
    inside_comment = False
    comment_depth = 0

    while i < len(code):
        # Start of a comment
        if code[i:i+2] == "/*":
            if not inside_comment:
                start_index = i
            inside_comment = True
            comment_depth += 1
            i += 2
            continue

        # End of a comment
        if code[i:i+2] == "*/":
            comment_depth -= 1
            if comment_depth == 0:
                inside_comment = False
            i += 2
            continue

        # If not inside a comment, append the character to the result
        if not inside_comment:
            result.append(code[i])
        i += 1

    return ''.join(result)

def def_value_data_type(data_type):

    def_value = "None"

    if data_type == "str":
        def_value = '""'
    elif data_type == "int":
        def_value = "0"
    elif data_type == "float":
        def_value = "0.0"        
    elif data_type == "decimal":
        def_value = "to_decimal(\"0.0\")"        
    elif data_type == "bool":
        def_value = "False"        

    return def_value

def get_model_field_type(model_name, field_name):
    global table_field_list
    
    clean_field_name = field_name.split("[")[0]

    field_list = table_field_list[model_name]
    type = field_list.get(clean_field_name)

    if clean_field_name != field_name and type:
        type = type.strip("[").strip("]")

    if not type:
        for field in field_list.keys():
            if re.match(f'^{clean_field_name}.*$',field):
                type = field_list[field]
                incomplete_var_names[model_name + "." + clean_field_name] = model_name + "." + field
                return type
    if not type:
        return ""
    
    return type


def get_dataclass_field_type(class_name: str, field_name: str):
    clean_field_name = field_name.split("[")[0].lower()
    class_name = class_name.lower()



    for field in dataclass_field_list[class_name]:
        if re.match(f"^{clean_field_name}.*$",field):
            return dataclass_field_list[class_name][field]


def get_model_default_value(model_name, field_name):
    
    def_value = table_field_def_value_list[model_name].get(field_name)

    return def_value

def get_default_value(field):
    def_value = ""
    words = field.split(".")

    #TODO
    if len(words) == 1:
        pass
    else:
        table_name = words[0]
        table_name = get_incomplete_table_name(table_name)

        field_name = words[1]
        if table_name in db_tables:
            def_value = get_model_default_value(table_name,field_name.lower())
        # TODO
        # else:
        #     data_type = get_dataclass_default_value(table_name, field_name)

    return def_value

def get_data_type(field):
    data_type = ""
    field = field.lower().split("[")[0]
    words = field.split(".")


    if len(words) == 1:
        for var in main_func_vars:
            if var.split(":")[0] == field:
                data_type = var.split(":")[1].replace("List","")
        for var in main_func_params:
            if var.split(":")[0] == field:
                data_type = var.split(":")[1].replace("List","")
        for var in curr_inner_func_vars:
            if var.split(":")[0] == field:
                data_type = var.split(":")[1].replace("List","")
        for var in curr_inner_func_params:
            if var.split(":")[0] == field:
                data_type = var.split(":")[1].replace("List","")
    else:
        table_name = words[0]
        table_name = get_incomplete_table_name(table_name)

        field_name = words[1]


        if table_name in db_tables:
            data_type = get_model_field_type(table_name,field_name.lower())
        else:
            data_type = get_dataclass_field_type(table_name, field_name)

    if not data_type:
        return ""
    else:
        return data_type


# TODO: complete data type
def convert_data_type(data_type):
    if re.match(r"INT.*",data_type, re.IGNORECASE): return "int"
    elif re.match(r"CHAR.*",data_type, re.IGNORECASE): return "str"
    elif re.match(r"LONGCHAR.*",data_type, re.IGNORECASE): return "str"
    elif re.match(r"DEC.*",data_type, re.IGNORECASE): return "decimal"
    elif re.match(r"LOGICAL",data_type, re.IGNORECASE) or data_type == "logical": return "bool"
    elif data_type == "BLOB" or data_type == "blob": return "bytes"
    elif data_type == "RAW" or data_type == "raw": return "bytes"
    elif data_type == "MEMPTR" or data_type == "memptr": return "bytes"
    elif data_type == "DATETIME" or data_type == "datetime": return "datetime"
    elif data_type == "DATE" or data_type == "date": 
        update_import("from datetime import date")
        return "date"
    else: return ""
    

def clean_line(line):
    line = line.replace("IF AVAILABLE","IF")
    line = line.replace("IF AVAIL","IF")
    line = line.strip(" ")

    return " ".join(line.split())
    
def convert_name(name):
    return name
    # return name.replace("_","__").replace("-","_")


def add_prev_line(line):
    for prev_line_index in range(1,5):
        prev_line_index *= -1
        curr_body_str = curr_body[prev_line_index].replace("\n"," ").rstrip(" ")
        if  curr_body_str != "":
            curr_body[prev_line_index] = curr_body[prev_line_index] + " \\"
            line_case.append("PREV")
            append_body("\n")
            append_body("    " + line)
            append_body("\n")
            line_case.pop()
            return
        else:
            curr_body[prev_line_index] = ""     

def append_return():
    global converted
    curr_body.append("\n    return generate_output()")

    converted = True


def append_body(line, keep_indentation=False):
    global add_indentation, curr_body, converted
    global curr_lines, multiple_lines, if_without_do, if_level, if_inside_if
    global debug_flag, is_assign, line_case
    global curr_temp_table_name, delete_curr_temp_table_flag

    if line == ".":
        line = "pass"

    line_append = line.strip(".")
    line_append = line_append.replace("{4spaces}","    ")
    if line_append == "":
        return   

    line_append = '    ' * (len(line_case) - line_case.count("DO:")  - line_case.count("DO TRANSACTION:")+ \
                            add_indentation + if_level) + line_append
    curr_body.append(line_append)

    if curr_temp_table_name != "" and (re.match(r".* " + curr_temp_table_name + "\..*", " " + line) or
                                       re.match(r".*\(" + curr_temp_table_name + "\).*", " " + line) )and delete_curr_temp_table_flag:
        delete_curr_temp_table_flag = False

    if (line_append.replace(" ","").replace("\n","") != "" and 
        not (re.match(r"^if .*$",line) or re.match(r"^find .*$",line) or 
                re.match(r"^for .*$",line) or re.match(r"^elif .*$",line) or 
                line == "else:")):
        if if_without_do and not is_assign and not keep_indentation:
            if_without_do = False
            line_case.pop()
        """
        if if_without_do and len(line_case) > 1 and line_case[-2] != "IF-IF" and \
            line_case[-1] != "IF DO" :
            if_without_do = False
            line_case.pop()

        if (len(line_case) > 1 and 
            (line_case[-1] == "IF-IF" or line_case[-1] == "IF")):
            if line_case[-2] == "IF-IF" or line_case[-1] == "IF":
                line_case.pop()

        
        while line_case[-1] == "IF-IF":
            line_case.pop()
        """
        while line_case[-1] == "IF-IF":
            line_case.pop()


    converted = True
    add_indentation = 0

def append_py_vars(var_name):
    global py_vars
    py_vars.insert(0,var_name)
    # py_vars.append(var_name)


def append_input_param_names(param_name):
    global curr_inner_func_param_names, main_func_param_names, line_case
    if "PROCEDURE" in line_case:
        curr_inner_func_param_names.append(param_name)
    else:
        main_func_param_names.append(param_name)


def append_input_param(line):
    global curr_input_params, converted
    curr_input_params.append(line)
    converted = True

def append_output_param(line):
    global curr_output_params,converted
    curr_output_params.append(line)



    converted = True

def update_import(import_str):
    global import_line
    
    if not import_str in import_line:
        import_line.append(import_str)    


def convert_to_class_name(class_name):
    return class_name[0].upper() + class_name[1:]

def add_dataclass_object(table_name):
    if not table_name in data_class_objects:
        data_class_objects.append(table_name)    

def add_dataclass_list(list_name):
    if not list_name in data_class_list:
        data_class_list.append(list_name)    

def add_table_import (table_name):
    global table_field_list

    converted_table_name = convert_to_class_name(table_name)
    if not converted_table_name in table_import_list and table_name in db_tables:
        table_import_list.append(converted_table_name)


def query_db(table_name, condition = "", first_last = "", sort_by=[], join_tables=[], join_table_names=[]):
    add_table_import(table_name)

    for sub_condition in condition.split("("):        
        field = sub_condition.split(" ")[0]
        if field == "not":
            field = sub_condition.split(" ")[1]

    condition = replace_exact(condition,table_name + ".", convert_to_class_name(table_name) + ".")


    other_tables = ""
    other_class_tables = ""

    if join_table_names != []:
        other_tables = ", " + ", ".join(join_table_names)
        other_class_tables = ", " + ", ".join([convert_to_class_name(table_name) for table_name in join_table_names])

    query_str = ""
    if first_last == "":
        query_str = "for " + table_name + other_tables + " in db_session.query(" + convert_to_class_name(table_name) + \
            other_class_tables + ")" 

        for join_table in join_tables:
            for inner_table_name in join_table_names:
                join_table = replace_exact(join_table,inner_table_name + ".", convert_to_class_name(inner_table_name) + ".")
            query_str += join_table

        if condition != "()":
            query_str += ".filter(\n" +  '    ' * (len(line_case) + 2) +  condition + ")" 

        sort_str = ""
        if sort_by != []:      
            sort_str += ".order_by(" + ", ".join(sort_by) + ")"
            sort_str = sort_str.replace(" descending",".desc()").replace(" desc",".desc()").replace("substring(","func.substring(")

            sort_str = replace_exact(sort_str,table_name + ".", convert_to_class_name(table_name) + ".")

            for inner_table_name in join_table_names:
                sort_str = replace_exact(sort_str,inner_table_name + ".", convert_to_class_name(inner_table_name) + ".")
        else:
            sort_str = ".order_by(" + convert_to_class_name(table_name) + "._recid)"

        query_str += sort_str
        query_str += ".all():"
    else:
        query_str = table_name + " = db_session.query(" + convert_to_class_name(table_name) + ")"
        if condition != "()":
            query_str += ".filter(\n" + '    ' * (len(line_case) + 2) +  condition + ")"
    
        if first_last == "PREV":
            append_body("curr_recid = " + table_name + "._recid",keep_indentation=True)
            append_body("\n")
            query_str += ".filter(" + convert_to_class_name(table_name) + "._recid < curr_recid)"
        elif first_last == "NEXT":
            append_body("curr_recid = " + table_name + "._recid",keep_indentation=True)
            append_body("\n")
            query_str += ".filter(" + convert_to_class_name(table_name) + "._recid > curr_recid)"

        if first_last.upper() in ["LAST","PREV"]:
            query_str += ".order_by(" + convert_to_class_name(table_name) + "._recid.desc())"        

        query_str += ".first()"

        # db_query_index_matches = re.findall(r"\b[A-Z]\w*\.\w*\[.*\]",query_str)
        
        # if db_query_index_matches:
        #     for match_str in db_query_index_matches:
        #         modified_index = match_str.replace("[","[inc_value(").replace("]",")]")
        #         query_str = query_str.replace(match_str,modified_index)

    return query_str

def query_dataclass(table_name, condition = "", first_last = "", sort_by=""):
    query_str = ""


    if first_last != "":
        query_str = table_name + " = "
    else:
        query_str = "for " + table_name + " in "

    query_str += "query(" + table_name + "_list"



    condition = adjust_match_conditions(condition)    
    if condition != "":

        query_str += ", filters=(lambda " + table_name + ": " + table_name + "." + condition + ")"
        query_str = query_str.replace(" " + table_name + ".not ", " not " + table_name + ".")

        query_str = query_str.replace(" " + table_name + "." + table_name + ".", " " + table_name + ".")
        query_str = query_str.replace(" " + table_name + ".( ", "(")


    if first_last != "":
        query_str += ", " + first_last.lower() + "=True"

    
    all_sort_str = ""
    

    for sort_str in sort_by:
        field_name = sort_str.split(" ")[0]

        if len(field_name.split(".")) == 2:
            field_name = field_name.split(".")[1]

        all_sort_str += "(\"" + field_name + "\"," 

        if re.match(r".* desc.*",sort_str,re.IGNORECASE):
            all_sort_str += "True"
        else:
            all_sort_str += "False"

        all_sort_str += "),"

    all_sort_str = all_sort_str.rstrip(",")

    if all_sort_str != "":
        all_sort_str = ", sort_by=[" + all_sort_str + "]"

    query_str += all_sort_str + ")"


    if first_last == "":
        query_str += ":"
    
    return query_str

def convert_empty_temp_table(line):
    line = line.strip(".")
    table_name = line.split(" ")[2]

    return table_name + "_list.clear()"

def convert_def_temp_table(lines):
    global converted, dataclass_field_list, py_var_names
    lines = lines.strip(".")
    table_name = convert_name(lines.split(" ")[2].split("|")[0]).lower()

    field_list = {}

    like_table_name = ""

    if lines.split(" ")[3] == "LIKE":
        like_table_name = convert_name(lines.split(" ")[4]).split("|")[0].lower()
        like_table_name = get_incomplete_table_name(like_table_name)
        add_table_import(like_table_name)
        if like_table_name in db_tables:
            field_list = table_field_list[like_table_name].copy()
        else:
            field_list = dataclass_field_list[like_table_name].copy()

    dataclass_str = table_name + "_list, " + convert_to_class_name(table_name) + " = "

    if like_table_name:
        dataclass_str += "create_model_like(" + convert_to_class_name(like_table_name)
    else:
        dataclass_str += "create_model(\"" + convert_to_class_name(table_name) + "\""

    fields_str = ""
    def_value_str = ""


    for line in lines.split("|")[1:]:
        if re.match(r"^FIELD .*",line):
            words = line.split(" ")

            data_type = ""
            if words[2] == "AS" or words[2] == "as":
                data_type = convert_data_type(words[3])

                if re.match(r".* EXTENT .*",line):
                    extent = line.split(" EXTENT ")[1].split(" ")[0]

                    data_type = "[" + data_type + "," + str(extent) + "]"
            else:
                data_type = get_data_type(words[3].lower())
                if re.match(r"\[.*\]",data_type):
                    like_table_name = words[3].split(".")[0]
                    like_field_name = words[3].split(".")[1]

                    if buffer_list.get(like_table_name):
                        like_table_name = buffer_list[like_table_name]

                    def_value = table_field_def_value_list.get(like_table_name).get(like_field_name.split("[")[0])
                    if def_value and len(like_field_name.split("[")) > 1: 
                        data_type = data_type.replace("[","").replace("]","") 
                    else:   
                        data_type = data_type.replace("]","," + str(len(def_value)) + "]")


            field_name = words[1].lower()
            if len(words) > 5:
                # if words[4] == "EXTENT":
                #     data_type = "[" + data_type + ", " + words[5] + "]"
                # elif words[4] == "INIT" or words[4] == "INITIAL":
                if words[4] == "INIT" or words[4] == "INITIAL":
                    def_value = words[5]
                    if def_value != "NO" and def_value != "0" and def_value != "?":
                        def_value_str += "\"" + field_name + "\": " + convert_value(def_value) + ", "
            
            field_list[field_name] = data_type


            fields_str += "\"" + field_name + "\":" + data_type + ", "

    dataclass_field_list[table_name] = field_list
    add_dataclass_object(table_name)
    add_dataclass_list(table_name + "_list")

    fields_str.rstrip(" ")
    fields_str.rstrip(",")

    if fields_str != "":
        dataclass_str += ", {" + fields_str.strip(", ") + "}"

    if def_value_str != "":
        dataclass_str += ", {" + def_value_str.strip(", ") + "}"

    dataclass_str += ")"

    def_dataclass.append(dataclass_str)

    converted = True

# TODO: add to var list definition
def convert_def_var(line):
    global converted, all_vars

    line = line.strip(".")

    words = line.split(" ")
    data_type = ""

    if words[3] == "AS" or words[3] == "as":
        if words[4]  == "HANDLE":
            converted = True
            return
        data_type = convert_data_type(words[4])
    else:
        data_type = get_data_type(words[4])

    var_name = convert_name(words[2].lower())

    # if re.match(r".*%",var_name):
    #     incomplete_var_names[var_name] = var_name.replace("%","_perc")
    #     var_name = var_name.replace("%","_perc")

    def_value_str = ""
    extent = 0
    def_value = ""


    if len(words) > 6:
        if re.match(r".* EXTENT .*",line):
            line = line.replace(" - 1]","]")
            extent = int(line.split(" EXTENT ")[1].split(" ")[0])

        # if words[5] == "EXTENT":
        #     extent = int(words[6]) + 1
            if not re.match(r".* (INIT|INITIAL) .*",line):
                def_array_value = ""
                if data_type == "str":
                    def_array_value = "\"\""
                elif data_type == "int":
                    def_array_value = "0"
                elif data_type == "float":
                    def_array_value = "0.0"
                elif data_type == "decimal":
                    def_array_value = "to_decimal(\"0\")"
                else:
                    def_array_value = "None"


                def_value_str = "create_empty_list(" + str(extent) + "," + def_array_value + ")"

                """
                def_value_str = "["
                
                for i in range(0, extent):
                    if data_type == "str":
                        def_value_str += "\"\""
                    elif data_type == "int" or data_type == "float" or data_type == "decimal":
                        def_value_str += "0"
                    else:
                        def_value_str += "None"
                    def_value_str += ", "
                
                def_value_str = def_value_str.strip(", ")

                def_value_str += "]"
                """

            data_type = "List[" + data_type + "]"

            # data_type = ""

        if re.match(r".* (INIT|INITIAL) .*",line):                
            initial_line = line.split(" INITIAL ")
            if len(initial_line) == 1:
                initial_line = line.split(" INIT ")

            def_value = initial_line[1]


            if extent > 0:
                def_value = def_value.replace(" - 1]","]")


        # elif words[5] == "INIT" or words[5] == "INITIAL":
        #     def_value = words[6]
        
            if def_value != "NO" and def_value != "0" and def_value != "?":
                def_value_str += convert_value(def_value)
    
    if extent > 0 and re.match(r".* (INIT|INITIAL) .*",line):   
            if def_value[0] != "[":
                def_value_str = "create_empty_list(" + str(extent) + ", " + convert_value(def_value) + ")"

    if def_value_str == "" and len(data_type.split("=") ) == 1:
        if data_type == "int": 
            def_value_str = "0"
        elif data_type == "float": 
            def_value_str = "0.0"
        elif data_type == "decimal": 
            def_value_str = "to_decimal(\"0.0\")"
        elif data_type == "str": 
            def_value_str = '""'
        elif data_type == "bool": 
            def_value_str = 'False'
        else:
            def_value_str = 'None'

    def_var_str = var_name

    if data_type != "":
        def_var_str += ":" + data_type

    if def_value_str != "":
        def_var_str += " = " + def_value_str
    curr_vars.append(def_var_str)

    all_vars[var_name] = data_type
    

    converted = True

def convert_copy_lob(line):
    line = line.strip(".").strip(" ")
    line = line.replace("COPY_LOB FROM","")
    line = line.replace("COPY_LOB ","")
    line = line.replace("copy_lob from","")
    line = line.replace("copy_lob ","")

    words = line.split(" TO ")

    copy_lob_str = ""
    if not re.match(r".* FILE.*", line):
        copy_lob_str = words[1] + " = " + words[0]
    
    append_body(copy_lob_str)
    append_body("\n")
    

def convert_buffer_copy(line):
    global converted
         
    line = line.strip(".").strip(" ")
    except_line = ""
    except_line_match = re.search(r"EXCEPT .* TO",line)
    if except_line_match:
        except_line = except_line_match.group(0).replace("TO","")
        line = line.replace(except_line,"")
        except_line = ",except_fields=[\"" + except_line.replace("EXCEPT ","").strip(" ").replace(" ","\",\"") + "\"]"
    source_table_name = convert_name(line.split(" ")[1])
    object_name = convert_name(line.split(" ")[3]).lower()

    # create_object = object_name + " = " + "buffer_copy(" + source_table_name + ", " + convert_to_class_name(object_name) + except_line + ")"
    create_object = "buffer_copy(" + source_table_name + ", " + object_name + except_line + ")"
    
    append_body(create_object)
    append_body("\n")
    converted = True

def get_incomplete_table_name(table_name):
    global incomplete_var_names

    # if not table_name in db_tables and not buffer_list.get(table_name) in db_tables and not table_name in data_class_objects:
    if (not convert_to_class_name(table_name) in table_import_list and 
        not (buffer_list.get(table_name) and 
        convert_to_class_name(buffer_list.get(table_name)) in table_import_list) and 
        not table_name in data_class_objects):

        if table_name in db_tables:
            return table_name
        elif buffer_list.get(table_name) in db_tables:
            return buffer_list.get(table_name)

        r = re.compile(f"^{table_name}.*$")
        table_match = list(filter(r.match, data_class_objects))

        if table_match == []:
            table_match = list(filter(r.match, db_tables))
        
        if table_match == []:
            table_match = list(filter(r.match, buffer_list.keys()))

        if table_match != []:
            incomplete_var_names[table_name] = table_match[0]
            table_name = table_match[0]

    return table_name

# TODO
def convert_find(line):
    global db_tables, incomplete_var_names,curr_buffer_list, add_indentation

    line = line.strip(".")

    use_index = re.search(r" USE_INDEX .*",line)

    if use_index:
        line = line[:use_index.span()[0]]

    query = ""
    first_last = line.split(" ")[1]
    table_name = line.split(" ")[2].lower()


    table_name = get_incomplete_table_name(table_name).lower()

    condition = re.search(r".* WHERE ",line, re.IGNORECASE)
    if condition:
        condition = line.replace(condition.group(),"")
    else:
        condition = ""

    """
    pre_find = "if not " + table_name

    if (condition != "" and 
        not re.match(r".*<.*", condition) and 
        not re.match(r".*>.*",condition) and
        not re.match(r".*re\.match.*",condition)
        ):
        pre_find += " or not(" + convert_condition(condition) + ")"

    pre_find += ":"

    append_body(pre_find)
    append_body("\n")
    add_indentation = 1
    """
    
    if not table_name in data_class_objects or table_name in db_tables or buffer_list.get(table_name) in db_tables or curr_buffer_list.get(table_name) in db_tables:
        query = query_db(table_name, convert_condition(condition, True, table_name),first_last=first_last)
    else:
        query = query_dataclass(table_name, convert_condition(condition), first_last)

    return query


def get_condition(line):
    condition = ""

    if re.match(r".* WHERE .*", line):
        condition = line.replace(re.search(r".* WHERE ", line, re.IGNORECASE).group(),"")

    return condition


# TODO: sort by, first inner table with dataclass
def convert_for(line):
    global db_tables, add_indentation, curr_buffer_list
    global curr_temp_table_name, curr_temp_table_line, curr_line_case, delete_curr_temp_table_flag
    join_tables = []
    later_join_tables = []
    join_table_names = []   
    temp_table_join_tables = []
    # main_sort_by = ""
    first_flag = False
    main_table_is_db = False
    sort_list = []

    ori_line = line
    line = line.strip(":").strip(".").strip(" ")


    if re.match(r".* BY .*", line, re.IGNORECASE):   
        sort_list = line.split(" BY ")[1:]
        sort_list = [sort_str.lower() for sort_str in sort_list]

        sort_by_pos = re.search(r" BY ",line, re.IGNORECASE).span()
        # main_sort_by = line[sort_by_pos[1]:].strip(" ")
        line = line[:sort_by_pos[0]].strip(" ")

    query = ""

    table_list_line = []
    for tmp_line in line.split(", EACH "):
        tmp_line = tmp_line.strip(" ")
        if not tmp_line.split(" ")[0] in ["EACH","FIRST","FOR"]:
            tmp_line = "EACH " + tmp_line

        for sub_query in tmp_line.split(", FIRST "):
        # for sub_query in tmp_line.split(", FIRST"):
            sub_query = sub_query.strip(" ")
            if not sub_query.split(" ")[0] in ["EACH","FIRST","FOR"]:
                sub_query = "FIRST " + sub_query

            table_list_line.append(sub_query)

    main_table = table_list_line[0].strip(" ")

    use_index = re.search(r" USE_INDEX .*",main_table)

    if use_index:
        main_table = main_table[:use_index.span()[0]]

    main_table_name = convert_name(main_table.split(" ")[2]).strip(" ").lower()
    main_table_name = get_incomplete_table_name(main_table_name)
    main_table_is_db = main_table_name in db_tables or buffer_list.get(main_table_name) in db_tables or curr_buffer_list.get(main_table_name) in db_tables

    main_condition = get_condition(main_table)

    first_inner_db_table_name = ""
    first_inner_db_table_condition = ""
    first_inner_db_table_condition_ori = ""
    curr_main_table_name = main_table_name
    main_table_name_ori = ""

    for inner_table_line in table_list_line[1:]:
        inner_table_line = inner_table_line.strip(" ")
        first_each = inner_table_line.split(" ")[0]

        if first_each  == "FIRST":
            first_flag = True

        use_index = re.search(r" USE_INDEX .*",inner_table_line)

        if use_index:
            inner_table_line = inner_table_line[:use_index.span()[0]]

        inner_table_name = inner_table_line.split(" ")[1]
        inner_table_name = get_incomplete_table_name(inner_table_name)
        inner_table_is_db = inner_table_name in db_tables or buffer_list.get(inner_table_name) in db_tables or curr_buffer_list.get(inner_table_name) in db_tables
        # TODO: convert condition for join with mulitple conditions
        inner_table_condition = get_condition(inner_table_line)
        inner_table_condition = convert_condition(inner_table_condition,inner_table_is_db,inner_table_name).strip(" ")

        inner_table_condition = inner_table_condition.replace("(","( ").replace(")"," )")

        if not main_table_is_db and inner_table_is_db:
            temp_table_and_db_loop_line.append(ori_line)



        if main_table_is_db or first_inner_db_table_name != "":
            inner_table_condition = inner_table_condition.replace(" " + curr_main_table_name + ".", " " + convert_to_class_name(curr_main_table_name) + ".")
        if inner_table_is_db:
            inner_table_condition = inner_table_condition.replace(" " + inner_table_name + ".", " " + convert_to_class_name(inner_table_name) + ".")
        # inner_table_condition = " ".join([convert_to_class_name(table_name) for table_name in inner_table_condition.split(" ")])
        # inner_table_condition = " ".join([convert_to_class_name(inner_table_name) for inner_table_name in inner_table_condition.split(" ")])
        inner_table_condition = inner_table_condition.replace("( ","(").replace(" )",")")

        if main_table_is_db:
            # DB table join DB table
            if inner_table_is_db:
                join_tables.append(".join(" + convert_to_class_name(inner_table_name) + "," + inner_table_condition + ")")
            # DB table join temp table
            else:
                inner_table_name = inner_table_name.lower()
                inner_table_condition = inner_table_condition.replace(" " + convert_to_class_name(curr_main_table_name) + ".", " " + curr_main_table_name + ".")
                later_join_tables.append(inner_table_name + " = query(" + inner_table_name + "_list, (lambda " + inner_table_name + ": " + inner_table_condition + "), first=True)")
                later_join_tables.append("if not " + inner_table_name + ":")
                later_join_tables.append("{4spaces}continue\n")
        else:
            # Temp table join DB table
            if inner_table_is_db:
                if first_inner_db_table_name == "":

                    first_inner_db_table_condition_ori = inner_table_condition

                    right_value = inner_table_condition.split(" == ")[1].split(")")[0].strip(" ")
                    

                    if len(right_value.split(".")) == 1:
                        table_name = main_table_name
                        field_name = right_value
                    elif len(right_value.split(".")) == 2:
                        table_name = right_value.split(".")[0]
                        field_name = right_value.split(".")[1]

                    if main_condition != "":
                        main_condition = " if " + main_condition

                    replace_condition = ".in_(list(set([" + table_name + "." + field_name + " for " + table_name + " in " + table_name + "_list" + main_condition + "])))"
                    inner_table_condition = inner_table_condition.replace("== " + right_value, replace_condition)

                    first_inner_db_table_name = inner_table_name
                    first_inner_db_table_condition = inner_table_condition
                    curr_main_table_name = inner_table_name
                else:
                    join_tables.append(".join(" + convert_to_class_name(inner_table_name) + "," + inner_table_condition + ")")


                # join_tables.append(inner_table_name + " = db_session.query(" + convert_to_class_name(inner_table_name) + ")" \
                #                    + ".filter(" + inner_table_condition + ").first()")
            # Temp table join temp table
            else:
                join_tables.append(inner_table_name + " = query(" + inner_table_name + "_list, (lambda " + inner_table_name + ": " + inner_table_condition + "), first=True)")

                join_tables.append("if not " + inner_table_name + ":")
                join_tables.append("{4spaces}continue\n")

        if inner_table_name != first_inner_db_table_name and inner_table_is_db:
            join_table_names.append(inner_table_name)

        add_table_import(inner_table_name)    

    if first_inner_db_table_name != "":
        main_table_is_db = True
        main_table_name_ori = main_table_name
        main_table_name = first_inner_db_table_name
        main_condition = first_inner_db_table_condition

    if main_table_is_db:
        if first_flag:
            append_body(main_table_name + "_obj_list = []")
            append_body("\n")
        query = query_db(main_table_name, convert_condition(main_condition,True,main_table_name), sort_by=sort_list, join_tables=join_tables, join_table_names=join_table_names)
        join_tables = []
        join_table_names = []
    else:
        query = query_dataclass(main_table_name, convert_condition(main_condition), sort_by=sort_list)

    append_body(query)

    for join_lines in join_tables:
        append_body("\n")
        add_indentation = 1
        append_body(join_lines)


    for join_lines in later_join_tables:
        append_body("\n")
        add_indentation = 1
        append_body(join_lines)

    if first_flag and main_table_is_db:
        append_body("\n")
        add_indentation = 1
        append_body("if " + main_table_name + "._recid in " + main_table_name + "_obj_list:")

        append_body("\n")
        add_indentation = 2
        append_body("continue")
        append_body("\n")
        add_indentation = 1
        append_body("else:")
        append_body("\n")
        add_indentation = 2
        append_body(main_table_name + "_obj_list.append(" + main_table_name + "._recid)")            
        append_body("\n")
        append_body("\n")

    if main_table_name_ori != "":
        add_indentation = 1
        append_body(main_table_name_ori + " = query(" + main_table_name_ori + "_list, (lambda " + main_table_name_ori + ": " + first_inner_db_table_condition_ori.lower().split("&")[0].split("|")[0].strip(" ") + "), first=True)")
        curr_line_case = line_case.copy()
        curr_temp_table_line = len(curr_body) - 1
        curr_temp_table_name = main_table_name_ori
        delete_curr_temp_table_flag = True
    # return query


# TODO
def convert_run_param(run_parameters):
    run_parameters = run_parameters.replace("?","None").strip(" ").replace(" = "," == ")
    run_parameters = run_parameters.replace(" AND "," and ").replace(" OR "," or ")

    output_params = ""
    input_params = ""
    for param in run_parameters.split(","):
        param = param.strip(" ")
        if re.match(r".*OUTPUT .*", param):
            param_var = param.replace("INPUT_OUTPUT","").replace("OUTPUT ","").strip(" ")

            output_params += param_var.replace("TABLE ","")

            if re.match(r".*TABLE .*", param):
                output_params += "_list"
            output_params += ", "

        if not re.match(r"^OUTPUT .*", param):
            param = param.replace("INPUT_OUTPUT","").replace("OUTPUT ","").replace("INPUT ","").strip(" ")
            param = param.replace("NO","False")

            input_params += convert_value(param.replace("TABLE ",""))

            if re.match(r".*TABLE .*", param) :
                input_params += "_list"
            
            input_params += ", "


    input_params = input_params. strip(", ")

    if output_params != "":
        output_params = output_params.strip(", ") + " = "

    run_parameters = run_parameters.replace("INPUT_OUTPUT","").replace("OUTPUT ","").replace("TABLE ","").replace("INPUT ","").strip(" ")

    return output_params, input_params



def convert_run(line):
    global import_line, import_file_list

    run_value_flag = False
    if re.match(r".*RUN VALUE.*",line,re.IGNORECASE):
        run_value_flag = True
        line = line.replace(" VALUE (","(").replace(" value (","(")

    line = line.lstrip("run ").lstrip("RUN ").strip(".")
    is_other_module = False
    is_combo = False

    if re.match(r".*ON hServer.*",line, re.IGNORECASE):
        is_combo = True
        line = line.replace(" ON hServer","").strip(" ")

    if run_value_flag:
        function_name = line.split(") (")[0].strip("(").strip(" ")
    else:
        function_name = line.split(" ")[0]

        if not re.match(r".*\(.*\).*", line, re.IGNORECASE):
            function_name = function_name + "()"

        function_name = function_name.split("(")[0].strip(" ")

    run_parameters = ""
    output_params = ""

    converted_func_name = convert_name(function_name.replace(".p","").replace(".i","")).lower().replace("__","_")
    if re.match(r".*\.(p|i)",function_name, re.IGNORECASE):
        if not converted_func_name in import_file_list:
            import_file_list.append(converted_func_name)
        update_import("from functions." + converted_func_name + " import " + converted_func_name)
        is_other_module = True

    if len(line.split("(")) > 1 :
        if run_value_flag and len(line.split(") (")) > 1:
            run_parameters = line.split(") (")[1].strip(" ").strip("(").strip(")")
        else:
            run_parameters = line.replace(function_name + " (","(").strip(" ").strip("(").strip(")")
        if run_parameters != "":
            output_params, run_parameters = convert_run_param(run_parameters)

    if run_value_flag:
        run_str = converted_func_name + ",(" + run_parameters + ")"
    else:
        run_str = converted_func_name + "(" + run_parameters + ")"

    if run_value_flag:
        is_other_module = True
        run_str = "run_program(" + run_str + ")"

    if is_other_module:
        run_str = "get_output(" + run_str + ")"

    run_str =  output_params + run_str

    if is_combo:
        append_body("local_storage.combo_flag = True",True)
        append_body("\n",True)
        append_body(run_str, True)
        append_body("\n", True)
        append_body("local_storage.combo_flag = False")
        append_body("\n")
    else:
        append_body(run_str)

# def convert_db_query_condition(condition_str,table_name=""):
#     condition_str = adjust_match_conditions(condition_str,True)
#     # Replace & and | with space surrounding for splitting
#     condition_str = re.sub(r'(AND|OR)', r' \1 ', condition_str)
    
#     # Split the conditions by & or |
#     conditions = re.split(r' AND | OR ', condition_str)
    
#     # Process each condition:
#     # 1. If it starts with "Not ", replace with "~" and put it in parenthesis.
#     # 2. Otherwise, just wrap it in parenthesis.
#     processed_conditions = []
#     for condition in conditions:
#         condition = condition.strip()
#         if condition.startswith("Not "):
#             processed_conditions.append("~(" + condition[4:] + ")")
#         else:
#             processed_conditions.append("(" + condition + ")")

#     # Join processed conditions with " & "
#     condition_str = ' & '.join(processed_conditions)
#     condition_str = convert_string_comparison(condition_str, True,table_name)
#     return condition_str


import re

def convert_db_query_condition(condition_str, table_name=""):
    # condition_str = adjust_match_conditions(condition_str, True)
    
    # Split the conditions and operators
    parts = re.split(r' (AND|OR) ', condition_str)
    conditions = parts[::2]  # Even indices are conditions
    operators = parts[1::2]  # Odd indices are operators

    # Process each condition
    processed_conditions = []
    for condition in conditions:
        condition = condition.strip()
        if condition.startswith("Not "):
            processed_conditions.append("~(" + condition[4:] + ")")
        else:
            processed_conditions.append("(" + condition + ")")

    # Join processed conditions with corresponding operators
    condition_str = ' '.join(
        processed_condition + (' ' + operators[i] + ' ' if i < len(operators) else '')
        for i, processed_condition in enumerate(processed_conditions)
    )
    condition_str = convert_string_comparison(condition_str, True, table_name)
    return condition_str

def convert_value(var):
    var = var.replace("?", "None")
    var = var.replace("NOT", "no")
    var = var.replace("NO", "False")
    var = var.replace("YES", "True")
    return var

def check_missing_table_name(var):
    # print(var)
    if len(var.split(".")) == 1:
        if var in all_vars.keys() or var in db_tables or var in data_class_objects:
            return

        for table_name in table_import_list:
            table_name = table_name.lower()
            
            r = re.compile(f"^{var}.*$")
            field_match = list(filter(r.match, table_field_list[table_name]))
            if field_match != []:
                incomplete_var_names[var] = table_name + "." + field_match[0]


            # for field in table_field_list[table_name]:
            #     if re.match(f"^{var}.*$",field):
            #         print(var, field)
            #         incomplete_var_names[var] = table_name + "." + field
            #         return


def convert_string_comparison(condition, is_sqlachemy_query=False,table_name=""):
    left_value_list = []
    right_value_list = []
    tmp_condition = condition.replace("&","AND").replace("|","OR")
    tmp_condition = tmp_condition.replace("<=","==").replace(">=","==").replace("<","==").replace(">","==").replace("!=","==")
    for and_condition in tmp_condition.split("AND"):
        for condition_str in and_condition.split("OR"):
            condition_str = condition_str.strip(" ")
            var_values = condition_str.split(" == ")
            if len(var_values) == 1:
                if not is_sqlachemy_query:
                    if re.match(r".* MATCHES .*",condition_str):
                        # condition = condition.replace("'","\"")
                        # condition = condition.replace(condition_str,adjust_match_conditions(condition_str))
                        clean_var_value = (" " + var_values[0]).replace(" elif ","").replace(" if ","").strip(" ").strip(":").strip(" ")
                        left_value = clean_var_value.split(" MATCHES ")[0]
                        right_value = clean_var_value.split(" MATCHES ")[1].replace("*",".*").replace("$","\$")

                        if len(right_value.split("+")) > 1:
                            right_value = "(r" + right_value + ")"

                        match_str = "re.match(" + right_value + "," + left_value + ", re.IGNORECASE)"
                        condition = condition.replace(clean_var_value, match_str)

                    else:

                        for var_value in var_values[0].split(" "):
                            var_value = var_value.strip(":").split("[")[0]
                            if var_value != "if" and len(var_value.split(".")) == 1 and len(var_value) > 2 and \
                                len(var_value.split("(")) == 1 and var_value[0] != '"' and var_value != "not":
                                
                                check_missing_table_name(var_value)
                else:
                    # TODO:check value if no table
                    var_value = var_values[0].replace("(not ","").strip("(").strip(")").strip(" ").replace(" not ( ","")
                    if var_value != "" :
                        if len(var_value.split(".")) == 1:
                            condition = condition.replace(var_value,convert_to_class_name(table_name) + "." + var_value)

                    if re.match(r".* MATCHES .*", var_values[0]):
                        var_value = var_values[0][1:-1]
                        var_value = var_value.replace("func.lower","")
                        match_param = var_value.split(" MATCHES ")
                        # pattern = match_param[1].strip(" ").strip(" ").replace("*",".*")
                        pattern = match_param[1].strip(" ").strip(" ")
                        input_str = match_param[0].strip(" ").strip(" ")
                        match_str =  "func.lower(" + input_str + ").op(\"~\")" + "((" + pattern + ").lower().replace(\"*\",\".*\"))"

                        update_import("from sqlalchemy import func")
                        condition = condition.replace(var_value, match_str)

                    
            if len(var_values) == 2:  
                left_value = " " + var_values[0]      
                right_value = var_values[1].strip(":").strip("(").strip(" ").strip(")")
                left_value = left_value.replace(" elif ","").replace(" if ","").strip(" ").strip(":")
                tmp_right_value = right_value.strip(" ").strip(":").strip("(").split("+")[0].strip(")").strip(" ")

                if tmp_right_value.isdigit():
                    right_data_type = "int"
                elif re.match('^".*"$',tmp_right_value):
                    right_data_type = "str"
                else:
                    right_data_type = all_vars.get(tmp_right_value.split(" ")[0])

                to_left_value = left_value
                if is_sqlachemy_query:
                    if len(left_value.split(".")) == 1:
                        
                        var_name = left_value.strip("(").replace("substring","").strip("(").split(",")[0].strip(" ").strip("(")

                        if not var_name in main_func_param_names and not var_name in curr_inner_func_param_names:
                            to_left_value = "(" * var_name.count("(") + convert_to_class_name(table_name) + "." + var_name.strip("(").strip(" ").strip("(")
                            to_left_value = to_left_value.replace(convert_to_class_name(table_name) + ".not ", "not " + convert_to_class_name(table_name) + ".")
                            # to_left_value = "(" + convert_to_class_name(table_name) + "." + left_value.strip("(")
                            condition = condition.replace(var_name + " ", to_left_value + " ")
                            condition = condition.replace(var_name + ", ", to_left_value + ", ")

                            left_value = to_left_value
                    else:
                        curr_table_name = left_value.split(".")[0].strip("(")
                        if len(curr_table_name.split(" ")) > 1:
                            curr_table_name = curr_table_name.split(" ")[-1]
                        if len(curr_table_name.split("(")) > 1:
                            curr_table_name = curr_table_name.split("(")[-1]

                        if curr_table_name != table_name:
                            
                            condition = condition.replace("(" + curr_table_name + ".", "(" + table_name + ".")
                else:
                    for var in left_value.split(" "):
                        var = var.strip(",").strip(")")
                        if not var.isdigit() and len(var) > 2 and len(var.split(".")) == 1\
                            and len(var.split("(")) == 1 and var[0] != '"' and var != "not":
                            check_missing_table_name(var.strip("(").strip(" ").split("[")[0])
                
                left_value = left_value.strip("(").replace("not ( ","").strip(" ")

                if right_data_type == "str" and tmp_right_value != '""' and tmp_right_value != '"{space}"':   
                    if left_value != '""' and not left_value in left_value_list:
                        left_value_list.append(left_value)
                    if right_value != '""' and  not right_value in right_value_list:
                        right_value_list.append(right_value)
                elif right_data_type == "date":
                    replace_date_str = ""
                    
                    replace_right_value = convert_date_operation(right_value)

                    if right_value != replace_right_value:
                        condition = condition.replace(right_value,replace_right_value)
                    # if not re.match(r".*/.*",left_value):
                    #     replace_date_str = left_value + " and "
                    # if not re.match(r".*/.*",right_value):
                    #     replace_date_str += right_value + " and "

                    if replace_date_str != "":
                        condition = replace_exact(condition,left_value, replace_date_str + left_value)


    for left_value in left_value_list:
        if is_sqlachemy_query:
            update_import("from sqlalchemy import func")
            condition = replace_exact(condition, left_value,"func.lower(" + convert_to_class_name(left_value.lower()) +")")
        else:
            condition = replace_exact(condition, left_value,left_value.rstrip(" ") + ".lower() ")

    for right_value in right_value_list:
        condition = condition.replace(" " + right_value, " (" + right_value.rstrip(" ") + ").lower() ")     
        condition = condition.replace(".(" + right_value.rstrip(" ") + ").lower()", "." + right_value)     

    if is_sqlachemy_query:
        condition = condition.replace("(not (","(not_ (")

    return condition

def convert_condition(condition, is_sqlachemy_query=False, table_name = ""):

    condition = condition.replace("\n","")
    condition = condition.strip(".").strip(" ")
    condition = condition.strip(".").strip(" ")
    condition = condition.replace(" == "," = ").replace("="," = ").replace("! = ","!= ").replace("  "," ")
    condition = condition.replace("> = ",">= ").replace("< = ","<= ")
    condition = condition.replace(" EQ "," == ").replace(" = ", " == ").replace(" NE "," != ").replace(" <> "," != ")
    condition = condition.replace(" eq "," == ").replace(" = ", " == ").replace(" NE "," != ").replace(" <> "," != ")
    condition = condition.replace(" ne "," != ").replace(" = ", " == ").replace(" NE "," != ").replace(" <> "," != ")
    condition = condition.replace(" ge "," >= ").replace(" gt ", " > ")
    condition = condition.replace(" GE "," >= ").replace(" GT ", " > ")
    condition = condition.replace(" le "," <= ").replace(" lt ", " < ")
    condition = condition.replace(" LE "," <= ").replace(" LT ", " < ")
    condition = condition.replace(" == YES"," ").replace(" == NO", " == False")
    condition = replace_exact(condition," == no", " == False")
    # condition = condition.replace(" = YES"," ").replace(" = NO", " = False")
    condition = condition.replace(" == TRUE"," ").replace(" == FALSE", " == False")
    condition = condition.replace("?","None").replace(" NOT "," not ")
    condition = condition.replace(" available "," ")
    condition = condition.replace(" AVAILABLE "," ")
    condition = condition.replace(" AVAIL "," ")
    condition = condition.replace("(AVAILABLE ","(")
    condition = condition.replace("(AVAIL ","(")

    # condition = condition.replace(" not None != ", " None == ")
    condition = condition.replace(" not None != ", " not ")
    condition = condition.replace(" None != ", " ")


    

    if is_sqlachemy_query:
        condition = convert_db_query_condition(condition,table_name)
        condition = condition.replace(" not "," ~")
        condition = condition.replace(" AND "," & ").replace(" OR ", " | ")
        # condition = condition.replace(" MATCHES ( ",".op('~')(r")
    else:
        condition = convert_string_comparison(condition, is_sqlachemy_query)
        condition = condition.replace(" AND "," and ").replace(" OR ", " or ")

    return condition

def convert_do_to(line):
    line = line.replace("REPEAT ", "DO ")
    line = "for" + line[2:-1]
    var_name = line.split(" ")[1]
    if get_data_type(var_name).split(" ")[0] == "date":
        return line.replace(" = "," in date_range(").replace(" TO ",",").replace(" to ",",").replace( "BY -1","") + ") :"

    return line.replace(" = "," in range(").replace(" TO ",",").replace(" to ",",") + " + 1) :"

def convert_do_while(line):
    table_name = ""


    if re.match(r"DO WHILE None != .*:",line, re.IGNORECASE):
        table_name = line.split(" ")[4].strip(":")
        
        if table_name != "" and re.match(r"FIND FIRST " + table_name + " .*", curr_body[-1]):
            curr_body[-2] = curr_body[-2].replace(" " + table_name + " = ", " for " + table_name + " in ").replace(".first()",".all():").replace(", first=True)","):")

            return ""
        
    return "while " + convert_condition(line.replace(" transaction "," ").replace(" TRANSACTION "," ").replace("DO WHILE ","").replace("do while ","")) + ":"

def convert_if(line):
    global converted
    line = line.replace("ELSE IF ","elif ").replace("IF ","if ").replace(" THEN",":").strip(" ")
    condition = convert_condition(line)
    condition = adjust_match_conditions(condition)

    return condition

def convert_case(line):
    global converted

    global first_case
    condition = line.replace("WHEN ","").replace(" THEN","").strip(" ")

    if_clause = "if " + convert_name(curr_case_var) + " == " + condition + ":"

    if not first_case:
        if_clause = "el" + if_clause

    if_clause = if_clause.replace(" OR "," or " + curr_case_var + " == ")
    
    first_case = False

    return if_clause

def convert_create(line):
    global converted
    line = line.rstrip(".").strip(" ")
    if len(line.split(" ")) > 2:
        converted = True
        return

    table_name = line.split(" ")[1].lower()
    table_name = get_incomplete_table_name(table_name)

    add_table_import(table_name)

    create_table_name = table_name
    if curr_buffer_list.get(table_name) in db_tables:
        create_table_name = curr_buffer_list[table_name]

    create_str = table_name + " = " + convert_to_class_name(create_table_name) + "()"
    append_body(create_str)
    append_body("\n")

    append_str = ""
    if table_name in db_tables or buffer_list.get(table_name) in db_tables or curr_buffer_list.get(table_name) in db_tables:
        append_str = "db_session.add(" + table_name + ")"
    else:
        append_str = table_name + "_list.append(" + table_name + ")"
    append_body(append_str)
    append_body("\n\n")

def convert_function_header(line):
    global curr_func_name, curr_inner_func_params,curr_input_params, all_vars
    line = line.strip(":").strip(" ")
    line = line.strip(".").strip(" ")

    input_params = line.split("(")[1].replace("INPUT ","").strip(")").strip(" ").split(",")

    for input_param in input_params:
        words = input_param.strip(" ").split(" ")
        var_name = words [0]
        data_type = convert_data_type(words[2])
        curr_input_params.append(var_name + ":" + data_type)
        all_vars[var_name.lower()] = data_type

    curr_func_name = line.split(" ")[1]



def convert_input_param_table(line):
    line = line.rstrip(".")
    line_words = line.split(" ")   

    table_name = line_words[5].lower()
    table_name = convert_name(table_name)

    table_data_type = table_name[0] + table_name[1:]

    input_parameter = table_name + "_list" + ":" + "[" + convert_to_class_name(table_data_type) + "]"
    # input_parameter = table_name + "_list" + ":" + "List[" + convert_to_class_name(table_data_type) + "]"

    for def_str in def_dataclass:
        if re.match(table_name + "_list, .*", def_str):
            py_vars.append(def_str)
            def_dataclass.remove(def_str)

            if re.match(r".*create_model_like.*",def_str):
                like_table_name = def_str.split("(")[1].strip(")").split(",")[0]
                for like_def_str in def_dataclass:

                    if re.match(r".* " + like_table_name + " = .*",like_def_str):
                        py_vars.insert(0,like_def_str)
                        def_dataclass.remove(like_def_str)

                        main_func_vars.append(like_table_name.lower() + "_list = []")

            break
    
    append_input_param(input_parameter)

def convert_input_param_var(line):
    global all_vars
    line = line.rstrip(".")
    line_words = line.split(" ")   

    var_name = line_words[3].lower()
    var_name = convert_name(var_name)

    var_type = ""
    if line_words[4] in ["AS","as"]:
        var_type = convert_data_type(line_words[5])
    else:
        var_type = get_data_type(line_words[5])
    var_default = ""

    def_type = ""

    for word in line_words:
        if def_type == "INITIAL":
            var_default += word

        if word in ["INIT","INITIAL"]:
            def_type = "INITIAL"
        elif word == "FORMAT":
            def_type = "FORMAT"


    input_parameter = var_name + ":" + var_type
    all_vars[var_name] = var_type
    # if var_default != "":
    #     input_parameter += "=" + var_default
    append_input_param_names(var_name)
    append_input_param(input_parameter)

# TODO:
def convert_output_param_var(line, set_default_value = True):
    global converted, all_vars

    line = line.rstrip(".")
    line_words = line.split(" ")   

    field_name = line_words[3]
    var_name = convert_name(field_name.lower())
    
    data_type = ""

    if line_words[4] == "AS":
        data_type = convert_data_type(line_words[5])
    else:
        data_type = get_data_type(line_words[5])

    if "PROCEDURE" in line_case:
        curr_output_params.append(var_name)
    else:
        curr_output_params.append('"' + field_name + '": ' + var_name)
    
    def_value_str = ""
    if len(line_words) > 6:
        extent = 0
        if re.match(r".* EXTENT .*",line):
            extent = int(line.split(" EXTENT ")[1].split(" ")[0])

            if not re.match(r".* (INIT|INITIAL) .*",line):
                def_value_str = "["

                for i in range(0, extent):
                    if data_type == "str":
                        def_value_str += "\"\""
                    elif data_type == "int" or data_type == "float" or data_type == "decimal":
                        def_value_str += "0"
                    else:
                        def_value_str += "None"
                    def_value_str += ", "
                
                def_value_str = def_value_str.strip(", ")

                def_value_str += "]"
                data_type = "[" + data_type + "]"

        if re.match(r".* (INIT|INITIAL) .*",line):                
            initial_line = line.split(" INITIAL ")
            if len(initial_line) == 1:
                initial_line = line.split(" INIT ")

            def_value = initial_line[1]

            if extent > 0:
                def_value = def_value.replace(" - 1]","]")

            if def_value != "NO" and def_value != "0" and def_value != "?":
                def_value_str += convert_value(def_value)


    if def_value_str == "":
        def_value_str = def_value_data_type(data_type)         
       
    if set_default_value:
        def_var_str = "    " + var_name + " = " + def_value_str
        curr_vars.append(def_var_str)

    all_vars[var_name] = def_value_str
    

    # def_var_str = "    " + var_name + " = " + def_value_data_type(data_type)
    # curr_vars.append(def_var_str)
    # all_vars[var_name] = def_value_data_type(data_type)

    converted = True


# TODO:
def convert_output_param_table(line, set_default_value=True):
    global converted 

    line = line.rstrip(".")
    line_words = line.split(" ")   

    field_name = line_words[5]
    table_name = convert_name(field_name).lower()

    def_var_str = ""
    if "PROCEDURE" in line_case:
        curr_output_params.append(table_name)
    else:
        def_var_str = '"' + field_name.replace("__","_").replace("_","-") + '": ' + table_name + "_list"

        curr_output_params.append(def_var_str)

        if not table_name + ":[" + convert_to_class_name(table_name) + "]" in curr_input_params:
            if set_default_value:
                def_var_str = "    " + table_name + "_list = []"
                curr_vars.append(def_var_str)

    converted = True

def convert_assign(line):
    global if_then_assign, add_indentation, is_assign,debug_flag

    is_last_line = False
    line = line.replace("assign ","").replace("ASSIGN ","").strip(".").strip(" ")
    for var_assign in line.split("\n"):
        var_assign = var_assign.strip(".").strip(" ")
        var_assign = convert_var_assignment(var_assign)
        
        
        if var_assign != "":
            if if_then_assign:
                add_indentation = 1

            # if var_assign[-1] == "." and var_assign == convert_var_assignment(line.split("\n")[-1].strip(".").strip(" ")):
            #     is_assign = False            
            if var_assign == convert_var_assignment(line.split("\n")[-1].strip(".").strip(" ")):
                is_assign = False   
                is_last_line = True      

            if re.match(r".*{backslash}.*",var_assign):
                i = 0
                for sub_line in var_assign.split("{newline}"):
                    if i > 0:
                        add_indentation = 2
                    append_body(sub_line)
                    append_body("\n")
                    i += 1
            else:
                append_body(var_assign)
                append_body("\n")
            
            if is_last_line:
                break

    append_body("\n")
    if_then_assign = False

def convert_decimal_operation(value):
    # modified_value = value
    # modify_list = []

    value = value.replace(","," , ").replace("(","( ").replace(")"," )").replace("  "," ")

    # matches = re.findall(r'\[\s*[\w_]+\s*[\+\-]\s*[\w_]+\s*\]',value)
    matches = re.findall(r'\[.*\]',value)


    for match in matches:
        change_match = match.replace("+","{plus}").replace("-","{minus}")
        value = value.replace(match,change_match)
    
    words = re.split('\+|-|\*|/', value)
    # words = value.split(" ")


    modified_value =  " " + value + " "
    is_array = False


    for word in words:
        word = word.strip(" ")
        # word = word.replace("(","").replace(")","").replace(" ","")
        if word == "":
            continue

        if word.isnumeric() or word.isdecimal():
            modified_value = modified_value.replace(" " + word + " ", " " + "to_decimal(\"" + word + "\")" + " ")
        else:
            modified_value = modified_value.replace(" " + word + " ", " " + "to_decimal(" + word + ")" + " ")
        """
        elif re.match(r".*\[.*\]",word):
            is_array = True            
            modified_value += " to_decimal(" + word + ") "
        elif word in ["+","-","*","/","(",")",","] or re.match(r".*\(",word) or is_array:
            modified_value += " " + word
            if re.match(r".*\]",word):
                is_array = False
                modified_value += ")"
                
        elif word.strip(" ") != "":
            if word.isnumeric() or word.isdecimal():
                # modified_value = replace_exact(modified_value, modify_list," to_decimal(\"" + modify_value + "\") ")
                modified_value += " to_decimal(\"" + word + "\") "
            else:
                # modified_value = replace_exact(modified_value, modify_list," to_decimal(" + modify_value + ") ")
                modified_value += " to_decimal(" + word + ") "
        """
    modified_value = modified_value.replace("{plus}","+").replace("{minus}","-")


    """
    for word in words:

        word = word.strip(" ")
        if word == "":
            continue

        word = word.replace(" ","").replace("(","").replace(")","")
        

        if not word in ["+","-","*","/","(",")"] and not word in modify_list:
            if len(words) > 1:
                word = " " + word

            modify_list.append(word)

        
    for modify_value in modify_list:
        if modify_value.isnumeric() or modify_value.isdecimal():
            # modified_value = replace_exact(modified_value, modify_list," to_decimal(\"" + modify_value + "\") ")
            modified_value = modified_value.replace(modify_value, " to_decimal(\"" + modify_value + "\") ")
        else:            
            # modified_value = replace_exact(modified_value, modify_list," to_decimal(" + modify_value + ") ")
            modified_value = modified_value.replace(modify_value, " to_decimal(" + modify_value + ") ")

    modified_value = modified_value.replace("{plus}","+").replace("{minus}","-")

   
    if re.match(r"genstat.*",value):
        print()
    """

    return modified_value

def convert_date_operation(value):
    add_days_str = ""
    modified_value = ""


    matches = re.findall(r'\b\w+\((?:[\w\s+\-*/.]+(?:,\s*)?)+\)',value)

    for match in matches:
        
        words = re.split('\+|-|\*|/', match)
        if len(words) > 1:
            left_value = words[0].strip("(").strip(" ")
            right_value = words[1].strip(")").strip(" ")
            if get_data_type(left_value) == date and (right_value.isdecimal() or right_value.isnumeric()):
                value = value.replace(" " + right_value + " ", " timedelta(days=" + right_value + ")")
            elif get_data_type(left_value) == date and get_data_type(right_value) == date:
                value = value.replace(match, "(" + match + ").days")

 
        modified_match = match.replace("+","{plus}").replace("-","{minus}")
        value = value.replace(match, modified_match)



    if value.count(" + ") == 1: 
        add_days_str = value.split(" + ")[1]
        
    elif value.count(" - ") == 1:
        add_days_str = value.split(" - ")[1]


    if add_days_str != "":
        value = " " + value + " "
        add_days_str = add_days_str.strip(" ")
        modified_add_days_str = "timedelta(days=" + add_days_str + ")"
        modified_value = value.replace(" " + add_days_str + " ", " " + modified_add_days_str + " ")
        value = value.strip(" ")
    else:

        return value

    modified_value = modified_value.strip(" ")    
    modified_value = modified_value.replace("{plus}","+").replace("{minus}","-")

    return modified_value

def convert_var_assignment(line):
    line_ori = line
    line = line.replace("= TRUE","= True")
    line = line.replace("= FALSE","= True")
    line = line.replace("= YES","= True")
    line = line.replace("= yes","= True")
    line = line.replace("= NO","= False")
    line = line.replace("= no ","= False ")
    line = line.replace("= no.","= False.")

    line = line.replace(" AND "," and ")
    line = line.replace(" OR "," or ")

    line = line.replace(" NE "," != ")
    line = line.replace(" EQ "," == ")

    line = line.replace(" GT "," > ")
    line = line.replace(" GE "," >= ")
    line = line.replace(" LT "," < ")
    line = line.replace(" LE "," <= ")

    line = transform_equal_signs(line)

    line = adjust_match_conditions(line)
    if re.match(f'^entry\(.*\) = .*$',line):
        line = line.split(",")[1].strip(" ") + " = " + line.strip(".").strip(" ").replace(" ) = ",", ") + ")"
    elif re.match(f'^substring\(.*\) = .*$',line):
        line = line.split(",")[0].replace("substring(","").strip(" ") + " = " + line.replace("substring(","replace_substring(").strip(".").strip(" ").replace(" ) = ",", ") + ")"

    if len(line.split("=")) == 2:
        left_value = line.split("=")[0]
        line = line.replace(left_value,left_value.lower())

        var_name = line.split(" = ")[0]
        value = line.split(" = ")[1].strip(".").strip(")").strip("(").strip(" ")
        value_ori = line.split(" = ")[1].strip(".").strip(" ")
        modified_value = ""

        if not re.match(r".*\(.*\).*",var_name):
            data_type = entry(0,get_data_type(var_name)," = ")

            if data_type == "date":
                # modified_value = convert_date_operation(value)
                modified_value = convert_date_operation(value_ori)
                line = line.replace(value_ori,modified_value)
            elif (data_type == "decimal" and 
                    not re.search(r".*substring.*",value)):
                
                # line = line.replace("(","( ").replace(")"," )")
                modified_value = convert_decimal_operation(value)

                if re.match(r".* = \(.*",line):
                    line = line.replace(value, modified_value)
                else:
                    line = line.replace(" = " + value, " = " + modified_value)
            elif re.search(r"\d{4}[-_]\d{2}[-_]\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{1,2}:\d{2}",value):
                line = line.replace(value,"parse(\"" + value.replace("_","-") + "\")")


    line = line.replace("()()","()")

    return line

# TODO
def convert_buffer(line):
    global curr_buffer_list, data_class_objects, curr_file_name

    words = line.strip(".").split(" ")
    buffer_name = words[2].lower()
    table_name = words[4].lower()

    table_name = get_incomplete_table_name(table_name)
    is_db_table = False

    if table_name in db_tables:
        add_table_import(table_name)
        is_db_table = True

        dataclass_field_list[buffer_name] = table_field_list[table_name].copy()
    else:
        dataclass_field_list[buffer_name] = dataclass_field_list[table_name].copy()

    if "PROCEDURE" in line_case:
        if table_name in db_tables:
            curr_vars.append(buffer_name + " = None")
            curr_buffer_list[buffer_name] = table_name
            append_body(convert_to_class_name(buffer_name) + " =  create_buffer(\"" + convert_to_class_name(buffer_name) + "\","  + convert_to_class_name(table_name) + ")")
            append_body("\n")
        else: 
            data_class_objects.append(buffer_name)
            append_body(convert_to_class_name(buffer_name) + " = " + convert_to_class_name(table_name))
            append_body("\n")
            append_body(buffer_name + "_list" + " = " + table_name + "_list")
            append_body("\n")
    else:
        buffer_list[buffer_name] = table_name
        add_dataclass_object(buffer_name)

    return line    

def convert_include_file(line):
    line = line.split("{")[1].split("}")[0].strip(" ")

    program_name = line.split(" ")[0]
    line = line.replace(program_name + " ", "i_" + program_name + "(") + ")"
    line = "RUN " + line.replace(" "," , ").replace("("," ( ").replace(")"," )")

    convert_run(line)

def convert_delete(line):
    words = line.strip(".").strip(" ").split(" ")

    if len(words) > 2:
        return ""

    table_name = words[1].lower()
    table_name = get_incomplete_table_name(table_name)

    if table_name in db_tables or curr_buffer_list.get(table_name) in db_tables:
        return "db_session.delete(" + table_name + ")"
    else:
        return table_name + "_list.remove(" + table_name + ")"

def convert_other(line):
    global add_indentation,converted



    if not(re.match(r"^DEF.* STREAM .*",line,re.IGNORECASE) or
           re.match(r"^PAUSE.*",line,re.IGNORECASE) or
           re.match(r"^PUT .*",line,re.IGNORECASE) or
           re.match(r"^MESSAGE .*",line,re.IGNORECASE) or
           re.match(r"^HIDE .*",line,re.IGNORECASE) or
           re.match(r"^DISP.*",line,re.IGNORECASE) or
           re.match(r"^status default .*",line,re.IGNORECASE) or
           re.match(r"^&ANALYZE_SUSPEND .*",line,re.IGNORECASE) or
           re.match(r"^&ANALYZE_RESUME.*",line,re.IGNORECASE) or
           re.match(r"^&Scoped_define.*",line,re.IGNORECASE) or
           re.match(r"^PROCESS EVENTS.*",line,re.IGNORECASE) or
           re.match(r"^FIND CURRENT .*",line,re.IGNORECASE) or
           re.match(r".*THIS_PROCEDURE.*",line,re.IGNORECASE) or

           
        #    re.match(r"^{.*",line) or
           line.upper() == "DO:" or line.upper() == "DO :" or 
           line.upper() == "DO TRANSACTION:" or line.upper() == "DO TRANSACTION :" or 
           line == "" ):
        

        line = convert_var_assignment(line)
        # line = lowercase_vars_not_strings(line)

        if re.match(r".*{backslash}.*",line):
            i = 0
            for sub_line in line.split("{newline}"):
                if i > 0:
                    add_indentation = 2
                
                append_body(sub_line)
                append_body("\n")
                i += 1
        elif re.match(r".*\.clear\(\)$",line):
            line = line.lower()
            append_body(line)
            append_body("\n")

        # if re.match(r"^(\+|\*|/|\-).*",line):
        #     add_prev_line(line)
        else:
            append_body(line)
            append_body("\n")

        converted = True



def convert_line(line):  
    global curr_input_params, curr_output_params, curr_body, curr_vars, line_case, curr_lines
    global inner_functions, curr_func_name
    global curr_case_var, add_indentation, check_if_do_statement
    global if_without_do, multiple_lines, first_case
    global curr_inner_func_params, curr_body_inner_func_line, curr_inner_func_return, curr_inner_func_vars
    global main_func_params,body_main_func_line, main_func_return, main_func_vars
    global converted, is_assign, if_then_assign, assign_str, if_inside_if
    global debug_flag, prev_clean_curr_line, curr_buffer_list, curr_inner_func_param_names
    global curr_line_case, curr_temp_table_line,curr_temp_table_name, delete_curr_temp_table_flag, preprocesor_pos

    converted = False

    if "PROCEDURE" in line_case or "FUNCTION" in line_case:
        curr_input_params = curr_inner_func_params
        curr_output_params = curr_inner_func_return
        curr_body = curr_body_inner_func_line
        curr_vars = curr_inner_func_vars
    else:
        curr_input_params = main_func_params
        curr_output_params = main_func_return
        curr_body = body_main_func_line
        curr_vars = main_func_vars

    curr_clean_line = clean_line(line)    


    if curr_clean_line == "":
        return
    
    if curr_clean_line == "<START>":
        debug_flag = True
        return
    elif curr_clean_line == "<END>":
        print("\n\n" )
        debug_flag = False
        return

    curr_clean_line = adjust_function_arg(curr_clean_line,"entry",1)
    curr_clean_line = adjust_function_arg(curr_clean_line,"substring",2)



    if debug_flag:
        print(line_case, curr_clean_line, "\n" )

    if check_if_do_statement:
        check_if_do_statement = False
        if curr_clean_line.upper() == "DO:" or curr_clean_line.upper() == "DO :":    
            line_case.append("IF DO") 
            converted = True
        elif curr_clean_line.upper() == "DO TRANSACTION:" or curr_clean_line.upper() == "DO TRANSACTION :":    
            line_case.append("IF DO TRANSACTION") 
        elif re.match(r"^CASE .*:$",curr_clean_line, re.IGNORECASE):
            line_case.append("IF DO TO")
        elif re.match(r"^DO .*:$",curr_clean_line, re.IGNORECASE):
            line_case.append("IF DO TO")
        elif re.match(r"REPEAT:",curr_clean_line, re.IGNORECASE):
            line_case.append("IF DO TO")
        elif re.match(r"^FOR .*",curr_clean_line, re.IGNORECASE):
            line_case.append("IF FOR")
        elif re.match(r"^IF .* THEN$",curr_clean_line, re.IGNORECASE) or re.match(r"^ELSE IF .* THEN$",curr_clean_line,re.IGNORECASE):
            line_case.append("IF-IF")
        else:
            line_case.append("IF")   
            if_without_do = True    

    elif curr_clean_line.upper() == "DO:" or curr_clean_line.upper() == "DO :":
        line_case.append("DO:")
        converted = True
    elif curr_clean_line.upper() == "DO TRANSACTION:":
        line_case.append("DO TRANSACTION:")
        converted = True
    
    if re.match(r"^FIND (FIRST|LAST|PREV|NEXT).*\.$", curr_clean_line, re.IGNORECASE):
        append_body("\n")
        append_body(convert_find(curr_clean_line))
        append_body("\n")
        converted = True
    # elif re.match(r"^FIND NEXT.*\.$", curr_clean_line, re.IGNORECASE):
    #     append_body("\n")
    elif re.match(r"^FOR .*(:|\.)$", curr_clean_line, re.IGNORECASE):
        append_body("\n")
        # append_body(convert_for(curr_clean_line))
        convert_for(curr_clean_line)
        line_case.append("FOR")
        append_body("\n")
        converted = True
    elif re.match(r"DEF.* (TEMP_TABLE|WORKFILE) .*\.$",curr_clean_line, re.IGNORECASE):
        convert_def_temp_table(curr_clean_line)
        append_body("\n")
        converted = True
    elif re.match(r"^DEF.* BUFFER .* FOR .*$",curr_clean_line, re.IGNORECASE):
        convert_buffer(curr_clean_line)
        converted = True
    elif re.match(r"^RUN .*\.", curr_clean_line, re.IGNORECASE):
        

        convert_run(curr_clean_line)
        append_body("\n")
        converted = True
    # elif re.match(r"^ASSIGN.*\.$",assign_str.replace("\n","").replace(" ",""), re.IGNORECASE):
    elif re.match(r"^ASSIGN .*\.$",curr_clean_line, re.IGNORECASE) or \
            is_assign and re.match(r".*\.$",curr_clean_line, re.IGNORECASE):
        
        assign_str += curr_clean_line + "\n"

        convert_assign(assign_str.strip("\n"))
        is_assign = False
        assign_str = ""
        append_body("\n")
        converted = True
    elif re.match(r"^IF .* THEN$",curr_clean_line, re.IGNORECASE) or re.match(r"^ELSE IF .* THEN$",curr_clean_line, re.IGNORECASE):
        append_body("\n")
        if_clause = re.search(r"^IF .* THEN",curr_clean_line, re.IGNORECASE)

        if not if_clause:
            if_clause = re.search(r"^ELSE IF .* THEN",curr_clean_line, re.IGNORECASE)
        
        append_body(convert_if(if_clause.group()))

        check_if_do_statement = True

        append_body("\n")
        converted = True
            
    elif re.match(r"^{.*",line):
        convert_include_file(line)
        append_body("\n")
        converted = True

    elif re.match(r"^DEF.*INP.*PARAM.*(AS|LIKE) .*",curr_clean_line, re.IGNORECASE):
        convert_input_param_var(curr_clean_line)
        if re.match(r"^DEF.*OUT.*PARAM.*(AS|LIKE) .*",curr_clean_line, re.IGNORECASE):
            convert_output_param_var(curr_clean_line, False)

    elif re.match(r"^DEF.*INP.*PARAM.*TABLE .*",curr_clean_line, re.IGNORECASE):
        convert_input_param_table(curr_clean_line)
        if re.match(r"^DEF.*OUT.*PARAM.*TABLE .*",curr_clean_line, re.IGNORECASE):
            convert_output_param_table(curr_clean_line, False)

    elif re.match(r"^DEF.*OUT.*PARAM.*(AS|LIKE) .*",curr_clean_line, re.IGNORECASE):
        convert_output_param_var(curr_clean_line)
    elif re.match(r"^DEF.*OUT.*PARAM.*TABLE .*",curr_clean_line, re.IGNORECASE):
        convert_output_param_table(curr_clean_line)
    
    
    elif re.match(r"^DEF.*VAR.*(AS|LIKE) .*",curr_clean_line, re.IGNORECASE):
        convert_def_var(curr_clean_line)
        
    elif re.match(r"^BUFFER_COPY .*\.$", curr_clean_line, re.IGNORECASE):
        convert_buffer_copy(curr_clean_line)
    
    elif re.match(r"^CREATE .*", curr_clean_line, re.IGNORECASE):
        convert_create(curr_clean_line)    

    elif re.match(r"^END .*\.$",curr_clean_line, re.IGNORECASE) or curr_clean_line in ["END.","end."]: 
        if prev_clean_curr_line == "DO:" or re.match(r"IF .*",prev_clean_curr_line,re.IGNORECASE):
            append_body("pass")
            append_body("\n")
 
        if curr_clean_line != "END CASE." and len(line_case) > 0 and line_case[-1] != "def":
                
            if len(line_case) > 1 and line_case[-2] == "IF FOR" :
                append_body("\n")
                line_case.pop()
            elif line_case[-2] == "IF DO TO" or line_case[-2] == "IF DO TRANSACTION":
                line_case.pop()                    
            elif line_case[-2] == "IF-IF":
                line_case.pop()
            elif line_case[-1] == "PROCEDURE" or line_case[-1] == "FUNCTION":
                # append_body("db_session.commit()")
                append_body("\n")
                inner_functions.append((convert_name(curr_func_name), curr_input_params.copy(),curr_body.copy(),curr_inner_func_vars.copy(),curr_output_params.copy(),curr_inner_func_param_names))
                curr_line_case = []
                curr_temp_table_line = 0
                curr_temp_table_name = ""
                delete_curr_temp_table_flag = False

                curr_input_params = []
                curr_body = []
                curr_inner_func_params = []
                curr_body_inner_func_line = []
                curr_inner_func_vars = []
                curr_inner_func_return = []
                curr_inner_func_param_names = []
                curr_output_params = []
            elif line_case[-1] == "DO TRANSACTION:":
                # append_body("db_session.commit()")
                append_body("\n")
            if len(line_case) > 0:
                line_case.pop()
            
            while len(line_case) > 0 and line_case[-1] == "IF-IF":
                line_case.pop()
        if curr_clean_line == "END CASE." and line_case[-1] == "IF DO TO" and len(line_case) > 0 and line_case[-1] != "def":
            line_case.pop()

        if curr_temp_table_name != "" and ("\n").join(curr_line_case) == ("\n").join(line_case):

            if delete_curr_temp_table_flag:
                curr_body[curr_temp_table_line] = ""

            curr_temp_table_name = ""
            curr_line_case = []
            curr_temp_table_line = 0
            delete_curr_temp_table_flag = False


        converted = True
    
    elif re.match(r"^CASE .*:", curr_clean_line, re.IGNORECASE):
        curr_case_var = curr_clean_line.replace("CASE ","").strip(":").strip(" ")
        # curr_case_var = replace_exact(curr_clean_line,"CASE ","").strip(":").strip(" ")
        # curr_case_var = curr_clean_line.split(" ")[1].replace(":","")
        first_case = True
        append_body("\n")
        converted = True
        
    
    elif re.match(r"^WHEN .* THEN$", curr_clean_line, re.IGNORECASE):
        converted_code = convert_case(curr_clean_line)
        append_body(converted_code)
        append_body("\n")
        # line_case.append("CASE")
        check_if_do_statement = True
        converted = True

    elif curr_clean_line == "ELSE":
        check_if_do_statement = True
        append_body("else:")
        append_body("\n")
        converted = True

    elif re.match(r"^DO .*WHILE .*", curr_clean_line, re.IGNORECASE):
        append_body(convert_do_while(curr_clean_line))
        append_body("\n")
        # TODO:transaction?
        # if re.match(r"^DO TRANSACTION WHILE .*", curr_clean_line, re.IGNORECASE):

        line_case.append("WHILE")
        converted = True
    elif re.match(r"^(DO|REPEAT) .* TO .*", curr_clean_line, re.IGNORECASE):
        append_body(convert_do_to(curr_clean_line))
        append_body("\n")
        line_case.append("DO TO")
        converted = True
    elif re.match(r"^REPEAT:", curr_clean_line, re.IGNORECASE):
        append_body("while True:")
        append_body("\n")
        line_case.append("DO TO")
        converted = True

   
 
    elif not converted and re.match(r"^ASSIGN.*", curr_clean_line, re.IGNORECASE):
        is_assign = True 
        converted = True

    elif re.match(r"^FUNCTION .*", curr_clean_line, re.IGNORECASE):
        convert_function_header(curr_clean_line)

        converted = True

    elif re.match(r"^PROCEDURE .*", curr_clean_line, re.IGNORECASE):
        curr_clean_line = curr_clean_line.strip(":").strip(" ")
        curr_func_name = curr_clean_line.split(" ")[1].lower()

        converted = True

    elif re.match(r"^DELETE .*", curr_clean_line, re.IGNORECASE):
        append_body(convert_delete(curr_clean_line))
        append_body("\n")
        converted = True

    elif re.match(r"^EMPTY TEMP_TABLE .*", curr_clean_line, re.IGNORECASE):
        append_body(convert_empty_temp_table(curr_clean_line))
        append_body("\n")
        converted = True


    elif re.match(r"^(RELEASE|DISPLAY|DISP) .*",curr_clean_line, re.IGNORECASE):
        # append_body("db_session.commit()")
        append_body("pass")
        append_body("\n")
        converted = True

    elif re.match(r".*random.randint.*",curr_clean_line, re.IGNORECASE):
        update_import("import random")

    elif re.match(r"^COPY_LOB .*",curr_clean_line, re.IGNORECASE):
        convert_copy_lob(curr_clean_line)

    elif curr_clean_line == "break.":
        if "PROCEDURE" in line_case and not "FOR" in line_case:
            if curr_output_params == []:
                append_body("return")
            else:
                append_body("return generate_inner_output()")

            append_body("\n")
            converted = True
    elif curr_clean_line == "<START&IF>.":
        preprocesor_pos = len(line_case)
        converted = True
    elif re.match(r"&ENDIF*",curr_clean_line, re.IGNORECASE):
        if len(line_case) > preprocesor_pos:
            line_case.pop()
        preprocesor_pos = 0
        converted = True
    elif re.match(r"^OVERLAY .*",curr_clean_line, re.IGNORECASE):
        curr_clean_line = curr_clean_line.replace("OVERLAY","overlay").replace(") = ",",") + ")"
        curr_clean_line = curr_clean_line.replace(".)",")") 
        append_body(curr_clean_line)
        append_body("\n")
        converted = True

    # TODO
    if curr_clean_line.lower() == "return." or curr_clean_line.lower() == "stop.":
        append_body("\n")
        if "PROCEDURE" in line_case:
            if curr_output_params == []:
                append_body("return")
            else:
                append_body("return generate_inner_output()")
        else:
            append_body("return generate_output()")
        append_body("\n")
        converted = True


    if is_assign:
        assign_str += curr_clean_line + "\n"

        converted = True


    if not converted:
        convert_other(curr_clean_line)

    if converted:
        prev_clean_curr_line = curr_clean_line



def convert_function_pre_post(code, from_function_name, to_function_name):
    # Pattern to match the function with inner function argument
    pattern_inner = re.compile(r'{0}\s*\(([\w\-_\.]+)\s*\(\s*([^)]+)\s*\)\)'.format(re.escape(from_function_name)))
    # Pattern to match the function with simple variable argument
    pattern_simple = re.compile(r'{0}\s*\(([\w\-_\.]+)\)'.format(re.escape(from_function_name)))

    # Replacement for function with inner function argument
    def replacement_function_inner(match):
        inner_function_name = match.group(1)
        inner_function_arg = match.group(2)
        return '{}({}).{}'.format(inner_function_name, inner_function_arg, to_function_name)

    # Replacement for function with simple variable argument
    def replacement_function_simple(match):
        arg = match.group(1)
        return '{}.{}'.format(arg, to_function_name.rstrip())

    # Apply the replacements
    code = pattern_inner.sub(replacement_function_inner, code)
    code = pattern_simple.sub(replacement_function_simple, code)

    return code



def prepare_content(file_content):
    global num_vars_include_file, include_file_flag

    lines = []
    is_assign = False
    is_translate = False
    curr_line = ""
    file_content = remove_abl_comments(file_content)

    if include_file_flag:
        numbers = re.findall(r'\{(\d+)\}', file_content)

        # Convert the found strings to integers
        numbers_int = [int(number) for number in numbers]

        if numbers_int != []:
            num_vars_include_file = max(numbers_int)

            for i in range(1, num_vars_include_file + 1):
                file_content = file_content.replace("{" + str(i) + "}", "var" + str(i))

    file_content = file_content.replace("UPDATE ","ASSIGN ")

    # file_content = file_content.replace("&IF","IF")
    file_content = file_content.replace("&IF","<START&IF>.\n\nIF")
    file_content = file_content.replace("&THEN","THEN")
    # file_content = file_content.replace("&ENDIF","END.")
    # file_content = file_content.replace("END..","END.")
    # file_content = file_content.replace("&ENDIF.","END.\n\n<END&IF>.")

    file_content = file_content.replace("ASSIGN","\n\nASSIGN\n")
    file_content = file_content.replace(" then ", " THEN ")
    file_content = file_content.replace(" THEN ."," THEN\npass\n\n")
    file_content = file_content.replace(" THEN"," THEN\n")
    file_content = file_content.replace(" THEN\n"," THEN\n\n\n")

    file_content = replace_char_in_strings(file_content,",","{comma}")
    file_content = replace_char_in_strings(file_content,"&","{a_n_d}")
    file_content = replace_char_in_strings(file_content,"-","{dash}")
    file_content = replace_char_in_strings(file_content,"_","{underscore}")
    file_content = replace_char_in_strings(file_content,"VHP","{V_H_P}")
    file_content = replace_char_in_strings(file_content,"vhp","{v_h_p}")
    file_content = replace_char_in_strings(file_content,"(","{open_bracket}")
    file_content = replace_char_in_strings(file_content,")","{close_bracket}")
    file_content = replace_char_in_strings(file_content,"[","{open_square_bracket}")
    file_content = replace_char_in_strings(file_content,"]","{close_square_bracket}")
    file_content = replace_char_in_strings(file_content,"~{","{open_curly_bracket}")
    file_content = replace_char_in_strings(file_content,"~}","{close_curly_bracket}")
    file_content = replace_char_in_strings(file_content,"?","{question_mark}")
    file_content = replace_char_in_strings(file_content,":","{colon}")
    file_content = replace_char_in_strings(file_content,"\\","{backslash}{backslash}")
    file_content = replace_char_in_strings(file_content,"%","{perc}")
    file_content = replace_char_in_strings(file_content,"=","{equal}")

    file_content = convert_variable_names(file_content)



    for line in file_content.split("\n"):        
        line = line.strip(" ").strip("\t").strip(" ")
        
        if ((re.match(r".*{.*\.i.*}.*",line) and not re.match(r".*{.*intevent_1\.i.*}.*", line)) or
                re.match(r"^&ANALYZE_SUSPEND .*",line,re.IGNORECASE) or
                re.match(r"^&ANALYZE_RESUME.*",line,re.IGNORECASE) or
                re.match(r"^&Scoped_define.*",line,re.IGNORECASE)):
            continue
        
        if is_assign:
            if line != "":
                if re.match(r".* = .* = .*",line):
                    line = re.sub(r'(\d+)\s*(?=\w)', r'\1\n', line)
                elif re.match(r"OR .*",line):
                    curr_line = curr_line.rstrip("\n") + " "
                curr_line += line + "\n"

            if re.match(r".*cl_list.droom.*",line):
                print("1 ",curr_line)

        elif is_translate:
            if line != "":
                curr_line += line.strip(" ") + " "
        else:
            curr_line += line + " "

        if re.match (r".*\.$", line) or \
                re.match(r".*:$", line):
            lines.append(curr_line.strip(" "))
            if is_assign and re.match(r".*cl_list.droom.*",curr_line):
                print(curr_line)
            # if is_assign:
            #     print(curr_line)
            curr_line = ""
            is_assign = False
            is_translate = False
        elif re.match (r"^ASSIGN.*", line):
            is_assign = True
        elif re.match(r".*translateExtended.*",line,re.IGNORECASE) :
            is_translate = True
    

    file_content = "\n".join(lines)
    file_content = remove_multiple_chars(file_content," ")

    file_content = replace_char_in_strings(file_content," ","{space}")


    file_content = file_content.replace("( ","(")
    file_content = file_content.replace(" )",")")
    file_content = file_content.replace("[ ","[")
    file_content = file_content.replace(" ]","]")

    file_content = file_content.replace(",",", ")
    file_content = file_content.replace(",  ",", ")

    # file_content = adjust_function_arg(file_content,"ENTRY",1)
    # file_content = adjust_function_arg(file_content,"SUBSTR",2)
    # file_content = adjust_function_arg(file_content,"SUBSTRING",2)

    file_content = decrement_array_indices(file_content)
    file_content = convert_function_pre_post(file_content,"RECID","_recid")
    file_content = convert_function_pre_post(file_content,"ROWID","_recid")
    file_content = convert_function_pre_post(file_content,"rowid","_recid")
    file_content = convert_function_pre_post(file_content,"CAPS","upper()")
    file_content = convert_function_pre_post(file_content,"caps","upper()")
    file_content = convert_function_pre_post(file_content,"LC","lower()")
    file_content = convert_function_pre_post(file_content,"HEX_ENCODE","hexdigest()")

    file_content = file_content.replace("\n  (","(")
    file_content = file_content.replace("\n (","(")


    file_content = file_content.replace("("," ( ")
    file_content = file_content.replace(")"," ) ")
    file_content = file_content.replace("[","[ ")
    file_content = file_content.replace("]"," ]")
    file_content = file_content.replace("[  ","[ ")
    file_content = file_content.replace("]"," ]")
    file_content = file_content.replace("  "," ")

    file_content = file_content.replace("for each ","\nFOR EACH ")
    file_content = file_content.replace("find first ","\nFIND FIRST ")
    file_content = file_content.replace("if available ","IF AVAILABLE ")

    file_content = file_content.replace("%","_perc")


    file_content = file_content.replace(" NO_LOCK","")
    file_content = file_content.replace(" no_lock","")
    file_content = file_content.replace("SHARE_LOCK","")
    file_content = file_content.replace("share_lock","")
    file_content = file_content.replace("EXCLUSIVE_LOCK","")
    file_content = file_content.replace("exclusive_lock","")
    file_content = file_content.replace("EXCLUSIVE","")
    file_content = file_content.replace(" no_wait","")
    file_content = file_content.replace(" NO_WAIT","")
    file_content = file_content.replace(" NO_ERROR","")
    file_content = file_content.replace(" no_error","")
    file_content = file_content.replace(" NO_UNDO","")
    file_content = file_content.replace(" NO_APPLY","")
    file_content = file_content.replace(" NUM_ENTRIES ( "," num_entries(")

    file_content = file_content.replace(" GENERATE_UUID"," generate_uuid()")
    file_content = file_content.replace(" GUID ("," guid(")
    file_content = file_content.replace("PROVERSION ","proversion() ")
    file_content = file_content.replace("PROVERSION,","proversion(),")
    file_content = file_content.replace(" yield "," yield_ ")
    file_content = file_content.replace(".yield ",".yield_ ")


    file_content = file_content.replace("round_it (","round_it (round_method,round_betrag,")

    
    file_content = file_content.replace("BASE64_DECODE (","base64_decode(")
    file_content = file_content.replace("BASE64_ENCODE (","base64_encode(")
    file_content = file_content.replace("substr (","substring(")
    file_content = file_content.replace("SUBSTR (","substring(")
    file_content = file_content.replace("SUBSTRING (","substring(")
    file_content = file_content.replace("Substring (","substring(")
    file_content = file_content.replace("TRIM (","trim(")
    file_content = file_content.replace("FILL (","fill(")
    file_content = file_content.replace("REPLACE (","replace_str(")
    # file_content = file_content.replace("STRING (","to_string(")
    file_content = file_content.replace("(STRING (","to_string(")
    file_content = file_content.replace("\nSTRING (","\nto_string(")
    file_content = file_content.replace(" STRING ("," to_string(")
    file_content = file_content.replace(" string ("," to_string(")
    file_content = file_content.replace("CHR (","chr(")
    file_content = file_content.replace("ASC (","ord(")
    file_content = file_content.replace(" asc ("," ord(")
    file_content = file_content.replace("LOGICAL (","logical(")
    file_content = file_content.replace("INTEGER (","to_int(")
    file_content = file_content.replace(" integer ("," to_int(")
    file_content = replace_exact(file_content,"integer (","to_int(")
    file_content = file_content.replace("DECIMAL (","to_decimal(")
    file_content = file_content.replace("DEC (","to_decimal(")
    file_content = file_content.replace("INT (","to_int(")
    file_content = file_content.replace("ENTRY (","entry(")
    file_content = file_content.replace("ROUND (","round(")
    file_content = file_content.replace("TRUNCATE (","truncate(")
    file_content = file_content.replace(" MODULO "," % ")
    file_content = file_content.replace(" MOD "," % ")
    file_content = file_content.replace("EXTENT (","len(")
    file_content = file_content.replace("RANDOM (","random.randint(")
    file_content = file_content.replace(" random ("," random.randint(")
    file_content = file_content.replace("translateextended (","translateExtended (")


    file_content = file_content.replace("\nlen ","\nlen_ ")
    file_content = file_content.replace(" len "," len_ ")
    file_content = file_content.replace(" len,"," len_,")
    file_content = file_content.replace(" LENGTH ("," len(")
    file_content = file_content.replace("\nLENGTH ("," len(")
    file_content = file_content.replace(" length ("," len(")
    file_content = file_content.replace(" hServer:CONNECT (","set_combo_session(")
    file_content = file_content.replace("hServer:DISCONNECT (","reset_combo_session(")


    file_content = file_content.replace(" DATE ("," date_mdy(")
    file_content = file_content.replace(" ADD-INTERVAL ("," add_interval(")
    file_content = file_content.replace(" ADD_INTERVAL ("," add_interval(")
    file_content = file_content.replace(" TIME"," get_current_time_in_seconds()")

    file_content = file_content.replace(" NOW"," get_current_datetime()")
    file_content = file_content.replace(" INTERVAL ("," get_interval(")


    file_content = file_content.replace("SOURCE","source")

    file_content = replace_with_clear(file_content)

    file_content = remove_multiple_chars(file_content," ")

    # file_content = remove_multiple_chars(file_content," ")
    file_content = "\n".join([line.strip(" ") for line in file_content.split("\n")])


    file_content = file_content.replace("\n.",".")

    # file_content = file_content.replace("\n:",":")
    # file_content = file_content.replace("\n.",".")
    # file_content = file_content.replace(",\n",", ")
    
    file_content = file_content.replace(" AND\n"," AND ")
    file_content = file_content.replace(" AND \n"," AND ")
    file_content = file_content.replace(" OR\n"," OR ")
    file_content = file_content.replace(" OR \n"," OR ")
    # file_content = file_content.replace("\n\nAND "," AND ")
    # file_content = file_content.replace("\nAND "," AND ")
    # file_content = file_content.replace("\nOR "," OR ")

    file_content = file_content.replace("NOT ","not ")

    file_content = file_content.replace(" AVAILABLE "," None != ")
    file_content = file_content.replace(" AVAIL "," None != ")

    # file_content = file_content.replace(" RECID ("," recid(")

    file_content = file_content.replace(" DAY ("," get_day(")
    file_content = file_content.replace(" day ("," get_day(")
    file_content = file_content.replace(" MONTH ("," get_month(")
    file_content = file_content.replace(" month ("," get_month(")
    file_content = file_content.replace(" YEAR ("," get_year(")
    file_content = file_content.replace(" year ("," get_year(")
    file_content = file_content.replace(" WEEKDAY ("," get_weekday(")
    file_content = file_content.replace(" weekday ("," get_weekday(")
    file_content = file_content.replace(" TODAY)"," get_current_date()),")
    file_content = file_content.replace(" TODAY,"," get_current_date(),")
    file_content = file_content.replace(" TODAY."," get_current_date().")
    file_content = file_content.replace(" TODAY "," get_current_date() ")
    file_content = file_content.replace(" TODAY\n"," get_current_date()\n")
    file_content = file_content.replace(" today."," get_current_date().")
    file_content = file_content.replace(" today "," get_current_date() ")
    file_content = file_content.replace(" today\n"," get_current_date()\n")
    file_content = file_content.replace(" DATETIME ("," to_datetime(")
    file_content = file_content.replace(" TIME"," get_current_time_in_seconds()")
    file_content = file_content.replace(" time "," get_current_time_in_seconds() ")
    file_content = file_content.replace(" time."," get_current_time_in_seconds()")
    file_content = file_content.replace(" time\n"," get_current_time_in_seconds()\n")
    file_content = file_content.replace(" SESSION:DATE_FORMAT "," session_date_format() ")

    file_content = file_content.replace(" GENERATE_PBE_KEY ("," create_cipher_suite(")
    file_content = file_content.replace(" ENCRYPT ("," encrypt_with_cipher_suite(")


    

    file_content = file_content.replace("\n\nFIELD ","\nFIELD ")
    file_content = file_content.replace("\nFIELD ","|FIELD ")
    file_content = file_content.replace(" FIELD ","|FIELD ")

    file_content = file_content.replace(",FIRST ",", FIELD ")
    file_content = file_content.replace(",EACH ",", EACH ")

    file_content = file_content.replace(" INDEX ("," 1 + get_index(")


    file_content = file_content.replace(".NAME ",".name ")
    file_content = file_content.replace(".KEY ",".key ")

    file_content = file_content.replace("INTERFACE","interface")
    file_content = file_content.replace("PRINTER","printer")
    file_content = file_content.replace("NEXT."," continue")

    file_content = file_content.replace("vhp.","")
    file_content = file_content.replace("vhp .","")
    file_content = file_content.replace("VHP.","")
 
    file_content = file_content.replace(" SHA1_DIGEST ("," sha1(")

    file_content = file_content.replace("\nINIT "," INIT ")
    file_content = file_content.replace("\nINITIAL "," INITIAL ")

    file_content = file_content.replace("?","None")

    file_content = file_content.replace(" then ", " THEN ")
    file_content = file_content.replace(" THEN ."," THEN\npass\n\n")
    file_content = file_content.replace(" THEN"," THEN\n")
    file_content = file_content.replace(" THEN\n"," THEN\n\n\n")

    file_content = file_content.replace("DO:.","DO:\n.")
    file_content = file_content.replace("DO: ","DO:\n")

    file_content = file_content.replace("OTHERWISE ","ELSE ")

    file_content = file_content.replace("else ","\ELSE\n")
    file_content = file_content.replace("else\nif","ELSE IF")

    file_content = file_content.replace("else do:","ELSE\nDO:\n")
    file_content = file_content.replace("else if ","ELSE IF ")

    file_content = file_content.replace("ELSE .","")
    file_content = file_content.replace("ELSE.","")

    file_content = file_content.replace("ELSE ","\nELSE\n")
    file_content = file_content.replace("ELSE\nIF","ELSE IF")
    file_content = file_content.replace("} IF ","}\nIF ")
    file_content = file_content.replace("} {","}\n{")

    file_content = file_content.replace("LEAVE","break")
    file_content = file_content.replace("RETURN","return")


    file_content = file_content.replace("\nrun ","\nRUN ")

    file_content = file_content.replace("[ ","[")
    file_content = file_content.replace(" ]","]")
    file_content = file_content.replace(" END.","\nEND.")

    file_content = file_content.replace("\n\n","\n")

    file_content = file_content.replace("\n ","\n")
    file_content = file_content.replace(" \n","\n")
    file_content = file_content.replace(",\n",", ")

    file_content = file_content.replace("..",".")
    file_content = file_content.replace(". .",".")

    file_content = file_content.replace('"":U','""')

    file_content = remove_multiple_chars(file_content," ")

    file_content = file_content.replace("\n+ "," +{backslash}{newline}")
    file_content = file_content.replace("\n- "," -{backslash}{newline}")
    file_content = file_content.replace("\n* "," *{backslash}{newline}")
    file_content = file_content.replace("\n/ "," /{backslash}{newline}")

    # file_content = file_content.replace("\n + "," +backslash}{newline}")
    # file_content = file_content.replace("\n - "," -{backslash}{newline}")
    # file_content = file_content.replace("\n * "," *{backslash}{newline}")
    # file_content = file_content.replace("\n / "," /{backslash}{newline}")

    # file_content = file_content.replace("\n  + "," +backslash}{newline}")
    # file_content = file_content.replace("\n  - "," -{backslash}{newline}")
    # file_content = file_content.replace("\n  * "," *{backslash}{newline}")
    # file_content = file_content.replace("\n  / "," /{backslash}{newline}")


    file_content = file_content.replace(" =\n"," ={backslash}{newline}")
    file_content = file_content.replace(" +\n"," +{backslash}{newline}")
    file_content = file_content.replace(" /\n"," /{backslash}{newline}")
    file_content = file_content.replace(" *\n"," *{backslash}{newline}")
    file_content = file_content.replace(" /\n"," /{backslash}{newline}")
    
    file_content = file_content.replace("<START>","<START>\n")
    file_content = file_content.replace("<END>","<END>\n")


    return file_content

def finishing_py_content(file_content):

    return file_content

def update_var_names(file_content):

    main_var_names = [var.split(":")[0].split("=")[0].strip(" ") for var in main_func_vars]
    if not "fchar" in main_var_names and not "fchar" in [var_name.split(":")[0] for var_name in main_func_params]:
        file_content = file_content.replace(" fchar "," htparam.fchar ")
        file_content = file_content.replace(" fchar\n"," htparam.fchar\n")
        file_content = file_content.replace("(fchar)","(htparam.fchar)")
        file_content = file_content.replace(",fchar ",",htparam.fchar ")

    if not "fdate" in main_var_names and not "fdate" in [var_name.split(":")[0] for var_name in main_func_params]:
        file_content = file_content.replace(" fdate "," htparam.fdate ")
        file_content = file_content.replace(" fdate\n"," htparam.fdate\n")
        file_content = file_content.replace("(fdate)","(htparam.fdate)")
        file_content = file_content.replace(",fdate ",",htparam.fdate ")


    if not "finteger" in main_var_names and not "finteger" in [var_name.split(":")[0] for var_name in main_func_params]:
        file_content = file_content.replace(" finteger "," htparam.finteger ")
        file_content = file_content.replace(" finteger\n"," htparam.finteger\n")
        file_content = file_content.replace("(finteger)","(htparam.finteger)")
        file_content = file_content.replace(",finteger ",",htparam.finteger ")
    
    if not "flogical" in main_var_names and not "flogical" in [var_name.split(":")[0] for var_name in main_func_params]:
        file_content = file_content.replace(" flogical "," htparam.flogical ")
        file_content = file_content.replace(" flogical\n"," htparam.flogical\n")
        file_content = file_content.replace("(flogical)","(htparam.flogical)")
        file_content = file_content.replace(",flogical ",",htparam.flogical ")
    
    if not "ptexte" in main_var_names and not "ptexte" in [var_name.split(":")[0] for var_name in main_func_params]:
        file_content = file_content.replace(" ptexte "," paramtext.ptexte ")
        file_content = file_content.replace(" ptexte\n"," paramtext.ptexte\n")
        file_content = file_content.replace("(ptexte)","(paramtext.ptexte)")
        file_content = file_content.replace(",ptexte ",",paramtext.ptexte ")

    return file_content

def create_py_file(file_path, file_name):
    global file_content, py_vars, curr_file_name
    global import_line, line_case, table_import_list,inner_functions, curr_body, buffer_list
    global def_dataclass, def_main_func, main_func_vars, main_func_return, body_main_func_line
    global data_class_list, curr_buffer_list, temp_table_and_db_loop_line
    global include_file_flag
    

    f = open(file_path + "/" + file_name, "r")
    if re.match(r".*\.i",file_name):
        include_file_flag = True


    import_line = ["from functions.additional_functions import *","import decimal"]


    line_case = ["def"]

    file_content = f.read()
    file_content = prepare_content(file_content)

    for line in file_content.split("\n"):
        # print(line)
        if re.match(r"PROCEDURE .*:.*",line, re.IGNORECASE):
            curr_buffer_list = {}
            line_case.append("PROCEDURE")
        if re.match(r"FUNCTION .*",line, re.IGNORECASE):
            line_case.append("FUNCTION")
        convert_line(line)

    curr_body = body_main_func_line

    if len(body_main_func_line) > 0 and body_main_func_line[-1].strip(" ").replace("\n","") == "":
        body_main_func_line.pop()

    if len(body_main_func_line) > 0 and body_main_func_line[-1].strip(" ").replace("\n","") != "return generate_output()":
        append_body("\n")
        append_return()

    py_file_name = convert_name(file_name.lower().replace(".i","").replace(".p","")).replace("-","_")

        
    if include_file_flag:
        py_file_name = "i_" + py_file_name
        if num_vars_include_file > 0:
            for i in range(1, num_vars_include_file + 1):
                main_func_params.append("var" + str(i))

    def_main_func = "def " + py_file_name + "(" + ", ".join(main_func_params) + "):"

    py_vars_str = ""

    if len(py_vars) > 0 :
        py_vars_str = "\n".join(py_vars) + "\n\n"


    def_table_objects = ""

    if table_import_list != []:
        def_table_objects = " = ".join(table_name.lower() for table_name in table_import_list)
        main_func_vars.append("    " + def_table_objects + " = None")
        import_line.append("from models import " + ", ".join(table_import_list))

    inner_func_str = ""
    global_fields = ""

    if main_func_vars:
        global_fields += "||||||||nonlocal "
        for var in main_func_vars:
            # var = var.strip(" ").replace ("= None","")
            if len(var.split("=")) <= 2:
                global_fields += var.split("=")[0].split(":")[0].strip(" ") + ", "
            else:
                global_fields += var.replace(" = ",", ").replace(" None","").strip(" ")
        global_fields = global_fields.strip(", ") + "\n"

    main_func_param_names = []


    for param in main_func_params:
        if not re.match(r".*\[[A-Z][a-z_]+\].*",param):
            main_func_param_names.append(param.split(":")[0])

    if main_func_param_names:
        global_fields += "||||||||nonlocal " 
        global_fields += ", ".join(main_func_param_names) + "\n"
            
    
    if buffer_list:
        global_fields += "||||||||nonlocal " 
        global_fields += ", ".join(buffer_list.keys()) + "\n"

    if global_fields != "":
        global_fields = global_fields.strip(", ") + "\n\n"

    data_class_objects_str = ""
    if data_class_objects != []:
        data_class_objects_str = "    " + " = ".join(data_class_objects)
        data_class_objects_str += " = None\n\n"
        global_fields += "||||||||nonlocal " 
        global_fields += ", ".join(data_class_objects) + "\n"

    if data_class_list != []:       
        global_fields += "||||||||nonlocal " 
        global_fields += ", ".join(data_class_list) + "\n"

    for name, params, body_lines, vars, output_params, input_param_names in inner_functions:
        define_var_list = []
        for var in vars:
            if re.match(r".*:.* = .*",var):
                define_var_list.append(var.split(":")[0].strip(" "))


        # print(global_fields)
        inner_func_str += "    def " + name + "(" + ", ".join(params) + "):\n\n"
        # if file_name == "mkres-gname_1BL.p":
        #     print(name)
        #     print(name, params, vars, output_params, input_param_names)

        for field in global_fields.split(" "):

            field_clean = field.replace(",","").strip(" ").split("\n")[0]

            # if not field_clean in [param.split(":")[0] for param in params][1:] and\
            if not field_clean in [param.split(":")[0] for param in params] and\
                not field_clean in define_var_list and\
                not field_clean in input_param_names:


                inner_func_str += field.replace("|"," ") + " "
        
        inner_func_str = inner_func_str.rstrip(", ")  
                

        # inner_func_str += global_fields
        inner_func_str += "\n"
        inner_func_str += "\n".join(["        " + var.strip(" ") for var in vars]) + "\n"
        

        if output_params != []:

            inner_func_str += "\n"
            inner_func_str += "        def generate_inner_output():\n"
            inner_func_str += "            return (" + ", ".join(output_params) + ")\n\n"
    
        body_line_str = "".join(body_lines) + "\n"
        inner_func_str += update_var_names(body_line_str) + "\n"

        if output_params != []:
            # inner_func_str += "        db_session.commit()\n"
            inner_func_str += "        return generate_inner_output()\n\n"

        inner_func_str += "\n"

    main_return_func  = "    def generate_output():\n"
    main_return_func += global_fields.replace("|"," ")
    # main_return_func += "        db_session.commit()\n"
    main_return_func += "        return {" + ", ".join(main_func_return) + "}"


    buf_str = ""

    for buffer_name,table_name in buffer_list.items():
        if table_name in db_tables:
            buf_str += "    " + convert_to_class_name(buffer_name) + " = create_buffer(\"" + convert_to_class_name(buffer_name) + "\","  + convert_to_class_name(table_name) + ")\n"
        else:        
            buf_str += "    " + convert_to_class_name(buffer_name) + " = "  + convert_to_class_name(table_name) + "\n"

        if not table_name in db_tables:
            buf_str += "    " + buffer_name + "_list = "  + table_name + "_list\n\n"


        
    """    
    file_content = (
        "\n".join(import_line) + "\n\n" + 
        

        "\n".join([var.strip(" ") for var in main_func_vars]) + "\n\n" +

        data_class_objects_str +

        "\n".join(def_dataclass) + "\n\n" +
        buf_str + "\n" + 

        def_main_func + "\n\n" +
        global_fields.replace("|"," ").replace("        ","    ") + "\n"
        "    db_session = local_storage.db_session" + "\n" +
        
        "\n\n" +

        main_return_func + "\n\n" +
        inner_func_str +

        "".join(body_main_func_line)
    )
    """

    file_content = (
        "\n".join(import_line) + "\n\n" + 

        py_vars_str + 

        def_main_func + "\n" +
        # global_fields.replace("|"," ").replace("        ","    ") + "\n"

        "\n".join(["    " + var.strip(" ") for var in main_func_vars]) + "\n\n" +

        data_class_objects_str +

        "    " + "\n    ".join(def_dataclass) + "\n\n" +
        buf_str + "\n" + 


        "    db_session = local_storage.db_session" +
        
        "\n\n" +

        main_return_func + "\n\n" +
        inner_func_str +

        update_var_names("".join(body_main_func_line))
    )

    file_content = replace_incomplete_variable_names(file_content,incomplete_var_names)

    for table_name in table_import_list:
        table_name = table_name.lower()
        # file_content = replace_exact(file_content,table_name + "." + table_name + ".",table_name + ".")
        file_content = replace(file_content,"(" + table_name + "." + table_name + ".", "(" + table_name + ".")
        file_content = replace(file_content," " + table_name + "." + table_name + ".", " " + table_name + ".")
        file_content = replace(file_content,convert_to_class_name(table_name) + "." + table_name + ".", convert_to_class_name(table_name) + ".")

        if table_name == "arrangement":
            file_content = file_content.replace(" arrangement.lower()"," arrangement.arrangement.lower()")
            file_content = file_content.replace("(arrangement.lower()","(arrangement.arrangement.lower()")

    file_content = "\n".join([line.rstrip(" ") for line in file_content.split("\n")])
    

    file_content = canonicalize_variables(file_content,all_vars.keys())
    db_query_index_matches = re.findall(r"\b[A-Z]\w*\.\w*\[.*\]",file_content)
    
    modified_index = ""
    if db_query_index_matches:
        for match_str in db_query_index_matches:
            modified_index = match_str.replace("[","[inc_value(").replace("]",")]")
            file_content = file_content.replace(match_str,modified_index)

    file_content = file_content.replace(" ASSIGN\n"," \n")
    file_content = file_content.replace(".CODE"," .code")

    file_content = file_content.replace("tFrequency", "tfrequency")
    file_content = file_content.replace("FB_vatlist", "fb_vatlist")
    file_content = file_content.replace("drBuff"    , "drbuff")
    file_content = file_content.replace("tb3Buff"   , "tb3buff")
    file_content = file_content.replace("artBuff"   , "artbuff")
    file_content = file_content.replace("actionBuff", "actionbuff")
    file_content = file_content.replace("actionBuff", "actionbuff")
    file_content = file_content.replace("vatBuff"   , "vatbuff")

    file_content = file_content.replace("MENU"   , "menu")

    
    file_content = file_content.replace("fLocation_list", "flocation_list")
    file_content = file_content.replace("tLocation_list", "tlocation_list")
    file_content = file_content.replace("dynaRate_list" , "dynarate_list")
    file_content = file_content.replace("res_dynaRate"  , "res_dynarate")
    file_content = file_content.replace("gc_PIbline"    , "gc_pibline")

    file_content = file_content.replace("UserSkill_list", "userskill_list")
    file_content = file_content.replace("eg_Duration"   , "eg_duration")
    file_content = file_content.replace("tStatus_list"  , "tstatus_list")
    file_content = file_content.replace("tMaintask_list", "tmaintask_list")
    file_content = file_content.replace("comCategory"   , "comcategory")
    file_content = file_content.replace("eg_propMeter"  , "eg_propmeter")

    file_content = file_content.replace(".STR, "  , ".str, ")
    file_content = file_content.replace(".STR , "  , ".str , ")

    file_content = file_content.replace("::",":")

    file_content = file_content.replace(" &  (not "," & not_(")
    


    file_content = file_content.replace("::",":")
    file_content = file_content.replace("if None != ","if ")
    file_content = file_content.replace("if None == ","if not ")
    file_content = file_content.replace("( ","(")
    file_content = file_content.replace(" )",")")
    file_content = file_content.replace(" ()","()")
    file_content = file_content.replace(" .",".")
    file_content = file_content.replace("DO TRANSACTION","")
    file_content = file_content.replace("{V_H_P}","VHP")
    file_content = file_content.replace("{V__H__P}","VHP")
    file_content = file_content.replace("{v_h_p}","vhp")
    file_content = file_content.replace("{v__h__p}","vhp")
    file_content = file_content.replace("{space}"," ")
    file_content = file_content.replace("{comma}",",")
    file_content = file_content.replace("{dash}","-")
    file_content = file_content.replace("{underscore}","_")
    file_content = file_content.replace("{open_square_bracket}","[")
    file_content = file_content.replace("{open__square__bracket}","[")
    file_content = file_content.replace("{close_square_bracket}","]")
    file_content = file_content.replace("{close__square__bracket}","]")
    file_content = file_content.replace("{open_bracket}","(")
    file_content = file_content.replace("{open__bracket}","(")
    file_content = file_content.replace("{close_bracket}",")")
    file_content = file_content.replace("{close__bracket}",")")
    file_content = file_content.replace("{open_curly_bracket}","{")
    file_content = file_content.replace("{open__curly__bracket}","{")
    file_content = file_content.replace("{close_curly_bracket}","}")
    file_content = file_content.replace("{close__curly__bracket}","}")
    file_content = file_content.replace("{question_mark}","?")
    file_content = file_content.replace("{question__mark}","?")
    file_content = file_content.replace("{backslash}","\\")
    file_content = file_content.replace("{newline}","\n")
    file_content = file_content.replace("{colon}",":")
    file_content = file_content.replace("{perc}","%")
    file_content = file_content.replace("{equal}","=")
    file_content = file_content.replace("{a_n_d}","&")
    file_content = file_content.replace("{a__n__d}","&")
    file_content = remove_multiple_chars(file_content, "\n\n")
    reset_variables()

    return file_content

create_table_field_list()


# file_path = "/Users/christoferyie/Documents/Projects/VHP Serverless/convert" 
file_path = f"D:/docker/app_konversi/input/vhp-serverless/image/src/output"
file_path = file_path.rstrip("/") + "/"

# source_file_path = file_path + "check-p-files2/"
# source_file_path = file_path + "check-p-files3/"

source_file_path = file_path + "check-p-files2/"
target_file_path = file_path + "converted2/"

# source_file_path = file_path + "check-p-files/"
# target_file_path = file_path + "converted2/"

# source_file_path = file_path + "p-files/"
# target_file_path = file_path + "converted/"

temp_table_and_db_loop_list = []

for file_name in sorted(os.listdir(source_file_path)):
    if re.match(r".*\.(p|i)$",file_name, re.IGNORECASE)\
        and not re.match(r"-.*",file_name) and\
                file_name != "get-user-tokenBL.p":
        print(file_name)
        curr_file_name = file_name

        file_content = create_py_file(source_file_path, file_name)

        if(temp_table_and_db_loop_line != []):
            temp_table_and_db_loop_list.append(file_name)
            
            for line in temp_table_and_db_loop_line:
                temp_table_and_db_loop_list.append(line)

            temp_table_and_db_loop_list.append("")    
            temp_table_and_db_loop_line = []

        new_file_name = ""
        if re.match(r".*\.i", file_name):
            new_file_name = "i_" + convert_name(file_name.replace(".i",".py").replace("-","_").lower())
        else:
            new_file_name = convert_name(file_name.replace(".p",".py").replace("-","_").lower())

        f = open(target_file_path + new_file_name, "w")
        f.write(file_content)
        f.close()


all_operation_path = os.getcwd() + "/modules/additional_operation.txt"

with open(all_operation_path, 'w') as output_file_all:
    all_operations_str = "\n".join(import_file_list)
    output_file_all.write(f"{all_operations_str}")

temp_table_and_db_loop_path = os.getcwd() + "/temp_table_and_db_loop.txt"

with open(temp_table_and_db_loop_path, 'w') as output_file_all:
    lines_str = "\n".join(temp_table_and_db_loop_list)
    output_file_all.write(f"{lines_str}")
