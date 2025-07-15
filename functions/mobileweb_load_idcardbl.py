#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestbook

def mobileweb_load_idcardbl(guestno:int):

    prepare_cache ([Guest, Guestbook])

    imagedata = ""
    result_message = ""
    pointer:bytes = None
    guest = guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal imagedata, result_message, pointer, guest, guestbook
        nonlocal guestno

        return {"imagedata": imagedata, "result_message": result_message}


    if guestno == None or guestno == 0:
        result_message = "3 - GuestNumber Can't be Null!"

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, guestno)]})

    if not guest:
        result_message = "2 - Guest Not Found!"

        return generate_output()

    guestbook = get_cache (Guestbook, {"gastnr": [(eq, guest.gastnr)]})

    if not guestbook:
        result_message = "1 - Image ID Card Not exist!"

        return generate_output()
    else:
        pointer = guestbook.imagefile
        imagedata = base64_encode(pointer)
        result_message = "0 - Image ID Card Already Exist!"

    return generate_output()