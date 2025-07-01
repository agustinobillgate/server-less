#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest

def eg_mkreq_get_guestnamebl(request1_zinr:string, ci_date:date):

    prepare_cache ([Res_line, Guest])

    request1_gastnr = 0
    guestname = ""
    request1_resnr = 0
    request1_reslinnr = 0
    res_line = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal request1_gastnr, guestname, request1_resnr, request1_reslinnr, res_line, guest
        nonlocal request1_zinr, ci_date

        return {"request1_gastnr": request1_gastnr, "guestname": guestname, "request1_resnr": request1_resnr, "request1_reslinnr": request1_reslinnr}

    def get_guestname():

        nonlocal request1_gastnr, guestname, request1_resnr, request1_reslinnr, res_line, guest
        nonlocal request1_zinr, ci_date

        resline1 = None
        guest1 = None
        Resline1 =  create_buffer("Resline1",Res_line)
        Guest1 =  create_buffer("Guest1",Guest)

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, request1_zinr)],"resstatus": [(ne, 12)],"ankunft": [(le, ci_date)],"abreise": [(ge, ci_date)]})

        if resline1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

            if guest1:
                request1_gastnr = resline1.gastnrmember
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
                request1_resnr = resline1.resnr
                request1_reslinnr = resline1.reslinnr


    get_guestname()

    return generate_output()