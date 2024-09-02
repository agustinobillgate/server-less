from functions.additional_functions import *
import decimal
from models import Eg_request, Queasy

def egcategory_btn_delartbl(category_number1:int, rec_id:int):
    er_code = 0
    eg_request = queasy = None

    egreq = queasybuff = None

    Egreq = Eg_request
    Queasybuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal er_code, eg_request, queasy
        nonlocal egreq, queasybuff


        nonlocal egreq, queasybuff
        return {"er_code": er_code}


    queasybuff = db_session.query(Queasybuff).filter(
            (Queasybuff.key == 133) &  (Queasybuff.number2 == category_number1)).first()

    if queasybuff:
        er_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    queasy = db_session.query(Queasy).first()
    db_session.delete(queasy)

    return generate_output()