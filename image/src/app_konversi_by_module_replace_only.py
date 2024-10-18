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
vhp_module = "Common"
nfiles = 0
nAnakCucu = 0


# -----------------------------------------------------------------
# Proses AddOn
# -----------------------------------------------------------------
vhp_module = "Replace_Only"
recid = datetime.now().strftime("%Y%m%d_%H%M%S")

def replace_in_files(dest_folder, search_list, log_file=f"{folder_log}/{vhp_module}_{recid}_replacement.txt"):
    # Open the log file for writing
    print("Log:",log_file)
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
    (" zimmer.zis ", " zimmer.zistatus "),
    (" zimmer.zistat ", " zimmer.zistatus "),
    ("[zimmer.zistat ", "[zimmer.zistatus "),
    ("zimmer.zistatusus", "zimmer.zistatus"),
    ("Zimmer.Zimmer.Zimmer.", "Zimmer."),                                       # hk_zimaidbl 
    ("Zimmer.Zimmer.", "Zimmer."),                                              # hk_zimaidbl 
    
    ("and n < len(vstring) :", "and n < len(parameters.vstring) :"),            # prepare_if_country1bl.py, baris 73 dan 138
    ("i = zinrstat.datum - datum1 + 1", "i = (zinrstat.datum - datum1).days + 1"),   # def day_ruse_create_browsebl(from_room:str, curr_date:date):
    ("datum2 = datum1 + 1", "datum2 = datum1 + timedelta(days=1)"),
    ("for datum in range(curr_date,datum1 + 1) :", "for datum in date_range(curr_date,datum1 + timedelta(days=1)) :"),
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
    ("segm1_list.bezeich = to_string(segmentcode, \">>9 \") + entry(0, segment.bezeich, \"$$0\")", "segm1_list.bezeich = to_string(segment.segmentcode, \">>9 \") + entry(0, segment.bezeich, \"$$0\")"),
    ("to_string(counter.counter, \"9999\")", "to_string(counters.counter, \"9999\")"),
    ("(func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) ", "(func.lower(L_ophdr1.(lscheinnr)) == (lscheinnr).lower()) "),
    ("Rline.Rline.", "Rline."),
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
    (" (not Res_line.curr_date >= Res_line.abreise))", " (not curr_date >= Res_line.abreise))")

]





replace_in_files(folder_py, search_list)

print("--------------------------------------------------------------")
print("Replace String selesai.")
print("--------------------------------------------------------------\n")


# print((json_output))
os.chdir(curdir)
