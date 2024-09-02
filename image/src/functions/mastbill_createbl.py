from functions.additional_functions import *
import decimal
from models import Master, Guest, Reservation, Counters, Bill

def mastbill_createbl(resnr:int, curr_segm:int):
    bill_receiver = ""
    t_master_list = []
    t_guest_list = []
    master = guest = reservation = counters = bill = None

    t_master = t_guest = None

    t_master_list, T_master = create_model_like(Master)
    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_receiver, t_master_list, t_guest_list, master, guest, reservation, counters, bill


        nonlocal t_master, t_guest
        nonlocal t_master_list, t_guest_list
        return {"bill_receiver": bill_receiver, "t-master": t_master_list, "t-guest": t_guest_list}


    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    master = db_session.query(Master).filter(
            (Master.resnr == resnr)).first()

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

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == reservation.gastnr)).first()
    bill_receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

    counters = db_session.query(Counters).filter(
            (Counters.counter_no == 3)).first()
    counters = counters + 1

    counters = db_session.query(Counters).first()
    master.rechnr = counters

    bill = db_session.query(Bill).filter(
            (Bill.resnr == resnr) &  (Bill.reslinnr == 0)).first()

    if not bill:
        bill = Bill()
    db_session.add(bill)

    bill.resnr = resnr
    bill.reslinnr = 0
    bill.rgdruck = 1
    billtyp = 2
    bill.rechnr = counters
    bill.gastnr = gastnrpay
    bill.name = bill_receiver
    bill.segmentcode = curr_segm

    bill = db_session.query(Bill).first()

    master = db_session.query(Master).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()
    reservation.verstat = 1

    reservation = db_session.query(Reservation).first()
    t_master = T_master()
    t_master_list.append(t_master)

    buffer_copy(master, t_master)
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    return generate_output()