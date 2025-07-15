#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_update_hbill_servicebl(rec_id:int, str:string):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id, str

        return {}


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill.service[4] = to_decimal(str)

    return generate_output()