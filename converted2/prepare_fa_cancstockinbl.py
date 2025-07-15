#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_fa_cancstockinbl():

    prepare_cache ([Htparam])

    price_decimal = 0
    from_date = None
    to_date = None
    beg_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, from_date, to_date, beg_date, htparam

        return {"price_decimal": price_decimal, "from_date": from_date, "to_date": to_date, "beg_date": beg_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    from_date = htparam.fdate
    to_date = from_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    beg_date = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate))

    return generate_output()