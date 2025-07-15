#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def htpdec(htparamnum:int):

    prepare_cache ([Htparam])

    htpdecimal = to_decimal("0.0")
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpdecimal, htparam
        nonlocal htparamnum

        return {"htpdecimal": htpdecimal}

    htpdecimal =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

    if htparam:
        htpdecimal =  to_decimal(htparam.fdecimal)

    return generate_output()

    return generate_output()