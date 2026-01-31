#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def get_check_in_datebl():

    prepare_cache ([Htparam])

    check_in_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal check_in_date, htparam

        return {"check_in_date": check_in_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    check_in_date = htparam.fdate

    return generate_output()