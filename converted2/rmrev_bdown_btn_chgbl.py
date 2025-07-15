#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def rmrev_bdown_btn_chgbl(res_recid:int):

    prepare_cache ([Res_line])

    res_gatsnr = 0
    res_resnr = 0
    res_reslinnr = 0
    res_zipreis = to_decimal("0.0")
    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_gatsnr, res_resnr, res_reslinnr, res_zipreis, res_line
        nonlocal res_recid

        return {"res_gatsnr": res_gatsnr, "res_resnr": res_resnr, "res_reslinnr": res_reslinnr, "res_zipreis": res_zipreis}


    res_line = get_cache (Res_line, {"_recid": [(eq, res_recid)]})

    if res_line:
        res_gatsnr = res_line.gastnr
        res_resnr = res_line.resnr
        res_reslinnr = res_line.reslinnr
        res_zipreis =  to_decimal(res_line.zipreis)

    return generate_output()