import os
import re, json

dotp_directory = r'D:\docker\pixcdk\image\src\dotp'
output_directory = r'D:\docker\pixcdk\image\output'
df_file_path = r'D:\docker\pixcdk\image\src\df\240830_vhpFull.df'
df_output = r'D:\docker\pixcdk\image\output\1df.json'
log_output = r'D:\docker\pixcdk\image\output\1log.txt'
log_summary = r'D:\docker\pixcdk\image\output\1log_summary.txt'
ntable = 0

def extract_table_and_fields(df_content):
    global ntable
    table_fields = {}
    current_table = None

    for line in df_content.splitlines():
        # Detect a new table
        table_match = re.match(r'ADD TABLE "(.*?)"', line)
        if table_match:
            current_table = table_match.group(1)
            table_fields[current_table] = []
        
        # Detect a field in the current table
        field_match = re.match(r'ADD FIELD "(.*?)" OF "', line)
        if field_match and current_table:
            field_name = field_match.group(1)
            table_fields[current_table].append(field_name)
    
        # Sort fields for each table
    for table in table_fields:
        ntable = ntable + 1
        table_fields[table].sort()

    return table_fields

def generate_table_fields_from_df(df_file):
    with open(df_file, 'r', encoding='utf-8') as f:
        df_content = f.read()
    
    return extract_table_and_fields(df_content)

def save_table_fields_to_json(table_fields, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(table_fields, f, indent=4)

def create_temp_table_fields(temp_tables, table_fields):
    new_table_fields = {}

    for temp_table, like_table in temp_tables:
        if like_table in table_fields:
            # Only copy fields from the like_table to the temp_table
            new_table_fields[temp_table] = table_fields[like_table]

    return new_table_fields

def search_and_replace_in_dotp(dotp_dir, table_fields, output_directory ):
    temp_table_pattern = re.compile(
        r'^DEFINE\s+TEMP-TABLE\s+(\S+)\s+LIKE\s+(\S+)\s*\.?\s*$',
        re.IGNORECASE
    )
    
    with open(log_output, 'w', encoding='utf-8') as log, open(log_summary, 'w', encoding='utf-8') as logsummary:
        for root, dirs, files in os.walk(dotp_dir):
            counter = 0
            for file in files:
                
                if file.endswith(".p"):
                    counter = counter + 1
                    nupdate = 0
                    new_table_fields = table_fields
                    
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Search TEMP-TABLE
                    # --------------------------------------------
                    for line in lines:
                        match = temp_table_pattern.match(line.strip())
                        if match:
                            temp_table_name = match.group(1).strip('.').lower()
                            like_table_name = match.group(2).strip('.').lower()
                            if like_table_name.endswith("-list"):
                                pass
                            else:
                                new_table_fields[temp_table_name] = table_fields[like_table_name]
                                # print("Temp:", temp_table_name, like_table_name)

                    updated_lines = []

                    # Start Process
                    # --------------------------------------------
                    lineno = 0
                    for line in lines:
                        lineno += 1   
                        line = line.rstrip('\n') + ' \n'
                                       
                        original_line = line
                        for table, fields in new_table_fields.items():
                            
                            for field in fields:
                                for i in range(1, len(field)):
                                    incomplete_field = f"{table}.{field[:i]} "
                                    
                                    # Check if the incomplete field is found in the line
                                    if incomplete_field in line and not f"{table}.{field} " in line:
                                        complete_field = f"{table}.{field} "
                                        
                                        # Only replace if the complete field is not already present
                                        if complete_field not in line:
                                            # Check if replacement does not conflict with existing fields
                                            field_exists = any(f"{table}.{existing_field} " in line for existing_field in fields)
                                            
                                            if not field_exists:
                                                nupdate += 1
                                                line = line.replace(incomplete_field, complete_field)
                                                log.write(f"Updated in file: {file_path}, Line:{lineno}\n")
                                                log.write(f"Original: {original_line.strip()}\n")
                                                log.write(f"Updated:  {line.strip()}\n")
                                                log.write("-" * 60 + "\n")
                                                break  # Once replaced, no need to check further

                        updated_lines.append(line)
                        
                    # Save changes back to the output folder
                    output_file_path = os.path.join(output_directory, file)
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)
                        if nupdate > 0:
                            logsummary.write(f"file:{file}, UpdateField:{nupdate}x \n")
                            print("* nDotp:", file, counter, "/", len(files))
                        else:
                            print("nDotp:", file, counter, "/", len(files))


    with open(log_summary, 'r+', encoding='utf-8') as log1, open(log_output, 'r+', encoding='utf-8') as log2:
        log1_content = log1.read()
        log2_content = log2.read() 

        log1.seek(0, 0)
        log1.write(log1_content + "\n" + ("-" * 60 )  + "\n" + log2_content)         
                        

table_fields = generate_table_fields_from_df(df_file_path)
save_table_fields_to_json(table_fields, df_output)
search_and_replace_in_dotp(dotp_directory, table_fields, output_directory)

