from functions.additional_functions import *
import decimal
from models import Guest, Htparam

t_guest_list, T_guest = create_model_like(Guest)

def mk_gcf0bl(t_guest_list:[T_guest]):
    f_logical = False
    guest = htparam = None

    t_guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_logical, guest, htparam


        nonlocal t_guest
        nonlocal t_guest_list
        return {"f_logical": f_logical}

    t_guest = query(t_guest_list, first=True)

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == t_guest.gastnr)).first()

    if not guest:
        guest = Guest()
    db_session.add(guest)

    buffer_copy(t_guest, guest)
    pass

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 223)).first()

    if htparam.flogical:
        f_logical = True

    return generate_output()