#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Brief

def sel_printminvbl(ind:int, briefnr:int):

    prepare_cache ([Htparam])

    htparam = brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, brief
        nonlocal ind, briefnr

        return {"briefnr": briefnr}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 688)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            briefnr = htparam.finteger

    if ind == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 495)]})

        if htparam.finteger > 0:

            brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

            if brief:
                briefnr = htparam.finteger

    return generate_output()