from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Guestbook

def delete_image_housekeepingbl(case_type:str, record_key:str, image_nr:int):
    msg_str = ""
    i:int = 0
    pointer:bytes = None
    queasy = guestbook = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, i, pointer, queasy, guestbook
        nonlocal case_type, record_key, image_nr


        return {"msg_str": msg_str}


    if case_type.lower()  != ("OOO").lower()  and case_type.lower()  != ("LostAndFound").lower() :

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 195) & (func.lower(Queasy.char1) == (case_type + ";" + record_key).lower())).order_by(Queasy.number2).all():
        i = i + 1

        if image_nr == i:
            break

    if queasy:

        guestbook = db_session.query(Guestbook).filter(
                 (Guestbook.gastnr == queasy.number1)).first()

        if guestbook:
            db_session.delete(guestbook)
        db_session.delete(queasy)

    return generate_output()