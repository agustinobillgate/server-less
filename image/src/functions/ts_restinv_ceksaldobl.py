from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_ceksaldobl(rechnr:int, dept:int, saldo:int):
    avail_new = False
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_new, h_bill


        return {"avail_new": avail_new}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == rechnr) &  (H_bill.departement == dept)).first()

    if h_bill:

        if h_bill.saldo != saldo:
            avail_new = True

        elif h_bill.saldo == saldo:
            avail_new = False

    return generate_output()