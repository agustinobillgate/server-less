from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill

def ts_hbline_get_cashless_saldobl(cashless_code:str):
    cashless_saldo = 0
    ok_flag = False
    str_code:str = ""
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_saldo, ok_flag, str_code, bill


        return {"cashless_saldo": cashless_saldo, "ok_flag": ok_flag}

    str_code = trim(cashless_code)

    if str_code != "":

        bill = db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.rechnr > 0) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (func.lower(Bill.vesrdepot2) == (str_code).lower())).first()

        if bill:
            cashless_saldo = bill.saldo
            ok_flag = True

    return generate_output()