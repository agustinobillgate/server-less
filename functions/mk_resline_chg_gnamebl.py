#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from models import Guest

def mk_resline_chg_gnamebl(guestnr:int, gastnr:int):
    guestname = ""
    ind_flag = False
    t_guest_data = []
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    guest = None

    t_guest = None

    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, ind_flag, t_guest_data, ind_gastnr, wig_gastnr, guest
        nonlocal guestnr, gastnr


        nonlocal t_guest
        nonlocal t_guest_data

        return {"guestname": guestname, "ind_flag": ind_flag, "t-guest": t_guest_data}

    guest = get_cache (Guest, {"gastnr": [(eq, guestnr)]})
    guestname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)
    wig_gastnr = get_output(htpint(109))
    ind_gastnr = get_output(htpint(123))

    if (guest.gastnr == wig_gastnr) or (guest.gastnr == ind_gastnr):
        ind_flag = True

    return generate_output()