#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def prepare_mk_aktionbl(inp_gastnr:int):
    t_guest_list = []
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_list, guest
        nonlocal inp_gastnr


        nonlocal t_guest
        nonlocal t_guest_list

        return {"t-guest": t_guest_list}

    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

    if guest:
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        buffer_copy(guest, t_guest)

    return generate_output()