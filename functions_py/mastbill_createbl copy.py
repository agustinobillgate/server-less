#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Master, Guest, Bill, Reservation, Counters

def mastbill_createbl(resnr:int, curr_segm:int):

    prepare_cache ([Reservation, Counters])

    bill_receiver = ""
    t_master_data = []
    t_guest_data = []
    bill_no:int = 0
    master = guest = bill = reservation = counters = None

    t_master = t_guest = buff_bill = None

    t_master_data, T_master = create_model_like(Master)
    t_guest_data, T_guest = create_model_like(Guest)

    Buff_bill = create_buffer("Buff_bill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_receiver, t_master_data, t_guest_data, bill_no, master, guest, bill, reservation, counters
        nonlocal resnr, curr_segm
        nonlocal buff_bill


        nonlocal t_master, t_guest, buff_bill
        nonlocal t_master_data, t_guest_data

        return {"bill_receiver": bill_receiver, "t-master": t_master_data, "t-guest": t_guest_data}


    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    master = get_cache (Master, {"resnr": [(eq, resnr)]})

    if not master:
        master = Master()
        db_session.add(master)

    master.resnr = resnr
    master.gastnr = reservation.gastnr
    master.gastnrpay = reservation.gastnr
    master.active = True
    master.rechnrstart = 1
    master.rechnrend = 1
    master.umsatzart[0] = True
    master.umsatzart[1] = True

    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
    bill_receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

    counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()
    counters.counter = counters.counter + 1
    
    master.rechnr = counters.counter

    bill = db_session.query(Bill).filter(Bill.resnr == resnr, Bill.reslinnr == 0).with_for_update().first()
    if not bill:
        bill = Bill()
        db_session.add(bill)

    bill.resnr = resnr
    bill.reslinnr = 0
    bill.rgdruck = 1
    bill.billtyp = 2
    bill.rechnr = counters.counter
    bill.gastnr = master.gastnrpay
    bill.name = bill_receiver
    bill.segmentcode = curr_segm

    bill_no = bill.rechnr

    reservation = db_session.query(Reservation).filter(Reservation.resnr == resnr).with_for_update().first()
    reservation.verstat = 1

    t_master = T_master()
    t_master_data.append(t_master)

    buffer_copy(master, t_master)
    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)

    buff_bill = db_session.query(Buff_bill).filter(
        Buff_bill.rechnr == bill_no,
        Buff_bill.resnr == 0,
        Buff_bill.reslinnr == 1,
        Buff_bill.billtyp != 2
    ).first()
    
    if buff_bill:
        db_session.refresh(buff_bill, with_for_update=True)
        db_session.delete(buff_bill)

    return generate_output()