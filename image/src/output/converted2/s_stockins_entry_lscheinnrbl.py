#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, L_lager

def s_stockins_entry_lscheinnrbl(lief_nr:int, curr_lager:int):

    prepare_cache ([L_lieferant, L_lager])

    err_code = 0
    err_code1 = 0
    lager_bezeich = ""
    a_firma = ""
    l_lieferant = l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, err_code1, lager_bezeich, a_firma, l_lieferant, l_lager
        nonlocal lief_nr, curr_lager

        return {"err_code": err_code, "err_code1": err_code1, "lager_bezeich": lager_bezeich, "a_firma": a_firma}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if not l_lieferant:
        err_code = 1

        return generate_output()

    elif l_lieferant:
        err_code = 2
        a_firma = l_lieferant.firma

    l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

    if not l_lager:
        err_code1 = 1

        return generate_output()
    else:
        err_code1 = 2
        lager_bezeich = l_lager.bezeich

    return generate_output()