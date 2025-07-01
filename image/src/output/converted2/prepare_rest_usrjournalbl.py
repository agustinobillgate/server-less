#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_rest_usrjournalbl():

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    long_digit = False
    price_decimal = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, long_digit, price_decimal, htparam

        return {"from_date": from_date, "to_date": to_date, "long_digit": long_digit, "price_decimal": price_decimal}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    return generate_output()