from functions.additional_functions import *
import decimal
from models import Akt_code, Akthdr

def akt_proadmin_btn_delnamebl(rec_id:int):
    err = 0
    akt_code = akthdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_code, akthdr


        return {"err": err}


    akt_code = db_session.query(Akt_code).filter(
            (Akt_code._recid == rec_id)).first()

    akthdr = db_session.query(Akthdr).filter(
            (Akthdr.product[0] == akt_code.aktionscode) |  (Akthdr.product[2] == akt_code.aktionscode) |  (Akthdr.product[2] == akt_code.aktionscode)).first()

    if akthdr:
        err = 1
    else:

        akt_code = db_session.query(Akt_code).first()
        db_session.delete(akt_code)

    return generate_output()