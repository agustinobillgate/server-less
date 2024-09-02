from functions.additional_functions import *
import decimal
from models import Guest

def ba_plan_btn_guestbl(gastnr:int):
    guest_gastnr = 0
    avail_guest = False
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_gastnr, avail_guest, guest


        return {"guest_gastnr": guest_gastnr, "avail_guest": avail_guest}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    if guest:
        guest_gastnr = guest.gastnr
        avail_guest = True

    return generate_output()