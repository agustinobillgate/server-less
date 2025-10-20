#using conversion tools version: 1.0.0.
#------------------------------------------
# Rd, 20/10/2025

# vhpNA/reprintNaPrepare -> prepare_reprint_nabl
# vhpFOC/naStartPrepare -> prepare_na_startbl
# vhpFOC/naCheck1 -> na_check1bl
# vhpFOC/naStart -> na_start_webbl
# vhpFOC/naStart2 -> na_start_web2bl
# vhpFOC/naStartGetInfo -> na_start_get_info_webbl
#------------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Htparam, Nightaudit

def na_startbl(case_type:int, user_init:string, htparam_recid:int):

    prepare_cache ([Bediener, Htparam, Nightaudit])

    mnstart_flag = False
    store_flag = False
    printer_nr = 0
    t_nightaudit_data = []
    na_date = None
    na_time = 0
    na_name = ""
    ci_date:date = None
    bediener = htparam = nightaudit = None

    t_nightaudit = None

    t_nightaudit_data, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":string, "hogarest":int, "reihenfolge":int, "programm":string, "abschlussart":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit
        nonlocal case_type, user_init, htparam_recid


        nonlocal t_nightaudit
        nonlocal t_nightaudit_data

        return {"mnstart_flag": mnstart_flag, "store_flag": store_flag, "printer_nr": printer_nr, "t-nightaudit": t_nightaudit_data, "na_date": na_date, "na_time": na_time, "na_name": na_name}

    def na_prog():

        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit
        nonlocal case_type, user_init, htparam_recid


        nonlocal t_nightaudit
        nonlocal t_nightaudit_data

        night_type:int = 0
        mn_stopped:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        for nightaudit in db_session.query(Nightaudit).filter(
                 (Nightaudit.selektion)).order_by((1 - Nightaudit.hogarest), Nightaudit.reihenfolge).all():
            t_nightaudit = T_nightaudit()
            t_nightaudit_data.append(t_nightaudit)

            t_nightaudit.bezeichnung = nightaudit.bezeichnung
            t_nightaudit.hogarest = nightaudit.hogarest
            t_nightaudit.reihenfolge = nightaudit.reihenfolge
            t_nightaudit.programm = nightaudit.programm
            t_nightaudit.abschlussart = nightaudit.abschlussart


    def check_mn_start():

        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit
        nonlocal case_type, user_init, htparam_recid


        nonlocal t_nightaudit
        nonlocal t_nightaudit_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 105)]})

        if htparam.fdate < get_current_date():
            mnstart_flag = True


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 230)]})

    if htparam.feldtyp == 4 and htparam.flogical:
        store_flag = True

    if case_type == 1:

        htparam = get_cache (Htparam, {"_recid": [(eq, htparam_recid)]})
        htparam.flogical = True
        check_mn_start()

        if mnstart_flag:

            return generate_output()
        na_prog()

    if case_type == 2:
        na_prog()

    if case_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
        htparam.fchar = bediener.username
        htparam.fdate = get_current_date()
        htparam.finteger = get_current_time_in_seconds()
        htparam.flogical = False
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 102)]})
        htparam.fdate = get_current_date()
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 103)]})
        htparam.finteger = get_current_time_in_seconds()
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 99)]})
        printer_nr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 102)]})
        na_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 103)]})
        na_time = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
        na_name = htparam.fchar

    return generate_output()