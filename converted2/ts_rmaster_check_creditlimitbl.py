#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest

def ts_rmaster_check_creditlimitbl(bill_gastnr:int):

    prepare_cache ([Htparam, Guest])

    klimit = to_decimal("0.0")
    htparam = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, htparam, guest
        nonlocal bill_gastnr

        return {"klimit": klimit}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

    guest = get_cache (Guest, {"gastnr": [(eq, bill_gastnr)]})

    if guest.kreditlimit != 0:
        klimit =  to_decimal(guest.kreditlimit)
    else:

        if htparam.fdecimal != 0:
            klimit =  to_decimal(htparam.fdecimal)
        else:
            klimit =  to_decimal(htparam.finteger)

    return generate_output()