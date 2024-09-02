from functions.additional_functions import *
import decimal
from models import Guest

def correct_statistic_rsvnamebl(a_int:int):
    guestname = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, guest


        return {"guestname": guestname}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == a_int)).first()

    if guest:
        guestname = guest.name

    return generate_output()