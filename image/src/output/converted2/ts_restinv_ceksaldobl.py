#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_ceksaldobl(rechnr:int, dept:int, saldo:int):

    prepare_cache ([H_bill])

    avail_new = False
    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_new, h_bill
        nonlocal rechnr, dept, saldo

        return {"avail_new": avail_new}


    h_bill = get_cache (H_bill, {"rechnr": [(eq, rechnr)],"departement": [(eq, dept)]})

    if h_bill:

        if h_bill.saldo != saldo:
            avail_new = True

        elif h_bill.saldo == saldo:
            avail_new = False

    return generate_output()