#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

def edit_baraum_webbl(raum:string):
    bk_list_list = []
    t_bk_raum_list = []
    bk_raum = None

    t_bk_raum = bk_list = None

    t_bk_raum_list, T_bk_raum = create_model_like(Bk_raum)
    bk_list_list, Bk_list = create_model_like(Bk_raum, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_list, t_bk_raum_list, bk_raum
        nonlocal raum


        nonlocal t_bk_raum, bk_list
        nonlocal t_bk_raum_list, bk_list_list

        return {"bk-list": bk_list_list, "t-bk-raum": t_bk_raum_list}


    bk_raum = get_cache (Bk_raum, {"raum": [(eq, raum)]})
    bk_list = Bk_list()
    bk_list_list.append(bk_list)

    buffer_copy(bk_raum, bk_list)
    bk_list.rec_id = bk_raum._recid

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_list.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)

    return generate_output()