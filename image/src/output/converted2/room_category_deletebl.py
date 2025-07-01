#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy

def room_category_deletebl(pvilanguage:int, number1:int):

    prepare_cache ([Zimkateg])

    msg_str = ""
    success_flag = False
    lvcarea:string = "room-category-admin"
    zimkateg = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, zimkateg, queasy
        nonlocal pvilanguage, number1

        return {"msg_str": msg_str, "success_flag": success_flag}


    zimkateg = get_cache (Zimkateg, {"typ": [(eq, number1)]})

    if zimkateg:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Room Type exists, deleting not possible:", lvcarea, "") + " " + zimkateg.kurzbez
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, number1)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass
            success_flag = True

    return generate_output()