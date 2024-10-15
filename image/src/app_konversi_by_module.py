import os, re, importlib, json, textwrap, subprocess, sys, shutil
from functions.additional_functions import *
import sqlalchemy as sa
from fuzzywuzzy import process
import psycopg2
from psycopg2.extras import RealDictCursor

curdir = os.getcwd()
os.chdir(f"D:/docker/app_konversi/input/vhp-serverless/image/src")
current_file_name = os.path.basename(__file__)
folder_p = f"D:/docker/app_konversi/input/vhp-serverless/image/src/output/check-p-files2"
folder_py = f"D:/docker/app_konversi/input/vhp-serverless/image/src/output/converted2"
folder_log = f"D:/docker/app_konversi/input/vhp-serverless/image/src/output/log"
base_folder = f"D:/docker/app_konversi"
vhp_module = "vhpHK"
nfiles = 0
nAnakCucu = 0

if len(sys.argv) > 1:
    param = sys.argv[1]  # The parameter will be the second argument
    print(f"Received parameter: {param}")
    vhp_module = param
else:
    print("No parameter received.")


def get_list_mapping(module):
    sql_list_url_to_py = """
            select 
            m.p_filename,
            concat(m.py_filename, '.py') as py_filename,  
            p.p_nr, p.p_path
            from mapping m 
            left join p_files p on (p.p_filename = m.p_filename)
            where m.vhp_module = %s
            ORDER BY m.p_filename 
        ;
    """
    cursor.execute(sql_list_url_to_py, ( module,))
    rows = cursor.fetchall()
    return rows

def get_p_child(parent_nr):
    sql = """
        WITH RECURSIVE tree AS (
            SELECT id, parent_nr, modul_name, p_nr
            FROM p_trees
            WHERE parent_nr = %s
            UNION ALL
            SELECT t.id, t.parent_nr, t.modul_name, t.p_nr
            FROM p_trees t
            INNER JOIN tree pt ON pt.p_nr = t.parent_nr
        )
        SELECT p_filename, '-' as py_filename, tree.p_nr, p_files.p_path
        FROM tree
        left join p_files  on p_files.p_nr = tree.p_nr;
        """
    
    cursor.execute(sql, (parent_nr,))
    rows = cursor.fetchall()
    return rows

def list_files_from_sql(module):
    global nfiles, nAnakCucu
    results_list = []
    recs = get_list_mapping(module)
    nfiles = 0
    for r in recs:
        if r["p_path"] != None:
            if r["p_path"].endswith("ui.p"):
                continue
            print(r['p_filename'])
            results_list.append(r["p_path"])
            source_file  = f"{base_folder}/{r['p_path']}"
            destination_file = f"{folder_p}/{r['p_filename']}"
            if os.path.isfile(source_file ):
                nfiles += 1
                shutil.copy(source_file , destination_file)
            #cari anak_cucu
            anak_cucu = get_p_child(r["p_nr"])
            # for anak in anak_cucu:
            #     source_file  = f"{base_folder}/{anak['p_path']}"
            #     destination_file = f"{folder_p}/{anak['p_filename']}"
            #     if os.path.isfile(source_file ):
            #         if not os.path.exists(destination_file):
            #             print("Copying file: ", source_file, "to", destination_file)
            #             try:
            #                 nAnakCucu += 1
            #                 shutil.copy(source_file, destination_file)
            #                 print("File copied successfully!")
            #             except Exception as e:
            #                 print(f"Failed to copy file: {e}")
            #         else:
            #             print(f"File {source_file} already exists. Skipping copy.")
            #     results_list.append(r["p_path"])
        
    return results_list

def list_files_in_folder(folder_path):
    # List all files in the specified folder
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # Convert the list of files to JSON format
        json_output = json.dumps(files, indent=4)
        
        return json_output

    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

def cleanup_folder(folder_path):
    # Use subprocess to run the del command, and ensure path handling with quotes
    command = f'del /Q "{folder_path}\\*"'
    subprocess.run(command, shell=True)
    print(f"All files in {folder_path} have been deleted.")

