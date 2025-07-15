#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guestbook

def upload_image_housekeepingbl(case_type:string, record_key:string, imagedata:string, imagedescription:string):

    prepare_cache ([Queasy, Guestbook])

    msg_str = ""
    i:int = 0
    lastnumber:int = 0
    last_guestbook_nr:int = 0
    pointer:bytes = None
    max_images:int = 0
    queasy = guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, i, lastnumber, last_guestbook_nr, pointer, max_images, queasy, guestbook
        nonlocal case_type, record_key, imagedata, imagedescription

        return {"msg_str": msg_str}

    max_images = 3

    if case_type.lower()  != ("OOO").lower()  and case_type.lower()  != ("LostAndFound").lower() :

        return generate_output()

    if imagedescription == None:
        imagedescription = ""

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 195) & (Queasy.char1 == (case_type + ";" + record_key).lower())).order_by(Queasy.number2).all():
        lastnumber = queasy.number2
        i = i + 1

    if i < max_images:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.char1 = case_type + ";" + record_key
        queasy.char3 = imagedescription
        queasy.key = 195
        queasy.number2 = lastnumber + 1

        guestbook = get_cache (Guestbook, {"gastnr": [(le, -40000000)]})

        if not guestbook:
            guestbook = Guestbook()
            db_session.add(guestbook)

            guestbook.gastnr = -40000000
        else:
            last_guestbook_nr = guestbook.gastnr
            guestbook = Guestbook()
            db_session.add(guestbook)

            guestbook.gastnr = last_guestbook_nr - 1
        pointer = base64_decode(imagedata)
        guestbook.imagefile = pointer
        queasy.number1 = guestbook.gastnr
        pass
        pass
        pass
        pass
    else:
        msg_str = "You are only allowed to upload up to " + to_string(max_images) + " images for each room"

    return generate_output()