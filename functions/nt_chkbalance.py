from functions.additional_functions import *
import decimal
from models import Bill, Bill_line

def nt_chkbalance():
    sum:decimal = to_decimal("0.0")
    bill = bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sum, bill, bill_line

        return {}


    for bill in db_session.query(Bill).filter(
             (Bill.flag == 0) & (Bill.rechnr != 0)).order_by(Bill._recid).all():
        sum =  to_decimal("0")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
            sum =  to_decimal(sum) + to_decimal(bill_line.betrag)

        if sum != bill.saldo:
            pass

    return generate_output()