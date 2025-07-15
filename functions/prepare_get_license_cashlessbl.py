#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def prepare_get_license_cashlessbl():

    prepare_cache ([Htparam])

    cashless_license = False
    cashless_minsaldo = to_decimal("0.0")
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_license, cashless_minsaldo, htparam

        return {"cashless_license": cashless_license, "cashless_minsaldo": cashless_minsaldo}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1022) & (Htparam.bezeichnung != ("not used").lower()) & (Htparam.flogical)).first()

    if htparam:
        cashless_license = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 586)]})

    if htparam:
        cashless_minsaldo =  to_decimal(htparam.fdecimal)

    return generate_output()