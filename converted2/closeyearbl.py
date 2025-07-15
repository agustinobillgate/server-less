#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_acct

def closeyearbl():

    prepare_cache ([Htparam, Gl_acct])

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 993)]})
    end_month = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    curr_date = htparam.fdate
    curr_month = get_month(htparam.fdate)

    if curr_month != end_month:
        err_code = 1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})

    if (get_year(htparam.fdate) + 1) != get_year(curr_date):
        err_code = 2

        return generate_output()
    curr_yr = get_year(htparam.fdate) + 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 599)]})

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 612)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

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