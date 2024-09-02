from functions.additional_functions import *
import decimal
from models import Res_line, Queasy

def rsvpurpose_admin_btn_delbl(pvilanguage:int, number1:int):
    msg_str = ""
    success_flag = False
    search_str:str = "segm__pur"
    lvcarea:str = "rsvpurpose_admin"
    res_line = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, search_str, lvcarea, res_line, queasy


        return {"msg_str": msg_str, "success_flag": success_flag}

    search_str = "segm__pur" + to_string(number1) + ";"

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag <= 1 AND1 + get_index(Res_line.zimmer_wunsch, search_str) > 0)).first()

    if res_line:
        msg_str = msg_str + chr(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 143) &  (Queasy.number1 == number1)).first()
        db_session.delete(queasy)
        success_flag = True

    return generate_output()