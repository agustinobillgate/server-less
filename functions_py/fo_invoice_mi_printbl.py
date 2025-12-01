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


    bill = db_session.query(Bill).filter(Bill._recid == bil_recid).first()

    if bill:
        db_session.refresh(bill, with_for_update=True)
        bill.rgdruck = 1
        bill.printnr = bill.printnr + 1

    return generate_output()