#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def arl_list_ask_voucherbl(lresnr:int):

    prepare_cache ([Res_line])

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


    rline = get_cache (Res_line, {"resnr": [(eq, lresnr)],"active_flag": [(le, 1)]})
    sorttype = rline.active_flag + 1

    return generate_output()