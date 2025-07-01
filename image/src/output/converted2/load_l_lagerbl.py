#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

def load_l_lagerbl():
    t_l_lager_list = []
    l_lager = None

    t_l_lager = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lager_list, l_lager


        nonlocal t_l_lager
        nonlocal t_l_lager_list

        return {"t-l-lager": t_l_lager_list}

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    return generate_output()