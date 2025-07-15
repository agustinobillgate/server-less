#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_cancel_rsv_listbl():

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, htparam

        return {"from_date": from_date, "to_date": to_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = htparam.fdate + timedelta(days=1)

    return generate_output()