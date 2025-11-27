#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Master, Reservation, Bill, Counters
from sqlalchemy.orm.attributes import flag_modified

def mastbill_exitbl(resnr:int, gastnrpay:int, rechnrstart:int, rechnrend:int, curr_segm:int, master_active:bool, umsatz1:bool, umsatz3:bool, umsatz4:bool, bill_receiver:string):

    prepare_cache ([Master, Reservation, Bill, Counters])

    master = reservation = bill = counters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal master, reservation, bill, counters
        nonlocal resnr, gastnrpay, rechnrstart, rechnrend, curr_segm, master_active, umsatz1, umsatz3, umsatz4, bill_receiver

        return {}


    master = db_session.query(Master).filter(Master.resnr == resnr).with_for_update().first()
    
    if master_active != master.active:
        pass
    
    master.active = master_active
    master.rechnrstart = rechnrstart
    master.rechnrend = rechnrend
    master.umsatzart[0] = umsatz1
    master.umsatzart[1] = master.umsatzart[0]
    master.umsatzart[2] = umsatz3
    master.umsatzart[3] = umsatz4
    master.gastnrpay = gastnrpay
    master.name = bill_receiver

    flag_modified(master, "umsatzart")

    if not master.active:
        reservation = db_session.query(Reservation).filter(Reservation.resnr == resnr).with_for_update().first()
        reservation.verstat = 0

    else:
        reservation = db_session.query(Reservation).filter(Reservation.resnr == resnr).with_for_update().first()
        reservation.verstat = 1

    bill = db_session.query(Bill).filter(Bill.resnr == resnr, Bill.reslinnr == 0).with_for_update().first()
    
    if not bill:
        bill = Bill()
        db_session.add(bill)

        bill.resnr = resnr
        bill.reslinnr = 0
        bill.rgdruck = 1
        bill.billtyp = 2

        counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()

        counters.counter = counters.counter + 1
        bill.rechnr = counters.counter
        
        db_session.refresh(master, with_for_update=True)
        master.rechnr = bill.rechnr

    bill.gastnr = gastnrpay
    bill.name = bill_receiver
    bill.segmentcode = curr_segm
    
    return generate_output()