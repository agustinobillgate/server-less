from functions.additional_functions import *
import decimal
from models import Bk_raum

def prepare_ba_raum_1bl():
    t_bk_raum_list = []
    bk_raum = None

    t_bk_raum = None

    t_bk_raum_list, T_bk_raum = create_model_like(Bk_raum, {"rec_id":int, "flag_desc":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_raum_list, bk_raum


        nonlocal t_bk_raum
        nonlocal t_bk_raum_list
        return {"t-bk-raum": t_bk_raum_list}

    for bk_raum in db_session.query(Bk_raum).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_list.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)
        t_bk_raum.rec_id = bk_raum._recid

        if bk_raum.betriebsnr == 0:
            t_bk_raum.flag_desc = False

        elif bk_raum.betriebsnr == 1:
            t_bk_raum.flag_desc = True

    return generate_output()