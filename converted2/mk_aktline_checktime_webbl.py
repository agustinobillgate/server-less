#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

def mk_aktline_checktime_webbl(zeit:string, dauer:string):
    akt_line1_zeit = 0
    akt_line1_dauer = 0
    msg_str = ""
    lvcarea:string = "mk-aktline"

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_line1_zeit, akt_line1_dauer, msg_str, lvcarea
        nonlocal zeit, dauer

        return {"zeit": zeit, "dauer": dauer, "akt_line1_zeit": akt_line1_zeit, "akt_line1_dauer": akt_line1_dauer, "msg_str": msg_str}


    if substring(zeit, 0, 2) > ("24").lower()  or substring(zeit, 2, 2) > ("59").lower() :
        msg_str = translateExtended ("Incorrect start time input.", lvcarea, "")
        zeit = "0000"

        return generate_output()

    if substring(dauer, 0, 2) > ("24").lower()  or substring(dauer, 2, 2) > ("59").lower() :
        msg_str = translateExtended ("Incorrect end time input.", lvcarea, "")
        dauer = "0000"

        return generate_output()
    akt_line1_zeit = to_int(substring(zeit, 0, 2)) * 3600 + to_int(substring(zeit, 2, 2)) * 60
    akt_line1_dauer = to_int(substring(dauer, 0, 2)) * 3600 + to_int(substring(dauer, 2, 2)) * 60

    return generate_output()