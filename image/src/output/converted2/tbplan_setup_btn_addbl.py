#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Tisch

def tbplan_setup_btn_addbl(curr_n:int, location:int, from_table:int):
    err_flag = 0
    queasy = tisch = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, queasy, tisch
        nonlocal curr_n, location, from_table

        return {"err_flag": err_flag}


    queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, location)],"number2": [(eq, from_table)],"betriebsnr": [(eq, 0)]})

    if queasy:
        err_flag = 1

        return generate_output()

    tisch = get_cache (Tisch, {"departement": [(eq, location)],"tischnr": [(eq, from_table)]})

    if curr_n == 100:
        err_flag = 2

        return generate_output()

    return generate_output()