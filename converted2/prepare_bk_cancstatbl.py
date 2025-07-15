#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def prepare_bk_cancstatbl():

    prepare_cache ([Htparam])

    p_417 = ""
    p_547 = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_417, p_547, htparam

        return {"p_417": p_417, "p_547": p_547}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})
    p_417 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 547)]})
    p_547 = htparam.finteger

    return generate_output()