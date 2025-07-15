#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from models import H_bill

def tada_post_payment_restsale_updatehbillbl(rec_id:int):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id

        return {}


    h_bill = db_session.query(H_bill).filter(
             (H_bill._recid == rec_id)).first()
    h_bill.rgdruck = 1

    return generate_output()