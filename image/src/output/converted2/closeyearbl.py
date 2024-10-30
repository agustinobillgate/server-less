from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_acct

def closeyearbl():
    curr_date = None
    curr_yr = 0
    err_code = 0
    curr_month:int = 0
    end_month:int = 0
    acct_correct:bool = True
    htparam = gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, curr_yr, err_code, curr_month, end_month, acct_correct, htparam, gl_acct

        return {"curr_date": curr_date, "curr_yr": curr_yr, "err_code": err_code}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 993)).first()
    end_month = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 558)).first()
    curr_date = htparam.fdate
    curr_month = get_month(htparam.fdate)

    if curr_month != end_month:
        err_code = 1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()

    if (get_year(htparam.fdate) + 1) != get_year(curr_date):
        err_code = 2

        return generate_output()
    curr_yr = get_year(htparam.fdate) + 1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 599)).first()

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 612)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == htparam.fchar)).first()

        if not gl_acct:
            acct_correct = False
        else:

            if gl_acct.fibukonto == "":
                acct_correct = False

            if gl_acct.acc_type != 4:
                acct_correct = False

        if not acct_correct:
            err_code = 3

            return generate_output()
    err_code = 4

    return generate_output()