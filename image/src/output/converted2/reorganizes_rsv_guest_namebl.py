#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest, Reservation

def reorganizes_rsv_guest_namebl():

    prepare_cache ([Guest, Reservation])

    v_success = False
    counter = 0
    gname:string = ""
    res_line = guest = reservation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, counter, gname, res_line, guest, reservation

        return {"v_success": v_success, "counter": counter}


    res_line = get_cache (Res_line, {"resstatus": [(ne, 8),(ne, 9),(ne, 10),(ne, 12),(ne, 99)],"gastnrmember": [(gt, 0)]})
    while None != res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

            if res_line.name.lower()  != (gname).lower() :
                pass
                res_line.name = gname
                pass
                counter = counter + 1

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation:

            if reservation.gastnr != res_line.gastnr:
                pass
                res_line.gastnr = reservation.gastnr
                pass
                counter = counter + 1

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.gastnrmember > 0) & (Res_line._recid > curr_recid)).first()
    pass
    v_success = True

    return generate_output()