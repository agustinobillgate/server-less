from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill

def gcheck_saldo_cashless_webbl(guest_name:str, cashless_code:str):
    cashless_saldo = 0
    str_code:str = ""
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_saldo, str_code, bill


        return {"cashless_saldo": cashless_saldo}

    str_code = trim(cashless_code)

    if str_code == None:
        str_code = ""

    elif guest_name == None:
        guest_name = ""

    if str_code != "":

        bill = db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.rechnr > 0) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (func.lower(Bill.vesrdepot2) == (str_code).lower()) &  (Bill.name.op("~")(".*" + guest_name + ".*"))).first()

        if bill:
            cashless_saldo = bill.saldo

    return generate_output()