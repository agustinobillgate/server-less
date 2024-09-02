from functions.additional_functions import *
import decimal
from models import Mc_guest

def read_mc_guestbl(case_type:int, guestno:int, cardnum:str):
    t_mc_guest_list = []
    mc_guest = None

    t_mc_guest = None

    t_mc_guest_list, T_mc_guest = create_model_like(Mc_guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mc_guest_list, mc_guest


        nonlocal t_mc_guest
        nonlocal t_mc_guest_list
        return {"t-mc-guest": t_mc_guest_list}

    if case_type == 1:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == guestno) &  (Mc_guest.activeflag)).first()

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_list.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 2:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.cardnum == cardnum)).first()

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_list.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 3:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.cardnum == cardnum) &  (Mc_guest.gastnr != guestno)).first()

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_list.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 4:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == guestno)).first()

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_list.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)
    elif case_type == 5:

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.cardnum == cardnum) &  (Mc_guest.activeflag)).first()

        if mc_guest:
            t_mc_guest = T_mc_guest()
            t_mc_guest_list.append(t_mc_guest)

            buffer_copy(mc_guest, t_mc_guest)

    return generate_output()