from functions.additional_functions import *
import decimal
from models import Akt_code, Akthdr

def aktstage_admin_btn_delnamebl(rec_id:int):
    err = 0
    akt_code = akthdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_code, akthdr
        nonlocal rec_id


        return {"err": err}


    akt_code = db_session.query(Akt_code).filter(
             (Akt_code._recid == rec_id)).first()

    akthdr = db_session.query(Akthdr).filter(
             (Akthdr.stufe == akt_code.aktionscode)).first()

    if akthdr:
        err = 1
    else:
        db_session.delete(akt_code)

    return generate_output()