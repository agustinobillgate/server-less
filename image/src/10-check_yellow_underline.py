import subprocess
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
nfiles = 0


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

def insert_activity(json_source_list, json_results_list, lognotes):
    try:
        query = "INSERT INTO log_activity (logtype, logjson, result_json, lognotes, call_from) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        cursor.execute(query, ('SEARCH_YELLOW', json_source_list, json_results_list, lognotes, current_file_name))
        recid = cursor.fetchone()['id']
        conn.commit()
    except Exception as e:
        recid = uuid.uuid4().hex
        print(e)

# List of scripts to run sequentially
list_py = ['mk_po_btn_val_chg_currencybl.py',
           'hk_ooo_remove_selected_data_webbl.py',
           'main_gl_mi_reportbl.py']

list_scripts = ['10a-collect_var_func_fields.py',
                '10b-check_variable.py' 
                ]
list_py = list_files_in_folder(folder_p)

def update_log(recid, lognotes):
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

for script in list_scripts:
    for file_py in list_py:
        json_source_list = {"tools_py": script}
        json_results_list = {"file_py": file_py}
        lognotes = "-"
        recid = insert_activity(json.dumps(json_source_list), json.dumps(json_results_list), lognotes)
        print(f"Running {script} with arguments {file_py}")
        subprocess.run(['python', script, file_py, recid], check=True)
        subprocess.run(['python', script, file_py, recid], check=True)
        print(f"Finished {script}.\n")

