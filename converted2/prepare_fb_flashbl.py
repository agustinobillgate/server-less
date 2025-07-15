#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_fb_flashbl():

    prepare_cache ([Htparam])

    food = 0
    bev = 0
    date2 = None
    date1 = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, date2, date1, htparam

        return {"food": food, "bev": bev, "date2": date2, "date1": date1}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    food = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bev = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    date2 = htparam.fdate
    date1 = date_mdy(get_month(date2) , 1, get_year(date2))

    return generate_output()