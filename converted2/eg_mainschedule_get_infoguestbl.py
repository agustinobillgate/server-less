#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest

def eg_mainschedule_get_infoguestbl(h_zinr:string):

    prepare_cache ([Res_line, Guest])

    str = ""
    guestname:string = ""
    res_line = guest = None

    resline1 = guest1 = None

    Resline1 = create_buffer("Resline1",Res_line)
    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, guestname, res_line, guest
        nonlocal h_zinr
        nonlocal resline1, guest1


        nonlocal resline1, guest1

        return {"str": str}


    resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

    if resline1:

        guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

        if guest1:
            guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        str = "InHouse Guest : " + guestname + chr_unicode(13) + "Expected Departure " + to_string(resline1.abreise, "99/99/99") + " " + to_string(resline1.abreisezeit , "HH:MM")
    else:

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

        if resline1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            str = "Reservation Guest : " + guestname + chr_unicode(13) + "Expected Arrival " + to_string(resline1.ankunft, "99/99/99") + " " + to_string(resline1.ankzeit , "HH:MM")
        else:
            str = "Reservation or Inhouse record not found"

    return generate_output()