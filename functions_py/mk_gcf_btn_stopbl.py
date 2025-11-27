#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestseg

def mk_gcf_btn_stopbl(gastnr:int, gcf_ok:bool, karteityp:int, curr_gastnr:int):

    prepare_cache ([Guest])

    err_nr = 0
    guest = guestseg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_nr, guest, guestseg
        nonlocal gastnr, gcf_ok, karteityp, curr_gastnr

        return {"curr_gastnr": curr_gastnr, "err_nr": err_nr}


    if gcf_ok == False:

        if karteityp == 0:

            # guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)],"karteityp": [(eq, karteityp)]})
            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == curr_gastnr) &
                     (Guest.karteityp == karteityp)).with_for_update().first()
        else:

            # guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)],"karteityp": [(gt, 0)]})
            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == curr_gastnr) &
                     (Guest.karteityp > 0)).with_for_update().first()
        guest.gastnr = - guest.gastnr
        curr_gastnr = 0
    else:

        if karteityp >= 0:

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastnr)]})

            if not guestseg:
                err_nr = 1

                return generate_output()

    return generate_output()
