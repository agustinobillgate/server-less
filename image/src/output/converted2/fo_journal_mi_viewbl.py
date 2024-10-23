from functions.additional_functions import *
import decimal
from models import Bill

def fo_journal_mi_viewbl(rechnr:int):
    bill_resnr = 0
    bill_rechnr = 0
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_resnr, bill_rechnr, bill
        nonlocal rechnr


        return {"bill_resnr": bill_resnr, "bill_rechnr": bill_rechnr}


    bill = db_session.query(Bill).filter(
             (Bill.rechnr == rechnr)).first()
    bill_resnr = bill.resnr
    bill_rechnr = bill.rechnr

    return generate_output()