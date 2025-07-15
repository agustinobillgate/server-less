#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def prepare_gst_initbl():
    t_l_artikel_data = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_data, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"t-l-artikel": t_l_artikel_data}

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    return generate_output()