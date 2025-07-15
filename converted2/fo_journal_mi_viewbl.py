#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def fo_journal_mi_viewbl(rechnr:int):

    prepare_cache ([Bill])

    bill_resnr = 0
    bill_rechnr = 0
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_resnr, bill_rechnr, bill
        nonlocal rechnr

        return {"bill_resnr": bill_resnr, "bill_rechnr": bill_rechnr}


    bill = get_cache (Bill, {"rechnr": [(eq, rechnr)]})
    bill_resnr = bill.resnr
    bill_rechnr = bill.rechnr

    return generate_output()