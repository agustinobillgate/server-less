#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fo_invoice_rev_bdownbl import fo_invoice_rev_bdownbl
from models import Bill, Artikel, Htparam, Counters, Res_line, Bill_line, Arrangement, Umsatz, Billjournal, Debitor, Reservation, Guest, Bediener, Argt_line
from functions.next_counter_for_update import next_counter_for_update

def fo_invoice_update_bill2bl(pvilanguage:int, b_rechnr:int, b_artnr:int, bil_flag:int, amount:Decimal, amount_foreign:Decimal, 
                              price_decimal:int, double_currency:bool, foreign_rate:bool, bill_date:date, transdate:date, billart:int, 
                              description:string, qty:int, curr_room:string, user_init:string, artnr:int, price:Decimal, 
                              cancel_str:string, currzeit:int, voucher_nr:string, exchg_rate:Decimal, bil_recid:int, curr_department:int):

    prepare_cache ([Artikel, Htparam, Counters, Res_line, Bill_line, Arrangement, Umsatz, Billjournal, Debitor, Guest, Bediener, Argt_line])

    msg_str = ""
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    cancel_flag = False
    void_approve = False
    flag1 = 0
    flag2 = 0
    flag3 = 0
    rechnr = 0
    t_bill_data = []
    r_recid:int = 0
    na_running:bool = False
    gastnrmember:int = 0
    lvcarea:string = "fo-invoice"
    bill = artikel = htparam = counters = res_line = bill_line = arrangement = umsatz = billjournal = debitor = reservation = guest = bediener = argt_line = None

    t_bill = None

    t_bill_data, T_bill = create_model_like(Bill)

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    description = description.strip()
    curr_room = curr_room.strip()
    user_init = user_init.strip()
    cancel_str = cancel_str.strip()
    voucher_nr = voucher_nr.strip()


    def generate_output():
        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_data, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, htparam, counters, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal pvilanguage, b_rechnr, b_artnr, bil_flag, amount, amount_foreign, price_decimal, double_currency, foreign_rate, bill_date, transdate, billart, description, qty, curr_room, user_init, artnr, price, cancel_str, currzeit, voucher_nr, exchg_rate, bil_recid, curr_department


        nonlocal t_bill
        nonlocal t_bill_data

        return {"msg_str": msg_str, "balance": balance, "balance_foreign": balance_foreign, "cancel_flag": cancel_flag, "void_approve": void_approve, "flag1": flag1, "flag2": flag2, "flag3": flag3, "rechnr": rechnr, "t-bill": t_bill_data}

    def inv_ar(curr_art:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, t_bill_data, r_recid, na_running, lvcarea, bill, artikel, htparam, counters, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal pvilanguage, b_rechnr, b_artnr, bil_flag, amount, amount_foreign, price_decimal, transdate, billart, description, qty, curr_room, user_init, artnr, price, cancel_str, currzeit, exchg_rate, bil_recid, curr_department


        nonlocal t_bill
        nonlocal t_bill_data

        comment:string = ""
        verstat:int = 0
        fsaldo:Decimal = to_decimal("0.0")
        lsaldo:Decimal = to_decimal("0.0")
        foreign_rate:bool = False
        currency_nr:int = 0
        double_currency:bool = False
        debt = None
        debt1 = None
        main_res = None
        resline = None
        bill1 = None
        bline = None
        guest1 = None
        Debt =  create_buffer("Debt",Debitor)
        Debt1 =  create_buffer("Debt1",Debitor)
        Main_res =  create_buffer("Main_res",Reservation)
        Resline =  create_buffer("Resline",Res_line)
        Bill1 =  create_buffer("Bill1",Bill)
        Bline =  create_buffer("Bline",Bill_line)
        Guest1 =  create_buffer("Guest1",Guest)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
        foreign_rate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        double_currency = htparam.flogical

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})

        if not htparam.flogical:

            return

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
        billname = to_string(guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma, "x(36)")

        debt = get_cache (Debitor, {"artnr": [(eq, curr_art)],"rechnr": [(eq, rechnr)],"opart": [(eq, 0)],"rgdatum": [(eq, bill_date)],"counter": [(eq, 0)],"saldo": [(eq, saldo)]})

        if debt:

            # debt1 = get_cache (Debitor, {"_recid": [(eq, debt._recid)]})
            debt1 = db_session.query(Debitor).filter(
                     (Debitor._recid == debt._recid)).with_for_update().first()

            if debt1:
                db_session.delete(debt1)
                pass

                return
            else:
                debt1 = Debitor()
                db_session.add(debt1)

                buffer_copy(debt, debt1)
                debt1.saldo =  - to_decimal(debt1.saldo)
                debt1.bediener_nr = bediener.nr
                debt1.transzeit = get_current_time_in_seconds()


                pass
                pass

                return

        bill1 = db_session.query(Bill1).filter(
                 (Bill1.rechnr == rechnr)).first()

        if bill1 and bill1.resnr != 0:

            resline = get_cache (Res_line, {"resnr": [(eq, bill1.resnr)],"active_flag": [(le, 2)],"resstatus": [(le, 8)],"zipreis": [(ne, 0)]})

            if not resline:

                resline = get_cache (Res_line, {"resnr": [(eq, bill1.resnr)],"active_flag": [(le, 2)],"resstatus": [(le, 8)]})

            if resline:
                currency_nr = resline.betriebsnr

            main_res = db_session.query(Main_res).filter(
                     (Main_res.resnr == bill1.resnr)).first()

            if main_res:
                comment = main_res.groupname

            if comment == "" and gastnrmember != gastnr:

                guest1 = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})

                if guest1:
                    comment = to_string(guest1.name + "," + guest1.vorname1, "x(20)")

                    if resline:
                        comment = comment + " " + to_string(resline.ankunft) + "-" + to_string(resline.abreise)

            if bill1.reslinnr == 0:
                verstat = 1

            if main_res and main_res.insurance:

                resline = get_cache (Res_line, {"resnr": [(eq, main_res.resnr)],"reserve_dec": [(ne, 0),(ne, 1)]})

                if resline:
                    saldo_foreign =  to_decimal(saldo) / to_decimal(resline.reserve_dec)

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
        debitor.saldo =  - to_decimal(saldo)
        debitor.transzeit = get_current_time_in_seconds()
        debitor.rgdatum = bill_date
        debitor.bediener_nr = bediener.nr
        debitor.name = billname
        debitor.verstat = verstat

        if double_currency or foreign_rate:
            debitor.vesrdep =  - to_decimal(saldo_foreign)
        debitor.vesrcod = comment + ";" + voucher_nr + ";"
        pass


    def rev_bdown1(currzeit:int):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_data, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, htparam, counters, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal pvilanguage, b_rechnr, b_artnr, bil_flag, amount, amount_foreign, price_decimal, double_currency, foreign_rate, bill_date, transdate, billart, description, qty, curr_room, user_init, artnr, price, cancel_str, voucher_nr, exchg_rate, bil_recid, curr_department


        nonlocal t_bill
        nonlocal t_bill_data

        artikel1 = None
        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        p_sign:int = 1
        Artikel1 =  create_buffer("Artikel1",Artikel)
        rest_betrag =  to_decimal(amount)

        if qty < 0:
            p_sign = -1

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            if argt_line.betrag != 0:
                argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)

                if double_currency or artikel.pricetab:
                    argt_betrag =  to_decimal(round (argt_betrag) * to_decimal(exchg_rate , price_decimal))
            else:
                argt_betrag =  to_decimal(amount) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                argt_betrag =  to_decimal(round (argt_betrag , price_decimal))
            rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artikel1.artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel1.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag)
            umsatz.anzahl = umsatz.anzahl + qty


            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng =  to_decimal(argt_line.betrag)
            billjournal.betrag =  to_decimal(argt_betrag)
            billjournal.bezeich = artikel1.bezeich
            billjournal.zinr = curr_room
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, arrangement.intervall)]})

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr_room
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if double_currency:
            billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(exchg_rate , 6))
        pass


    def rev_bdown(currzeit:int):

        nonlocal msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_data, r_recid, na_running, gastnrmember, lvcarea, bill, artikel, htparam, counters, res_line, bill_line, arrangement, umsatz, billjournal, debitor, reservation, guest, bediener, argt_line
        nonlocal pvilanguage, b_rechnr, b_artnr, bil_flag, amount, amount_foreign, price_decimal, double_currency, foreign_rate, bill_date, transdate, billart, description, qty, curr_room, user_init, artnr, price, cancel_str, voucher_nr, exchg_rate, bil_recid, curr_department


        nonlocal t_bill
        nonlocal t_bill_data


        balance = get_output(fo_invoice_rev_bdownbl(bil_recid, currzeit, exchg_rate, amount, artikel.artnr, artikel.departement, arrangement.argtnr, price_decimal, bill_date, curr_room, cancel_str, user_init, curr_department, qty, double_currency, foreign_rate, price, balance_foreign))
        flag2 = 1


    artikel = get_cache (Artikel, {"artnr": [(eq, b_artnr)],"departement": [(eq, curr_department)]})

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
    r_recid = bill._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    bill = get_cache (Bill, {"_recid": [(eq, r_recid)]})

    if bill.flag == 1 and bil_flag == 0:
        msg_str = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr_unicode(10) + "Bill entry is no longer possible!"
        pass

        return generate_output()
    else:

        if artikel.umsatzart == 1:
            bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(amount)
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)

        elif artikel.umsatzart == 2:
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)

        elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
            bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(amount)

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        balance =  to_decimal(balance) + to_decimal(amount)
        balance_foreign =  to_decimal(balance_foreign) + to_decimal(amount_foreign)

        if not artikel.autosaldo:
            bill.rgdruck = 0

        elif artikel.artart == 6:
            bill.rgdruck = 0
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)

        if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
            bill.saldo =  to_decimal("0")

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.datum < bill_date or bill.datum == None:
            bill.datum = bill_date

        if bill.rechnr == 0:

            # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
            
            pass

        if rechnr == 0 and bill.rechnr != 0:
            flag1 = 1
            rechnr = bill.rechnr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
        na_running = htparam.flogical

        if transdate != None:
            bill_date = transdate
        else:

            if na_running and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

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
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.zinr = curr_room
        bill_line.departement = artikel.departement
        bill_line.bill_datum = bill_date
        bill_line.zeit = currzeit
        bill_line.userinit = user_init

        if voucher_nr != "":
            bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr

        if artikel.artart == 9:

            arrangement = get_cache (Arrangement, {"argt_artikelnr": [(eq, artikel.artnr)]})

            if arrangement and res_line:
                bill_line.epreis =  to_decimal(res_line.zipreis)

        elif artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
            bill_line.epreis =  to_decimal(price)

        if res_line:
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.arrangement = res_line.arrangement

        if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if arrangement:
                bill_line.bezeich = arrangement.argt_rgbez
        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, billart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = billart
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + qty


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = billart
        billjournal.anzahl = qty
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.betrag =  to_decimal(amount)
        billjournal.bezeich = description
        billjournal.zinr = curr_room
        billjournal.departement = artikel.departement
        billjournal.epreis =  to_decimal(price)
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
        pass

    if artikel.artart == 2 or artikel.artart == 7:
        inv_ar(billart, curr_room, bill.gastnr, gastnrmember, bill.rechnr, amount, amount_foreign, bill_date, bill.name, user_init, voucher_nr)

    if artikel.artart == 9:

        if artikel.artgrp == 0:
            rev_bdown(currzeit)
        else:
            rev_bdown1(currzeit)
    balance =  to_decimal(bill.saldo)

    if double_currency or foreign_rate:
        balance_foreign =  to_decimal(bill.mwst[98])
    flag3 = 1
    pass
    t_bill = T_bill()
    t_bill_data.append(t_bill)

    buffer_copy(bill, t_bill)

    return generate_output()