#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def prepare_mk_aktionbl(inp_gastnr:int):
    t_guest_data = []
    guest = None

    t_guest = None

    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_data, guest
        nonlocal inp_gastnr


        nonlocal t_guest
        nonlocal t_guest_data

        return {"t-guest": t_guest_data}

    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

    if guest:
        t_guest = T_guest()
        t_guest_data.append(t_guest)

        buffer_copy(guest, t_guest)

    return generate_output()