#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def htpdate(htparamnum:int):

    prepare_cache ([Htparam])

    htpdate = get_current_date()
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpdate, htparam
        nonlocal htparamnum

        return {"htpdate": htpdate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

    if htparam:
        htpdate = htparam.fdate

    return generate_output()

    return generate_output()