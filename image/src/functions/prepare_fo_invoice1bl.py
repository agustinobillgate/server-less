from functions.additional_functions import *
import decimal
from models import Res_line, Bill

def prepare_fo_invoice1bl(inp_rechnr:int):
    room = ""
    gname = ""
    bill_recid = 0
    res_line = bill = None

    rline = None

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room, gname, bill_recid, res_line, bill
        nonlocal rline


        nonlocal rline
        return {"room": room, "gname": gname, "bill_recid": bill_recid}


    bill = db_session.query(Bill).filter(
            (Bill.rechnr == inp_rechnr)).first()
    bill_recid = bill._recid

    rline = db_session.query(Rline).filter(
            (Rline.resnr == bill.resnr) &  (Rline.reslinnr == bill.reslinnr)).first()
    room = bill.zinr

    if rline:
        gname = rline.name

    return generate_output()