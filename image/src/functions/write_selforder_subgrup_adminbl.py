from functions.additional_functions import *
import decimal
from models import Queasy

def write_selforder_subgrup_adminbl(dept:int, subgrup_no:int, subgrup:str, maingrup_no:int):
    success_flag = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        return {"success_flag": success_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 229) &  (Queasy.number1 == subgrup_no) &  (Queasy.number2 == dept)).first()

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

        queasy = db_session.query(Queasy).first()
        queasy.number3 = maingrup_no
        success_flag = True

        queasy = db_session.query(Queasy).first()

    return generate_output()