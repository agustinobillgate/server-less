#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Gc_piacct

def gc_piacct_btn_delartbl(g_nr:int):
    flag = 0
    reservation = gc_piacct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, reservation, gc_piacct
        nonlocal g_nr

        return {"flag": flag}


    reservation = get_cache (Reservation, {"resart": [(eq, g_nr)]})

    if reservation:
        flag = 1
    else:

        gc_piacct = get_cache (Gc_piacct, {"nr": [(eq, g_nr)]})
        pass
        db_session.delete(gc_piacct)
        pass

    return generate_output()