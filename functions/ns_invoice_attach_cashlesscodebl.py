#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Queasy, Bill_line

def ns_invoice_attach_cashlesscodebl(cashless_code:string, bill_recid:int):

    prepare_cache ([Bill])

    ok_flag = False
    msg_int = 0
    found_sameqr:bool = False
    invalid_code:bool = False
    transaction_exist:bool = False
    bill = queasy = bill_line = None

    buf_bill = None

    Buf_bill = create_buffer("Buf_bill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, msg_int, found_sameqr, invalid_code, transaction_exist, bill, queasy, bill_line
        nonlocal cashless_code, bill_recid
        nonlocal buf_bill


        nonlocal buf_bill

        return {"ok_flag": ok_flag, "msg_int": msg_int}


    for buf_bill in db_session.query(Buf_bill).filter(
             (Buf_bill.flag == 0) & (Buf_bill.resnr == 0) & (Buf_bill.reslinnr == 1) & (Buf_bill.rechnr > 0)).order_by(Buf_bill._recid).yield_per(100):

        if buf_bill.vesrdepot2.lower()  != "" and buf_bill.vesrdepot2.lower()  == (cashless_code).lower() :
            found_sameqr = True
            break

    if found_sameqr:
        msg_int = 1

        return generate_output()

    if cashless_code != "":

        queasy = get_cache (Queasy, {"key": [(eq, 248)],"char2": [(eq, cashless_code)]})

        if not queasy:
            invalid_code = True

        if invalid_code:
            msg_int = 2

            return generate_output()

    buf_bill = get_cache (Bill, {"_recid": [(eq, bill_recid)],"flag": [(eq, 0)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"rechnr": [(gt, 0)],"vesrdepot2": [(ne, "")]})

    if buf_bill:

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, buf_bill.rechnr)]})

        if bill_line:
            msg_int = 3

            return generate_output()

    bill = get_cache (Bill, {"_recid": [(eq, bill_recid)]})

    if bill:
        pass
        bill.vesrdepot2 = cashless_code
        pass
        pass
        ok_flag = True

    return generate_output()