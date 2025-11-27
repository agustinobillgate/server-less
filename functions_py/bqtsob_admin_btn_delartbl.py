#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener

def bqtsob_admin_btn_delartbl(recid_queasy:int):
    err = 0
    queasy = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, queasy, bediener
        nonlocal recid_queasy

        return {"err": err}


    # queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == recid_queasy)).with_for_update().first()

    if queasy:

        bediener = get_cache (Bediener, {"user_group": [(eq, int (queasy.char1))],"flag": [(eq, 0)]})

        if bediener:
            err = 1
        else:
            pass

            if queasy:
                db_session.delete(queasy)

    return generate_output()