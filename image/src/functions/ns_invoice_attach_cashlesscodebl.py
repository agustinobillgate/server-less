from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill, Queasy, Bill_line

def ns_invoice_attach_cashlesscodebl(cashless_code:str, bill_recid:int):
    ok_flag = False
    msg_int = 0
    found_sameqr:bool = False
    invalid_code:bool = False
    transaction_exist:bool = False
    bill = queasy = bill_line = None

    buf_bill = None

    Buf_bill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, msg_int, found_sameqr, invalid_code, transaction_exist, bill, queasy, bill_line
        nonlocal buf_bill


        nonlocal buf_bill
        return {"ok_flag": ok_flag, "msg_int": msg_int}


    for buf_bill in db_session.query(Buf_bill).filter(
            (Buf_bill.flag == 0) &  (Buf_bill.resnr == 0) &  (Buf_bill.reslinnr == 1) &  (Buf_bill.rechnr > 0)).all():

        if buf_bill.vesrdepot2.lower()  != "" and buf_bill.vesrdepot2.lower()  == (cashless_code).lower() :
            found_sameqr = True
            break

    if found_sameqr:
        msg_int = 1

        return generate_output()

    if cashless_code != "":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 248) &  (func.lower(Queasy.char2) == (cashless_code).lower())).first()

        if not queasy:
            invalid_code = True

        if invalid_code:
            msg_int = 2

            return generate_output()

    buf_bill = db_session.query(Buf_bill).filter(
            (Buf_bill._recid == bill_recid) &  (Buf_bill.flag == 0) &  (Buf_bill.resnr == 0) &  (Buf_bill.reslinnr == 1) &  (Buf_bill.rechnr > 0) &  (Buf_bill.vesrdepot2 != "")).first()

    if buf_bill:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == buf_bill.rechnr)).first()

        if bill_line:
            msg_int = 3

            return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bill_recid)).first()

    if bill:

        bill = db_session.query(Bill).first()
        bill.vesrdepot2 = cashless_code

        bill = db_session.query(Bill).first()

        ok_flag = True

    return generate_output()