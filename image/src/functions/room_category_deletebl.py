from functions.additional_functions import *
import decimal
from models import Zimkateg, Queasy

def room_category_deletebl(pvilanguage:int, number1:int):
    msg_str = ""
    success_flag = False
    lvcarea:str = "room_category_admin"
    zimkateg = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, zimkateg, queasy


        return {"msg_str": msg_str, "success_flag": success_flag}


    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.typ == number1)).first()

    if zimkateg:
        msg_str = msg_str + chr(2) + translateExtended ("Room Type exists, deleting not possible:", lvcarea, "") + " " + zimkateg.kurzbez
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152) &  (Queasy.number1 == number1)).first()
        db_session.delete(queasy)
        success_flag = True

    return generate_output()