#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_gc_cashsummary_webbl():

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    curr_local = ""
    curr_foreign = ""
    double_curr = False
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, curr_local, curr_foreign, double_curr, htparam

        return {"from_date": from_date, "to_date": to_date, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_curr": double_curr}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        from_date = htparam.fdate
        to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    if htparam:
        curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam:
        curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        double_curr = htparam.flogical

    return generate_output()