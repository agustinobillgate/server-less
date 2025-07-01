#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def prepare_select_posusrbl():
    t_bediener_list = []
    bediener = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, bediener


        nonlocal t_bediener
        nonlocal t_bediener_list

        return {"t-bediener": t_bediener_list}

    for bediener in db_session.query(Bediener).filter(
             (Bediener.flag == 0)).order_by(Bediener.username).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()