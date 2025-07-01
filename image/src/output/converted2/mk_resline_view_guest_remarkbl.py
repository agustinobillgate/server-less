#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest_remark, Guest

def mk_resline_view_guest_remarkbl(inp_gastnr:int):

    prepare_cache ([Guest])

    guest_name = ""
    t_guest_remark_list = []
    guest_remark = guest = None

    t_guest_remark = None

    t_guest_remark_list, T_guest_remark = create_model_like(Guest_remark)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, t_guest_remark_list, guest_remark, guest
        nonlocal inp_gastnr


        nonlocal t_guest_remark
        nonlocal t_guest_remark_list

        return {"guest_name": guest_name, "t-guest-remark": t_guest_remark_list}

    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

    if guest:
        guest_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    for guest_remark in db_session.query(Guest_remark).filter(
             (Guest_remark.gastnr == inp_gastnr)).order_by(Guest_remark._recid).all():
        t_guest_remark = T_guest_remark()
        t_guest_remark_list.append(t_guest_remark)

        buffer_copy(guest_remark, t_guest_remark)

    return generate_output()