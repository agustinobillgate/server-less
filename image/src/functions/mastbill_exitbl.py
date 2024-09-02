from functions.additional_functions import *
import decimal
from models import Master, Reservation, Bill, Counters

def mastbill_exitbl(resnr:int, gastnrpay:int, rechnrstart:int, rechnrend:int, curr_segm:int, master_active:bool, umsatz1:bool, umsatz3:bool, umsatz4:bool, bill_receiver:str):
    master = reservation = bill = counters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal master, reservation, bill, counters


        return {}


    master = db_session.query(Master).filter(
            (Master.resnr == resnr)).first()
    master.ACTIVE = master_active
    master.rechnrstart = rechnrstart
    master.rechnrend = rechnrend
    master.umsatzart[0] = umsatz1
    master.umsatzart[1] = master.umsatzart[0]
    master.umsatzart[2] = umsatz3
    master.umsatzart[3] = umsatz4
    master.gastnrpay = gastnrpay
    master.name = bill_receiver

    master = db_session.query(Master).first()

    if not master.active:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resnr)).first()
        reservation.verstat = 0

        reservation = db_session.query(Reservation).first()
    else:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resnr)).first()
        reservation.verstat = 1

        reservation = db_session.query(Reservation).first()

    bill = db_session.query(Bill).filter(
            (Bill.resnr == resnr) &  (Bill.reslinnr == 0)).first()

    if not bill:
        bill = Bill()
        db_session.add(bill)

        bill.resnr = resnr
        bill.reslinnr = 0
        bill.rgdruck = 1
        billtyp = 2

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1
        bill.rechnr = counters

        counters = db_session.query(Counters).first()

        master = db_session.query(Master).first()
        master.rechnr = bill.rechnr

        master = db_session.query(Master).first()
    bill.gastnr = gastnrpay
    bill.name = bill_receiver
    bill.segmentcode = curr_segm

    bill = db_session.query(Bill).first()

    return generate_output()