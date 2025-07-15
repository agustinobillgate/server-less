from functions.additional_functions import *
import decimal
from models import Guest

def mk_aktion_btn_help1bl(gastnr:int):
    t_guest_list = []
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_list, guest
        nonlocal gastnr


        nonlocal t_guest
        nonlocal t_guest_list
        return {"t-guest": t_guest_list}

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == gastnr)).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    return generate_output()