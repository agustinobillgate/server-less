#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_biltransfer_update_h_billbl(rec_id:int, char1:string):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id, char1

        return {}


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill.bilname = char1
    pass

    return generate_output()