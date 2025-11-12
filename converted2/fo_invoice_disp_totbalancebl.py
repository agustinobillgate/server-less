#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def fo_invoice_disp_totbalancebl(bil_recid:int):

    prepare_cache ([Bill])

    tot_balance = to_decimal("0.0")
    bill = None

    bill1 = None

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_balance, bill
        nonlocal bil_recid
        nonlocal bill1


        nonlocal bill1

        return {"tot_balance": tot_balance}

    tot_balance =  to_decimal("0")

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    # for bill1 in db_session.query(Bill1).filter(
    #          (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.flag == 0) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
    for bill1 in db_session.query(Bill1).filter(
            (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.flag == 0) & (Bill1.zinr == bill.zinr.strip())).order_by(Bill1._recid).all():
        tot_balance =  to_decimal(tot_balance) + to_decimal(bill1.saldo)

    return generate_output()