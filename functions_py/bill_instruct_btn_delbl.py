#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Queasy

def bill_instruct_btn_delbl(pvilanguage:int, number1:int, logi1:bool):
    success_flag = False
    msg_str = ""
    lvcarea:string = "bill-instruct"
    res_line = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, lvcarea, res_line, queasy
        nonlocal pvilanguage, number1, logi1

        return {"success_flag": success_flag, "msg_str": msg_str}


    res_line = db_session.query(Res_line).filter(
             (Res_line.active_flag <= 1) & (to_int(Res_line.code) == number1)).first()

    if res_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists for this code, deleting not possible.", lvcarea, "")

        return generate_output()
    else:

        # queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, number1)],"logi1": [(eq, logi1)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 9) &
                 (Queasy.number1 == number1) &
                 (Queasy.logi1 == logi1)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
            success_flag = True

    return generate_output()