#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.zugriff_testui import zugriff_testui
from functions.na_check1bl import na_check1bl
from functions.na_startbl import na_startbl
from functions.mn_startui import mn_startui
from functions.na_start_update_flagbl import na_start_update_flagbl
from functions.delete_nitestorbl import delete_nitestorbl
from functions.nt_tauziarptui import nt_tauziarptui
from functions.nt_exportgcfui import nt_exportgcfui
from functions.nt_salesboard import nt_salesboard
from functions.delete_nitehistbl import delete_nitehistbl

def na_start_webbl(user_init:string, def_natcode:string, session_parameter:string):
    msg_str = ""
    w_flag = False
    names_ok = False
    na_can_run = False
    mn_stopped:bool = False
    msg_str2:string = ""
    msg_str3:string = ""
    msg_ans:bool = False
    htparam_recid:int = 0
    mnstart_flag:bool = False
    na_date1:date = None
    na_time1:int = 0
    na_name1:string = ""
    zugriff:bool = False
    i:int = 0
    its_ok:bool = False
    store_flag:bool = False
    printer_nr:int = 0
    na_date:date = None
    na_time:int = 0
    na_name:string = ""
    success_flag:bool = False

    t_nightaudit = na_list = reslist = None

    t_nightaudit_list, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":string, "hogarest":int, "reihenfolge":int, "programm":string, "abschlussart":bool})
    na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":string})
    reslist_list, Reslist = create_model("Reslist", {"resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, w_flag, names_ok, na_can_run, mn_stopped, msg_str2, msg_str3, msg_ans, htparam_recid, mnstart_flag, na_date1, na_time1, na_name1, zugriff, i, its_ok, store_flag, printer_nr, na_date, na_time, na_name, success_flag
        nonlocal user_init, def_natcode, session_parameter


        nonlocal t_nightaudit, na_list, reslist
        nonlocal t_nightaudit_list, na_list_list, reslist_list

        return {"msg_str": msg_str, "w_flag": w_flag, "names_ok": names_ok, "na_can_run": na_can_run}

    def na_prog():

        nonlocal msg_str, w_flag, names_ok, na_can_run, msg_str2, msg_str3, msg_ans, htparam_recid, mnstart_flag, na_date1, na_time1, na_name1, zugriff, i, its_ok, store_flag, printer_nr, na_date, na_time, na_name, success_flag
        nonlocal user_init, def_natcode, session_parameter


        nonlocal t_nightaudit, na_list, reslist
        nonlocal t_nightaudit_list, na_list_list, reslist_list

        night_type:int = 0
        mn_stopped:bool = False
        a:int = 0
        na_list_list.clear()
        i = 0
        msg_str = "Night Audit is running!!"

        for t_nightaudit in query(t_nightaudit_list, sort_by=[("(",False),("reihenfolge",False))]:
            i = i + 1
            na_list = Na_list()
            na_list_list.append(na_list)

            na_list.reihenfolge = i
            na_list.bezeich = t_nightaudit.bezeichnung
            na_list.flag = t_nightaudit.hogarest

            if store_flag:

                if t_nightaudit.hogarest == 0:
                    night_type = 0
                else:
                    night_type = 2
                success_flag = get_output(delete_nitestorbl(1, night_type, t_nightaudit.reihenfolge))

            if matches(t_nightaudit.programm,r"nt-tauziarpt.r"):
                get_output(nt_tauziarptui(session_parameter))

            elif matches(t_nightaudit.programm,r"nt-exportgcf.r"):
                get_output(nt_exportgcfui(session_parameter))

            elif matches(t_nightaudit.programm,r"nt-salesboard.r"):
                get_output(nt_salesboard(session_parameter))
            else:

                if matches(t_nightaudit.programm,r"*bl.p*"):
                    run_program(t_nightauditrogramm.lower())
                else:

                    if to_int(t_nightaudit.abschlussart) == 1:
                        run_program(t_nightauditrogramm.lower())
                    else:
                        a = R_INDEX (t_nightaudit.programm, ".p")
                        run_program(substring(t_nightauditrogramm.lower() , 0, a - 1) + "bl")

            if store_flag:
                success_flag = get_output(delete_nitehistbl(1, None, t_nightaudit.reihenfolge))

    zugriff = get_output(zugriff_testui(user_init, 21, 2))

    if zugriff:
        msg_str, msg_str2, msg_str3, w_flag, names_ok, its_ok, htparam_recid = get_output(na_check1bl(0, def_natcode))

        if msg_str != "":
            na_can_run = False

            return generate_output()

        if w_flag :
            na_can_run = False

            return generate_output()

        if not names_ok:
            na_can_run = False

            return generate_output()
        na_can_run = True

        if its_ok:
            mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date1, na_time1, na_name1 = get_output(na_startbl(1, user_init, htparam_recid))

            if mnstart_flag:
                mn_stopped = get_output(mn_startui("mnstartp"))

                if mn_stopped:
                    get_output(na_start_update_flagbl(htparam_recid))

                    return generate_output()
                else:
                    mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date1, na_time1, na_name1 = get_output(na_startbl(2, user_init, htparam_recid))
            na_prog()
            mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date, na_time, na_name = get_output(na_startbl(3, user_init, htparam_recid))
            msg_str = "Night Audit finished."

    return generate_output()