#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Bill, Reservation, Res_line, Debitor, Guest, Htparam

def update_gcfname(gastnr:int):

    prepare_cache ([Bill, Reservation, Res_line, Debitor, Guest])

    bill = reservation = res_line = debitor = guest = htparam = None

    bbill = rsev = rline = bdebt = None

    Bbill = create_buffer("Bbill",Bill)
    Rsev = create_buffer("Rsev",Reservation)
    Rline = create_buffer("Rline",Res_line)
    Bdebt = create_buffer("Bdebt",Debitor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, reservation, res_line, debitor, guest, htparam
        nonlocal gastnr
        nonlocal bbill, rsev, rline, bdebt


        nonlocal bbill, rsev, rline, bdebt

        return {}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    bill = get_cache (Bill, {"gastnr": [(eq, gastnr)]})
    while None != bill:

        bbill = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
        bbill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1


        pass
        pass

        curr_recid = bill._recid
        bill = db_session.query(Bill).filter(
                 (Bill.gastnr == gastnr) & (Bill._recid > curr_recid)).first()

    reservation = get_cache (Reservation, {"gastnr": [(eq, gastnr)],"activeflag": [(eq, 0)]})
    while None != reservation:

        rsev = get_cache (Reservation, {"_recid": [(eq, reservation._recid)]})
        rsev.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1


        pass
        pass

        curr_recid = reservation._recid
        reservation = db_session.query(Reservation).filter(
                 (Reservation.gastnr == gastnr) & (Reservation.activeflag == 0) & (Reservation._recid > curr_recid)).first()

    res_line = get_cache (Res_line, {"gastnrmember": [(eq, gastnr)],"active_flag": [(le, 1)]})
    while None != res_line:

        rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
        rline.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1


        pass
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam and htparam.flogical:

            if res_line.active_flag == 1:
                get_output(intevent_1(1, res_line.zinr, "Change Guestname!", res_line.resnr, res_line.reslinnr))

        curr_recid = res_line._recid
        res_line = db_session.query(Res_line).filter(
                 (Res_line.gastnrmember == gastnr) & (Res_line.active_flag <= 1) & (Res_line._recid > curr_recid)).first()

    debitor = get_cache (Debitor, {"opart": [(le, 1)],"gastnr": [(eq, gastnr)]})
    while None != debitor:

        bdebt = get_cache (Debitor, {"_recid": [(eq, debitor._recid)]})
        bdebt.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1

        bdebt = db_session.query(Bdebt).first()
        pass

        curr_recid = debitor._recid
        debitor = db_session.query(Debitor).filter(
                 (Debitor.opart <= 1) & (Debitor.gastnr == gastnr) & (Debitor._recid > curr_recid)).first()

    return generate_output()