#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def htpint(htparamnum:int):

    prepare_cache ([Htparam])

    htpint = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpint, htparam
        nonlocal htparamnum

        return {"htpint": htpint}


    htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

    if htparam:
        htpint = htparam.finteger

    return generate_output()

    return generate_output()