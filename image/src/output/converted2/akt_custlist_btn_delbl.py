from functions.additional_functions import *
import decimal
from models import Akt_cust, Akthdr

def akt_custlist_btn_delbl(a_gastnr:int, rec_id:int):
    err = 0
    akt_cust = akthdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, akt_cust, akthdr
        nonlocal a_gastnr, rec_id


        return {"err": err}


    akt_cust = db_session.query(Akt_cust).filter(
             (Akt_cust._recid == rec_id)).first()

    akthdr = db_session.query(Akthdr).filter(
             (Akthdr.gastnr == a_gastnr)).first()

    if akthdr:
        err = 1
    db_session.delete(akt_cust)

    return generate_output()