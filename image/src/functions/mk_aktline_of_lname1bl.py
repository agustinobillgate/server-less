from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def mk_aktline_of_lname1bl(guest_gastnr:int, lname:str, akt_line1_gastnr:int):
    guest1_gastnr = 0
    guest_name = ""
    avail_guest1 = False
    avail_guest = False
    guest = None

    guest1 = None

    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest1_gastnr, guest_name, avail_guest1, avail_guest, guest
        nonlocal guest1


        nonlocal guest1
        return {"guest1_gastnr": guest1_gastnr, "guest_name": guest_name, "avail_guest1": avail_guest1, "avail_guest": avail_guest}


    guest1 = db_session.query(Guest1).filter(
            (func.lower(Guest1.name) == (lname).lower()) |  ((func.lower(Guest1.name) + ", " + Guest1.anredefirma) == (lname).lower())).first()

    if not guest1:
        1
    else:
        avail_guest1 = True
        guest1_gastnr = guest1.gastnr

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == guest1.gastnr)).first()

        if guest and guest.name != "":
            lname = guest.name + ", " + guest.anredefirma
            guest_gastnr = guest.gastnr
            avail_guest = True
            guest_name = ""

    return generate_output()