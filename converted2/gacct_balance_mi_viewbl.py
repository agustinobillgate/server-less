#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def gacct_balance_mi_viewbl(rechnr:int):

    prepare_cache ([Bill])

    a_resnr = 0
    a_rechnr = 0
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_resnr, a_rechnr, bill
        nonlocal rechnr

        return {"a_resnr": a_resnr, "a_rechnr": a_rechnr}


    bill = get_cache (Bill, {"rechnr": [(eq, rechnr)]})
    a_resnr = bill.resnr
    a_rechnr = bill.rechnr

    return generate_output()