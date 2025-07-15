#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_bqt_cutoffbl():

    prepare_cache ([Htparam])

    ci_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, htparam

        return {"ci_date": ci_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    return generate_output()