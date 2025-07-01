#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_stockout_init_dispbl():
    t_l_ophdr_list = []
    l_ophdr = None

    t_l_ophdr = None

    t_l_ophdr_list, T_l_ophdr = create_model_like(L_ophdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_ophdr_list, l_ophdr


        nonlocal t_l_ophdr
        nonlocal t_l_ophdr_list

        return {"t-l-ophdr": t_l_ophdr_list}


    l_ophdr = L_ophdr()
    db_session.add(l_ophdr)

    pass
    t_l_ophdr = T_l_ophdr()
    t_l_ophdr_list.append(t_l_ophdr)

    buffer_copy(l_ophdr, t_l_ophdr)
    t_l_ophdr.rec_id = l_ophdr._recid

    return generate_output()