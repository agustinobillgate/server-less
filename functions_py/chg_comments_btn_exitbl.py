#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 24-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Guest, Reservation, Res_line

def chg_comments_btn_exitbl(bill_recid:int, g_com_screen_value:string, res_com_screen_value:string, resl_com_screen_value:string, bill_com_screen_value:string):

    prepare_cache ([Bill, Guest, Reservation, Res_line])

    bill = guest = reservation = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, guest, reservation, res_line
        nonlocal bill_recid, g_com_screen_value, res_com_screen_value, resl_com_screen_value, bill_com_screen_value

        return {}


    # bill = get_cache (Bill, {"_recid": [(eq, bill_recid)]})
    bill = db_session.query(Bill).filter(Bill._recid == bill_recid).first()
    if not bill:

        return generate_output()

    # guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
    guest = db_session.query(Guest).filter(Guest.gastnr == bill.gastnr).first()

    if bill.resnr > 0:

        # reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
        reservation = db_session.query(Reservation).filter(Reservation.resnr == bill.resnr).first()

    if bill.resnr > 0 and bill.reslinnr > 0:

        # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
        res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.reslinnr)).first()

        # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        guest = db_session(Guest).filter(Guest.gastnr == res_line.gastnrmember).first()
    pass

    guest = guest.with_for_update().all()
    guest.bemerkung = g_com_screen_value
    # pass

    if reservation:
        reservation = reservation.with_for_update().first()
        # pass
        reservation.bemerk = res_com_screen_value
        # pass

    if res_line:
        # pass
        res_line = res_line.with_for_update().first()
        res_line.bemerk = resl_com_screen_value
        # pass
    # pass
    bill = bill.with_for_update().first()
    bill.vesrdepot = bill_com_screen_value
    # pass

    db_session.commit()

    return generate_output()