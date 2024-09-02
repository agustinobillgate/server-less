from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Outorder

def hk_statadmin_chk_btn_exitbl(pvilanguage:int, resflag:bool, dept:int, zinr:str, from_date:date, to_date:date):
    flag = 0
    msg_str = ""
    resname = ""
    lvcarea:str = "hk_statadmin"
    res_line = outorder = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg_str, resname, lvcarea, res_line, outorder


        return {"flag": flag, "msg_str": msg_str, "resname": resname}


    if not resflag:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == dept) &  (func.lower(Res_line.(zinr).lower()) == (zinr).lower())).first()

        if not res_line:
            flag = 1

            return generate_output()

        if res_line.active_flag == 1:
            flag = 2

            return generate_output()
        resname = res_line.name

        outorder = db_session.query(Outorder).filter(
                (func.lower(Outorder.(zinr).lower()) == (zinr).lower()) &  (Outorder.betriebsnr == dept)).first()

        if outorder:
            flag = 3
            msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

            return generate_output()
    else:

        outorder = db_session.query(Outorder).filter(
                (func.lower(Outorder.(zinr).lower()) == (zinr).lower()) &  (Outorder.betriebsnr == dept) &  (not Outorder.gespstart > to_date) &  (not Outorder.gespende < from_date)).first()

        if outorder:
            flag = 4
            msg_str = translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

            return generate_output()