#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_bqt_reportrevbl():

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    ci_date:date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, ci_date, htparam

        return {"from_date": from_date, "to_date": to_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if from_date == None:
        from_date = htparam.fdate
        to_date = htparam.fdate + timedelta(days=1)

    return generate_output()