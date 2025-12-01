#using conversion tools version: 1.0.0.119
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def tada_post_payment_restsale_updatehbillbl(rec_id:int):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id

        return {}


    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill = db_session.query(H_bill).filter(
        H_bill._recid == rec_id
    ).with_for_update().first()
    pass
    h_bill.rgdruck = 1
    pass

    return generate_output()