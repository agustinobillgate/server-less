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
    ("zimmer.zistat\n", "zimmer.zistatus\n"),
    ("zimmer.zista\n", "zimmer.zistatus\n"),
    ("zimmer.zist\n", "zimmer.zistatus\n"),
    ("zimmer.zis\n", "zimmer.zistatus\n"),
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
    ("segm1_list.bezeich = to_string(segmentcode, \">>9 \") + entry(0, segment.bezeich, \"$$0\")", "segm1_list.bezeich = to_string(segment.segmentcode, \">>9 \") + entry(0, segment.bezeich, \"$$0\")"),
    ("to_string(counter.counter, \"9999\")", "to_string(counters.counter, \"9999\")"),
    ("(func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) ", "(func.lower(L_ophdr1.(lscheinnr)) == (lscheinnr).lower()) "),
    ("Rline.Rline.", "Rline."),
    ("Rline.Rline.", "Rline."),
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
    ("if bill_line.bill_datum <= date_mdy(08, 31, 18):", "if bill_line.bill_datum <= date_mdy(8, 31, 18):"),
    ("d2 = date_mdy(get_month(dateval) + timedelta(days=1, 1, get_year(dateval)) - 1)", "d2 = date_mdy(get_month(dateval) + 1, 1, get_year(dateval) - timedelta(days=1))"),
    ("ci_date = fdate", "ci_date = htparam.fdate"),
    (f"bediener = db_session.query(Bediener).filter(()).first()", ""),
    ("(sleeping)).all():", "(Zimmer.sleeping)).all():"),
    ("(Waehrungsnr == res_line.betriebsnr)).first()", "(Waehrung.waehrungsnr == res_line.betriebsnr)).first()"),
    ("frate = reserve_dec", "frate = res_line.reserve_dec"), 
    ("= finteger", "= htparam.finteger"),
    ("= fdate", "= htparam.fdate"),
    ("(Sourccod.source_cod)", "(Sourccod.source_code)"),
    ("(Kontline.kontstat ", "(Kontline.kontstatus "),
    ("(not Res_line.ankunft > tdate)", "(Res_line.ankunft <= tdate)"),
    ("(not Res_line.abreise <= fdate)", "(Res_line.abreise > fdate)"),
    ("(datum -1)", "(datum - timedelta(days=1)"),
    ("i = get_month(natstat.datum)", "i = get_month(natstat1.datum)"),
    (": 01/01/1998,", ": 1/1/1998,"),
    (": 01/01/1900,", ": 1/1/1900,"),
    (": 01/01/2099,", ": 1/1/2099,"),

    ("segm_list.segm_code = segmentcode", "segm_list.segm_code = segment.segmentcode"),
    ("(Waehrungsnr == res_line.betriebsnr)).first()", "(Waehrung.waehrungsnr == res_line.betriebsnr)).first()"),
    ("(Waehrungsnr == genstat.wahrungsnr)).first()", "(Waehrung.waehrungsnr == genstat.wahrungsnr)).first()"),
    ("tot_avail = tot_avail * (to_date - from_date + 1)", "tot_avail * (date_range(to_date - from_date) + timedelta(days=1))"),
    ("res_line.CANCELLED", "res_line.cancelled"),
    ("if get_month(datum) == get_month(to_date):", "if get_month(zinrstat.datum) == get_month(to_date):"),
    ("to_date = curr_date + 27", "to_date = curr_date + timedelta(days=27)"),
    ("pvlstopped:bool = false", "pvlstopped:bool = False"),
    ("last_fdate = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))", "last_fdate = date_mdy(1, 1, get_year(to_date) - 1)"),
    ("(Segmentcode != black_list) &  (not Segment.", "(Segment.segmentcode != black_list) &  (not Segment."),
    ("from_date = htparam.fdate + 1", "from_date = htparam.fdate + timedelta(days=1)"),
    ("(active_flag == 1) &  (Res_line.", "(Res_line.active_flag == 1) &  (Res_line."),
    (" comcategory.comcategory.categ_SELECTED)):", " comcategory.categ_selected):"),
    ("eg_request.reserve_int = location2 eg_request.zinr == zinr", "eg_request.reserve_int = location2 \neg_request.zinr == zinr"),
    ("if egReq or egmain:", "if egreq or egmain:"),
    ("if egReq.reqstatus", "if egreq.reqstatus"),
    ("(Qbuff.mobile != ", "(Qbuff.mobilenr != "),
    ("(Paramtext.txtnr == arr[i - 1)]).first()", "(Paramtext.txtnr == arr[i - 1])).first()"),
    ("frate =  to_decimal(reserve_dec)", "frate =  to_decimal(res_line.reserve_dec)"),
    ("arr = res_line.ankunf\n", "arr = res_line.ankunft\n"),
    ("if bill_list.deptNo == 0:", "if bill_list.deptno == 0:"),
    ("beg_date = date_mdy(get_month(fdate) , 1, get_year(fdate))", "beg_date = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate))"),
    ("(L_art1.artnr == ss_artnr[0)]).first()", "(L_art1.artnr == ss_artnr[0])).first()"),
    ("(L_art1.artnr == ss_artnr[1)]).first()", "(L_art1.artnr == ss_artnr[1])).first()"),
    ("(L_art1.artnr == ss_artnr[2)]).first()", "(L_art1.artnr == ss_artnr[2])).first()"),
    ("close_date = fdate", "close_date = htparam.fdate"),
    ("f_endkum = finteger", "f_endkum = htparam.finteger"),
    ("b_endkum = finteger", "b_endkum = htparam.finteger"),
    ("m_endkum = finteger", "m_endkum = htparam.finteger"),
    ("food = finteger", "food = htparam.finteger"),
    ("bev = finteger", "bev = htparam.finteger"),
    ("date2 = fdate", "date2 = htparam.fdate"),
    ("bill_date = fdate", "bill_date = htparam.fdate"),
    ("foreign_nr = waehrungsnr", "foreign_nr = waehrung.waehrungsnr"),
    ("transdate = fdate", "transdate = htparam.fdate"),
    ("to_date = fdate", "to_date = htparam.fdate"),
    ("L_artikel.min_best ", "L_artikel.min_bestand "),
    ("local_nr = waehrungsnr", "local_nr = waehrung.waehrungsnr"),
    ("enforce_rflag = flogical", "enforce_rflag = htparam.flogical"),
    ("date_mat = fdate", "date_mat = htparam.fdate"),
    ("date_fb = fdate", "date_fb = htparam.fdate"),
    ("qty = qty + anz_verbrau", "qty = qty + L_verbrauch.anz_verbrau"),
    ("val = val + wert_verbrau", "val = val + L_verbrauch.wert_verbrau"),
    ("str_list.d_unit = l_artikel.traubensort\n", "str_list.d_unit = l_artikel.traubensorte\n")
    ("p_224 = fdate", "p_224 = htparam.fdate"),
    ("if (last_acctdate + 1) <= last_acct_period:", "if (last_acctdate + timedelta(days=1) <= last_acct_period:"),
    ("str_list.d_unit = l_artikel.traubensort", "str_list.d_unit = l_artikel.traubensorte"),
    ("to_date = from_date + 32", "to_date = from_date + timedelta(days=32)"),
    ("for datum in range(from_date,to_date + 1) :", "for datum in date_range(from_date,to_date + timedelta(days=1)) :"),
    ("if htparam and htparam.bezeich.lower()", "if htparam and htparam.bezeichnung.lower()"),
    ("ldry = finteger", "ldry = htparam.finteger"),
    ("f_eknr = finteger", "f_eknr = htparam.finteger"),
    ("f1_eknr = finteger", "f1_eknr = htparam.finteger"),
    ("b_eknr = finteger", "b_eknr = htparam.finteger"),
    ("b1_eknr = finteger", "b1_eknr = htparam.finteger"),
    ("(Gl_acct.fibukonto == fchar)).first()", "(Gl_acct.fibukonto == htparam.fchar)).first()"),
    ("argt_list.bezeich = argt_bez", "argt_list.bezeich = arrangement.argt_bez")


    




















]





replace_in_files(folder_py, search_list)

print("--------------------------------------------------------------")
print("Replace String selesai.")
print("--------------------------------------------------------------\n")


# print((json_output))
os.chdir(curdir)
