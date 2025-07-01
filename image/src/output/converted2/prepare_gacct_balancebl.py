#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_gacct_balancebl():

    prepare_cache ([Htparam])

    heute = None
    billdate = None
    long_digit = False
    price_decimal = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal heute, billdate, long_digit, price_decimal, htparam

        return {"heute": heute, "billdate": billdate, "long_digit": long_digit, "price_decimal": price_decimal}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    heute = htparam.fdate
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    return generate_output()