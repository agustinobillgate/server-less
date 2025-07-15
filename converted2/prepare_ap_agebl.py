#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_ap_agebl():

    prepare_cache ([Htparam])

    day1 = 0
    day2 = 0
    day3 = 0
    to_date = None
    price_decimal = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal day1, day2, day3, to_date, price_decimal, htparam

        return {"day1": day1, "day2": day2, "day3": day3, "to_date": to_date, "price_decimal": price_decimal}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 330)]})

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 331)]})

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 332)]})

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2
    to_date = get_current_date()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    return generate_output()