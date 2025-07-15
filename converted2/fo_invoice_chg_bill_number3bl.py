#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam

def fo_invoice_chg_bill_number3bl(bill_gastnr:int):

    prepare_cache ([Guest, Htparam])

    kreditlimit = to_decimal("0.0")
    guest = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kreditlimit, guest, htparam
        nonlocal bill_gastnr

        return {"kreditlimit": kreditlimit}


    guest = get_cache (Guest, {"gastnr": [(eq, bill_gastnr)]})

    if guest.kreditlimit != 0:
        kreditlimit =  to_decimal(guest.kreditlimit)
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        if htparam.fdecimal != 0:
            kreditlimit =  to_decimal(htparam.fdecimal)
        else:
            kreditlimit =  to_decimal(htparam.finteger)

    return generate_output()