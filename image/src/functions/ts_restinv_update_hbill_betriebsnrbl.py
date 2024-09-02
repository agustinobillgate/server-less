from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_update_hbill_betriebsnrbl(rec_id:int, order_taker:int):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    h_bill = db_session.query(H_bill).first()
    h_bill.betriebsnr = order_taker

    h_bill = db_session.query(H_bill).first()

    return generate_output()