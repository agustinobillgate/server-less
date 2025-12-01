#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line, Htparam, Guestat, Bediener, Guest, Akt_cust, Salestat, Interface, Bk_veran, Bk_reser, Bk_func, B_history

def inv_closebillbl(invoice_type:string, s_recid:int, curr_dept:int, transdate:date, user_init:string):

    prepare_cache ([Bill, Res_line, Htparam, Guestat, Bediener, Guest, Akt_cust, Salestat, Interface, Bk_veran, B_history])

    bill_recid = 0
    bill_date:date = None
    ba_dept:int = 0
    curr_billnr:int = 0
    bill_anzahl:int = 0
    max_anzahl:int = 0
    bill = res_line = htparam = guestat = bediener = guest = akt_cust = salestat = interface = bk_veran = bk_reser = bk_func = b_history = None

    bill1 = usrbuff = rguest = None

    Bill1 = create_buffer("Bill1",Bill)
    Usrbuff = create_buffer("Usrbuff",Bediener)
    Rguest = create_buffer("Rguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal invoice_type, s_recid, curr_dept, transdate, user_init
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest

        return {"bill_recid": bill_recid}

    def close_banquet():

        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal invoice_type, s_recid, curr_dept, transdate, user_init
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest

        ci_date:date = None

        bk_veran = db_session.query(Bk_veran).filter(Bk_veran.rechnr == bill.rechnr).first()

        if not bk_veran:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        ci_date = htparam.fdate

        db_session.refresh(bk_veran, with_for_update=True)
        bk_veran.activeflag = 1
        

        bk_reser = db_session.query(Bk_reser).filter(Bk_reser.veran_nr == bk_veran.veran_nr, Bk_reser.resstatus == 1).first()

        while bk_reser is not None:
            db_session.refresh(bk_reser, with_for_update=True)
            bk_reser.resstatus = 8
            
            curr_recid = bk_reser._recid
            bk_reser = db_session.query(Bk_reser).filter(
                         (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.resstatus == 1) & (Bk_reser._recid > curr_recid)).first()

        bk_func = db_session.query(Bk_func).filter(Bk_func.veran_nr == bk_veran.veran_nr, Bk_func.resstatus == 1).first()
        
        while bk_func is not None:
            create_bahistory()
            db_session.refresh(bk_func, with_for_update=True)
            bk_func.resstatus = 8
            bk_func.c_resstatus[0] = "I"
            bk_func.r_resstatus[0] = 8

            curr_recid = bk_func._recid
            bk_func = db_session.query(Bk_func).filter(
                         (Bk_func.veran_nr == bk_veran.veran_nr) & (Bk_func.resstatus == 1) & (Bk_func._recid > curr_recid)).first()

        if bk_veran.rechnr > 0:
            db_session.refresh(bill, with_for_update=True)
            bill.flag = 1
            bill.datum = ci_date
            bill.vesrcod = user_init


    def create_bahistory():

        nonlocal bill_recid, bill_date, ba_dept, curr_billnr, bill_anzahl, max_anzahl, bill, res_line, htparam, guestat, bediener, guest, akt_cust, salestat, interface, bk_veran, bk_reser, bk_func, b_history
        nonlocal invoice_type, s_recid, curr_dept, transdate, user_init
        nonlocal bill1, usrbuff, rguest


        nonlocal bill1, usrbuff, rguest


        b_history = B_history()
        db_session.add(b_history)

        buffer_copy(bk_func, b_history)
        b_history.deposit =  to_decimal(bk_veran.deposit)
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
        b_history.total_paid =  to_decimal(bk_veran.total_paid)


        pass
        pass

    bill = db_session.query(Bill).filter(Bill._recid == s_recid).first()

    if not bill:
        return generate_output()

    res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.active_flag <= 1).first()

    if res_line:
        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 985)]})

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

        if htparam.finteger != 0:
            ba_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

    if htparam.flogical and invoice_type.lower()  != ("guest").lower() :

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        guestat = db_session.query(Guestat).filter(
            Guestat.gastnr == bill.gastnr,
            Guestat.monat == get_month(bill_date),
            Guestat.jahr == get_year(bill_date),
            Guestat.betriebsnr == 0
        ).with_for_update().first()

        if not guestat:
            guestat = Guestat()
            db_session.add(guestat)
            guestat.gastnr = bill.gastnr
            guestat.monat = get_month(bill_date)
            guestat.jahr = get_year(bill_date)

        guestat.logisumsatz =  to_decimal(guestat.logisumsatz) + to_decimal(bill.logisumsatz)
        guestat.argtumsatz =  to_decimal(guestat.argtumsatz) + to_decimal(bill.argtumsatz)
        guestat.f_b_umsatz =  to_decimal(guestat.f_b_umsatz) + to_decimal(bill.f_b_umsatz)
        guestat.sonst_umsatz =  to_decimal(guestat.sonst_umsatz) + to_decimal(bill.sonst_umsatz)
        guestat.gesamtumsatz =  to_decimal(guestat.gesamtumsatz) + to_decimal(bill.gesamtumsatz)

    if curr_dept == ba_dept and invoice_type.lower()  == ("NS").lower() :
        close_banquet()

    elif invoice_type.lower()  == ("master").lower() :

        akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, bill.gastnr)]})

        if akt_cust:

            usrbuff = get_cache (Bediener, {"userinit": [(eq, akt_cust.userinit)]})

        if not akt_cust or not usrbuff:

            rguest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

            if rguest.phonetik3 != "":

                usrbuff = get_cache (Bediener, {"userinit": [(eq, rguest.phonetik3)]})

        if usrbuff:
            salestat = db_session.query(Salestat).filter(
                Salestat.bediener_nr == usrbuff.nr,
                Salestat.jahr == get_year(bill_date),
                Salestat.monat == get_month(bill_date)
            ).with_for_update().first()

            if not salestat:
                salestat = Salestat()
                db_session.add(salestat)
                
                salestat.bediener_nr = usrbuff.nr
                salestat.jahr = get_year(bill_date)
                salestat.monat = get_month(bill_date)

            salestat.logisumsatz =  to_decimal(salestat.logisumsatz) + to_decimal(bill.logisumsatz)
            salestat.argtumsatz =  to_decimal(salestat.argtumsatz) + to_decimal(bill.argtumsatz)
            salestat.f_b_umsatz =  to_decimal(salestat.f_b_umsatz) + to_decimal(bill.f_b_umsatz)
            salestat.sonst_umsatz =  to_decimal(salestat.sonst_umsatz) + to_decimal(bill.sonst_umsatz)
            salestat.gesamtumsatz =  to_decimal(salestat.gesamtumsatz) + to_decimal(bill.gesamtumsatz)

    if invoice_type.lower()  == ("guest").lower() :
        curr_billnr = bill.billnr
        bill_anzahl = 0

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.parent_nr != 0) & (Bill1.flag == 0) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
            bill_anzahl = bill_anzahl + 1

        if bill_anzahl != curr_billnr:
            bill1 = db_session.query(Bill).filter(
                Bill.resnr == bill.resnr,
                Bill.parent_nr == bill.parent_nr,
                Bill.billnr == bill_anzahl,
                Bill.flag == 0,
                Bill.zinr == bill.zinr
            ).with_for_update().first()
            bill1.billnr = curr_billnr
            
        max_anzahl = bill_anzahl + 1

        if max_anzahl < 5:
            max_anzahl = 5

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == bill.resnr) & (Bill1.parent_nr == bill.parent_nr) & (Bill1.parent_nr != 0) & (Bill1.flag == 1) & (Bill1.zinr == bill.zinr)).order_by(Bill1._recid).all():
            max_anzahl = max_anzahl + 1
            
        db_session.refresh(bill, with_for_update=True)
        bill.billnr = max_anzahl
        bill.vesrcod = user_init

        res_line = db_session.query(Res_line).filter(
            Res_line.resnr == bill.resnr,
            Res_line.reslinnr == bill.reslinnr,
            Res_line.zinr == bill.zinr
        ).with_for_update().first()
        
        res_line.abreise = bill_date
        res_line.abreisezeit = get_current_time_in_seconds()
        res_line.changed = get_current_date()
        res_line.changed_id = user_init
        res_line.active_flag = 2

        bill1 = get_cache (Bill, {"resnr": [(eq, bill.resnr)],"parent_nr": [(eq, bill.parent_nr)],"billnr": [(eq, 1)],"flag": [(eq, 0)],"zinr": [(eq, bill.zinr)]})
        bill_recid = bill1._recid


    db_session.refresh(bill, with_for_update=True)
    
    bill.flag = 1
    interface = Interface()
    db_session.add(interface)

    interface.key = 38
    interface.action = True
    interface.nebenstelle = ""
    interface.parameters = "close-bill"
    interface.intfield = bill.rechnr
    interface.decfield =  to_decimal(bill.billtyp)
    interface.int_time = get_current_time_in_seconds()
    interface.intdate = get_current_date()
    interface.resnr = bill.resnr
    interface.reslinnr = bill.reslinnr


    return generate_output()