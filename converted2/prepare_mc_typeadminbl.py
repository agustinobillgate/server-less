#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_fee, Mc_types, Mc_guest

def prepare_mc_typeadminbl():
    t_mc_types_data = []
    t_mc_fee_data = []
    t_mc_guest_data = []
    mc_fee = mc_types = mc_guest = None

    t_mc_fee = t_mc_types = t_mc_guest = None

    t_mc_fee_data, T_mc_fee = create_model_like(Mc_fee)
    t_mc_types_data, T_mc_types = create_model_like(Mc_types, {"rec_id":int})
    t_mc_guest_data, T_mc_guest = create_model_like(Mc_guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mc_types_data, t_mc_fee_data, t_mc_guest_data, mc_fee, mc_types, mc_guest


        nonlocal t_mc_fee, t_mc_types, t_mc_guest
        nonlocal t_mc_fee_data, t_mc_types_data, t_mc_guest_data

        return {"t-mc-types": t_mc_types_data, "t-mc-fee": t_mc_fee_data, "t-mc-guest": t_mc_guest_data}

    for mc_types in db_session.query(Mc_types).order_by(Mc_types._recid).all():
        t_mc_types = T_mc_types()
        t_mc_types_data.append(t_mc_types)

        buffer_copy(mc_types, t_mc_types)
        t_mc_types.rec_id = mc_types._recid

    for mc_fee in db_session.query(Mc_fee).filter(
             (Mc_fee.key == 1)).order_by(Mc_fee._recid).all():
        t_mc_fee = T_mc_fee()
        t_mc_fee_data.append(t_mc_fee)

        buffer_copy(mc_fee, t_mc_fee)

    for mc_guest in db_session.query(Mc_guest).order_by(Mc_guest._recid).all():
        t_mc_guest = T_mc_guest()
        t_mc_guest_data.append(t_mc_guest)

        buffer_copy(mc_guest, t_mc_guest)

    return generate_output()