#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def ap_edit_return_firmabl(firma:string):

    prepare_cache ([L_lieferant])

    lief_nr = 0
    fl_temp = 0
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr, fl_temp, l_lieferant
        nonlocal firma

        return {"lief_nr": lief_nr, "fl_temp": fl_temp}


    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, firma)]})

    if not l_lieferant:
        fl_temp = 1

        return generate_output()
    lief_nr = l_lieferant.lief_nr
    fl_temp = 0

    return generate_output()