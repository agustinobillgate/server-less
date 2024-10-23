from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, Res_history

def closemonth3bl(case_type:int, user_init:str, acct_date:date):
    fdefault:str = ""
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

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 597)).first()
        htparam.fdate = acct_date
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        fdefault = htparam.fdefault


        pass

        bparam = db_session.query(Bparam).filter(
                     (Bparam.paramnr == 558)).first()

        if bparam:
            bparam.fdefault = fdefault


            pass


    elif case_type == 2:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 597)).first()
        curr_date = htparam.fdate

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Closing Month - " + to_string(curr_date)
        res_history.action = "G/L"


        pass

    return generate_output()