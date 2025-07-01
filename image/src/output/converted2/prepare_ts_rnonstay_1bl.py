#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest, Bill

def prepare_ts_rnonstay_1bl(dept:int):

    prepare_cache ([Htparam, Guest, Bill])

    overcl_flag = False
    mc_flag = False
    cashless_lic = False
    min_saldo = to_decimal("0.0")
    q1_list_list = []
    htparam = guest = bill = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rechnr":int, "resnr":int, "bill_name":string, "name":string, "gastnr":int, "anredefirma":string, "vorname1":string, "saldo":Decimal, "rec_id":int, "guest_rec_id":int, "barcode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal overcl_flag, mc_flag, cashless_lic, min_saldo, q1_list_list, htparam, guest, bill
        nonlocal dept


        nonlocal q1_list
        nonlocal q1_list_list

        return {"overcl_flag": overcl_flag, "mc_flag": mc_flag, "cashless_lic": cashless_lic, "min_saldo": min_saldo, "q1-list": q1_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 247)]})
    overcl_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 586)]})
    min_saldo =  to_decimal(htparam.fdecimal)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1022) & (Htparam.bezeichnung != ("not used").lower()) & (Htparam.flogical)).first()

    if htparam:
        cashless_lic = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 168)]})

    if htparam.bezeichnung.lower()  != ("Not Used").lower() :
        mc_flag = htparam.flogical

    if not mc_flag:

        bill_obj_list = {}
        bill = Bill()
        guest = Guest()
        for bill.rechnr, bill.resnr, bill.name, bill.saldo, bill._recid, bill.vesrdepot2, bill.vesrdepot, guest.name, guest.gastnr, guest.anredefirma, guest.vorname1, guest._recid in db_session.query(Bill.rechnr, Bill.resnr, Bill.name, Bill.saldo, Bill._recid, Bill.vesrdepot2, Bill.vesrdepot, Guest.name, Guest.gastnr, Guest.anredefirma, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Bill.gastnr)).filter(
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
            q1_list.barcode = bill.vesrdepot2

            if bill.vesrdepot != "":
                q1_list.vorname1 = q1_list.vorname1 + ";" + bill.vesrdepot

    return generate_output()