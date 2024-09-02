from functions.additional_functions import *
import decimal
from models import Htparam, Guest, Bill

def prepare_ts_rnonstaybl(dept:int):
    overcl_flag = False
    mc_flag = False
    q1_list_list = []
    htparam = guest = bill = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rechnr":int, "resnr":int, "bill_name":str, "name":str, "gastnr":int, "anredefirma":str, "vorname1":str, "saldo":decimal, "rec_id":int, "guest_rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal overcl_flag, mc_flag, q1_list_list, htparam, guest, bill


        nonlocal q1_list
        nonlocal q1_list_list
        return {"overcl_flag": overcl_flag, "mc_flag": mc_flag, "q1-list": q1_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 247)).first()
    overcl_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 168)).first()

    if htparam.bezeich.lower()  != "Not Used":
        mc_flag = htparam.flogical

    if not mc_flag:

        bill_obj_list = []
        for bill, guest in db_session.query(Bill, Guest).join(Guest,(Guest.gastnr == Bill.gastnr)).filter(
                (Bill.flag == 0) &  (Bill.resnr == 0) &  (Bill.zinr == "") &  (Bill.reslinnr == 1) &  (Billtyp == dept)).all():
            if bill._recid in bill_obj_list:
                continue
            else:
                bill_obj_list.append(bill._recid)


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.rechnr = bill.rechnr
            q1_list.resnr = bill.resnr
            q1_list.bill_name = bill.name
            q1_list.name = guest.name
            q1_list.gastnr = guest.gastnr
            q1_list.anredefirma = guest.anredefirma
            q1_list.vorname1 = guest.vorname1
            q1_list.saldo = bill.saldo
            q1_list.rec_id = bill._recid
            q1_list.guest_rec_id = guest._recid

            if bill.vesrdepot != "":
                q1_list.vorname1 = q1_list.vorname1 + ";" + bill.vesrdepot

    return generate_output()