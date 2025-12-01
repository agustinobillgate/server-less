#using conversion tools version: 1.0.0.117
# -------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
# -------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_update_hbill_betriebsnrbl(rec_id:int, order_taker:int):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id, order_taker

        return {}


    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill = db_session.query(H_bill).filter(
        (H_bill._recid == rec_id)).with_for_update().first()
    pass
    h_bill.betriebsnr = order_taker
    pass

    return generate_output()