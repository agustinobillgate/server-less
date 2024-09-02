from functions.additional_functions import *
import decimal
from models import H_bill, Bill

def ts_biltransferbl(rechnr:int, bil_rec_id:int, dept:int):
    h_bill = bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == bil_rec_id) &  (H_bill.departement == dept)).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == rechnr)).first()

    if bill:

        h_bill = db_session.query(H_bill).first()

        if h_bill:
            h_bill.resnr = bill.resnr
            h_bill.reslinnr = bill.reslinnr

            h_bill = db_session.query(H_bill).first()

    return generate_output()