#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def prepare_if_read_onlinetax_sbybl():

    prepare_cache ([Paramtext])

    hname = ""
    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hname, paramtext

        return {"hname": hname}


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    hname = paramtext.ptexte

    return generate_output()