def connect_db():
    conn = psycopg2.connect(
        # host = "vhp-devtest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com",
        # database = "vhptools",
        # user = "vhpadmin",
        # password = "bFdq8QsQoxH1vAvO"
        host = "localhost",
        database = "vhptools",
        user = "postgres",
        password = "bali2000"

    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn

conn = connect_db()
cursor = conn.cursor(cursor_factory=RealDictCursor)
cleanup_folder(folder_p)
cleanup_folder(folder_py)
print("--------------------------------------------------------------")
print(f" Collecting files (.p)")
print("--------------------------------------------------------------\n")
json_source_list = list_files_from_sql(vhp_module)

script_name = "app_konversi_p_py_converter.py"
# with open(script_name) as f:
#     code = f.read()
# exec(code) 
# Replace with the path to your Python environment
activate_env = r"D:\docker\app_konversi\env\Scripts\activate.bat"
python_path = r"D:\docker\app_konversi\env\Scripts\python.exe"
command = f'cmd /c "{activate_env} && {python_path} {script_name}"'
print("--------------------------------------------------------------")
print(f" Start konversi: nFiles = {nfiles}, nAnakCucu = {nAnakCucu}")
print("--------------------------------------------------------------\n")
result = subprocess.run(command, capture_output=True, text=True, shell=True)

# Cara Christofer, tidakberhasil, error dalam proses, skip dulu
# -------------------------------------------------------------
# import app_konversi_p_py_converter
# -------------------------------------------------------------

json_source_list = list_files_in_folder(folder_p)
json_results_list = list_files_in_folder(folder_py)
lognotes = f"{vhp_module}, nFiles: {nfiles}, nAnakCucu: {nAnakCucu}"
try:
    query = "INSERT INTO log_activity (logtype, logjson, result_json, lognotes, call_from) VALUES (%s, %s, %s, %s, %s) RETURNING id"
    cursor.execute(query, ('KONVERSI', json_source_list, json_results_list, lognotes, current_file_name))
    recid = cursor.fetchone()['id']
    conn.commit()
except Exception as e:
    recid = uuid.uuid4().hex
    print(e)

list_converted = json.loads(json_results_list)

# -----------------------------------------------------------------
# Proses AddOn
# -----------------------------------------------------------------

def replace_in_files(dest_folder, search_list, log_file=f"{folder_log}/{recid}_replacement.txt"):
    # Open the log file for writing
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("Replacement Log\n")
        log.write("=" * 50 + "\n\n")
    
    # Walk through all files in dest_folder
    for root, dirs, files in os.walk(dest_folder):
        for file in files:
            if file.endswith(".py"):  # Only check .py files
                file_path = os.path.join(root, file)
                process_file(file_path, search_list, log_file)

def process_file(file_path, search_list, log_file):
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Flag to track if any replacements were made
    file_modified = False
    
    # Process each line and replace strings based on search_list
    new_lines = []
    for idx, line in enumerate(lines):
        new_line = line
        for search, replace in search_list:
            if search in new_line:
                original_line = new_line  # Keep a copy of the original line
                new_line = new_line.replace(search, replace)
                file_modified = True

                # Log the replacement to the log file
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(f"Filename: {file_path}\n")
                    log.write(f"Line no: {idx + 1}\n")
                    log.write(f"Line before: {original_line.strip()}\n")
                    log.write(f"Line after: {new_line.strip()}\n")
                    log.write("=" * 50 + "\n")

        new_lines.append(new_line)

    # If the file was modified, create a backup and overwrite the original file
    if file_modified:
        # Copy the original file to a .pyy backup before modifying
        backup_file_path = file_path + "y"  # Create a .pyy file
        shutil.copy(file_path, backup_file_path)
        print(f"Backup created: {backup_file_path}")
        
        # Now overwrite the original file with modified content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
        print(f"Modified file: {os.path.basename(file_path)}")
    else:
        print(f"No changes made to: {os.path.basename(file_path)}")
# Define search-replace pairs
search_list = [
    ("if not htparam or not(paramnr ==", "if not htparam or not(htparam.paramnr =="),
    (".CODE", ".code"),
    (".NAME", ".name"),    
    ("htparam.paramgr ", "htparam.paramgruppe "),
    ("htparam.bezeich ", "htparam.bezeichnung "),
    ("(Gl_acct.Gl_acct.Gl_acct.acc_type ==", "(Gl_acct.acc_type =="),
    (f"bemerk:",)
]

replace_in_files(folder_py, search_list)


print("--------------------------------------------------------------\n Tracking ID:", recid)
print(f" Hasil konversi: {nfiles} files, anak cucu: {nAnakCucu} ")
print("--------------------------------------------------------------\n")
for l in list_converted:
    print(l)
json_output = {
    "folder_py": folder_py,
    "nfiles" : nfiles,
    "proses_time": datetime.timestamp(datetime.now()),
    "source" :[
        {"source_list" : json_source_list}
    ],
    "result" :[
        {"result_list" : json_results_list}
    ]
}
print("--------------------------------------------------------------")
print("Konversi selesai.")
print("--------------------------------------------------------------\n")
# print((json_output))
os.chdir(curdir)
