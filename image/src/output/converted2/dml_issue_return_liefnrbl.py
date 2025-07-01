#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def dml_issue_return_liefnrbl(lief_nr:int):

    prepare_cache ([L_lieferant])

    lief_bezeich = ""
    avail_lieferant = False
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_bezeich, avail_lieferant, l_lieferant
        nonlocal lief_nr

        return {"lief_bezeich": lief_bezeich, "avail_lieferant": avail_lieferant}


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    if not l_lieferant:

        return generate_output()

    elif l_lieferant:
        lief_bezeich = l_lieferant.firma
        avail_lieferant = True

    return generate_output()