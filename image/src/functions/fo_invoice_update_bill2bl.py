from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.fo_invoice_rev_bdownbl import fo_invoice_rev_bdownbl
from models import Bill, Artikel, Counters, Htparam, Res_line, Bill_line, Arrangement, Umsatz, Billjournal, Debitor, Reservation, Guest, Bediener, Argt_line

def fo_invoice_update_bill2bl(pvilanguage:int, b_rechnr:int, b_artnr:int, bil_flag:int, amount:decimal, amount_foreign:decimal, price_decimal:int, double_currency:bool, foreign_rate:bool, bill_date:date, transdate:date, billart:int, description:str, qty:int, curr_room:str, user_init:str, artnr:int, price:decimal, cancel_str:str, currzeit:int, voucher_nr:str, exchg_rate:decimal, bil_recid:int, curr_department:int):
    msg_str = ""
    balance = 0
    balance_foreign = 0
    cancel_flag = False
    void_approve = False
    flag1 = 0
    flag2 = 0
    flag3 = 0
    rechnr = 0
    t_bill_list = []
    r_recid:int = 0
    na_running:bool = False
    gastnrmember:int = 0
    lvcarea:str = "fo_invoice"
    bill = artikel = counters = htparam = res_line = bill_line = arrangement = umsatz = billjournal = debitor = reservation = guest = bediener = argt_line = None

    t_bill = debt = debt1 = main_res = resline = bill1 = bline = guest1 = artikel1 = None

    t_bill_list, T_bill = create_model_like(Bill)

    Debt = Debitor
    Debt1 = Debitor
    Main_res = Reservation
    Resline = Res_line
    Bill1 = Bill
    Bline = Bill_line
    Guest1 = Guest
    Artikel1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_list, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, counters, htparam, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal debt, debt1, main_res, resline, bill1, bline, guest1, artikel1


        nonlocal t_bill, debt, debt1, main_res, resline, bill1, bline, guest1, artikel1
        nonlocal t_bill_list
        return {"msg_str": msg_str, "balance": balance, "balance_foreign": balance_foreign, "cancel_flag": cancel_flag, "void_approve": void_approve, "flag1": flag1, "flag2": flag2, "flag3": flag3, "rechnr": rechnr, "t-bill": t_bill_list}

    def inv_ar(curr_art:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, t_bill_list, r_recid, na_running, lvcarea, bill, artikel, counters, htparam, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal debt, debt1, main_res, resline, bill1, bline, guest1, artikel1


        nonlocal t_bill, debt, debt1, main_res, resline, bill1, bline, guest1, artikel1
        nonlocal t_bill_list

        comment:str = ""
        verstat:int = 0
        fsaldo:decimal = 0
        lsaldo:decimal = 0
        foreign_rate:bool = False
        currency_nr:int = 0
        double_currency:bool = False
        Debt = Debitor
        Debt1 = Debitor
        Main_res = Reservation
        Resline = Res_line
        Bill1 = Bill
        Bline = Bill_line
        Guest1 = Guest

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 143)).first()
        foreign_rate = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()
        double_currency = htparam.flogical

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.(userinit).lower()) == (userinit).lower())).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 997)).first()

        if not htparam.flogical:

            return

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastnr)).first()
        billname = to_string(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma, "x(36)")

        debt = db_session.query(Debt).filter(
                (Debt.artnr == curr_art) &  (Debt.rechnr == rechnr) &  (Debt.opart == 0) &  (Debt.rgdatum == bill_date) &  (Debt.counters == 0) &  (Debt.saldo == saldo)).first()

        if debt:

            debt1 = db_session.query(Debt1).filter(
                    (Debt1._recid == debt._recid)).first()

            if debt1:
                db_session.delete(debt1)


                return
            else:
                debt1 = Debt1()
                db_session.add(debt1)

                buffer_copy(debt, debt1)
                debt1.saldo = - debt1.saldo
                debt1.bediener_nr = bediener.nr
                debt1.transzeit = get_current_time_in_seconds()

                debt1 = db_session.query(Debt1).first()


                return

        bill1 = db_session.query(Bill1).filter(
                (Bill1.rechnr == rechnr)).first()

        if bill1 and bill1.resnr != 0:

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == bill1.resnr) &  (Resline.active_flag <= 2) &  (Resline.resstatus <= 8) &  (Resline.zipreis != 0)).first()

            if not resline:

                resline = db_session.query(Resline).filter(
                        (Resline.resnr == bill1.resnr) &  (Resline.active_flag <= 2) &  (Resline.resstatus <= 8)).first()

            if resline:
                currency_nr = resline.betriebsnr

            main_res = db_session.query(Main_res).filter(
                    (Main_res.resnr == bill1.resnr)).first()

            if main_res:
                comment = main_res.groupname

            if comment == "" and gastnrmember != gastnr:

                guest1 = db_session.query(Guest1).filter(
                        (Guest1.gastnr == gastnrmember)).first()

                if guest1:
                    comment = to_string(guest1.name + "," + guest1.vorname1, "x(20)")

                    if resline:
                        comment = comment + " " + to_string(resline.ankunft) + "-" + to_string(resline.abreise)

            if bill1.reslinnr == 0:
                verstat = 1

            if main_res and main_res.insurance:

                resline = db_session.query(Resline).filter(
                        (Resline.resnr == main_res.resnr) &  (Resline.reserve_dec != 0) &  (Resline.reserve_dec != 1)).first()

                if resline:
                    saldo_foreign = saldo / resline.reserve_dec

        elif bill1 and bill1.resnr == 0:
            comment = bill1.bilname
        debitor = Debitor()
        db_session.add(debitor)

        debitor.artnr = curr_art
        debitor.betrieb_gastmem = currency_nr
        debitor.zinr = zinr
        debitor.gastnr = gastnr
        debitor.gastnrmember = gastnrmember
        debitor.rechnr = rechnr
        debitor.saldo = - saldo
        debitor.transzeit = get_current_time_in_seconds()
        debitor.rgdatum = bill_date
        debitor.bediener_nr = bediener.nr
        debitor.name = billname
        debitor.verstat = verstat

        if double_currency or foreign_rate:
            debitor.vesrdep = - saldo_foreign
        debitor.vesrcod = comment + ";" + voucher_nr + ";"


    def rev_bdown1(currzeit:int):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_list, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, counters, htparam, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal debt, debt1, main_res, resline, bill1, bline, guest1, artikel1


        nonlocal t_bill, debt, debt1, main_res, resline, bill1, bline, guest1, artikel1
        nonlocal t_bill_list

        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
        p_sign:int = 1
        Artikel1 = Artikel
        rest_betrag = amount

        if qty < 0:
            p_sign = -1

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == artikel.artgrp)).first()

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr)).all():

            if argt_line.betrag != 0:
                argt_betrag = argt_line.betrag * qty

                if double_currency or artikel.pricetab:
                    argt_betrag = round (argt_betrag * exchg_rate, price_decimal)
            else:
                argt_betrag = amount * argt_line.vt_percnt / 100
                argt_betrag = round (argt_betrag, price_decimal)
            rest_betrag = rest_betrag - argt_betrag

            artikel1 = db_session.query(Artikel1).filter(
                    (Artikel1.artnr == argt_line.argt_artnr) &  (Artikel1.departement == argt_line.departement)).first()

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artikel1.artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel1.departement


            umsatz.betrag = umsatz.betrag + argt_betrag
            umsatz.anzahl = umsatz.anzahl + qty

            umsatz = db_session.query(Umsatz).first()
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng = argt_line.betrag
            billjournal.betrag = argt_betrag
            billjournal.bezeich = artikel1.bezeich
            billjournal.zinr = curr_room
            billjournal.departement = artikel1.departement
            billjournal.epreis = 0
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            billjournal = db_session.query(Billjournal).first()

        artikel1 = db_session.query(Artikel1).filter(
                (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == arrangement.intervall)).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement


        umsatz.betrag = umsatz.betrag + rest_betrag
        umsatz.anzahl = umsatz.anzahl + qty

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag = rest_betrag
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr_room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if double_currency:
            billjournal.fremdwaehrng = round (rest_betrag / exchg_rate, 6)

        billjournal = db_session.query(Billjournal).first()

    def rev_bdown(currzeit:int):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_list, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, counters, htparam, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal debt, debt1, main_res, resline, bill1, bline, guest1, artikel1


        nonlocal t_bill, debt, debt1, main_res, resline, bill1, bline, guest1, artikel1
        nonlocal t_bill_list


        balance = get_output(fo_invoice_rev_bdownbl(bil_recid, currzeit, exchg_rate, amount, artikel.artnr, artikel.departement, arrangement.argtnr, price_decimal, bill_date, curr_room, cancel_str, user_init, curr_department, qty, double_currency, foreign_rate, price, balance_foreign))
        flag2 = 1

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == b_artnr) &  (Artikel.departement == curr_department)).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()
    r_recid = bill._recid

    bill = db_session.query(Bill).filter(
                (Bill._recid == r_recid)).first()

    if bill.flag == 1 and bil_flag == 0:
        msg_str = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr(10) + "Bill entry is no longer possible!"

        bill = db_session.query(Bill).first()

        return generate_output()
    else:

        if artikel.umsatzart == 1:
            bill.logisumsatz = bill.logisumsatz + amount
            bill.argtumsatz = bill.argtumsatz + amount

        elif artikel.umsatzart == 2:
            bill.argtumsatz = bill.argtumsatz + amount

        elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
            bill.f_b_umsatz = bill.f_b_umsatz + amount

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz = bill.sonst_umsatz + amount

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz = bill.gesamtumsatz + amount
        balance = balance + amount
        balance_foreign = balance_foreign + amount_foreign

        if not artikel.autosaldo:
            bill.rgdruck = 0

        elif artikel.artart == 6:
            bill.rgdruck = 0
        bill.saldo = bill.saldo + amount

        if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
            bill.saldo = 0

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.datum < bill_date or bill.datum == None:
            bill.datum = bill_date

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
            counters = counters + 1
            bill.rechnr = counters

            counters = db_session.query(Counters).first()

        if rechnr == 0 and bill.rechnr != 0:
            flag1 = 1
            rechnr = bill.rechnr

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()
        na_running = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            if na_running and bill_date < get_current_date():
                bill_date = bill_date + 1

        res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

        if res_line:
            gastnrmember = res_line.gastnrmember
        else:
            gastnrmember = bill.gastnr
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = billart
        bill_line.bezeich = description
        bill_line.anzahl = qty
        bill_line.betrag = amount
        bill_line.fremdwbetrag = amount_foreign
        bill_line.zinr = curr_room
        bill_line.departement = artikel.departement
        bill_line.bill_datum = bill_date
        bill_line.zeit = currzeit
        bill_line.userinit = user_init

        if voucher_nr != "":
            bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr

        if artikel.artart == 9:

            arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.argt_artikelnr == artikel.artnr)).first()

            if arrangement and res_line:
                bill_line.epreis = res_line.zipreis

        elif artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
            bill_line.epreis = price

        if res_line:
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.arrangement = res_line.arrangement

        if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

            arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

            if arrangement:
                bill_line.bezeich = arrangement.argt_rgbez

        bill_line = db_session.query(Bill_line).first()

        umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == billart) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = billart
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + qty

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = billart
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = amount_foreign
        billjournal.betrag = amount
        billjournal.bezeich = description
        billjournal.zinr = curr_room
        billjournal.departement = artikel.departement
        billjournal.epreis = price
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        cancel_str = ""
        cancel_flag = False
        void_approve = False

        if res_line:
            billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)

        if voucher_nr != "":
            billjournal.bezeich = billjournal.bezeich + "/" + voucher_nr

        billjournal = db_session.query(Billjournal).first()

    if artikel.artart == 2 or artikel.artart == 7:
        inv_ar(billart, curr_room, bill.gastnr, gastnrmember, bill.rechnr, amount, amount_foreign, bill_date, bill.name, user_init, voucher_nr)

    if artikel.artart == 9:

        if artikel.artgrp == 0:
            rev_bdown(currzeit)
        else:
            rev_bdown1(currzeit)
    balance = bill.saldo

    if double_currency or foreign_rate:
        balance_foreign = bill.mwst[98]
    flag3 = 1

    bill = db_session.query(Bill).first()
    t_bill = T_bill()
    t_bill_list.append(t_bill)

    buffer_copy(bill, t_bill)


    return generate_output()