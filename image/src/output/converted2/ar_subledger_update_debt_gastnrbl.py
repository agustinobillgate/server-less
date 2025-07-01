#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, H_artikel, Artikel, Debitor, Guest, Bill, Res_line, Res_history

age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":string, "billname":string, "gastnrmember":int, "zinr":string, "datum":date, "rgdatum":date, "paydatum":date, "user_init":string, "bezeich":string, "wabkurz":string, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "t_debt":Decimal, "tot_debt":Decimal, "rid":int, "dept":int, "gname":string, "voucher":string, "ankunft":date, "abreise":date, "stay":int, "remarks":string, "ttl":Decimal, "resname":string, "comp_name":string, "comp_add":string, "comp_fax":string, "comp_phone":string})

def ar_subledger_update_debt_gastnrbl(age_list_list:[Age_list], t_artnr:int, t_dept:int, gastpay:int, a_gastnr:int, a_rechnr:int, user_init:string):

    prepare_cache ([Bediener, Debitor, Guest, Bill, Res_line, Res_history])

    billname = ""
    temp_billnr:int = 0
    bediener = h_artikel = artikel = debitor = guest = bill = res_line = res_history = None

    age_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billname, temp_billnr, bediener, h_artikel, artikel, debitor, guest, bill, res_line, res_history
        nonlocal t_artnr, t_dept, gastpay, a_gastnr, a_rechnr, user_init


        nonlocal age_list

        return {"billname": billname}

    def update_debt_gastnr():

        nonlocal billname, temp_billnr, bediener, h_artikel, artikel, debitor, guest, bill, res_line, res_history
        nonlocal t_artnr, t_dept, gastpay, a_gastnr, a_rechnr, user_init


        nonlocal age_list

        debt = None
        gbuff = None
        Debt =  create_buffer("Debt",Debitor)

        guest = get_cache (Guest, {"gastnr": [(eq, gastpay)]})

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.rechnr == a_rechnr and age_list.gastnr == a_gastnr)):
            age_list.gastnr = gastpay

            if age_list.billname != "":
                age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.rechnr == a_rechnr) & (Debitor.gastnr == a_gastnr) & (Debitor.artnr == t_artnr) & (Debitor.opart >= 0)).order_by(Debitor._recid).all():

            if debitor.betriebsnr == 0:

                debt = get_cache (Debitor, {"_recid": [(eq, debitor._recid)]})

                if debt:
                    debt.gastnr = gastpay
                    debt.name = guest.name + ", " + guest.vorname1
                    pass

                    if debt.zahlkonto == 0:

                        bill = get_cache (Bill, {"rechnr": [(eq, a_rechnr)]})

                        if bill:
                            bill.name = guest.name + ", " + guest.vorname1
                            bill.gastnr = gastpay
                            temp_billnr = bill.rechnr


                            pass

                            if bill.resnr > 0 and bill.reslinnr > 0:

                                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                                if res_line:
                                    res_line.gastnrpay = gastpay
                                    pass
            else:

                debt = get_cache (Debitor, {"_recid": [(eq, debitor._recid)]})

                if debt:
                    debt.gastnr = gastpay
                    debt.name = guest.name + ", " + guest.vorname1
                    pass

        if gastpay != a_gastnr:
            Gbuff =  create_buffer("Gbuff",Guest)

            gbuff = get_cache (Guest, {"gastnr": [(eq, a_gastnr)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Bill Receiver Changed"


            res_history.aenderung = gbuff.name + chr_unicode(10) + chr_unicode(10) + "*** Changed to:" + chr_unicode(10) + chr_unicode(10) + guest.name + chr_unicode(10) + chr_unicode(10) + "*** Bill No: " + to_string(temp_billnr)

            if bediener:
                res_history.betriebsnr = bediener.nr
            pass
            pass


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    h_artikel = get_cache (H_artikel, {"artnrfront": [(eq, t_artnr)],"departement": [(eq, t_dept)]})

    if not h_artikel:

        artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, t_dept)]})

    if h_artikel or artikel:
        update_debt_gastnr()

    return generate_output()