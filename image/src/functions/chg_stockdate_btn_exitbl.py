from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Htparam, Gl_jouhdr

def chg_stockdate_btn_exitbl(billdate:date, init_time:int, init_date:date):
    err_code = 0
    flag_ok:bool = False
    a:int = 0
    b:date = None
    htparam = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, flag_ok, a, b, htparam, gl_jouhdr


        return {"err_code": err_code}

    flag_ok, a, b = get_output(check_timebl(3, 474, None, "htparam", init_time, init_date))

    if not flag_ok:
        err_code = 2

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    htparam.fdate = billdate
    htparam.lupdate = get_current_date()

    htparam = db_session.query(Htparam).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jtype == 6) &  (Gl_jouhdr.datum >= billdate)).first()

    if gl_jouhdr:
        err_code = 1
    flag_ok, a, b = get_output(check_timebl(2, 474, None, "htparam", init_time, init_date))

    return generate_output()