from functions.additional_functions import *
import decimal
from models import H_bill, Reservation, Master, Guest, Bill

def ts_rmasterbl(h_recid:int):
    q1_list_list = []
    h_bill = reservation = master = guest = bill = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rechnr":int, "gastnr":int, "bill_name":str, "name":str, "anredefirma":str, "groupname":str, "saldo":decimal, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, h_bill, reservation, master, guest, bill


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    def assign_it():

        nonlocal q1_list_list, h_bill, reservation, master, guest, bill


        nonlocal q1_list
        nonlocal q1_list_list


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.rechnr = bill.rechnr
        q1_list.gastnr = bill.gastnr
        q1_list.bill_name = bill.name
        q1_list.name = guest.name
        q1_list.anredefirma = guest.anredefirma
        q1_list.groupname = reservation.groupname
        q1_list.rec_id = bill._recid

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == h_recid)).first()

    bill_obj_list = []
    for bill, reservation, master, guest in db_session.query(Bill, Reservation, Master, Guest).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Master,(Master.resnr == Bill.resnr) &  (Master.active)).join(Guest,(Guest.gastnr == Bill.gastnr)).filter(
            (Bill.flag == 0) &  (Bill.zinr == "") &  (Bill.resnr > 0) &  (Billtyp == 2) &  (Bill.reslinnr == 0)).all():
        if bill._recid in bill_obj_list:
            continue
        else:
            bill_obj_list.append(bill._recid)


        assign_it()

    return generate_output()