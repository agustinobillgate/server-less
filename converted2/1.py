import re

def annotate_db_session_loops(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Pattern to match 'for ... in db_session.query(...)' including multiple variables
    loop_pattern = re.compile(r'^\s*for\s+[\w\s,]+\s+in\s+db_session\.query\(')

    # Pattern to match 'db_session.query(...)' in assignments (excluding loops)
    query_pattern = re.compile(r'^\s*\w+\s*=\s*db_session\.query\(')

    modified_lines = []

    for i, line in enumerate(lines):
        if loop_pattern.search(line):
            indentation = re.match(r'(\s*)', line).group(1)  # Capture indentation
            modified_lines.append(f"{indentation}# for loop\n")  # Add comment before loop
            modified_lines.append(line)
            continue

        if query_pattern.search(line):
            indentation = re.match(r'(\s*)', line).group(1)  # Capture indentation
            modified_lines.append(f"{indentation}# db query\n")  # Add comment before query
            modified_lines.append(line)
            continue

        modified_lines.append(line)

    output_file = f"_{input_file}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)

    print(f"Annotated file saved as: {output_file}")

# Example usage
input_filename = "cr_occfcast1_2_webbl.py"  # Replace with your actual filename
annotate_db_session_loops(input_filename)
