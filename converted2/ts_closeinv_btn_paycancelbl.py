#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def ts_closeinv_btn_paycancelbl(rechnr:int):

    prepare_cache ([Bill])

    bilflag = 0
    rec_id = 0
    zinr = ""
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bilflag, rec_id, zinr, bill
        nonlocal rechnr

        return {"bilflag": bilflag, "rec_id": rec_id, "zinr": zinr}


    bill = get_cache (Bill, {"rechnr": [(eq, rechnr)]})
    bilflag = bill.flag
    rec_id = bill._recid
    zinr = bill.zinr

    return generate_output()