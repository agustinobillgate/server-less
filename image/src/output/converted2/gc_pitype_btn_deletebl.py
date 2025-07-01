#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Gc_pitype

def gc_pitype_btn_deletebl(nr:int):
    success_flag = False
    reservation = gc_pitype = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, reservation, gc_pitype
        nonlocal nr

        return {"success_flag": success_flag}


    reservation = get_cache (Reservation, {"resart": [(eq, nr)]})

    if reservation:
        success_flag = False

        return generate_output()
    else:

        gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, nr)]})
        db_session.delete(gc_pitype)
        success_flag = True

    return generate_output()