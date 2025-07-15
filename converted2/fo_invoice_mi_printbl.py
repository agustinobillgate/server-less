#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def fo_invoice_mi_printbl(bil_recid:int):

    prepare_cache ([Bill])

    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill
        nonlocal bil_recid

        return {}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill:
        pass
        bill.rgdruck = 1
        bill.printnr = bill.printnr + 1
        pass

    return generate_output()