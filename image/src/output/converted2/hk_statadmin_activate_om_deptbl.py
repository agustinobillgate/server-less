#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Outorder

def hk_statadmin_activate_om_deptbl(pvilanguage:int, dept:int, zinr:string):

    prepare_cache ([Res_line, Outorder])

    avail_resline = False
    avail_outorder = False
    res_activeflag = 0
    msg_str = ""
    resname = ""
    from_date = None
    lvcarea:string = "hk-statadmin"
    res_line = outorder = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_resline, avail_outorder, res_activeflag, msg_str, resname, from_date, lvcarea, res_line, outorder
        nonlocal pvilanguage, dept, zinr

        return {"avail_resline": avail_resline, "avail_outorder": avail_outorder, "res_activeflag": res_activeflag, "msg_str": msg_str, "resname": resname, "from_date": from_date}


    res_line = get_cache (Res_line, {"resnr": [(eq, dept)],"zinr": [(eq, zinr)]})

    if res_line:
        avail_resline = True

        if res_line.active_flag == 1:
            res_activeflag = res_line.active_flag

            return generate_output()

    outorder = get_cache (Outorder, {"zinr": [(eq, zinr)],"betriebsnr": [(eq, dept)]})

    if outorder:
        msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

        return generate_output()

    if res_line:
        resname = res_line.name
        from_date = res_line.ankunft

    return generate_output()