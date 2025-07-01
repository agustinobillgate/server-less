#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_fa_depnbl():

    prepare_cache ([Htparam])

    last_acctdate = None
    datum = None
    acct_date = None
    close_year = None
    err_no = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_acctdate, datum, acct_date, close_year, err_no, htparam

        return {"last_acctdate": last_acctdate, "datum": datum, "acct_date": acct_date, "close_year": close_year, "err_no": err_no}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
    last_acctdate = htparam.fdate
    datum = last_acctdate + timedelta(days=35)
    datum = date_mdy(get_month(datum) , 1, get_year(datum)) - timedelta(days=1)

    if datum > get_current_date():
        err_no = 1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    return generate_output()