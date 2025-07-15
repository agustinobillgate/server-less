#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, H_rezept, Htparam

def prepare_mk_rezeptbl():

    prepare_cache ([Htparam])

    price_type = 0
    t_l_artikel_data = []
    t_h_rezept_data = []
    l_artikel = h_rezept = htparam = None

    t_l_artikel = t_h_rezept = None

    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_type, t_l_artikel_data, t_h_rezept_data, l_artikel, h_rezept, htparam


        nonlocal t_l_artikel, t_h_rezept
        nonlocal t_l_artikel_data, t_h_rezept_data

        return {"price_type": price_type, "t-l-artikel": t_l_artikel_data, "t-h-rezept": t_h_rezept_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    for l_artikel in db_session.query(L_artikel).filter(
             (L_artikel.herkunft == "")).order_by(L_artikel._recid).all():
        l_artikel.herkunft = ";;"


    pass

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_data.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()