from functions.additional_functions import *
import decimal
from models import Guest_pr

def read_guest_prbl(case_type:int, guestno:int, ratecode:str):
    t_guest_pr_list = []
    guest_pr = None

    t_guest_pr = None

    t_guest_pr_list, T_guest_pr = create_model_like(Guest_pr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_pr_list, guest_pr


        nonlocal t_guest_pr
        nonlocal t_guest_pr_list
        return {"t-guest-pr": t_guest_pr_list}

    if case_type == 1:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guestno)).first()

        if guest_pr:
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)
    elif case_type == 2:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.CODE == ratecode)).first()

        if guest_pr:
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)
    elif case_type == 3:

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guestno)).all():
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)

    elif case_type == 4:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guestno) &  (Guest_pr.CODE == ratecode)).first()

        if guest_pr:
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)
    elif case_type == 5:

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guestno) &  (Guest_pr.CODE != ratecode)).all():
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)

    elif case_type == 6:

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.CODE == ratecode)).all():
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)

    return generate_output()