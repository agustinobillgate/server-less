#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill

def prepare_fo_invoice1bl(inp_rechnr:int):

    prepare_cache ([Res_line, Bill])

    room = ""
    gname = ""
    bill_recid = 0
    res_line = bill = None

    rline = None

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room, gname, bill_recid, res_line, bill
        nonlocal inp_rechnr
        nonlocal rline


        nonlocal rline

        return {"room": room, "gname": gname, "bill_recid": bill_recid}


    bill = get_cache (Bill, {"rechnr": [(eq, inp_rechnr)]})
    bill_recid = bill._recid

    rline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
    room = bill.zinr

    if rline:
        gname = rline.name

    return generate_output()