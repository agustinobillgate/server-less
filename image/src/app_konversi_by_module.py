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
vhp_module = "vhpEG"
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
command = f'wsl bash -c "source /mnt/d/docker_linux/app_konversi/lenv/bin/activate && python /mnt/d/docker_linux/app_konversi/input/vhp-serverless/image/src/tflinux_p_py_converter.py"'
print("--------------------------------------------------------------")
print(f" Start konversi: nFiles = {nfiles}, nAnakCucu = {nAnakCucu}")
print("--------------------------------------------------------------\n")
result = subprocess.run(command, capture_output=True, text=True, shell=True)
print(result.stdout)
print("----------TF Konversi Selesai-------------------")
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

def replace_in_files(dest_folder, search_list, log_file=f"{folder_log}/{vhp_module}_{recid}_replacement.txt"):
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

def replace_get_month_day(query_str):
    # Replace get_month(Guest.geburtdatum1) with extract('month', Guest.geburtdatum1)
    query_str = re.sub(r'get_month\((\w+.\w+)\)', r"extract('month', \1)", query_str)
    # Replace get_day(Guest.geburtdatum1) with extract('day', Guest.geburtdatum1)
    query_str = re.sub(r'get_day\((\w+.\w+)\)', r"extract('day', \1)", query_str)
    # Replace get_current_date() with func.current_date() in SQLAlchemy format
    query_str = query_str.replace('get_current_date()', 'func.current_date()')
    return query_str

