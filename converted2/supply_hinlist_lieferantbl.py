#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def supply_hinlist_lieferantbl(lief_nr:int):

    prepare_cache ([L_lieferant])

    from_supp = ""
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_supp, l_lieferant
        nonlocal lief_nr

        return {"from_supp": from_supp}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    from_supp = l_lieferant.firma

    return generate_output()