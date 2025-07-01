#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_longshort_staybl():

    prepare_cache ([Htparam])

    long_stay = 0
    curr_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_stay, curr_date, htparam

        return {"long_stay": long_stay, "curr_date": curr_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 139)]})
    long_stay = htparam.finteger

    if long_stay == 0:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate

    return generate_output()