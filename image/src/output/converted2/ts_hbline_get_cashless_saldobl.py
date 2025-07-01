#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def ts_hbline_get_cashless_saldobl(cashless_code:string):

    prepare_cache ([Bill])

    cashless_saldo = to_decimal("0.0")
    ok_flag = False
    str_code:string = ""
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_saldo, ok_flag, str_code, bill
        nonlocal cashless_code

        return {"cashless_saldo": cashless_saldo, "ok_flag": ok_flag}

    str_code = trim(cashless_code)

    if str_code != "":

        bill = get_cache (Bill, {"flag": [(eq, 0)],"rechnr": [(gt, 0)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"vesrdepot2": [(eq, str_code)]})

        if bill:
            cashless_saldo =  to_decimal(bill.saldo)
            ok_flag = True

    return generate_output()