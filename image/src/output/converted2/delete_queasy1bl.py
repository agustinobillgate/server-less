from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def delete_queasy1bl(case_type:int, int1:int, int2:int, int3:int, char1:str):
    success_flag = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type, int1, int2, int3, char1


        return {"success_flag": success_flag}


    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == int1) & (Queasy.number1 == int2) & (Queasy.number2 == int3) & (func.lower(Queasy.char1) == (char1).lower())).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True


    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == int1)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True

    return generate_output()