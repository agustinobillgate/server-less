#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser

def ba_plan_res_cancel2bl(t_resnr:int, t_reslinnr:int):
    t_resline_list = []
    bk_reser = None

    t_resline = resline = None

    t_resline_list, T_resline = create_model_like(Bk_reser)

    Resline = create_buffer("Resline",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_resline_list, bk_reser
        nonlocal t_resnr, t_reslinnr
        nonlocal resline


        nonlocal t_resline, resline
        nonlocal t_resline_list

        return {"t-resline": t_resline_list}

    for resline in db_session.query(Resline).filter(
             (Resline.veran_nr == t_resnr)).order_by(Resline._recid).all():
        t_resline = T_resline()
        t_resline_list.append(t_resline)

        buffer_copy(resline, t_resline)

    return generate_output()