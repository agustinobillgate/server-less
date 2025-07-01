#using conversion tools version: 1.0.0.111

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


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    pass
    h_bill.rgdruck = 1
    pass

    return generate_output()