def process_file(file_path, search_list, log_file):
    py_filename_list = ["birthday_list_1bl.py"]
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

        # check get_month and get_day
        # check custom by filename, yg sudah dikenal
        if os.path.basename(file_path) in py_filename_list:
            new_line = replace_get_month_day(new_line)
    
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
    ("(Htparam.bezeich)", "(Htparam.bezeichnung)"),
    ("(Htparam.bezeich)", "(Htparam.bezeichnung)"),
    ("htparam.bezeich ", "htparam.bezeichnung "),
    ("Htparam.bezeich ", "Htparam.bezeichnung "),
    
    (".CODE", ".code"),
    (".CHAR", ".char"),
    
    (".NAME", ".name"),    
    (".SECTION", ".section"),
    
    (".PARENT", ".parent"),
    (".SOURCE", ".source"),    
    (".TERMINATE", ".terminate"),

    (".WARNING", ".warning"),
    (".YEAR", ".year"),    
    (".MONTH", ".month"),
    
    (".SELECTED", ".selected"),
    (".FREQUENCY", ".frequency"),
    (".TYPE", ".type"),    
    (".POSITION", ".position"),

    (".MODIFIED", ".modified"),
    (".REQUEST", ".request"),    
    (".LINE", ".line"),

    (".FILENAME", ".filename"),
    
    ("ASSIGN", ""),         # gl_joulist_1_webbl
    ("Res_line.Res_line.resstatus ", "Res_line.resstatus "),
    ("Res_line.Res_line.active_flag ", "Res_line.active_flag "),
    ("Res_line.Res_line.", "Res_line."),
    ("Res_line.Res_line.", "Res_line."),
    ("htparam.paramgr ", "htparam.paramgruppe "),
    ("Htparam.paramgr ", "Htparam.paramgruppe "),
    ("htparam.bezeich ", "htparam.bezeichnung "),
    ("(Gl_acct.Gl_acct.Gl_acct.acc_type ==", "(Gl_acct.acc_type =="),
    ("curr_stat = stat_list[zistatus + 1 - 1]", "curr_stat = stat_list[zimmer.zistatus + 1 - 1]"),
    ("if not parameters or not(progname.lower() ", "if not parameters or not(parameters.progname.lower() "),
    ("arl_list.bestat_dat = reservation.bestat_dat\n", "arl_list.bestat_dat = reservation.bestat_datum\n"),          # arl-list-disp-arlist3-webBL (1641)
    (" zimmer.zistat ", " zimmer.zistatus "),
    ("zimmer.zistat\n", "zimmer.zistatus\n"),
    ("zimmer.zista\n", "zimmer.zistatus\n"),
    ("zimmer.zist\n", "zimmer.zistatus\n"),
    ("zimmer.zis\n", "zimmer.zistatus\n"),
    (" zimmer.zis ", " zimmer.zistatus "),
    (" zimmer.zistat ", " zimmer.zistatus "),
    ("[zimmer.zistat ", "[zimmer.zistatus "),
    ("zimmer.zistatusus", "zimmer.zistatus"),
    ("Zimmer.Zimmer.Zimmer.", "Zimmer."),                                       # hk_zimaidbl 
    ("Zimmer.Zimmer.", "Zimmer."),                                              # hk_zimaidbl 
    
    ("and n < len(vstring) :", "and n < len(parameters.vstring) :"),            # prepare_if_country1bl.py, baris 73 dan 138
    ("i = zinrstat.datum - datum1 + 1", "i = (zinrstat.datum - datum1).days + 1"),   # def day_ruse_create_browsebl(from_room:str, curr_date:date):
    ("datum2 = datum1 + 1", "datum2 = datum1 + timedelta(days=1)"),
    ("htparam.fdate - 1", "htparam.fdate - timedelta(days=1)"),
    ("htparam.fdate + 1", "htparam.fdate + timedelta(days=1)"),
    ("for datum in range(curr_date,datum1 + 1) :", "for datum in date_range(curr_date,datum1 + timedelta(days=1)) :"),
    ("for i in range(1,(to_date - curr_date + 1)", "for i in range(1,(to_date - curr_date).days + timedelta(days=1))"),
    
    ("l_orderhdr.lieferdatum = billdate + 1", "l_orderhdr.lieferdatum = billdate + timedelta(days=1)"),
    ("to_date = date_mdy(mm + 1, 01, yy) - timedelta(days=1)", "to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)"),
    ("to_date = date_mdy(01, 01, yy + timedelta(days=1)) - timedelta(days=1)", " to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)"),
    ("from_date = date_mdy(mm, 01, yy)", "from_date = date_mdy(mm, 1, yy)"),
    ("from_date = date_mdy(01, 01, yy)", "from_date = date_mdy(1, 1, yy)"),
    ("from_date = date_mdy(mm {minus} 3, 01, yy)", "from_date = date_mdy(mm - 3, 1, yy)"),
    ("fromdate = billdate - 30", "fromdate = billdate - timedelta(days=30)"),
    ("gc_pi.chequeNo", "gc_pi.chequeno"),
    ("gc_pi.postDate", "gc_pi.postdate"),
    ("gc_pi.returnAmt", "gc_pi.returnamt"),
    ("gc_pi.rcvID", "gc_pi.rcvid"),

    ("Gc_pi.chequeNo", "Gc_pi.chequeno"),
    ("Gc_pi.postDate", "Gc_pi.postdate"),
    ("Gc_pi.returnAmt", "Gc_pi.returnamt"),
    ("Gc_pi.rcvID", "Gc_pi.rcvid"),
    ("Gc_pi.rcvName", "Gc_pi.rcvname"),
    ("(Gc_pi.pi_status == sorttype) &  (pay_type == 2)", " (Gc_pi.pi_status == sorttype) &  (Gc_pi.pay_type == 2)"),
    ("segm1_list.bezeich = to_string(segmentcode, ", "segm1_list.bezeich = to_string(segment.segmentcode, "),
    ("(func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) ", "(func.lower(L_ophdr1.(lscheinnr)) == (lscheinnr).lower()) "),
    ("Rline.Rline.", "Rline."),
    ("to_string(counter.counter, \"9999\")", "to_string(counters.counter, \"9999\")"),
    ("paramtext.ptext\n", "paramtext.ptexte\n"),
    ("l_order.lief_fax[2] = l_artikel.traubensort\n", "l_order.lief_fax[2] = l_artikel.traubensorte\n"),
    (" (artnr == s_artnr)).first()", " (L_artikel.artnr == s_artnr)).first()"),
    (" (func.lower(L_order.(docu_nr).lower()) ", " (func.lower(L_order.docu_nr) "),
    ("if not gc_PIacct:", "if not gc_piacct:"),
    ("   gc_piacct_bezeich = gc_PIacct.bezeich", "   gc_piacct_bezeich = gc_piacct.bezeich"),
    ("print_rc_list.arrival = to_string(ankunft, ", "print_rc_list.arrival = to_string(res_line.ankunft, "),
    ("print_rc_list.departure = to_string(abreise, ", "print_rc_list.departure = to_string(res_line.abreise, "),
    ("cl_list.firstname = RIGHT_trim(", "cl_list.firstname = right_trim("),
    ("cl_list.lastname = RIGHT_trim(", "cl_list.lastname = right_trim("),
    (".order_by(Zimkateg.bezeich)", ".order_by(Zimkateg.bezeichnung)"),
    ("(not Res_line.to_date < Res_line.ankunft) & ", "(not to_date < Res_line.ankunft) & "),
    (" (not Res_line.curr_date >= Res_line.abreise))", " (not curr_date >= Res_line.abreise))"),

    ("for zimmer in db_session.query(Zimmer).order_by(len(zinr), zinr).all():", "for zimmer in db_session.query(Zimmer).order_by(len(Zimmer.zinr), Zimmer.zinr).all():"),
    ("gl_journal.fibukonto = gc_PI.debit_fibu", "gl_journal.fibukonto = gc_pi.debit_fibu"),
    ("curr_lager = l_op.lager", "curr_lager = l_op.lager_nr"), 
    ("from_date = htparam.fdate + 1", "from_date = htparam.fdate + timedelta(days=1)"),
    ("(Qbuff.KEY == ", "(Qbuff.key == "),
    ("Queasy.KEY == ", "Queasy.key == "),
    ("comcategory.comcategory.categ_SELECTED)):", "comcategory.categ_selected):"),
    (").order_by(len(", ").order_by(func.length("),
    ("Eg_request.property)", "Eg_request.propertynr)"),
    ("qty = qty + anz_verbrau", "qty = qty + l_verbrauch.anz_verbrau"),
    ("val = val + wert_verbrau", "val = val + l_verbrauch.wert_verbrau"),


            

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
