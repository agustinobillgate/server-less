#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

def prepare_bk_select_roombl():
    t_bkraum_list = []
    bk_raum = None

    t_bkraum = None

    t_bkraum_list, T_bkraum = create_model_like(Bk_raum)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bkraum_list, bk_raum


        nonlocal t_bkraum
        nonlocal t_bkraum_list

        return {"t-bkraum": t_bkraum_list}

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bkraum = T_bkraum()
        t_bkraum_list.append(t_bkraum)

        buffer_copy(bk_raum, t_bkraum)

    return generate_output()