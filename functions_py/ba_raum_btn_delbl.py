#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset, Bk_raum

def ba_raum_btn_delbl(rec_id:int, t_raum:string):
    err = 0
    bk_rset = bk_raum = None

    db_session = local_storage.db_session
    t_raum = t_raum.strip()

    def generate_output():
        nonlocal err, bk_rset, bk_raum
        nonlocal rec_id, t_raum

        return {"err": err}


    bk_rset = get_cache (Bk_rset, {"raum": [(eq, t_raum)]})

    if bk_rset:
        err = 1

        return generate_output()

    # bk_raum = get_cache (Bk_raum, {"_recid": [(eq, rec_id)]})
    bk_raum = db_session.query(Bk_raum).filter(
             (Bk_raum._recid == rec_id)).with_for_update().first()

    if bk_raum:
        pass
        db_session.delete(bk_raum)
        pass

    return generate_output()