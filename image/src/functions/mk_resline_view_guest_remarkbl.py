from functions.additional_functions import *
import decimal
from models import Guest_remark, Guest

def mk_resline_view_guest_remarkbl(inp_gastnr:int):
    guest_name = ""
    t_guest_remark_list = []
    guest_remark = guest = None

    t_guest_remark = None

    t_guest_remark_list, T_guest_remark = create_model_like(Guest_remark)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, t_guest_remark_list, guest_remark, guest


        nonlocal t_guest_remark
        nonlocal t_guest_remark_list
        return {"guest_name": guest_name, "t-guest-remark": t_guest_remark_list}

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == inp_gastnr)).first()

    if guest:
        guest_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    for guest_remark in db_session.query(Guest_remark).filter(
            (Guest_remark.gastnr == inp_gastnr)).all():
        t_guest_remark = T_guest_remark()
        t_guest_remark_list.append(t_guest_remark)

        buffer_copy(guest_remark, t_guest_remark)

    return generate_output()