from functions.additional_functions import *
import decimal
from models import Bill, Res_line

def fo_invoice_chg_bill_number1bl(bil_recid:int, curr_billnr:int):
    bill = res_line = None

    bill1 = None

    Bill1 = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, res_line
        nonlocal bill1


        nonlocal bill1
        return {}


    bill1 = db_session.query(Bill1).filter(
            (Bill1._recid == bil_recid)).first()

    bill = db_session.query(Bill).filter(
            (Bill.resnr == bill1.resnr) &  (Bill.parent_nr == bill1.parent_nr) &  (Bill.flag == 0) &  (Bill.zinr == bill1.zinr) &  (Billnr == curr_billnr)).first()

    if not bill:

        bill = db_session.query(Bill).filter(
                (Bill.resnr == bill1.resnr) &  (Bill.parent_nr == bill1.parent_nr) &  (Bill.flag == 0) &  (Billnr == curr_billnr)).first()

        if bill:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

            if res_line:
                bill.zinr = res_line.zinr

            bill = db_session.query(Bill).first()

    if bill:
        bil_recid = bill._recid

    return generate_output()