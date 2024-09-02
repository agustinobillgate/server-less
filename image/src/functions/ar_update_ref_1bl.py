from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Debitor, H_bill, Queasy

def ar_update_ref_1bl(soa_list:[Soa_list], reference:int):
    success_flag = False
    bill = debitor = h_bill = queasy = None

    soa_list = bill1 = debt1 = debt2 = h_bill1 = soa_list1 = soa_list2 = None

    soa_list_list, Soa_list = create_model("Soa_list", {"counter":int, "debref":int, "done_step":int, "artno":int, "vesrdep":decimal, "to_sort":int, "outlet":bool, "datum":date, "ankunft":date, "abreise":date, "gastnr":int, "name":str, "inv_str":str, "rechnr":int, "refno":int, "voucherno":str, "voucherno1":str, "voucherno2":str, "saldo":decimal, "fsaldo":decimal, "printed":bool, "selected":bool, "printdate":date, "dptnr":int, "debt":decimal, "credit":decimal, "fdebt":decimal, "fcredit":decimal, "remarks":str, "arrecid":int, "newpayment":decimal, "newfpayment":decimal, "zinr":str, "erwachs":int, "child1":int, "child2":int, "roomrate":decimal, "tot_amount":decimal, "tot_balance":decimal, "exrate":decimal, "tot_exrate":decimal, "gst_tot_non_taxable":decimal, "gst_amount":decimal, "gst_tot_sales":decimal, "zimmeranz":int, "ar_flag":int, "foreign_exchg":decimal, "resv_name":str}, {"printdate": get_current_date()})

    Bill1 = Bill
    Debt1 = Debitor
    Debt2 = Debitor
    H_bill1 = H_bill
    Soa_list1 = Soa_list
    soa_list1_list = soa_list_list

    Soa_list2 = Soa_list
    soa_list2_list = soa_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill, debitor, h_bill, queasy
        nonlocal bill1, debt1, debt2, h_bill1, soa_list1, soa_list2


        nonlocal soa_list, bill1, debt1, debt2, h_bill1, soa_list1, soa_list2
        nonlocal soa_list_list
        return {"success_flag": success_flag}

    def update_ref():

        nonlocal success_flag, bill, debitor, h_bill, queasy
        nonlocal bill1, debt1, debt2, h_bill1, soa_list1, soa_list2


        nonlocal soa_list, bill1, debt1, debt2, h_bill1, soa_list1, soa_list2
        nonlocal soa_list_list


        Bill1 = Bill
        Debt1 = Debitor
        Debt2 = Debitor
        H_bill1 = H_bill
        Soa_list1 = Soa_list
        Soa_list2 = Soa_list

        for soa_list1 in query(soa_list1_list):

            soa_list = query(soa_list_list, filters=(lambda soa_list :soa_list._recid == soa_list1._recid), first=True)
            soa_list.refno = reference
            soa_list.inv_str = "INV" + to_string(reference, "9999999")

            soa_list = query(soa_list_list, current=True)

            if not soa_list1.outlet:

                bill1 = db_session.query(Bill1).filter(
                        (Bill1.rechnr == soa_list1.rechnr)).first()

                if bill1 and bill1.billref == 0:

                    bill1 = db_session.query(Bill1).first()
                    bill1.billref = reference
                    bill1.logidat = get_current_date()

                    bill1 = db_session.query(Bill1).first()
                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 192
                    queasy.number1 = soa_list1.rechnr
                    queasy.number2 = reference
                    queasy.date1 = get_current_date()

                if soa_list1.counter != 0:

                    for debt1 in db_session.query(Debt1).filter(
                            (Debt1.rechnr == soa_list1.rechnr) &  (Debt1.opart <= 1) &  (Debt1.counter == soa_list1.counter) &  (Debt1.betriebsnr == 0) &  (Debt1.saldo != 0)).all():

                        debt2 = db_session.query(Debt2).filter(
                                (Debt2._recid == debt1._recid)).first()
                        debt2.debref = reference

                        debt2 = db_session.query(Debt2).first()
                else:

                    for debt1 in db_session.query(Debt1).filter(
                            (Debt1.rechnr == soa_list1.rechnr) &  (Debt1.opart <= 1) &  (Debt1.betriebsnr == 0) &  (Debt1.saldo != 0) &  (Debt1._recid == soa_list1.arRecid)).all():

                        debt2 = db_session.query(Debt2).filter(
                                (Debt2._recid == debt1._recid)).first()
                        debt2.debref = reference

                        debt2 = db_session.query(Debt2).first()
                success_flag = True


            else:

                h_bill1 = db_session.query(H_bill1).filter(
                        (H_bill1.rechnr == soa_list1.rechnr) &  (H_bill1.departement == soa_list1.dptnr)).first()
                h_bill1.service[5] = decimal.Decimal(reference)
                h_bill1.service[6] = decimal.Decimal(to_string(get_month(get_current_date()) , "99") + to_string(get_day(get_current_date()) , "99") + to_string(get_year(get_current_date()) , "9999"))

                h_bill1 = db_session.query(H_bill1).first()

                for debt1 in db_session.query(Debt1).filter(
                        (Debt1.rechnr == soa_list1.rechnr) &  (Debt1.opart <= 1) &  (Debt1.betriebsnr > 0)).all():

                    debt2 = db_session.query(Debt2).filter(
                            (Debt2._recid == debt1._recid)).first()
                    debt2.debref = reference

                    debt2 = db_session.query(Debt2).first()
                    success_flag = True


    update_ref()

    return generate_output()