#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_fb_reconsilebl():

    prepare_cache ([Htparam])

    food = 0
    bev = 0
    to_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, to_date, htparam

        return {"food": food, "bev": bev, "to_date": to_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    food = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bev = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    to_date = htparam.fdate

    return generate_output()