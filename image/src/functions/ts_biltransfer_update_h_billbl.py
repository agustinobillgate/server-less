from functions.additional_functions import *
import decimal
from models import H_bill

def ts_biltransfer_update_h_billbl(rec_id:int, char1:str):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    h_bill.bilname = char1

    h_bill = db_session.query(H_bill).first()

    return generate_output()