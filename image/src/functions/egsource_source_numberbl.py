from functions.additional_functions import *
import decimal
from models import Queasy

def egsource_source_numberbl(curr_select:str, source_number1:int):
    err_code = 0
    queasy = None

    queasy1 = None

    Queasy1 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, queasy
        nonlocal queasy1


        nonlocal queasy1
        return {"err_code": err_code}


    if curr_select.lower()  == "chg":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.number1 == source_number1) &  (Queasy1.number2 == 0) &  (Queasy1.deci2 == 0) &  (Queasy1.key == 130) &  (Queasy1._recid != queasy._recid)).first()

    elif curr_select.lower()  == "add":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.number1 == source_number1) &  (Queasy1.number2 == 0) &  (Queasy1.deci2 == 0) &  (Queasy1.key == 130)).first()

    if queasy1:
        err_code = 1

    return generate_output()