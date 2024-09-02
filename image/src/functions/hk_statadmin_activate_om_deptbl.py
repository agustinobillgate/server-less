from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Outorder

def hk_statadmin_activate_om_deptbl(pvilanguage:int, dept:int, zinr:str):
    avail_resline = False
    avail_outorder = False
    res_activeflag = 0
    msg_str = ""
    resname = ""
    from_date = None
    lvcarea:str = "hk_statadmin"
    res_line = outorder = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_resline, avail_outorder, res_activeflag, msg_str, resname, from_date, lvcarea, res_line, outorder


        return {"avail_resline": avail_resline, "avail_outorder": avail_outorder, "res_activeflag": res_activeflag, "msg_str": msg_str, "resname": resname, "from_date": from_date}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == dept) &  (func.lower(Res_line.(zinr).lower()) == (zinr).lower())).first()

    if res_line:
        avail_resline = True

        if res_line.active_flag == 1:
            res_activeflag = res_line.active_flag

            return generate_output()

    outorder = db_session.query(Outorder).filter(
            (func.lower(Outorder.(zinr).lower()) == (zinr).lower()) &  (Outorder.betriebsnr == dept)).first()

    if outorder:
        msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

        return generate_output()

    if res_line:
        resname = res_line.name
        from_date = res_line.ankunft

    return generate_output()