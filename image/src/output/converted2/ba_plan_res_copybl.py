from functions.additional_functions import *
import decimal
from models import Bk_reser

def ba_plan_res_copybl(t_resnr:int, t_reslinnr:int):
    resline_veran_nr = 0
    resline_veran_resnr = 0
    avail_resline = False
    bk_reser = None

    resline = None

    Resline = create_buffer("Resline",Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resline_veran_nr, resline_veran_resnr, avail_resline, bk_reser
        nonlocal t_resnr, t_reslinnr
        nonlocal resline


        nonlocal resline
        return {"resline_veran_nr": resline_veran_nr, "resline_veran_resnr": resline_veran_resnr, "avail_resline": avail_resline}


    resline = db_session.query(Resline).filter(
             (Resline.veran_nr == t_resnr) & (Resline.veran_resnr == t_reslinnr)).first()

    if resline:
        resline_veran_nr = resline.veran_nr
        resline_veran_resnr = resline.veran_resnr
        avail_resline = True

    return generate_output()