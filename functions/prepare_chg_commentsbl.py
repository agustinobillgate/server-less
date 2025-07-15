#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Guest, Reservation, Res_line

def prepare_chg_commentsbl(bill_recid:int):

    prepare_cache ([Bill, Guest, Reservation, Res_line])

    rechnr = 0
    res_com = ""
    resl_com = ""
    g_com = ""
    bill_com = ""
    bill_resnr = 0
    bill = guest = reservation = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rechnr, res_com, resl_com, g_com, bill_com, bill_resnr, bill, guest, reservation, res_line
        nonlocal bill_recid

        return {"rechnr": rechnr, "res_com": res_com, "resl_com": resl_com, "g_com": g_com, "bill_com": bill_com, "bill_resnr": bill_resnr}


    bill = get_cache (Bill, {"_recid": [(eq, bill_recid)]})

    if not bill:

        return generate_output()
    rechnr = bill.rechnr

    guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

    if bill.resnr > 0:

        reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
        res_com = reservation.bemerk

    if bill.resnr > 0 and bill.reslinnr > 0:

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        resl_com = res_line.bemerk


    g_com = guest.bemerkung
    bill_com = bill.vesrdepot


    bill_resnr = bill.resnr

    return generate_output()