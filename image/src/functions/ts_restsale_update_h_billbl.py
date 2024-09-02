from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restsale_update_h_billbl(rec_id:int):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    h_bill = db_session.query(H_bill).first()
    h_bill.rgdruck = 1

    h_bill = db_session.query(H_bill).first()

    return generate_output()