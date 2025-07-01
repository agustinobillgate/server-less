#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line

def prepare_keycardbl(res_number:int, resline_number:int):

    prepare_cache ([Res_line])

    guest_name = ""
    room_number = ""
    checkout_date = None
    gname = ""
    checkout_time = 0
    checkin_date = None
    checkin_time = 0
    res_line = None

    bfr = None

    Bfr = create_buffer("Bfr",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, room_number, checkout_date, gname, checkout_time, checkin_date, checkin_time, res_line
        nonlocal res_number, resline_number
        nonlocal bfr


        nonlocal bfr

        return {"guest_name": guest_name, "room_number": room_number, "checkout_date": checkout_date, "gname": gname, "checkout_time": checkout_time, "checkin_date": checkin_date, "checkin_time": checkin_time}


    res_line = get_cache (Res_line, {"resnr": [(eq, res_number)],"reslinnr": [(eq, resline_number)]})

    if res_line:
        guest_name = res_line.name
        room_number = res_line.zinr
        checkout_date = res_line.abreise
        gname = res_line.name
        checkout_time = res_line.abreisezeit
        checkin_date = res_line.ankunft
        checkin_time = res_line.ankzeit

    return generate_output()