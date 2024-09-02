from functions.additional_functions import *
import decimal
from models import Res_line

def arl_list_check_depositbl(arl_list_resnr:int):
    anzahl = 0
    res_line = None

    resline = None

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, res_line
        nonlocal resline


        nonlocal resline
        return {"anzahl": anzahl}


    resline = db_session.query(Resline).filter(
            (Resline.resnr == arl_list_resnr) &  (Resline.active_flag == 1)).first()

    if resline:

        return generate_output()

    resline = db_session.query(Resline).filter(
            (Resline.resnr == arl_list_resnr) &  (Resline.active_flag == 2) &  (Resline.resstatus == 8)).first()

    if resline:

        return generate_output()

    for resline in db_session.query(Resline).filter(
            (Resline.resnr == arl_list_resnr) &  (Resline.active_flag == 0)).all():
        anzahl = anzahl + 1

    return generate_output()