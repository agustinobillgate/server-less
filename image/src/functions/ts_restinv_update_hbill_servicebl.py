from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_update_hbill_servicebl(rec_id:int, str:str):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    h_bill.service[4] = decimal.Decimal(str)

    return generate_output()