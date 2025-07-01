#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def s_stockiss_l_lieferantbl(lief_nr:int):

    prepare_cache ([L_lieferant])

    a_firma = ""
    avail_l_lieferant = False
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_firma, avail_l_lieferant, l_lieferant
        nonlocal lief_nr

        return {"a_firma": a_firma, "avail_l_lieferant": avail_l_lieferant}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if l_lieferant:
        avail_l_lieferant = True
        a_firma = l_lieferant.firma

    return generate_output()