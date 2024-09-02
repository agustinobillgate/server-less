from functions.additional_functions import *
import decimal
from models import Bill

def gacct_balance_mi_viewbl(rechnr:int):
    a_resnr = 0
    a_rechnr = 0
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_resnr, a_rechnr, bill


        return {"a_resnr": a_resnr, "a_rechnr": a_rechnr}


    bill = db_session.query(Bill).filter(
            (Bill.rechnr == rechnr)).first()
    a_resnr = bill.resnr
    a_rechnr = bill.rechnr

    return generate_output()