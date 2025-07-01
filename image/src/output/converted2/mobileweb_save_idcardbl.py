#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestbook

def mobileweb_save_idcardbl(inp_resnr:int, inp_reslinnr:int, guestno:int, imagedata:string, userinit:string):

    prepare_cache ([Guest, Guestbook])

    result_message = ""
    pointer:bytes = None
    info_str:string = ""
    guest = guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, pointer, info_str, guest, guestbook
        nonlocal inp_resnr, inp_reslinnr, guestno, imagedata, userinit

        return {"result_message": result_message}


    if inp_resnr == None or inp_resnr == 0:
        result_message = "2 - ResNumber Can't be Null!"

        return generate_output()

    if inp_reslinnr == None or inp_reslinnr == 0:
        result_message = "3 - ResLine Number Can't be Null!"

        return generate_output()

    if guestno == None or guestno == 0:
        result_message = "4 - Guest Can't be Null!"

        return generate_output()

    if imagedata == None or imagedata == "":
        result_message = "5 - imagedata Can't be Null!"

        return generate_output()

    if userinit == None or userinit == "":
        result_message = "6 - userinit Can't be Null!"

        return generate_output()
    info_str = "MC;RN" + to_string(inp_resnr) + ";RL" + to_string(inp_reslinnr) + ";GN" + to_string(guestno)

    guest = get_cache (Guest, {"gastnr": [(eq, guestno)]})

    if not guest:
        result_message = "1 - Guest Not Found!"

        return generate_output()

    guestbook = get_cache (Guestbook, {"gastnr": [(eq, guest.gastnr)]})

    if not guestbook:
        guestbook = Guestbook()
        db_session.add(guestbook)

        guestbook.gastnr = guest.gastnr
        guestbook.zeit = get_current_time_in_seconds()
        guestbook.userinit = userinit


    else:
        guestbook.cid = userinit
        guestbook.changed = get_current_date()


    guestbook.reserve_char[0] = to_string(get_current_time_in_seconds(), "99999") +\
            to_string(get_year(get_current_date())) +\
            to_string(get_month(get_current_date()) , "99") +\
            to_string(get_day(get_current_date()) , "99")
    guestbook.infostr = info_str


    pointer = base64_decode(imagedata)
    guestbook.imagefile = pointer
    pass
    pass
    result_message = "0 - Save Image Success"

    return generate_output()