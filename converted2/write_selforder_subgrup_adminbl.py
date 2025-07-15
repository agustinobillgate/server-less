#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def write_selforder_subgrup_adminbl(dept:int, subgrup_no:int, subgrup:string, maingrup_no:int):

    prepare_cache ([Queasy])

    success_flag = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal dept, subgrup_no, subgrup, maingrup_no

        return {"success_flag": success_flag}


    queasy = get_cache (Queasy, {"key": [(eq, 229)],"number1": [(eq, subgrup_no)],"number2": [(eq, dept)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 229
        queasy.number1 = subgrup_no
        queasy.number2 = dept
        queasy.number3 = maingrup_no
        queasy.char1 = subgrup


        success_flag = True
    else:
        pass
        queasy.number3 = maingrup_no
        success_flag = True


        pass

    return generate_output()