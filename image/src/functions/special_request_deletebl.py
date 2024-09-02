from functions.additional_functions import *
import decimal
from models import Queasy

def special_request_deletebl(number1:int):
    msg_str = ""
    success_flag = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, queasy


        return {"msg_str": msg_str, "success_flag": success_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 189) &  (Queasy.number1 == number1)).first()
    db_session.delete(queasy)
    success_flag = True

    return generate_output()