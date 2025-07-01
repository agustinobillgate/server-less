#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

def select_baraumbl():
    t_bk_raum_list = []
    bk_raum = None

    t_bk_raum = None

    t_bk_raum_list, T_bk_raum = create_model_like(Bk_raum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_raum_list, bk_raum


        nonlocal t_bk_raum
        nonlocal t_bk_raum_list

        return {"t-bk-raum": t_bk_raum_list}

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_list.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)

    return generate_output()