#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bediener

def prepare_sales_performbl(user_init:string):

    prepare_cache ([Htparam])

    price_decimal = 0
    from_date = ""
    to_date = ""
    usr_init = ""
    htparam = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, from_date, to_date, usr_init, htparam, bediener
        nonlocal user_init

        return {"price_decimal": price_decimal, "from_date": from_date, "to_date": to_date, "usr_init": usr_init}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = to_string(get_month(htparam.fdate) , "99") + to_string(get_year(htparam.fdate) , "9999")
    to_date = from_date
    usr_init = user_init

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    return generate_output()