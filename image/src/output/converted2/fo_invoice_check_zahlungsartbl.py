#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Bill

def fo_invoice_check_zahlungsartbl(bil_recid:int):

    prepare_cache ([Guest, Bill])

    r_zahlungsart = 0
    guest = bill = None

    receiver = None

    Receiver = create_buffer("Receiver",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_zahlungsart, guest, bill
        nonlocal bil_recid
        nonlocal receiver


        nonlocal receiver

        return {"r_zahlungsart": r_zahlungsart}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill:

        receiver = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
        r_zahlungsart = receiver.zahlungsart

    return generate_output()