#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_main, L_lieferant, Queasy

def prepare_gl_joulistbl():

    prepare_cache ([Htparam, Gl_main])

    from_date = None
    close_date = None
    close_year = None
    to_date = None
    curr_yr = 0
    from_main = 0
    main_bez = ""
    gst_flag = False
    cflow_flag = False
    tmp_date:date = None
    htparam = gl_main = l_lieferant = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, close_date, close_year, to_date, curr_yr, from_main, main_bez, gst_flag, cflow_flag, tmp_date, htparam, gl_main, l_lieferant, queasy

        return {"from_date": from_date, "close_date": close_date, "close_year": close_year, "to_date": to_date, "curr_yr": curr_yr, "from_main": from_main, "main_bez": main_bez, "gst_flag": gst_flag, "cflow_flag": cflow_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    from_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    close_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate
    tmp_date = date_mdy(get_month(close_year) , get_day(close_year) , get_year(close_year))
    close_year = tmp_date + timedelta(days=1)
    to_date = get_current_date()
    curr_yr = get_year(htparam.fdate) + 1

    gl_main = db_session.query(Gl_main).first()

    if gl_main:
        from_main = gl_main.code
        main_bez = gl_main.bezeich

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    queasy = get_cache (Queasy, {"key": [(eq, 177)]})

    if queasy:
        cflow_flag = True

    return generate_output()