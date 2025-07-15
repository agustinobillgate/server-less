#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def htpchar(htparamnum:int):

    prepare_cache ([Htparam])

    htpchar = ""
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpchar, htparam
        nonlocal htparamnum

        return {"htpchar": htpchar}


    htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

    if htparam:
        htpchar = htparam.fchar

    return generate_output()

    return generate_output()