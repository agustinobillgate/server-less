#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line

def prepare_messagesbl(gastnr:int, resnr:int, reslinnr:int):

    prepare_cache ([Guest, Res_line])

    gname = ""
    arrival = None
    depart = None
    zinr = ""
    pguest = False
    guest = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, arrival, depart, zinr, pguest, guest, res_line
        nonlocal gastnr, resnr, reslinnr

        return {"gname": gname, "arrival": arrival, "depart": depart, "zinr": zinr, "pguest": pguest}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    arrival = res_line.ankunft
    depart = res_line.abreise
    zinr = res_line.zinr

    if res_line.resstatus == 6 or res_line.resstatus == 13:
        pguest = True

    return generate_output()