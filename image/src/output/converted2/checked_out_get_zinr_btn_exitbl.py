from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line

def checked_out_get_zinr_btn_exitbl(ci_date:date, zinr:str):
    err_no = 0
    res_line = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, res_line
        nonlocal ci_date, zinr
        nonlocal resline


        nonlocal resline
        return {"err_no": err_no}


    res_line = db_session.query(Res_line).filter(
             (Res_line.resstatus == 8) & (Res_line.abreise == ci_date) & (func.lower(Res_line.zinr) == (zinr).lower())).first()

    if not res_line:
        err_no = 1
    else:

        resline = db_session.query(Resline).filter(
                 (Resline.resnr != res_line.resnr) & (func.lower(Resline.zinr) == (zinr).lower()) & (Resline.active_flag == 1)).first()

        if resline:
            err_no = 2
        else:
            err_no = 3

    return generate_output()