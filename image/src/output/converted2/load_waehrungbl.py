#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung

def load_waehrungbl():
    t_waehrung_list = []
    waehrung = None

    t_waehrung = None

    t_waehrung_list, T_waehrung = create_model_like(Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_waehrung_list, waehrung


        nonlocal t_waehrung
        nonlocal t_waehrung_list

        return {"t-waehrung": t_waehrung_list}

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    return generate_output()