#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 27/10/2025
#--------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Guest

t_guest_data, T_guest = create_model_like(Guest)

def write_guestbl(case_type:int, t_guest_data:[T_guest]):
    success_flag = False
    guest = None

    t_guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, guest
        nonlocal case_type


        nonlocal t_guest

        return {"success_flag": success_flag}

    # t_guest = query(t_guest_data, first=True)
    t_guest = t_guest_data[0] if t_guest_data else None

    if case_type == 1:

        # guest = get_cache (Guest, {"gastnr": [(eq, t_guest.gastnr)]})
        guest = db_session.query(Guest).filter(Guest.gastnr == t_guest.gastnr).first()

        if guest:
            buffer_copy(t_guest, guest)
            guest.karteityp = t_guest.karteityp
            db_session.commit()
            success_flag = True
    elif case_type == 2:
        guest = Guest()
        db_session.add(guest)

        buffer_copy(t_guest, guest)
        pass
        success_flag = True
    elif case_type == 3:

        guest = get_cache (Guest, {"gastnr": [(eq, t_guest.gastnr)]})

        if guest:
            db_session.delete(guest)
            pass
            success_flag = True

    return generate_output()