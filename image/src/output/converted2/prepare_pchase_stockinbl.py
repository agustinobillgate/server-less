#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_pchase_stockinbl():

    prepare_cache ([Htparam])

    order_date = None
    billdate = None
    enforce_rflag = False
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_date, billdate, enforce_rflag, htparam

        return {"order_date": order_date, "billdate": billdate, "enforce_rflag": enforce_rflag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    order_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    return generate_output()