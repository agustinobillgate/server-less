from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Artikel, Debitor, Guest, Bill, Res_line, Res_history

age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":str, "billname":str, "gastnrmember":int, "zinr":str, "datum":date, "rgdatum":date, "paydatum":date, "user_init":str, "bezeich":str, "wabkurz":str, "debt":decimal, "credit":decimal, "fdebt":decimal, "t_debt":decimal, "tot_debt":decimal, "rid":int, "dept":int, "gname":str, "voucher":str, "ankunft":date, "abreise":date, "stay":int, "remarks":str, "ttl":decimal, "resname":str, "comp_name":str, "comp_add":str, "comp_fax":str, "comp_phone":str})

def ar_subledger_update_debt_gastnrbl(age_list_list:[Age_list], t_artnr:int, t_dept:int, gastpay:int, a_gastnr:int, a_rechnr:int, user_init:str):
    billname = ""
    temp_billnr:int = 0
    bediener = artikel = debitor = guest = bill = res_line = res_history = None

    age_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billname, temp_billnr, bediener, artikel, debitor, guest, bill, res_line, res_history
        nonlocal t_artnr, t_dept, gastpay, a_gastnr, a_rechnr, user_init


        nonlocal age_list
        nonlocal age_list_list
        return {"billname": billname}

    def update_debt_gastnr():

        nonlocal billname, temp_billnr, bediener, artikel, debitor, guest, bill, res_line, res_history
        nonlocal t_artnr, t_dept, gastpay, a_gastnr, a_rechnr, user_init


        nonlocal age_list
        nonlocal age_list_list

        debt = None
        gbuff = None
        Debt =  create_buffer("Debt",Debitor)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastpay)).first()

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.rechnr == a_rechnr and age_list.gastnr == a_gastnr)):
            age_list.gastnr = gastpay

            if age_list.billname != "":
                age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.rechnr == a_rechnr) & (Debitor.gastnr == a_gastnr) & (Debitor.artnr == t_artnr) & (Debitor.opart >= 0)).order_by(Debitor._recid).all():

            if debitor.betriebsnr == 0:

                debt = db_session.query(Debt).filter(
                         (Debt._recid == debitor._recid)).first()

                if debt:
                    debt.gastnr = gastpay
                    debt.name = guest.name + ", " + guest.vorname1

                    if debt.zahlkonto == 0:

                        bill = db_session.query(Bill).filter(
                                 (Bill.rechnr == a_rechnr)).first()

                        if bill:
                            bill.name = guest.name + ", " + guest.vorname1
                            bill.gastnr = gastpay
                            temp_billnr = bill.rechnr

                            if bill.resnr > 0 and bill.reslinnr > 0:

                                res_line = db_session.query(Res_line).filter(
                                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                                if res_line:
                                    res_line.gastnrpay = gastpay
            else:

                debt = db_session.query(Debt).filter(
                         (Debt._recid == debitor._recid)).first()

                if debt:
                    debt.gastnr = gastpay
                    debt.name = guest.name + ", " + guest.vorname1

        if gastpay != a_gastnr:
            Gbuff =  create_buffer("Gbuff",Guest)

            gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.gastnr == a_gastnr)).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Bill Receiver Changed"


            res_history.aenderung = gbuff.name + chr(10) + chr(10) + "*** Changed to:" + chr(10) + chr(10) + guest.name + chr(10) + chr(10) + "*** Bill No: " + to_string(temp_billnr)

            if bediener:
                res_history.betriebsnr = bediener.nr
            pass


    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == t_artnr) & (Artikel.departement == t_dept)).first()
    update_debt_gastnr()

    return generate_output()