#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Res_history

def closemonth3bl(case_type:int, user_init:string, acct_date:date):

    prepare_cache ([Htparam, Bediener, Res_history])

    fdefault:string = ""
    curr_date:date = None
    htparam = bediener = res_history = None

    bparam = None

    Bparam = create_buffer("Bparam",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdefault, curr_date, htparam, bediener, res_history
        nonlocal case_type, user_init, acct_date
        nonlocal bparam


        nonlocal bparam

        return {}


    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})

        if htparam:
            pass
            htparam.fdate = acct_date
            htparam.lupdate = get_current_date()
            htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
            fdefault = htparam.fdefault


            pass
            pass

        bparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})

        if bparam:
            pass
            bparam.fdefault = fdefault


            pass
            pass

    elif case_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        curr_date = htparam.fdate

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Closing Month - " + to_string(curr_date)
        res_history.action = "G/L"


        pass
        pass

    return generate_output()