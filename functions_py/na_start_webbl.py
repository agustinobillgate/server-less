#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.na_startbl import na_startbl
from functions.prepare_mn_startbl import prepare_mn_startbl
from functions.na_start_update_flagbl import na_start_update_flagbl

def na_start_webbl(case_type:int, user_init:string, language_code:int, htparam_recid:int):
    mn_stopped = False
    stop_it = False
    msg_str = ""
    mess_str = ""
    crm_license = False
    banquet_license = False
    printer_nr = 0
    store_flag = False
    arrival_guest = False
    mnstart_flag:bool = False
    na_date1:date = None
    na_time1:int = 0
    na_name1:string = ""

    t_nightaudit = na_list = None

    t_nightaudit_data, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":string, "hogarest":int, "reihenfolge":int, "programm":string, "abschlussart":bool})
    na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "anz":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mn_stopped, stop_it, msg_str, mess_str, crm_license, banquet_license, printer_nr, store_flag, arrival_guest, mnstart_flag, na_date1, na_time1, na_name1
        nonlocal case_type, user_init, language_code, htparam_recid


        nonlocal t_nightaudit, na_list
        nonlocal t_nightaudit_data, na_list_data

        return {"mn_stopped": mn_stopped, "stop_it": stop_it, "msg_str": msg_str, "mess_str": mess_str, "crm_license": crm_license, "banquet_license": banquet_license, "printer_nr": printer_nr, "store_flag": store_flag, "arrival_guest": arrival_guest}


    if case_type == 1:
        mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date1, na_time1, na_name1 = get_output(na_startbl(1, user_init, htparam_recid))

        if mnstart_flag:
            mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data = get_output(prepare_mn_startbl(1, language_code))

            if mn_stopped:
                get_output(na_start_update_flagbl(htparam_recid))

    elif case_type == 2:
        get_output(na_start_update_flagbl(htparam_recid))

    return generate_output()