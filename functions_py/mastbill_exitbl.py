#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Master, Reservation, Bill, Counters
from functions.next_counter_for_update import next_counter_for_update

def mastbill_exitbl(resnr:int, gastnrpay:int, rechnrstart:int, rechnrend:int, curr_segm:int, master_active:bool, 
                    umsatz1:bool, umsatz3:bool, umsatz4:bool, bill_receiver:string):

    prepare_cache ([Master, Reservation, Bill, Counters])

    master = reservation = bill = counters = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    bill_receiver = bill_receiver.strip()

    def generate_output():
        nonlocal master, reservation, bill, counters
        nonlocal resnr, gastnrpay, rechnrstart, rechnrend, curr_segm, master_active, umsatz1, umsatz3, umsatz4, bill_receiver

        return {}


    master = get_cache (Master, {"resnr": [(eq, resnr)]})

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


    pass

    if not master.active:

        reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
        reservation.verstat = 0
        pass
    else:

        reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
        reservation.verstat = 1
        pass

    bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)]})

    if not bill:
        bill = Bill()
        db_session.add(bill)

        bill.resnr = resnr
        bill.reslinnr = 0
        bill.rgdruck = 1
        bill.billtyp = 2

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        # counters.counter = counters.counter + 1
        # bill.rechnr = counters.counter
        last_count, error_lock = next_counter_for_update(3)
        bill.rechnr = last_count
        
        pass
        master.rechnr = bill.rechnr
        pass
    bill.gastnr = gastnrpay
    bill.name = bill_receiver
    bill.segmentcode = curr_segm


    pass

    return generate_output()