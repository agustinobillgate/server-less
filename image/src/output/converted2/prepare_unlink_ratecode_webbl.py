#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def prepare_unlink_ratecode_webbl(tb1_char3:string):
    adjust_combo = ""
    adjust_value = to_decimal("0.0")

    db_session = local_storage.db_session

    def generate_output():
        nonlocal adjust_combo, adjust_value
        nonlocal tb1_char3

        return {"adjust_combo": adjust_combo, "adjust_value": adjust_value}


    if substring(entry(2, tb1_char3, ";") , 0, 1) == ("%").lower() :
        adjust_combo = "Using Percentage(%)"
        adjust_value = to_decimal(substring(entry(2, tb1_char3, ";") , 1)) / 100
    else:
        adjust_combo = "Using Amount"
        adjust_value = to_decimal(substring(entry(2, tb1_char3, ";") , 1)) / 100

    return generate_output()