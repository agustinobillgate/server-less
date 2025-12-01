#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Nation

def officer_admin_btn_delartbl(rec_id:int):
    err_code = 0
    queasy = nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, queasy, nation
        nonlocal rec_id

        return {"err_code": err_code}


    # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).with_for_update().first()

    if queasy:
        nation = get_cache (Nation, {"untergruppe": [(eq, queasy.number3)]})

        if nation:
            err_code = 1

            return generate_output()
        pass
        db_session.delete(queasy)
        pass

    return generate_output()