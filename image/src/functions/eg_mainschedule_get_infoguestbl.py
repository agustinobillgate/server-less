from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Guest

def eg_mainschedule_get_infoguestbl(h_zinr:str):
    str = ""
    guestname:str = ""
    res_line = guest = None

    resline1 = guest1 = None

    Resline1 = Res_line
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, guestname, res_line, guest
        nonlocal resline1, guest1


        nonlocal resline1, guest1
        return {"str": str}


    resline1 = db_session.query(Resline1).filter(
            (Resline1.active_flag == 1) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

    if resline1:

        guest1 = db_session.query(Guest1).filter(
                (Guest1.gastnr == resline1.gastnrmember)).first()

        if guest1:
            guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        str = "InHouse Guest : " + guestname + chr(13) + "Expected Departure " + to_string(resline1.abreise, "99/99/99") + " " + to_string(resline1.abreisezeit , "HH:MM")
    else:

        resline1 = db_session.query(Resline1).filter(
                (Resline1.active_flag == 0) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

        if resline1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == resline1.gastnrmember)).first()

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            str = "Reservation Guest : " + guestname + chr(13) + "Expected Arrival " + to_string(resline1.ankunft, "99/99/99") + " " + to_string(resline1.ankzeit , "HH:MM")
        else:
            str = "Reservation or Inhouse record not found"

    return generate_output()