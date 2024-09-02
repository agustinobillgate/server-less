from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, Guest, Bill

def prepare_ts_rnonstay_1bl(dept:int):
    overcl_flag = False
    mc_flag = False
    cashless_lic = False
    min_saldo = 0
    q1_list_list = []
    htparam = guest = bill = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rechnr":int, "resnr":int, "bill_name":str, "name":str, "gastnr":int, "anredefirma":str, "vorname1":str, "saldo":decimal, "rec_id":int, "guest_rec_id":int, "barcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal overcl_flag, mc_flag, cashless_lic, min_saldo, q1_list_list, htparam, guest, bill


        nonlocal q1_list
        nonlocal q1_list_list
        return {"overcl_flag": overcl_flag, "mc_flag": mc_flag, "cashless_lic": cashless_lic, "min_saldo": min_saldo, "q1-list": q1_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 247)).first()
    overcl_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 586)).first()
    min_saldo = htparam.fdecimal

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022) &  (func.lower(Htparam.bezeich) != "not used") &  (Htparam.flogical)).first()

    if htparam:
        cashless_lic = True

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
            q1_list.barcode = bill.vesrdepot2

            if bill.vesrdepot != "":
                q1_list.vorname1 = q1_list.vorname1 + ";" + bill.vesrdepot

    return generate_output()