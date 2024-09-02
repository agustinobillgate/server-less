from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bk_reser, Bk_raum

def copy_bares_t_reslinebl(frdate:date, todate:date, rraum:str):
    t_resline_list = []
    bk_reser = bk_raum = None

    t_resline = bkraum = resline = None

    t_resline_list, T_resline = create_model_like(Bk_reser, {"vorbereit":int})

    Bkraum = Bk_raum
    Resline = Bk_reser

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_resline_list, bk_reser, bk_raum
        nonlocal bkraum, resline


        nonlocal t_resline, bkraum, resline
        nonlocal t_resline_list
        return {"t-resline": t_resline_list}

    resline_obj_list = []
    for resline, bkraum in db_session.query(Resline, Bkraum).join(Bkraum,(Bkraum.raum == Resline.raum) &  (func.lower(Bkraum.lu_raum) == (rraum).lower())).filter(
            (Resline.datum >= frdate) &  (Resline.datum <= todate)).all():
        if resline._recid in resline_obj_list:
            continue
        else:
            resline_obj_list.append(resline._recid)


        t_resline = T_resline()
        t_resline_list.append(t_resline)

        buffer_copy(resline, t_resline)
        t_resline.vorbereit = bkraum.vorbereit

    return generate_output()