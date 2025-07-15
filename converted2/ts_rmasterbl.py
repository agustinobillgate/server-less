#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Reservation, Master, Guest, Bill

def ts_rmasterbl(h_recid:int):

    prepare_cache ([Reservation, Guest, Bill])

    q1_list_data = []
    h_bill = reservation = master = guest = bill = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"rechnr":int, "gastnr":int, "bill_name":string, "name":string, "anredefirma":string, "groupname":string, "saldo":Decimal, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, h_bill, reservation, master, guest, bill
        nonlocal h_recid


        nonlocal q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    def assign_it():

        nonlocal q1_list_data, h_bill, reservation, master, guest, bill
        nonlocal h_recid


        nonlocal q1_list
        nonlocal q1_list_data


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.rechnr = bill.rechnr
        q1_list.gastnr = bill.gastnr
        q1_list.bill_name = bill.name
        q1_list.name = guest.name
        q1_list.anredefirma = guest.anredefirma
        q1_list.groupname = reservation.groupname
        q1_list.rec_id = bill._recid


    h_bill = get_cache (H_bill, {"_recid": [(eq, h_recid)]})

    bill_obj_list = {}
    for bill, reservation, master, guest in db_session.query(Bill, Reservation, Master, Guest).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Master,(Master.resnr == Bill.resnr) & (Master.active)).join(Guest,(Guest.gastnr == Bill.gastnr)).filter(
             (Bill.flag == 0) & (Bill.zinr == "") & (Bill.resnr > 0) & (Bill.billtyp == 2) & (Bill.reslinnr == 0)).order_by(Bill.name).all():
        if bill_obj_list.get(bill._recid):
            continue
        else:
            bill_obj_list[bill._recid] = True


        assign_it()

    return generate_output()