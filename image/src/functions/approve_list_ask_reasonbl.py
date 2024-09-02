from functions.additional_functions import *
import decimal
from models import Queasy

def approve_list_ask_reasonbl(pvilanguage:int, trecid:int, user_init:str, reason_str:str, curr_select:str):
    msg_str = ""
    lvcarea:str = "approve_list"
    queasy = None

    qbuff = None

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, queasy
        nonlocal qbuff


        nonlocal qbuff
        return {"msg_str": msg_str}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == trecid)).first()

    if queasy:
        qbuff = Qbuff()
        db_session.add(qbuff)

        buffer_copy(queasy, qbuff)
        qbuff.logi1 = True
        qbuff.betriebsnr = 1
        qbuff.number2 = to_int(queasy._recid)
        qbuff.char2 = qbuff.char2 + ";" + user_init +\
                to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" +\
                to_string((get_year(get_current_date()) - 2000) , "99") + ";" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        qbuff.char3 = reason_str

        if curr_select.lower()  == "approve":
            qbuff.logi2 = True
        else:
            qbuff.logi2 = False

        qbuff = db_session.query(Qbuff).first()


        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)

    else:
        msg_str = msg_str + chr(2) + translateExtended ("The request has been cancelled by user.", lvcarea, "") + chr(10) + translateExtended ("Update no longer possible.", lvcarea, "")

    return generate_output()