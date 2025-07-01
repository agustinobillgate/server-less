#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest

def eg_mkreq_get_infoguestbl(request1_zinr:string, ci_date:date):

    prepare_cache ([Res_line, Guest])

    request1_gastnr = 0
    guestname = ""
    str = ""
    res_line = guest = None

    resline1 = guest1 = None

    Resline1 = create_buffer("Resline1",Res_line)
    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal request1_gastnr, guestname, str, res_line, guest
        nonlocal request1_zinr, ci_date
        nonlocal resline1, guest1


        nonlocal resline1, guest1

        return {"request1_gastnr": request1_gastnr, "guestname": guestname, "str": str}


    resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, request1_zinr)],"resstatus": [(ne, 13)],"ankunft": [(le, ci_date)],"abreise": [(ge, ci_date)]})

    if resline1:

        guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

        if guest1:
            request1_gastnr = resline1.gastnrmember
            guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        str = "InHouse Guest : " + guestname + chr_unicode(13) + "Expected Departure " + to_string(resline1.abreise, "99/99/99") + " " + to_string(resline1.abreisezeit , "HH:MM")
    else:

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, request1_zinr)],"resstatus": [(ne, 13)],"ankunft": [(le, ci_date)],"abreise": [(ge, ci_date)]})

        if resline1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

            if guest1:
                request1_gastnr = resline1.gastnrmember
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            str = "Reservation Guest : " + guestname + chr_unicode(13) + "Expected Arrival " + to_string(resline1.ankunft, "99/99/99") + " " + to_string(resline1.ankzeit , "HH:MM")
        else:
            str = "Reservation or Inhouse record not found"

    return generate_output()