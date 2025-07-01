#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def mk_aktline_check_okwebbl(aktionscode:int, zeit:int, dauer:int, gastnr:int, kontakt:string):
    msg_str2 = ""
    lvcarea:string = "mk-aktline"

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str2, lvcarea
        nonlocal aktionscode, zeit, dauer, gastnr, kontakt

        return {"msg_str2": msg_str2}


    if aktionscode == 0:
        msg_str2 = "Activity Type not yet defined"

        return generate_output()

    elif zeit == 0:
        msg_str2 = "Start Time not yet defined"

        return generate_output()

    elif dauer == 0:
        msg_str2 = "End Time not yet defined"

        return generate_output()

    elif gastnr == 0:
        msg_str2 = "Company name not yet defined"

        return generate_output()

    elif kontakt == "":
        msg_str2 = "Name Contact not yet defined"

        return generate_output()

    return generate_output()