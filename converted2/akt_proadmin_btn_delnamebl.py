#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code, Akthdr

def akt_proadmin_btn_delnamebl(rec_id:int):
    err = 0
    akt_code = akthdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_code, akthdr
        nonlocal rec_id

        return {"err": err}


    akt_code = get_cache (Akt_code, {"_recid": [(eq, rec_id)]})

    if akt_code:

        akthdr = db_session.query(Akthdr).filter(
                 (Akthdr.product[inc_value(0)] == akt_code.aktionscode) | (Akthdr.product[inc_value(1)] == akt_code.aktionscode) | (Akthdr.product[inc_value(2)] == akt_code.aktionscode)).first()

        if akthdr:
            err = 1


        else:
            pass
            db_session.delete(akt_code)
            pass

    return generate_output()