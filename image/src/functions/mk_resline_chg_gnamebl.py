from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Guest

def mk_resline_chg_gnamebl(guestnr:int, gastnr:int):
    guestname = ""
    ind_flag = False
    t_guest_list = []
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, ind_flag, t_guest_list, ind_gastnr, wig_gastnr, guest


        nonlocal t_guest
        nonlocal t_guest_list
        return {"guestname": guestname, "ind_flag": ind_flag, "t-guest": t_guest_list}

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == guestnr)).first()
    guestname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)
    wig_gastnr = get_output(htpint(109))
    ind_gastnr = get_output(htpint(123))

    if (guest.gastnr == wig_gastnr) or (guest.gastnr == ind_gastnr):
        ind_flag = True

    return generate_output()