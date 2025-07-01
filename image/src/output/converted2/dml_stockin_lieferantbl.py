#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def dml_stockin_lieferantbl(lief_nr:int):

    prepare_cache ([L_lieferant])

    err_flag = 0
    lief_bezeich = ""
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, lief_bezeich, l_lieferant
        nonlocal lief_nr

        return {"err_flag": err_flag, "lief_bezeich": lief_bezeich}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if not l_lieferant:
        err_flag = 1

        return generate_output()

    elif l_lieferant:
        err_flag = 2
        lief_bezeich = l_lieferant.firma

    return generate_output()