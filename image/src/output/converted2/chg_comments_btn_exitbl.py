#using conversion tools version: 1.0.0.111

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


    bill = get_cache (Bill, {"_recid": [(eq, bill_recid)]})

    if not bill:

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

    if bill.resnr > 0:

        reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

    if bill.resnr > 0 and bill.reslinnr > 0:

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
    pass
    guest.bemerkung = g_com_screen_value
    pass

    if reservation:
        pass
        reservation.bemerk = res_com_screen_value
        pass

    if res_line:
        pass
        res_line.bemerk = resl_com_screen_value
        pass
    pass
    bill.vesrdepot = bill_com_screen_value
    pass

    return generate_output()