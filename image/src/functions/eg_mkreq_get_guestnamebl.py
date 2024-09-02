from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest

def eg_mkreq_get_guestnamebl(request1_zinr:str, ci_date:date):
    request1_gastnr = 0
    guestname = ""
    request1_resnr = 0
    request1_reslinnr = 0
    res_line = guest = None

    resline1 = guest1 = None

    Resline1 = Res_line
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal request1_gastnr, guestname, request1_resnr, request1_reslinnr, res_line, guest
        nonlocal resline1, guest1


        nonlocal resline1, guest1
        return {"request1_gastnr": request1_gastnr, "guestname": guestname, "request1_resnr": request1_resnr, "request1_reslinnr": request1_reslinnr}

    def get_guestname():

        nonlocal request1_gastnr, guestname, request1_resnr, request1_reslinnr, res_line, guest
        nonlocal resline1, guest1


        nonlocal resline1, guest1


        Resline1 = Res_line
        Guest1 = Guest

        resline1 = db_session.query(Resline1).filter(
                (Resline1.active_flag == 1) &  (func.lower(Resline1.zinr) == (request1_zinr).lower()) &  (Resline1.resstatus != 12) &  (Resline1.ankunft <= ci_date) &  (Resline1.abreise >= ci_date)).first()

        if resline1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == resline1.gastnrmember)).first()

            if guest1:
                request1_gastnr = resline1.gastnrmember
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
                request1_resnr = resline1.resnr
                request1_reslinnr = resline1.reslinnr

    get_guestname()

    return generate_output()