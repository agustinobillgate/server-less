from functions.additional_functions import *
import decimal
from models import Guest

def write_guestbl(case_type:int, t_guest:[T_guest]):
    success_flag = False
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, guest


        nonlocal t_guest
        nonlocal t_guest_list
        return {"success_flag": success_flag}

    t_guest = query(t_guest_list, first=True)

    if case_type == 1:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == t_Guest.gastnr)).first()

        if guest:
            buffer_copy(t_guest, guest)

            guest = db_session.query(Guest).first()

            success_flag = True
    elif case_type == 2:
        guest = Guest()
        db_session.add(guest)

        buffer_copy(t_guest, guest)

        success_flag = True
    elif case_type == 3:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == t_Guest.gastnr)).first()

        if guest:
            db_session.delete(guest)

            success_flag = True

    return generate_output()