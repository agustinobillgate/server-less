#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.load_ratecode2bl import load_ratecode2bl
from models import Ratecode

p_list_data, P_list = create_model_like(Ratecode, {"s_recid":int, "rmcat_str":string, "wday_str":string, "adult_str":string, "child_str":string})

def ratecode_adm_check_plist_webbl(pvilanguage:int, curr_select:string, prcode:string, market:string, prlist_zikatnr:int, prlist_argtnr:int, market_nr:int, tb3_srecid:int, p_list_data:[P_list]):
    msg_str = ""
    child_error = False
    error_msg = ""
    lvcarea:string = "ratecode-adm-check-plistbl"
    curr_i:int = 0
    mesval:string = ""
    error_flag:bool = False
    err_result:string = ""
    ratecode = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, child_error, error_msg, lvcarea, curr_i, mesval, error_flag, err_result, ratecode
        nonlocal pvilanguage, curr_select, prcode, market, prlist_zikatnr, prlist_argtnr, market_nr, tb3_srecid


        nonlocal p_list

        return {"msg_str": msg_str, "child_error": child_error, "error_msg": error_msg}

    def proc_checka():

        nonlocal msg_str, child_error, error_msg, lvcarea, curr_i, mesval, error_flag, err_result, ratecode
        nonlocal pvilanguage, curr_select, prcode, market, prlist_zikatnr, prlist_argtnr, market_nr, tb3_srecid


        nonlocal p_list


        for curr_i in range(1,num_entries(p_list.wday_str, ",")  + 1) :
            mesval = trim(entry(curr_i - 1, p_list.wday_str, ","))

            if mesval != "":

                if asc(mesval) < 48 or asc(mesval) > 55:
                    msg_str = translateExtended ("Wrong weekday format.", lvcarea, "")

                    return
        for curr_i in range(1,num_entries(p_list.adult_str, ",")  + 1) :
            mesval = trim(entry(curr_i - 1, p_list.adult_str, ","))

            if mesval != "":

                if matches(mesval,r"*-*"):
                    msg_str = translateExtended ("Wrong adult format.", lvcarea, "")

                    return
        for curr_i in range(1,num_entries(p_list.child_str, ",")  + 1) :
            mesval = trim(entry(curr_i - 1, p_list.child_str, ","))

            if mesval != "":

                if asc(mesval) < 48 or asc(mesval) > 57:
                    msg_str = translateExtended ("Wrong child format.", lvcarea, "")

                    return


    def proc_checkb():

        nonlocal msg_str, child_error, error_msg, lvcarea, curr_i, mesval, error_flag, err_result, ratecode
        nonlocal pvilanguage, curr_select, prcode, market, prlist_zikatnr, prlist_argtnr, market_nr, tb3_srecid


        nonlocal p_list

        if p_list.erwachs == 0 and p_list.kind1 == 0 and p_list.kind2 == 0:
            msg_str = translateExtended ("adult and/or Child must be defined", lvcarea, "")

            return

        if p_list.kind1 != 0 and p_list.ch1preis != 0:
            msg_str = translateExtended ("Choose ChildNo or Child Price only", lvcarea, "")

            return

        if p_list.kind2 != 0 and p_list.ch2preis != 0:
            msg_str = translateExtended ("Choose ChildNo or Child Price only", lvcarea, "")

            return
        error_flag, child_error, error_msg = check_overlapping(curr_select, p_list.startperiode, p_list.endperiode, p_list.wday, p_list.erwachs, p_list.kind1, p_list.kind2, prcode, market, prlist_zikatnr, prlist_argtnr, p_list.zipreis)

        if error_flag:

            if child_error:
                err_result = translateExtended (error_msg, lvcarea, "")
                error_msg = translateExtended ("Overlapping period found with PARENT Code:", lvcarea, "") + chr_unicode(10) + translateExtended (err_result, lvcarea, "")
            msg_str = translateExtended ("Wrong Start/End- Periode.", lvcarea, "")

            return


    def check_overlapping(curr_mode:string, f_date:date, t_date:date, w_day:int, adult:int, child1:int, child2:int, prcode:string, market:string, zikatnr:int, argtnr:int, zipreis:Decimal):

        nonlocal msg_str, child_error, error_msg, lvcarea, curr_i, mesval, error_flag, err_result, ratecode
        nonlocal pvilanguage, curr_select, prlist_zikatnr, prlist_argtnr, market_nr, tb3_srecid


        nonlocal p_list

        error_flag = False
        child_error = False
        error_msg = ""
        str:string = ""

        def generate_inner_output():
            return (error_flag, child_error, error_msg)

        str = prcode + ";" + to_string(zipreis)

        if curr_mode.lower()  == ("insert").lower()  or curr_mode.lower()  == ("copy-rate").lower() :
            error_flag, child_error, error_msg = get_output(load_ratecode2bl(4, market_nr, prcode, argtnr, zikatnr, adult, child1, child2, w_day, f_date, t_date, None))

        elif curr_mode.lower()  == ("chg-rate").lower() :
            error_flag, child_error, error_msg = get_output(load_ratecode2bl(4, market_nr, str, argtnr, zikatnr, adult, child1, child2, w_day, f_date, t_date, tb3_srecid))

        return generate_inner_output()


    p_list = query(p_list_data, first=True)

    if p_list.startperiode == None or p_list.endperiode == None or p_list.startperiode > p_list.endperiode:
        msg_str = translateExtended ("Start- and/or End-periode incorrect", lvcarea, "")

        return generate_output()

    if p_list.zipreis == 0:
        msg_str = translateExtended ("Room Rate not defined", lvcarea, "")

        return generate_output()

    if curr_select.lower()  == ("insert").lower()  or curr_select.lower()  == ("update").lower() :
        proc_checka()

    elif curr_select.lower()  == ("chg-rate").lower() :
        proc_checkb()

    return generate_output()