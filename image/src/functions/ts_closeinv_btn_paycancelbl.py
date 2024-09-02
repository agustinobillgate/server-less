from functions.additional_functions import *
import decimal
from models import Bill

def ts_closeinv_btn_paycancelbl(rechnr:int):
    bilflag = 0
    rec_id = 0
    zinr = ""
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bilflag, rec_id, zinr, bill


        return {"bilflag": bilflag, "rec_id": rec_id, "zinr": zinr}


    bill = db_session.query(Bill).filter(
            (Bill.rechnr == rechnr)).first()
    bilflag = bill.flag
    rec_id = bill._recid
    zinr = bill.zinr

    return generate_output()