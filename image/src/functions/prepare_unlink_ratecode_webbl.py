from functions.additional_functions import *
import decimal

def prepare_unlink_ratecode_webbl(tb1_char3:str):
    adjust_combo = ""
    adjust_value = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal adjust_combo, adjust_value


        return {"adjust_combo": adjust_combo, "adjust_value": adjust_value}


    if substring(entry(2, tb1_char3, ";") , 0, 1) == "%":
        adjust_combo = "Using Percentage(%)"
        adjust_value = decimal.Decimal(substring(entry(2, tb1_char3, ";") , 1)) / 100
    else:
        adjust_combo = "Using Amount"
        adjust_value = decimal.Decimal(substring(entry(2, tb1_char3, ";") , 1)) / 100

    return generate_output()