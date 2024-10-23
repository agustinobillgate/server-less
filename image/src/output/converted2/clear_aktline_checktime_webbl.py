from functions.additional_functions import *
import decimal

def clear_aktline_checktime_webbl(zeit:str):
    akt_line_zeit = 0
    msg_str = ""
    lvcarea:str = "clear-aktline"


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_line_zeit, msg_str, lvcarea
        nonlocal zeit


        return {"zeit": zeit, "akt_line_zeit": akt_line_zeit, "msg_str": msg_str}


    if substring(zeit, 0, 2) > ("24").lower()  or substring(zeit, 2, 2) > ("59").lower() :
        msg_str = translateExtended ("Incorrect time input.", lvcarea, "")
        zeit = "0000"

        return generate_output()
    akt_line_zeit = to_int(substring(zeit, 0, 2)) * 3600 + to_int(substring(zeit, 2, 2)) * 60

    if akt_line_zeit == 0:
        msg_str = translateExtended ("Incorrect time input.", lvcarea, "")

        return generate_output()