#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code, Akthdr

def aktstage_admin_btn_delnamebl(rec_id:int):
    err = 0
    akt_code = akthdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_code, akthdr
        nonlocal rec_id

        return {"err": err}


    # akt_code = get_cache (Akt_code, {"_recid": [(eq, rec_id)]})
    akt_code = db_session.query(Akt_code).filter(
             (Akt_code._recid == rec_id)).with_for_update().first()

    if akt_code:

        akthdr = get_cache (Akthdr, {"stufe": [(eq, akt_code.aktionscode)]})

        if akthdr:
            err = 1
        else:
            pass
            db_session.delete(akt_code)

    return generate_output()