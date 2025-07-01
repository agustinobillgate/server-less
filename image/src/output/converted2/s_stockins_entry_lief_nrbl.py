#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def s_stockins_entry_lief_nrbl(lief_nr:int):

    prepare_cache ([L_lieferant])

    err_code = 0
    l_lieferant_firma = ""
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_lieferant_firma, l_lieferant
        nonlocal lief_nr

        return {"err_code": err_code, "l_lieferant_firma": l_lieferant_firma}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if not l_lieferant:
        err_code = 1

        return generate_output()

    elif l_lieferant:
        l_lieferant_firma = l_lieferant.firma
        err_code = 2

        return generate_output()

    return generate_output()