#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_raum

def copy_bares_t_reslinebl(frdate:date, todate:date, rraum:string):

    prepare_cache ([Bk_raum])

    t_resline_data = []
    bk_reser = bk_raum = None

    t_resline = bkraum = resline = None

    t_resline_data, T_resline = create_model_like(Bk_reser, {"vorbereit":int})

    Bkraum = create_buffer("Bkraum",Bk_raum)
    Resline = create_buffer("Resline",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_resline_data, bk_reser, bk_raum
        nonlocal frdate, todate, rraum
        nonlocal bkraum, resline


        nonlocal t_resline, bkraum, resline
        nonlocal t_resline_data

        return {"t-resline": t_resline_data}

    resline_obj_list = {}
    for resline, bkraum in db_session.query(Resline, Bkraum).join(Bkraum,(Bkraum.raum == Resline.raum) & (Bkraum.lu_raum == (rraum).lower())).filter(
             (Resline.datum >= frdate) & (Resline.datum <= todate)).order_by(Resline._recid).all():
        if resline_obj_list.get(resline._recid):
            continue
        else:
            resline_obj_list[resline._recid] = True


        t_resline = T_resline()
        t_resline_data.append(t_resline)

        buffer_copy(resline, t_resline)
        t_resline.vorbereit = bkraum.vorbereit

    return generate_output()