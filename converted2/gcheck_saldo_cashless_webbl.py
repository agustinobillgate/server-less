#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Bill

def gcheck_saldo_cashless_webbl(guest_name:string, cashless_code:string):

    prepare_cache ([Bill])

    cashless_saldo = to_decimal("0.0")
    str_code:string = ""
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_saldo, str_code, bill
        nonlocal guest_name, cashless_code

        return {"cashless_saldo": cashless_saldo}

    str_code = trim(cashless_code)

    if str_code == None:
        str_code = ""

    elif guest_name == None:
        guest_name = ""

    if str_code != "":

        bill = db_session.query(Bill).filter(
                 (Bill.flag == 0) & (Bill.rechnr > 0) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.vesrdepot2 == (str_code).lower()) & (matches(Bill.name,("*" + guest_name + "*")))).first()

        if bill:
            cashless_saldo =  to_decimal(bill.saldo)

    return generate_output()