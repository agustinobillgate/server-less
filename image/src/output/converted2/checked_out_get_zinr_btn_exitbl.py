#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line

def checked_out_get_zinr_btn_exitbl(ci_date:date, zinr:string):

    prepare_cache ([Res_line])

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


    res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"abreise": [(eq, ci_date)],"zinr": [(eq, zinr)]})

    if not res_line:
        err_no = 1
    else:

        resline = get_cache (Res_line, {"resnr": [(ne, res_line.resnr)],"zinr": [(eq, zinr)],"active_flag": [(eq, 1)]})

        if resline:
            err_no = 2
        else:
            err_no = 3

    return generate_output()