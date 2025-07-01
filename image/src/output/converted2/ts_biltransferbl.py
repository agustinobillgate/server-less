#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Bill

def ts_biltransferbl(rechnr:int, bil_rec_id:int, dept:int):

    prepare_cache ([H_bill, Bill])

    h_bill = bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, bill
        nonlocal rechnr, bil_rec_id, dept

        return {}


    h_bill = get_cache (H_bill, {"_recid": [(eq, bil_rec_id)],"departement": [(eq, dept)]})

    bill = get_cache (Bill, {"_recid": [(eq, rechnr)]})

    if bill:
        pass

        if h_bill:
            h_bill.resnr = bill.resnr
            h_bill.reslinnr = bill.reslinnr


            pass

    return generate_output()