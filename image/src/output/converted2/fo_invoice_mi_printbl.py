from functions.additional_functions import *
import decimal
from models import Bill

def fo_invoice_mi_printbl(bil_recid:int):
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill
        nonlocal bil_recid


        return {}


    bill = db_session.query(Bill).filter(
             (Bill._recid == bil_recid)).first()
    bill.rgdruck = 1
    bill.printnr = bill.printnr + 1

    return generate_output()