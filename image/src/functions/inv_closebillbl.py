from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Res_line, Htparam, Guestat, Bediener, Guest, Akt_cust, Salestat, Interface, Bk_veran, Bk_reser, Bk_func, B_history

def inv_closebillbl(invoice_type:str, s_recid:int, curr_dept:int, transdate:date, user_init:str):
    bill_recid = 0
    bill_date:date = None
    ba_dept:int = 0
    curr_billnr:int = 0
    bill_anzahl:int = 0
    max_anzahl:int = 0
    bill = res_line = htparam = guestat = bediener = guest = akt_cust = salestat = interface = bk_veran = bk_reser = bk_func = b_history = None

    bill1 = usrbuff = rguest = None

    Bill1 = Bill
    Usrbuff = Bediener
    Rguest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest
        return {"bill_recid": bill_recid}

    def close_banquet():

        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest

        ci_date:date = None

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.rechnr == bill.rechnr)).first()

        if not bk_veran:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        bk_veran = db_session.query(Bk_veran).first()
        bk_veran.activeflag = 1

        bk_veran = db_session.query(Bk_veran).first()

        bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.resstatus == 1)).first()
        while None != bk_reser:

            bk_reser = db_session.query(Bk_reser).first()
            bk_reser.resstatus = 8

            bk_reser = db_session.query(Bk_reser).first()

            bk_reser = db_session.query(Bk_reser).filter(
                        (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.resstatus == 1)).first()

        bk_func = db_session.query(Bk_func).filter(
                    (Bk_func.veran_nr == bk_veran.veran_nr) &  (Bk_func.resstatus == 1)).first()
        while None != bk_func:
            create_bahistory()

            bk_func = db_session.query(Bk_func).first()
            bk_func.resstatus = 8
            bk_func.c_resstatus[0] = "I"
            bk_func.r_resstatus[0] = 8

            bk_func = db_session.query(Bk_func).first()

            bk_func = db_session.query(Bk_func).filter(
                        (Bk_func.veran_nr == bk_veran.veran_nr) &  (Bk_func.resstatus == 1)).first()

        if bk_veran.rechnr > 0:

            bill = db_session.query(Bill).first()
            bill.flag = 1
            bill.datum = ci_date
            bill.vesrcod = user_init

            bill = db_session.query(Bill).first()


    def create_bahistory():

        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest


        b_history = B_history()
        db_session.add(b_history)

        buffer_copy(bk_func, b_history)
        b_history.deposit = bk_veran.deposit
        b_history.limit_date = bk_veran.limit_date
        b_history.deposit_payment[0] = bk_veran.deposit_payment[0]
        b_history.deposit_payment[1] = bk_veran.deposit_payment[1]
        b_history.deposit_payment[2] = bk_veran.deposit_payment[2]
        b_history.deposit_payment[3] = bk_veran.deposit_payment[3]
        b_history.deposit_payment[4] = bk_veran.deposit_payment[4]
        b_history.deposit_payment[5] = bk_veran.deposit_payment[5]
        b_history.deposit_payment[6] = bk_veran.deposit_payment[6]
        b_history.deposit_payment[7] = bk_veran.deposit_payment[7]
        b_history.deposit_payment[8] = bk_veran.deposit_payment[8]
        b_history.payment_date[0] = bk_veran.payment_date[0]
        b_history.payment_date[1] = bk_veran.payment_date[1]
        b_history.payment_date[2] = bk_veran.payment_date[2]
        b_history.payment_date[3] = bk_veran.payment_date[3]
        b_history.payment_date[4] = bk_veran.payment_date[4]
        b_history.payment_date[5] = bk_veran.payment_date[5]
        b_history.payment_date[6] = bk_veran.payment_date[6]
        b_history.payment_date[7] = bk_veran.payment_date[7]
        b_history.payment_date[8] = bk_veran.payment_date[8]
        b_history.payment_userinit[0] = bk_veran.payment_userinit[0]
        b_history.payment_userinit[1] = bk_veran.payment_userinit[1]
        b_history.payment_userinit[2] = bk_veran.payment_userinit[2]
        b_history.payment_userinit[3] = bk_veran.payment_userinit[3]
        b_history.payment_userinit[4] = bk_veran.payment_userinit[4]
        b_history.payment_userinit[5] = bk_veran.payment_userinit[5]
        b_history.payment_userinit[6] = bk_veran.payment_userinit[6]
        b_history.payment_userinit[7] = bk_veran.payment_userinit[7]
        b_history.payment_userinit[8] = bk_veran.payment_userinit[8]
        b_history.total_paid = bk_veran.total_paid

        b_history = db_session.query(B_history).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == s_recid)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill.resnr) &  (Res_line.active_flag <= 1)).first()

    if res_line:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 985)).first()

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 900)).first()

        if htparam.finteger != 0:
            ba_dept = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1002)).first()

    if htparam.flogical and invoice_type.lower()  != "guest":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + 1

        guestat = db_session.query(Guestat).filter(
                (Guestat.gastnr == bill.gastnr) &  (Guestat.monat == get_month(bill_date)) &  (Guestat.jahr == get_year(bill_date)) &  (Guestat.betriebsnr == 0)).first()

        if not guestat:
            guestat = Guestat()
            db_session.add(guestat)

            guestat.gastnr = bill.gastnr
            guestat.monat = get_month(bill_date)
            guestat.jahr = get_year(bill_date)


        guestat.logisumsatz = guestat.logisumsatz + bill.logisumsatz
        guestat.argtumsatz = guestat.argtumsatz + bill.argtumsatz
        guestat.f_b_umsatz = guestat.f_b_umsatz + bill.f_b_umsatz
        guestat.sonst_umsatz = guestat.sonst_umsatz + bill.sonst_umsatz
        guestat.gesamtumsatz = guestat.gesamtumsatz + bill.gesamtumsatz

        guestat = db_session.query(Guestat).first()

    if curr_dept == ba_dept and invoice_type.lower()  == "NS":
        close_banquet()

    elif invoice_type.lower()  == "master":

        akt_cust = db_session.query(Akt_cust).filter(
                (Akt_cust.gastnr == bill.gastnr)).first()

        if akt_cust:

            usrbuff = db_session.query(Usrbuff).filter(
                    (Usrbuff.userinit == akt_cust.userinit)).first()

        if not akt_cust or not usrbuff:

            rguest = db_session.query(Rguest).filter(
                    (Rguest.gastnr == bill.gastnr)).first()

            if rguest.phonetik3 != "":

                usrbuff = db_session.query(Usrbuff).filter(
                        (Usrbuff.userinit == rguest.phonetik3)).first()

        if usrbuff:

            salestat = db_session.query(Salestat).filter(
                    (Salestat.bediener_nr == usrbuff.nr) &  (Salestat.jahr == get_year(bill_date)) &  (Salestat.monat == get_month(bill_date))).first()

            if not salestat:
                salestat = Salestat()
                db_session.add(salestat)

                salestat.bediener_nr = usrbuff.nr
                salestat.jahr = get_year(bill_date)
                salestat.monat = get_month(bill_date)


            salestat.logisumsatz = salestat.logisumsatz + bill.logisumsatz
            salestat.argtumsatz = salestat.argtumsatz + bill.argtumsatz
            salestat.f_b_umsatz = salestat.f_b_umsatz + bill.f_b_umsatz
            salestat.sonst_umsatz = salestat.sonst_umsatz + bill.sonst_umsatz
            salestat.gesamtumsatz = salestat.gesamtumsatz + bill.gesamtumsatz

            salestat = db_session.query(Salestat).first()

    if invoice_type.lower()  == "guest":
        curr_billnr = billnr
        bill_anzahl = 0

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.parent_nr != 0) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).all():
            bill_anzahl = bill_anzahl + 1

        if bill_anzahl != curr_billnr:

            bill1 = db_session.query(Bill1).filter(
                    (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.billnr == bill_anzahl) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).first()
            bill1.billnr = curr_billnr

            bill1 = db_session.query(Bill1).first()
        max_anzahl = bill_anzahl + 1

        if max_anzahl < 5:
            max_anzahl = 5

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.parent_nr != 0) &  (Bill1.flag == 1) &  (Bill1.zinr == bill.zinr)).all():
            max_anzahl = max_anzahl + 1

        bill = db_session.query(Bill).first()
        billnr = max_anzahl
        bill.vesrcod = user_init

        bill = db_session.query(Bill).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr) &  (Res_line.zinr == bill.zinr)).first()
        res_line.abreise = bill_date
        res_line.abreisezeit = get_current_time_in_seconds()
        res_line.changed = get_current_date()
        res_line.changed_id = user_init
        res_line.active_flag = 2

        res_line = db_session.query(Res_line).first()

        bill1 = db_session.query(Bill1).filter(
                (Bill1.resnr == bill.resnr) &  (Bill1.parent_nr == bill.parent_nr) &  (Bill1.billnr == 1) &  (Bill1.flag == 0) &  (Bill1.zinr == bill.zinr)).first()
        bill_recid = bill1._recid

    bill = db_session.query(Bill).first()
    bill.flag = 1
    interface = Interface()
    db_session.add(interface)

    interface.key = 38
    interface.action = True
    interface.nebenstelle = ""
    interface.parameters = "close_bill"
    interface.intfield = bill.rechnr
    interface.decfield = billtyp
    interface.int_time = get_current_time_in_seconds()
    interface.intdate = get_current_date()
    interface.resnr = bill.resnr
    interface.reslinnr = bill.reslinnr

    interface = db_session.query(Interface).first()


    bill = db_session.query(Bill).first()

    return generate_output()