#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Htparam, Gl_jouhdr

def chg_stockdate_btn_exitbl(billdate:date, init_time:int, init_date:date):

    prepare_cache ([Htparam])

    err_code = 0
    flag_ok:bool = False
    a:int = 0
    b:date = None
    htparam = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, flag_ok, a, b, htparam, gl_jouhdr
        nonlocal billdate, init_time, init_date

        return {"err_code": err_code}

    flag_ok, a, b = get_output(check_timebl(3, 474, None, "htparam", init_time, init_date))

    if not flag_ok:
        err_code = 2

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    htparam.fdate = billdate
    htparam.lupdate = get_current_date()
    pass

    gl_jouhdr = get_cache (Gl_jouhdr, {"jtype": [(eq, 6)],"datum": [(ge, billdate)]})

    if gl_jouhdr:
        err_code = 1
    flag_ok, a, b = get_output(check_timebl(2, 474, None, "htparam", init_time, init_date))

    return generate_output()