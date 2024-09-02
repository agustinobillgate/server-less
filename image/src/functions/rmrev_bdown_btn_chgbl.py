from functions.additional_functions import *
import decimal
from models import Res_line

def rmrev_bdown_btn_chgbl(res_recid:int):
    res_gatsnr = 0
    res_resnr = 0
    res_reslinnr = 0
    res_zipreis = 0
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_gatsnr, res_resnr, res_reslinnr, res_zipreis, res_line


        return {"res_gatsnr": res_gatsnr, "res_resnr": res_resnr, "res_reslinnr": res_reslinnr, "res_zipreis": res_zipreis}


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == res_recid)).first()
    res_gatsnr = res_line.gastnr
    res_resnr = res_line.resnr
    res_reslinnr = res_line.reslinnr
    res_zipreis = res_line.zipreis

    return generate_output()