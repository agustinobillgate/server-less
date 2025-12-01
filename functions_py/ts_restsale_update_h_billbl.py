#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# if not availble -> return
# Rd, 01/12/2025, with_for_update added
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restsale_update_h_billbl(rec_id:int):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id

        return {}


    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == rec_id)).with_for_update().first()
    # Rd 3/8/2025
    # if not avail return
    if h_bill is None:
        return generate_output()
    
    pass
    h_bill.rgdruck = 1
    pass

    return generate_output()