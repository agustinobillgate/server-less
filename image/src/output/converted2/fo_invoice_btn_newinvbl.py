from functions.additional_functions import *
import decimal
from functions.create_newbillbl import create_newbillbl
from models import Bill, Res_line

def fo_invoice_btn_newinvbl(bil_recid:int, bill_anzahl:int):
    bill = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, res_line
        nonlocal bil_recid, bill_anzahl


        return {}


    bill = db_session.query(Bill).filter(
             (Bill._recid == bil_recid)).first()

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.reslinnr)).first()
    bil_recid = get_output(create_newbillbl(res_line.resnr, res_line.reslinnr, bill.parent_nr, bill_anzahl))

    return generate_output()