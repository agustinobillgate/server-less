#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Debitor, H_bill, Queasy, Bediener, Res_history

soa_list_data, Soa_list = create_model("Soa_list", {"counter":int, "debref":int, "done_step":int, "artno":int, "vesrdep":Decimal, "to_sort":int, "outlet":bool, "datum":date, "ankunft":date, "abreise":date, "gastnr":int, "name":string, "inv_str":string, "rechnr":int, "refno":int, "voucherno":string, "voucherno1":string, "voucherno2":string, "saldo":Decimal, "fsaldo":Decimal, "printed":bool, "selected":bool, "printdate":date, "dptnr":int, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "fcredit":Decimal, "remarks":string, "arrecid":int, "newpayment":Decimal, "newfpayment":Decimal, "zinr":string, "erwachs":int, "child1":int, "child2":int, "roomrate":Decimal, "tot_amount":Decimal, "tot_balance":Decimal, "exrate":Decimal, "tot_exrate":Decimal, "gst_tot_non_taxable":Decimal, "gst_amount":Decimal, "gst_tot_sales":Decimal, "zimmeranz":int, "ar_flag":int, "foreign_exchg":Decimal, "resv_name":string, "voucher_res_line":string}, {"printdate": get_current_date()})
t_payload_list_data, T_payload_list = create_model("T_payload_list", {"user_init":string})

def ar_update_ref_webbl(soa_list_data:[Soa_list], t_payload_list_data:[T_payload_list], reference:int):

    prepare_cache ([Bill, Debitor, H_bill, Queasy, Bediener, Res_history])

    success_flag = False
    bill = debitor = h_bill = queasy = bediener = res_history = None

    soa_list = t_payload_list = soa_list1 = soa_list2 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill, debitor, h_bill, queasy, bediener, res_history
        nonlocal reference


        nonlocal soa_list, t_payload_list, soa_list1, soa_list2

        return {"success_flag": success_flag}

    def update_ref():

        nonlocal success_flag, bill, debitor, h_bill, queasy, bediener, res_history
        nonlocal reference


        nonlocal soa_list, t_payload_list, soa_list1, soa_list2

        bill1 = None
        debt1 = None
        debt2 = None
        h_bill1 = None
        rechnr_list:string = ""
        Bill1 =  create_buffer("Bill1",Bill)
        Debt1 =  create_buffer("Debt1",Debitor)
        Debt2 =  create_buffer("Debt2",Debitor)
        H_bill1 =  create_buffer("H_bill1",H_bill)
        Soa_list1 = Soa_list
        soa_list1_data = soa_list_data
        Soa_list2 = Soa_list
        soa_list2_data = soa_list_data

        for soa_list in query(soa_list_data):
            soa_list.refno = reference
            soa_list.inv_str = "INV" + to_string(reference, "9999999")
            rechnr_list = rechnr_list + to_string(soa_list.rechnr) + ", "

            if not soa_list.outlet:

                bill1 = db_session.query(Bill1).filter(Bill1.rechnr == soa_list.rechnr).first()

                if bill1 and bill1.billref == 0:
                    db_session.refresh(bill1, with_for_update=True)
                    bill1.billref = reference
                    bill1.logidat = get_current_date()
                    
                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 192
                    queasy.number1 = soa_list.rechnr
                    queasy.number2 = reference
                    queasy.date1 = get_current_date()

                if soa_list.counter != 0:

                    for debt1 in db_session.query(Debt1).filter(
                             (Debt1.rechnr == soa_list.rechnr) & (Debt1.opart <= 1) & (Debt1.counter == soa_list.counter) & (Debt1.betriebsnr == 0) & (Debt1.saldo != 0)).order_by(Debt1._recid).all():

                        debt2 = db_session.query(Debt2).filter(Debt2._recid == debt1._recid).with_for_update().first()
                        debt2.debref = reference
                        
                else:

                    for debt1 in db_session.query(Debt1).filter(
                             (Debt1.rechnr == soa_list.rechnr) & (Debt1.opart <= 1) & (Debt1.betriebsnr == 0) & (Debt1.saldo != 0) & (Debt1._recid == soa_list.arrecid)).order_by(Debt1._recid).all():

                        debt2 = db_session.query(Debt2).filter(Debt2._recid == debt1._recid).with_for_update().first()
                        debt2.debref = reference
                        
                success_flag = True


            else:

                h_bill1 = get_cache (H_bill, {"rechnr": [(eq, soa_list.rechnr)],"departement": [(eq, soa_list.dptnr)]})
                h_bill1.service[5] = to_decimal(reference)
                h_bill1.service[6] = to_decimal(to_string(get_month(get_current_date()) , "99") + to_string(get_day(get_current_date()) , "99") + to_string(get_year(get_current_date()) , "9999"))
                pass

                for debt1 in db_session.query(Debt1).filter(
                         (Debt1.rechnr == soa_list.rechnr) & (Debt1.opart <= 1) & (Debt1.betriebsnr > 0)).order_by(Debt1._recid).all():

                    debt2 = db_session.query(Debt2).filter(Debt2._recid == debt1._recid).with_for_update().first()
                    debt2.debref = reference
                    
                    success_flag = True

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Statement Of Account"
            res_history.aenderung = "Transaction Bill Number " + substring(rechnr_list, 0, length(rechnr_list) - 2) +\
                    " has been printed / has been attached to Invoice NO : " +\
                    to_string(reference, "9999999")

    t_payload_list = query(t_payload_list_data, first=True)
    update_ref()

    return generate_output()