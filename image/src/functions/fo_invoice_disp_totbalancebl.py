from functions.additional_functions import *
import decimal
from models import Bill

def fo_invoice_disp_totbalancebl(bil_recid:int):
    tot_balance = 0
    bill = None

    bill1 = None

    Bill1 = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_balance, bill
        nonlocal bill1


        nonlocal bill1
        return {"tot_balance": tot_balance}

    tot_balance = 0

    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    for bill1 in db_session.query(Bill1).filter(
            (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).all():
        tot_balance = tot_balance + bill1.saldo

    return generate_output()