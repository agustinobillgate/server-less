#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def htplogic(htparamnum:int):

    prepare_cache ([Htparam])

    htplogic = None
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htplogic, htparam
        nonlocal htparamnum

        return {"htplogic": htplogic}

    htplogic = None

    htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

    if htparam:
        htplogic = htparam.flogical

    return generate_output()

    return generate_output()