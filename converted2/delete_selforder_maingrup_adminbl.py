#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def delete_selforder_maingrup_adminbl(maingrp_number1:int):
    int_flag = 0
    success_flag = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal int_flag, success_flag, queasy
        nonlocal maingrp_number1

        return {"int_flag": int_flag, "success_flag": success_flag}


    queasy = get_cache (Queasy, {"key": [(eq, 228)],"number1": [(eq, maingrp_number1)]})

    if queasy:
        db_session.delete(queasy)
        pass
        success_flag = True

    return generate_output()