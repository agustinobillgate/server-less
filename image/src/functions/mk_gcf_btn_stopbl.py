from functions.additional_functions import *
import decimal
from models import Guest, Guestseg

def mk_gcf_btn_stopbl(gastnr:int, gcf_ok:bool, karteityp:int, curr_gastnr:int):
    err_nr = 0
    guest = guestseg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_nr, guest, guestseg


        return {"err_nr": err_nr}


    if gcf_ok == False:

        if karteityp == 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == curr_gastnr) &  (Guest.karteityp == karteityp)).first()
        else:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == curr_gastnr) &  (Guest.karteityp > 0)).first()
        guest.gastnr = - guest.gastnr
        curr_gastnr = 0
    else:

        if karteityp >= 0:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastnr)).first()

            if not guestseg:
                err_nr = 1

                return generate_output()