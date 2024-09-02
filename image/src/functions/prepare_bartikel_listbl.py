from functions.additional_functions import *
import decimal
from models import Bk_raum

def prepare_bartikel_listbl():
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

    for bk_raum in db_session.query(Bk_raum).all():
        buffer_copy(bk_raum, t_bk_raum)

    return generate_output()