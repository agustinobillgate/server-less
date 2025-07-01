#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest, Bill

def prepare_ts_rnonstaybl(dept:int):

    prepare_cache ([Htparam, Guest, Bill])

    overcl_flag = False
    mc_flag = False
    q1_list_list = []
    htparam = guest = bill = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rechnr":int, "resnr":int, "bill_name":string, "name":string, "gastnr":int, "anredefirma":string, "vorname1":string, "saldo":Decimal, "rec_id":int, "guest_rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal overcl_flag, mc_flag, q1_list_list, htparam, guest, bill
        nonlocal dept


        nonlocal q1_list
        nonlocal q1_list_list

        return {"overcl_flag": overcl_flag, "mc_flag": mc_flag, "q1-list": q1_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 247)]})
    overcl_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 168)]})

    if htparam.bezeichnung.lower()  != ("Not Used").lower() :
        mc_flag = htparam.flogical

    if not mc_flag:

        bill_obj_list = {}
        bill = Bill()
        guest = Guest()
        for bill.rechnr, bill.resnr, bill.name, bill.saldo, bill._recid, bill.vesrdepot, guest.name, guest.gastnr, guest.anredefirma, guest.vorname1, guest._recid in db_session.query(Bill.rechnr, Bill.resnr, Bill.name, Bill.saldo, Bill._recid, Bill.vesrdepot, Guest.name, Guest.gastnr, Guest.anredefirma, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Bill.gastnr)).filter(
                 (Bill.flag == 0) & (Bill.resnr == 0) & (Bill.zinr == "") & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.resnr).all():
            if bill_obj_list.get(bill._recid):
                continue
            else:
                bill_obj_list[bill._recid] = True


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.rechnr = bill.rechnr
            q1_list.resnr = bill.resnr
            q1_list.bill_name = bill.name
            q1_list.name = guest.name
            q1_list.gastnr = guest.gastnr
            q1_list.anredefirma = guest.anredefirma
            q1_list.vorname1 = guest.vorname1
            q1_list.saldo =  to_decimal(bill.saldo)
            q1_list.rec_id = bill._recid
            q1_list.guest_rec_id = guest._recid

            if bill.vesrdepot != "":
                q1_list.vorname1 = q1_list.vorname1 + ";" + bill.vesrdepot

    return generate_output()