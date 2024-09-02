from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_main, L_lieferant, Queasy

def prepare_gl_joulist_webbl():
    from_date = None
    close_date = None
    close_year = None
    to_date = None
    curr_yr = 0
    from_main = 0
    main_bez = ""
    gst_flag = False
    cflow_flag = False
    htparam = gl_main = l_lieferant = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, close_date, close_year, to_date, curr_yr, from_main, main_bez, gst_flag, cflow_flag, htparam, gl_main, l_lieferant, queasy


        return {"from_date": from_date, "close_date": close_date, "close_year": close_year, "to_date": to_date, "curr_yr": curr_yr, "from_main": from_main, "main_bez": main_bez, "gst_flag": gst_flag, "cflow_flag": cflow_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    from_date = htparam.fdate + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    close_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate
    close_year = date_mdy(get_month(close_year) , get_day(close_year) , get_year(close_year) + 1)
    to_date = get_current_date()
    curr_yr = get_year(htparam.fdate)

    gl_main = db_session.query(Gl_main).first()

    if gl_main:
        from_main = gl_main.nr
        main_bez = gl_main.bezeich

    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 177)).first()

    if queasy:
        cflow_flag = True

    return generate_output()