#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guestbook

def get_image_housekeepingbl(case_type:string, record_key:string, image_nr:int):

    prepare_cache ([Queasy, Guestbook])

    imagedata = ""
    imagedescription = ""
    msg_str = ""
    i:int = 0
    pointer:bytes = None
    queasy = guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal imagedata, imagedescription, msg_str, i, pointer, queasy, guestbook
        nonlocal case_type, record_key, image_nr

        return {"imagedata": imagedata, "imagedescription": imagedescription, "msg_str": msg_str}


    if case_type.lower()  != ("OOO").lower()  and case_type.lower()  != ("LostAndFound").lower() :

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 195) & (Queasy.char1 == (case_type + ";" + record_key).lower())).order_by(Queasy.number2).yield_per(100):
        i = i + 1

        if image_nr == i:
            break

    if queasy:
        imagedescription = queasy.char3

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, queasy.number1)]})

        if guestbook:
            pointer = guestbook.imagefile
            imagedata = base64_encode(pointer)

    return generate_output()