from functions.additional_functions import *
import decimal
from models import Res_line

def arl_list_cancelrsv1_1bl(arl_list_resnr:int):
    avail_resline = False
    res_line = None

    resline = None

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_resline, res_line
        nonlocal resline


        nonlocal resline
        return {"avail_resline": avail_resline}


    resline = db_session.query(Resline).filter(
            (Resline.resnr == arl_list_resnr) &  (Resline.active_flag == 1) &  ((Resline.resstatus == 6) |  (Resline.resstatus == 13))).first()

    if resline:
        avail_resline = True

        return generate_output()