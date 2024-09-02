from functions.additional_functions import *
import decimal
from models import Bill, Guest, Reservation, Res_line

def prepare_chg_commentsbl(bill_recid:int):
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


        return {"rechnr": rechnr, "res_com": res_com, "resl_com": resl_com, "g_com": g_com, "bill_com": bill_com, "bill_resnr": bill_resnr}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bill_recid)).first()
    rechnr = bill.rechnr

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill.gastnr)).first()

    if bill.resnr > 0:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == bill.resnr)).first()
        res_com = reservation.bemerk

    if bill.resnr > 0 and bill.reslinnr > 0:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        resl_com = res_line.bemerk


    g_com = guest.bemerk
    bill_com = bill.vesrdepot


    bill_resnr = bill.resnr

    return generate_output()