#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def special_request_deletebl(number1:int):
    msg_str = ""
    success_flag = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, queasy
        nonlocal number1

        return {"msg_str": msg_str, "success_flag": success_flag}


    # queasy = get_cache (Queasy, {"key": [(eq, 189)],"number1": [(eq, number1)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 189) &
             (Queasy.number1 == number1)).with_for_update().first()

    if queasy:
        pass
        db_session.delete(queasy)
        pass
        success_flag = True

    return generate_output()