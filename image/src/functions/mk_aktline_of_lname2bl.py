from functions.additional_functions import *
import decimal
from models import Guest

def mk_aktline_of_lname2bl(gastnr:int):
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

    return generate_output()