from functions.additional_functions import *
import decimal
from models import Guest, Guestbook

def mobileweb_load_idcardbl(guestno:int):
    imagedata = ""
    result_message = ""
    pointer:bytes = None
    guest = guestbook = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal imagedata, result_message, pointer, guest, guestbook


        return {"imagedata": imagedata, "result_message": result_message}


    if guestno == None or guestno == 0:
        result_message = "3 - GuestNumber Can't be Null!"

        return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == guestno)).first()

    if not guest:
        result_message = "2 - Guest Not Found!"

        return generate_output()

    guestbook = db_session.query(Guestbook).filter(
            (Guestbook.gastnr == guest.gastnr)).first()

    if not guestbook:
        result_message = "1 - Image ID Card Not exist!"

        return generate_output()
    else:
        pointer = guestbook.imagefile        imagedata = BASE64_ENCODE (pointer)
        result_message = "0 - Image ID Card Already Exist!"

    return generate_output()