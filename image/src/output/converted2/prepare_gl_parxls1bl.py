#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_gl_parxls1bl():

    prepare_cache ([Htparam])

    price_decimal = 0
    close_date = None
    curr_close_year = 0
    p_418 = ""
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, close_date, curr_close_year, p_418, htparam

        return {"price_decimal": price_decimal, "close_date": close_date, "curr_close_year": curr_close_year, "p_418": p_418}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    close_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    curr_close_year = get_year(htparam.fdate) + 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 418)]})
    p_418 = htparam.fchar

    return generate_output()