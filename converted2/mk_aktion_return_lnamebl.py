from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def mk_aktion_return_lnamebl(lname:str):
    guest1_gastnr = 0
    guest_anredefirma = ""
    avail_guest = False
    guest = None

    guest1 = None

    Guest1 = create_buffer("Guest1",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest1_gastnr, guest_anredefirma, avail_guest, guest
        nonlocal lname
        nonlocal guest1


        nonlocal guest1
        return {"guest1_gastnr": guest1_gastnr, "guest_anredefirma": guest_anredefirma, "avail_guest": avail_guest}


    guest1 = db_session.query(Guest1).filter(
             (func.lower(Guest1.name) == (lname).lower())).first()

    if not guest1:
        pass
    else:
        avail_guest = True
        guest1_gastnr = guest1.gastnr

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == guest1.gastnr)).first()
        guest_anredefirma = guest.anredefirma

    return generate_output()