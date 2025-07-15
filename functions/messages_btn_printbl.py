#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Brief

def messages_btn_printbl():

    prepare_cache ([Htparam, Brief])

    brief_briefnr = 0
    avail_brief = False
    htparam = brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal brief_briefnr, avail_brief, htparam, brief

        return {"brief_briefnr": brief_briefnr, "avail_brief": avail_brief}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 434)]})

    brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

    if brief:
        avail_brief = True
        brief_briefnr = brief.briefnr

    return generate_output()