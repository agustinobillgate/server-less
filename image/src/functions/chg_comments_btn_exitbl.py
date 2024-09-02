from functions.additional_functions import *
import decimal
from models import Bill, Guest, Reservation, Res_line

def chg_comments_btn_exitbl(bill_recid:int, g_com_screen_value:str, res_com_screen_value:str, resl_com_screen_value:str, bill_com_screen_value:str):
    bill = guest = reservation = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, guest, reservation, res_line


        return {}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bill_recid)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill.gastnr)).first()

    if bill.resnr > 0:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == bill.resnr)).first()

    if bill.resnr > 0 and bill.reslinnr > 0:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

    guest = db_session.query(Guest).first()
    guest.bemerk = g_com_screen_value

    guest = db_session.query(Guest).first()

    if reservation:

        reservation = db_session.query(Reservation).first()
        reservation.bemerk = res_com_screen_value

        reservation = db_session.query(Reservation).first()

    if res_line:

        res_line = db_session.query(Res_line).first()
        res_line.bemerk = resl_com_screen_value

        res_line = db_session.query(Res_line).first()

    bill = db_session.query(Bill).first()
    bill.vesrdepot = bill_com_screen_value

    bill = db_session.query(Bill).first()

    return generate_output()