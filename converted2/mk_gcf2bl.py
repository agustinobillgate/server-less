from functions.additional_functions import *
import decimal
from models import Guest, Htparam, Akt_cust

t_guest_list, T_guest = create_model_like(Guest)

def mk_gcf2bl(t_guest_list:[T_guest], sales_id:str, user_init:str):
    f_logical = False
    guest = htparam = akt_cust = None

    t_guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_logical, guest, htparam, akt_cust
        nonlocal sales_id, user_init


        nonlocal t_guest
        nonlocal t_guest_list
        return {"f_logical": f_logical}

    t_guest = query(t_guest_list, first=True)

    if sales_id != "":

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1002)).first()

        if htparam.flogical:
            akt_cust = Akt_cust()
            db_session.add(akt_cust)

            akt_cust.gastnr = t_guest.gastnr
            akt_cust.c_init = user_init
            akt_cust.userinit = sales_id

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