from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Res_line

def prepare_messagesbl(gastnr:int, resnr:int, reslinnr:int):
    gname = ""
    arrival = None
    depart = None
    zinr = ""
    pguest = False
    guest = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, arrival, depart, zinr, pguest, guest, res_line


        return {"gname": gname, "arrival": arrival, "depart": depart, "zinr": zinr, "pguest": pguest}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    arrival = res_line.ankunft
    depart = res_line.abreise
    zinr = res_line.zinr

    if res_line.resstatus == 6 or res_line.resstatus == 13:
        pguest = True

    return generate_output()