from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Zimmer

def check_btn_add_flplanbl(pvilanguage:int, location:int, floor:int, from_room:str, curr_n:int):
    msg_str = ""
    msg_ans = True
    lvcarea:str = "check-btn-add-flplan"
    queasy = zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_ans, lvcarea, queasy, zimmer
        nonlocal pvilanguage, location, floor, from_room, curr_n


        return {"curr_n": curr_n, "msg_str": msg_str, "msg_ans": msg_ans}


    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 25) & (Queasy.number1 == location) & (Queasy.number2 == floor) & (func.lower(Queasy.char1) == (from_room).lower())).first()

    if queasy:
        msg_str = msg_str + chr(2) + translateExtended ("Room already assigned.", lvcarea, "")
        msg_ans = False

        return generate_output()

    zimmer = db_session.query(Zimmer).filter(
             (func.lower(Zimmer.zinr) == (from_room).lower())).first()

    if zimmer.etage != floor:
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("Room is not located on the selected floor.", lvcarea, "")
        msg_ans = True

    if curr_n == 100:
        msg_str = msg_str + chr(2) + translateExtended ("Number rooms of 100 reached.", lvcarea, "")
        msg_ans = False

        return generate_output()
    curr_n = curr_n + 1

    return generate_output()