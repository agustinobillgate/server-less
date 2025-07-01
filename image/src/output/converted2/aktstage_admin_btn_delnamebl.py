#using conversion tools version: 1.0.0.111

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


    akt_code = get_cache (Akt_code, {"_recid": [(eq, rec_id)]})

    if akt_code:

        akthdr = get_cache (Akthdr, {"stufe": [(eq, akt_code.aktionscode)]})

        if akthdr:
            err = 1
        else:
            pass
            db_session.delete(akt_code)

    return generate_output()