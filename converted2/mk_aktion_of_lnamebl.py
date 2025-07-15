from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

t_guest_list, T_guest = create_model_like(Guest)

def mk_aktion_of_lnamebl(t_guest_list:[T_guest], lname:str):
    guest1_gastnr = 0
    avail_guest1 = True
    guest = None

    t_guest = guest1 = None

    Guest1 = create_buffer("Guest1",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest1_gastnr, avail_guest1, guest
        nonlocal lname
        nonlocal guest1


        nonlocal t_guest, guest1
        nonlocal t_guest_list
        return {"t-guest": t_guest_list, "guest1_gastnr": guest1_gastnr, "avail_guest1": avail_guest1}

    guest1 = db_session.query(Guest1).filter(
             (func.lower(Guest1.name) == (lname).lower())).first()

    if not guest1:
        avail_guest1 = False

        return generate_output()
    else:
        guest1_gastnr = guest1.gastnr

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == guest1.gastnr)).first()
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        buffer_copy(guest, t_guest)

    return generate_output()