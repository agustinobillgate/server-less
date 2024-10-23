from functions.additional_functions import *
import decimal
from models import Res_line

def arl_list_ask_voucherbl(lresnr:int):
    sorttype = 0
    res_line = None

    rline = None

    Rline = create_buffer("Rline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sorttype, res_line
        nonlocal lresnr
        nonlocal rline


        nonlocal rline
        return {"sorttype": sorttype}


    rline = db_session.query(Rline).filter(
             (Rline.resnr == lresnr) & (Rline.active_flag <= 1)).first()
    sorttype = rline.active_flag + 1

    return generate_output()