#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Outorder

def hk_statadmin_chk_btn_exitbl(pvilanguage:int, resflag:bool, dept:int, zinr:string, from_date:date, to_date:date):

    prepare_cache ([Res_line, Outorder])

    flag = 0
    msg_str = ""
    resname = ""
    lvcarea:string = "hk-statadmin"
    res_line = outorder = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg_str, resname, lvcarea, res_line, outorder
        nonlocal pvilanguage, resflag, dept, zinr, from_date, to_date

        return {"flag": flag, "msg_str": msg_str, "resname": resname}


    if not resflag:

        res_line = get_cache (Res_line, {"resnr": [(eq, dept)],"zinr": [(eq, zinr)]})

        if not res_line:
            flag = 1

            return generate_output()

        if res_line.active_flag == 1:
            flag = 2

            return generate_output()
        resname = res_line.name

        outorder = get_cache (Outorder, {"zinr": [(eq, zinr)],"betriebsnr": [(eq, dept)]})

        if outorder:
            flag = 3
            msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

            return generate_output()
    else:

        outorder = get_cache (Outorder, {"zinr": [(eq, zinr)],"betriebsnr": [(eq, dept)],"gespstart": [(gt, to_date)],"gespende": [(lt, from_date)]})

        if outorder:
            flag = 4
            msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

            return generate_output()

    return generate_output()