#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def delete_queasy1bl(case_type:int, int1:int, int2:int, int3:int, char1:string):
    success_flag = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type, int1, int2, int3, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, int1)],"number1": [(eq, int2)],"number2": [(eq, int3)],"char1": [(eq, char1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, int1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True

    return generate_output()