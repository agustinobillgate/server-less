from functions.additional_functions import *
import decimal
from models import Guest, Bill

def fo_invoice_check_zahlungsartbl(bil_recid:int):
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


    bill = db_session.query(Bill).filter(
             (Bill._recid == bil_recid)).first()

    if bill:

        receiver = db_session.query(Receiver).filter(
                 (Receiver.gastnr == bill.gastnr)).first()
        r_zahlungsart = receiver.zahlungsart

    return generate_output()