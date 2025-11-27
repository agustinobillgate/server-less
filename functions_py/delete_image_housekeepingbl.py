#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guestbook

def delete_image_housekeepingbl(case_type:string, record_key:string, image_nr:int):
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
             (Queasy.key == 195) & (Queasy.char1 == (case_type + ";" + record_key).lower())).with_for_update().order_by(Queasy.number2):
        i = i + 1
        if image_nr == i:
            break

        # merubah logic,  delete queasy dan guestbook terkait, dalam for each loop
        # di .p ada di luar for loop.
        if queasy:

            # guestbook = get_cache (Guestbook, {"gastnr": [(eq, queasy.number1)]})
            guestbook = db_session.query(Guestbook).filter(Guestbook.gastnr == queasy.number1).with_for_update().first()

            if guestbook:
                db_session.delete(guestbook)
            pass
            db_session.delete(queasy)

    return generate_output()