#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimmer

def check_btn_add_flplanbl(pvilanguage:int, location:int, floor:int, from_room:string, curr_n:int):

    prepare_cache ([Zimmer])

    msg_str = ""
    msg_ans = True
    lvcarea:string = "check-btn-add-flplan"
    queasy = zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_ans, lvcarea, queasy, zimmer
        nonlocal pvilanguage, location, floor, from_room, curr_n

        return {"curr_n": curr_n, "msg_str": msg_str, "msg_ans": msg_ans}


    queasy = get_cache (Queasy, {"key": [(eq, 25)],"number1": [(eq, location)],"number2": [(eq, floor)],"char1": [(eq, from_room)]})

    if queasy:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Room already assigned.", lvcarea, "")
        msg_ans = False

        return generate_output()

    zimmer = get_cache (Zimmer, {"zinr": [(eq, from_room)]})

    if zimmer.etage != floor:
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Room is not located on the selected floor.", lvcarea, "")
        msg_ans = True

    if curr_n == 100:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Number rooms of 100 reached.", lvcarea, "")
        msg_ans = False

        return generate_output()
    curr_n = curr_n + 1

    return generate_output()