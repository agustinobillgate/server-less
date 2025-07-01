#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam

def prepare_ap_debtpaybl():

    prepare_cache ([Htparam])

    bill_date = None
    rundung = 0
    p_1118 = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, rundung, p_1118, htparam

        return {"bill_date": bill_date, "rundung": rundung, "p_1118": p_1118}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    rundung = htparam.finteger
    rundung = 2
    p_1118 = get_output(htpdate(1118))

    return generate_output()