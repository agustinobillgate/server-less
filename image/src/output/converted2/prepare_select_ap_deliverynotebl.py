#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Htparam

def prepare_select_ap_deliverynotebl(lief_nr:int):

    prepare_cache ([L_lieferant, Htparam])

    firma = ""
    fdate = None
    l_lieferant = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal firma, fdate, l_lieferant, htparam
        nonlocal lief_nr

        return {"firma": firma, "fdate": fdate}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    firma = l_lieferant.firma

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    fdate = htparam.fdate

    return generate_output()