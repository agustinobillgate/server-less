#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.prepare_ts_biltransferbl import prepare_ts_biltransferbl
from functions.ts_restinv_btn_transferbl import ts_restinv_btn_transferbl
from functions.ts_biltransfer_check_vatbl import ts_biltransfer_check_vatbl
from functions.read_hotelnamebl import read_hotelnamebl
from functions.prepare_ts_rzinrbl import prepare_ts_rzinrbl
from models import H_bill

def ts_prepare_roomtransfer_combobl(language_code:int, h_recid:int, balance:Decimal, pf_file1:string, pf_file2:string):
    mess_info = ""
    dept_mbar = 0
    dept_ldry = 0
    bilrecid = 0
    htl_name = ""
    vsuccess = False
    roomtf_list_data = []
    asremoteflag:bool = True
    multi_vat:bool = False
    splitted:bool = False
    dept:int = 0
    its_ok:bool = False
    fl_code:int = 0
    connect_param:string = ""
    connect_paramssl:string = ""
    lreturn:bool = False
    msg_str:string = ""
    msg_str2:string = ""
    mc_flag:bool = False
    mc_pos1:int = 0
    mc_pos2:int = 0
    flag:bool = False
    h_bill = None

    t_h_bill = q1_list = roomtf_list = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    q1_list_data, Q1_list = create_model("Q1_list", {"resnr":int, "zinr":string, "code":string, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":string, "billnr":int, "g_name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "bill_name":string, "ankunft":date, "abreise":date, "nation1":string, "parent_nr":int, "reslinnr":int, "resname":string, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})
    roomtf_list_data, Roomtf_list = create_model("Roomtf_list", {"resnr":int, "zinr":string, "code":string, "resstatus":int, "erwachs":int, "kind1":int, "gratis":int, "bemerk":string, "billnr":int, "g_name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "bill_name":string, "ankunft":date, "abreise":date, "nation1":string, "parent_nr":int, "reslinnr":int, "resname":string, "name_bg_col":int, "name_fg_col":int, "bill_bg_col":int, "bill_fg_col":int}, {"name_bg_col": 15, "bill_bg_col": 15})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_info, dept_mbar, dept_ldry, bilrecid, htl_name, vsuccess, roomtf_list_data, asremoteflag, multi_vat, splitted, dept, its_ok, fl_code, connect_param, connect_paramssl, lreturn, msg_str, msg_str2, mc_flag, mc_pos1, mc_pos2, flag, h_bill
        nonlocal language_code, h_recid, balance, pf_file1, pf_file2


        nonlocal t_h_bill, q1_list, roomtf_list
        nonlocal t_h_bill_data, q1_list_data, roomtf_list_data

        return {"mess_info": mess_info, "dept_mbar": dept_mbar, "dept_ldry": dept_ldry, "bilrecid": bilrecid, "htl_name": htl_name, "vsuccess": vsuccess, "roomtf-list": roomtf_list_data}


    multi_vat, dept, splitted, t_h_bill_data = get_output(prepare_ts_biltransferbl(h_recid))

    t_h_bill = query(t_h_bill_data, first=True)

    if balance != 0:
        flag = get_output(ts_restinv_btn_transferbl(t_h_bill.rechnr, t_h_bill.departement))

        if flag:
            mess_info = "Bill has been splitted, use Split Bill's Transfer Payment"

            return generate_output()
    fl_code, its_ok = get_output(ts_biltransfer_check_vatbl(h_recid, multi_vat, balance, False, splitted))

    if fl_code == 1:
        mess_info = "Transfer not allowed: Other Payment found."

        return generate_output()
    connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session-free"
    connect_paramssl = connect_param + " -ssl -nohostverify"
    lreturn = set_combo_session(connect_paramssl, None, None, None)

    if not lreturn:
        lreturn = set_combo_session(connect_param, None, None, None)

    if lreturn:
        local_storage.combo_flag = True
        htl_name = get_output(read_hotelnamebl("A120"))
        local_storage.combo_flag = False


    if not hServer:CONNECTED():
        mess_info = "Failed to connect to combo property's DB."


        return generate_output()
    local_storage.combo_flag = True
    dept_mbar, dept_ldry, bilrecid, mc_pos1, mc_pos2, mc_flag, fl_code, msg_str, msg_str2, q1_list_data = get_output(prepare_ts_rzinrbl(language_code, dept, "", 0, 0, balance))
    local_storage.combo_flag = False


    if fl_code == 1:
        mess_info = substring(msg_str, 1)
        bilrecid = 0

        return generate_output()

    if msg_str2 != "":
        mess_info = substring(msg_str2, 3)

    for q1_list in query(q1_list_data, sort_by=[("zinr",False),("parent_nr",False),("reslinnr",False),("resname",False)]):
        q1_list.g_name = q1_list.g_name + ", " + q1_list.vorname1 + " " + q1_list.anrede1 + q1_list.anredefirma
        roomtf_list = Roomtf_list()
        roomtf_list_data.append(roomtf_list)

        buffer_copy(q1_list, roomtf_list)

    vsuccess = True

    return generate_output()