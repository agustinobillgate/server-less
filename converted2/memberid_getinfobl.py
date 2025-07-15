#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Mc_guest

def memberid_getinfobl(gastnr:int):
    member_flag = False
    t_guest_data = []
    t_mcguest_data = []
    i:int = 0
    param1:string = ""
    status_token:string = ""
    guest = mc_guest = None

    t_guest = t_mcguest = None

    t_guest_data, T_guest = create_model_like(Guest)
    t_mcguest_data, T_mcguest = create_model_like(Mc_guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal member_flag, t_guest_data, t_mcguest_data, i, param1, status_token, guest, mc_guest
        nonlocal gastnr


        nonlocal t_guest, t_mcguest
        nonlocal t_guest_data, t_mcguest_data

        return {"member_flag": member_flag, "t-guest": t_guest_data, "t-mcguest": t_mcguest_data}

    member_flag = False

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        t_guest = T_guest()
        t_guest_data.append(t_guest)

        buffer_copy(guest, t_guest)

    mc_guest = db_session.query(Mc_guest).filter(
             (Mc_guest.gastnr == gastnr) & (Mc_guest.activeflag)).first()

    if mc_guest:
        member_flag = True
        t_mcguest = T_mcguest()
        t_mcguest_data.append(t_mcguest)

        buffer_copy(mc_guest, t_mcguest)

    return generate_output()