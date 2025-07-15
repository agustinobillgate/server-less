#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_outorderbl import read_outorderbl
from functions.read_res_linebl import read_res_linebl
from models import Outorder, Res_line

def hk_get_ooo_omdetailbl(roomnumber:string, resnumber:int, fromdate:date, todate:date):
    roomno = ""
    resno = 0
    resname = ""
    from_date = None
    to_date = None
    reason = ""
    outorder = res_line = None

    t_outorder = t_res_line = None

    t_outorder_data, T_outorder = create_model_like(Outorder)
    t_res_line_data, T_res_line = create_model_like(Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal roomno, resno, resname, from_date, to_date, reason, outorder, res_line
        nonlocal roomnumber, resnumber, fromdate, todate


        nonlocal t_outorder, t_res_line
        nonlocal t_outorder_data, t_res_line_data

        return {"roomno": roomno, "resno": resno, "resname": resname, "from_date": from_date, "to_date": to_date, "reason": reason}

    t_outorder_data = get_output(read_outorderbl(99, roomnumber, resnumber, fromdate, todate))
    t_res_line_data = get_output(read_res_linebl(24, resnumber, None, None, None, roomnumber, None, None, None, None, ""))

    t_outorder = query(t_outorder_data, first=True)
    roomno = t_outorder.zinr
    from_date = t_outorder.gespstart
    to_date = t_outorder.gespende
    resno = t_outorder.betriebsnr

    if matches(t_outorder.gespgrund,r"*$*"):
        reason = entry(0, t_outorder.gespgrund, "$")
    else:
        reason = t_outorder.gespgrund

    t_res_line = query(t_res_line_data, first=True)

    if t_res_line:
        resname = t_res_line.name

    return generate_output()