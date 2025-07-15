#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_guest

def read_mc_guestbl(case_type:int, guestno:int, cardnum:string):
    t_mc_guest_data = []
    mc_guest = None

    t_mc_guest = None

    t_mc_guest_data, T_mc_guest = create_model_like(Mc_guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mc_guest_data, mc_guest
        nonlocal case_type, guestno, cardnum


        nonlocal t_mc_guest
        nonlocal t_mc_guest_data

        return {"t-mc-guest": t_mc_guest_data}

    if case_type == 1:

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guestno)],"activeflag": [(eq, True)]})

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_data.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 2:

        mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)]})

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_data.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 3:

        mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)],"gastnr": [(ne, guestno)]})

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_data.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 4:

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guestno)]})

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_data.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 5:

        mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)],"activeflag": [(eq, True)]})

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_data.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)

    return generate_output()