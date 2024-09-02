from functions.additional_functions import *
import decimal
from models import Guest

def chg_akthdr_btn_help1bl(gastnr:int):
    lname = ""
    guest_gastnr = 0
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, guest_gastnr, guest


        return {"lname": lname, "guest_gastnr": guest_gastnr}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    lname = guest.name + ", " + guest.anredefirma
    guest_gastnr = guest.gastnr

    return generate_output()