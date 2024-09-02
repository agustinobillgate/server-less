from functions.additional_functions import *
import decimal
from models import Guest

def akt_account_btn_gcfbl(curr_gastnr:int):
    karteityp = 0
    gastnr = 0
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal karteityp, gastnr, guest


        return {"karteityp": karteityp, "gastnr": gastnr}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == curr_gastnr)).first()

    if guest:
        karteityp = guest.karteityp
        gastnr = guest.gastnr

    return generate_output()