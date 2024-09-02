from functions.additional_functions import *
import decimal
from models import Res_line, Queasy

def bill_instruct_btn_delbl(pvilanguage:int, number1:int, logi1:bool):
    success_flag = False
    msg_str = ""
    lvcarea:str = "bill_instruct"
    res_line = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, lvcarea, res_line, queasy


        return {"success_flag": success_flag, "msg_str": msg_str}


    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag <= 1) &  (to_int(Res_line.code) == number1)).first()

    if res_line:
        msg_str = msg_str + chr(2) + translateExtended ("Reservation exists for this code, deleting not possible.", lvcarea, "")

        return generate_output()
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 9) &  (Queasy.number1 == number1) &  (Queasy.logi1 == logi1)).first()

        if queasy:
            db_session.delete(queasy)
            success_flag = True

    return generate_output()