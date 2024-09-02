from functions.additional_functions import *
import decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from sqlalchemy import func
from models import Bill_line, Res_line, Htparam, Waehrung, Artikel, Bill, Arrangement, Counters, Umsatz, Billjournal, Argt_line, Master, Mast_art, Debitor, Reservation, Guest, Bediener

def inv_update_billbl(pvilanguage:int, bil_flag:int, invoice_type:str, transdate:date, r_recid:int, deptno:int, billart:int, qty:int, price:decimal, amount:decimal, amount_foreign:decimal, description:str, voucher_nr:str, cancel_str:str, user_init:str, billno:int, master_str:str, master_rechnr:str, balance:decimal, balance_foreign:decimal):
    master_flag = False
    msg_str = ""
    success_flag = False
    t_bill_line_list = []
    gastnrmember:int = 0
    price_decimal:int = 0
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:decimal = 1
    currzeit:int = 0
    bill_date:date = None
    curr_room:str = ""
    lvcarea:str = "fo_invoice"
    bill_line = res_line = htparam = waehrung = artikel = bill = arrangement = counters = umsatz = billjournal = argt_line = master = mast_art = debitor = reservation = guest = bediener = None

    t_bill_line = resline = buf_artikel = buf_bill_line = artikel1 = mbill = resline1 = debt = debt1 = main_res = bill1 = bline = guest1 = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})

    Resline = Res_line
    Buf_artikel = Artikel
    Buf_bill_line = Bill_line
    Artikel1 = Artikel
    Mbill = Bill
    Resline1 = Res_line
    Debt = Debitor
    Debt1 = Debitor
    Main_res = Reservation
    Bill1 = Bill
    Bline = Bill_line
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list
        return {"master_flag": master_flag, "msg_str": msg_str, "success_flag": success_flag, "t-bill-line": t_bill_line_list}

    def update_bill():

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

        skip_it:bool = False
        Buf_artikel = Artikel
        Buf_bill_line = Bill_line

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == billart) &  (Artikel.departement == deptno)).first()

        if not artikel:

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == billart) &  (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).first()

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

        if amount_foreign == None:
            amount_foreign = 0

        bill = db_session.query(Bill).filter(
                (Bill._recid == r_recid)).first()

        if bill.flag == 1 and bil_flag == 0:
            msg_str = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr(10) + translateExtended ("Bill entry is no longer possible!", lvcarea, "")
            success_flag = False

            return

        if artikel.artart == 9 and artikel.artgrp == 0:
            skip_it = True

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            buf_artikel = db_session.query(Buf_artikel).filter(
                    (Buf_artikel.artnr == arrangement.argt_artikelnr) &  (Buf_artikel.departement == 0)).first()

            buf_bill_line = db_session.query(Buf_bill_line).filter(
                    (Buf_bill_line.departement == 0) &  (Buf_bill_line.artnr == buf_artikel.artnr) &  (Buf_bill_line.bill_datum == bill_date) &  (Buf_bill_line.zinr != "") &  (Buf_bill_line.massnr == res_line.resnr) &  (Buf_bill_line.billin_nr == res_line.reslinnr)).first()
            skip_it = None != buf_bill_line

            if skip_it:
                success_flag = False
                msg_str = translateExtended ("Not possible", lvcarea, "") + chr(10) + translateExtended ("room Charge Already Posted", lvcarea, "") + " to bill no " + to_string(buf_bill_line.rechnr)

                return

        bill = db_session.query(Bill).first()
        curr_room = bill.zinr
        gastnrmember = bill.gastnr

        if invoice_type.lower()  == "guest":

            if bill.flag == 0:
                master_flag = update_masterbill(currzeit)

            if master_flag:

                return

            res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

            if res_line:
                gastnrmember = res_line.gastnrmember

        if artikel.umsatzart == 1:
            bill.logisumsatz = bill.logisumsatz + amount

        elif artikel.umsatzart == 2:
            bill.argtumsatz = bill.argtumsatz + amount

        elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
            bill.f_b_umsatz = bill.f_b_umsatz + amount

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz = bill.sonst_umsatz + amount

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz = bill.gesamtumsatz + amount

        if not artikel.autosaldo:
            bill.rgdruck = 0

        if bill.datum < bill_date or bill.datum == None:
            bill.datum = bill_date
        bill.saldo = bill.saldo + amount

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
            counters = counters + 1
            bill.rechnr = counters

            if transdate != None:
                bill.datum = transdate

            counters = db_session.query(Counters).first()
        billno = bill.rechnr


        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.massnr = bill.resnr
        bill_line.billin_nr = bill.reslinnr
        bill_line.zinr = curr_room
        bill_line.artnr = billart
        bill_line.anzahl = qty
        bill_line.betrag = amount
        bill_line.fremdwbetrag = amount_foreign
        bill_line.bezeich = description
        bill_line.departement = artikel.departement
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        if voucher_nr != "":
            bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr

        if artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
            bill_line.epreis = price

        if artikel.artart == 9:

            arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.argt_artikelnr == artikel.artnr)).first()

            if arrangement and res_line:
                bill_line.epreis = res_line.zipreis

        if res_line:
            bill_line.massnr = res_line.resnr
            bill_line.billin_nr = res_line.reslinnr
            bill_line.arrangement = res_line.arrangement

        if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

            arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()
            bill_line.bezeich = arrangement.argt_rgbez

        bill_line = db_session.query(Bill_line).first()
        t_bill_line = T_bill_line()
        t_bill_line_list.append(t_bill_line)

        buffer_copy(bill_line, t_bill_line)
        t_bill_line.artart = artikel.artart
        t_bill_line.bl_recid = to_int(bill_line._recid)

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
        billjournal.zinr = curr_room
        billjournal.artnr = billart
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = amount_foreign
        billjournal.betrag = amount
        billjournal.bezeich = description
        billjournal.departement = artikel.departement
        billjournal.epreis = price
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if voucher_nr != "":
            billjournal.bezeich = billjournal.bezeich + "/" + voucher_nr

        billjournal = db_session.query(Billjournal).first()

        if artikel.artart == 2 or artikel.artart == 7:

            if invoice_type.lower()  == "master":

                resline = db_session.query(Resline).filter(
                            (Resline.resnr == bill.resnr) &  ((Resline.resstatus == 6) |  (Resline.resstatus == 8))).first()

                if resline:
                    gastnrmember = resline.gastnrmember
            inv_ar(billart, "", bill.gastnr, gastnrmember, bill.rechnr, amount, amount_foreign, bill_date, bill.name, user_init, voucher_nr, deptno)

        elif artikel.artart == 9:

            if artikel.artgrp == 0:
                rev_bdown(currzeit)
            else:
                rev_bdown1(currzeit)
        balance = bill.saldo

        if double_currency or foreign_rate:
            balance_foreign = bill.mwst[98]

        bill = db_session.query(Bill).first()


    def rev_bdown(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

        service:decimal = 0
        vat:decimal = 0
        service_foreign:decimal = 0
        vat_foreign:decimal = 0
        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
        frate:decimal = 0
        ex_rate:decimal = 0
        p_sign:int = 1
        qty1:int = 0
        rm_vat:bool = False
        rm_serv:bool = False
        Artikel1 = Artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 127)).first()
        rm_vat = not htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 128)).first()
        rm_serv = not htparam.flogical

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line:

            if res_line.adrflag:
                frate = 1

            elif res_line.reserve_dec != 0:
                frate = res_line.reserve_dec
        else:
            frate = exchg_rate
        rest_betrag = amount

        if amount < 0:
            p_sign = -1

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():
            argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag = round (argt_betrag * ex_rate, price_decimal)
            rest_betrag = rest_betrag - argt_betrag * p_sign

            if argt_betrag != 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

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


                umsatz.betrag = umsatz.betrag + argt_betrag * p_sign
                umsatz.anzahl = umsatz.anzahl + qty1

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng = argt_line.betrag * p_sign
                billjournal.betrag = argt_betrag * p_sign
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
                (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == 0)).first()

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

        if rm_serv and artikel.service_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                service = htparam.fdecimal

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 133)).first()

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == 0)).first()
                service = service * price / 100
                service_foreign = round (service, 2) * qty

                if double_currency:
                    service = round (service * exchg_rate, price_decimal) * qty
                else:
                    service = round (service, price_decimal) * qty

                if artikel1.umsatzart == 1:
                    bill.logisumsatz = bill.logisumsatz + service
                    bill.argtumsatz = bill.argtumsatz + service

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz = bill.argtumsatz + service

                elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                    bill.f_b_umsatz = bill.f_b_umsatz + service

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz = bill.sonst_umsatz + service

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz = bill.gesamtumsatz + service
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag = service_foreign
                bill_line.betrag = service
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date

                if res_line:
                    bill_line.arrangement = res_line.arrangement

                bill_line = db_session.query(Bill_line).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement


                umsatz.betrag = umsatz.betrag + service
                umsatz.anzahl = umsatz.anzahl + qty

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng = service_foreign
                billjournal.betrag = service
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()

        if rm_vat and artikel.mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat = htparam.fdecimal

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 132)).first()

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == 0)).first()

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat = vat * (price + service_foreign / qty) / 100
                else:
                    vat = vat * price / 100
                vat_foreign = round (vat, 2) * qty

                if double_currency:
                    vat = round (vat * exchg_rate, price_decimal) * qty
                else:
                    vat = round (vat, price_decimal) * qty

                if artikel1.umsatzart == 1:
                    bill.logisumsatz = bill.logisumsatz + vat
                    bill.argtumsatz = bill.argtumsatz + vat

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz = bill.argtumsatz + vat

                elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                    bill.f_b_umsatz = bill.f_b_umsatz + vat

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz = bill.sonst_umsatz + vat

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz = bill.gesamtumsatz + vat
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag = vat_foreign
                bill_line.betrag = vat
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date

                if res_line:
                    bill_line.arrangement = res_line.arrangement

                bill_line = db_session.query(Bill_line).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement


                umsatz.betrag = umsatz.betrag + vat
                umsatz.anzahl = umsatz.anzahl + qty

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng = vat_foreign
                billjournal.betrag = vat
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()
        bill.saldo = bill.saldo + vat + service

        if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
            bill.saldo = 0

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign
        balance = bill.saldo

        if double_currency or foreign_rate:
            balance_foreign = bill.mwst[98]

    def rev_bdown1(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
        p_qty:int = 0
        Artikel1 = Artikel
        rest_betrag = amount

        if amount > 0:

            if qty > 0:
                p_qty = qty
            else:
                p_qty = - qty

        elif amount < 0:

            if qty < 0:
                p_qty = qty
            else:
                p_qty = - qty

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == artikel.artgrp)).first()

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr)).all():

            if argt_line.betrag != 0:
                argt_betrag = argt_line.betrag * p_qty

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
            billjournal.zinr = curr_room
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng = argt_line.betrag
            billjournal.betrag = argt_betrag
            billjournal.bezeich = artikel1.bezeich
            billjournal.departement = artikel1.departement
            billjournal.epreis = 0
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            billjournal = db_session.query(Billjournal).first()

        if rest_betrag != 0:

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
            billjournal.zinr = curr_room
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.betrag = rest_betrag
            billjournal.bezeich = artikel1.bezeich
            billjournal.departement = artikel1.departement
            billjournal.epreis = 0
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if double_currency:
                billjournal.fremdwaehrng = round (rest_betrag / exchg_rate, 6)

            billjournal = db_session.query(Billjournal).first()

    def update_masterbill(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

        master_flag = False
        room:str = ""
        transfer_case:int = 0
        na_running:bool = False
        transf_rm:str = ""
        mess_str:str = ""

        def generate_inner_output():
            return master_flag
        Mbill = Bill
        Resline = Res_line
        Resline1 = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()
        na_running = htparam.flogical

        if na_running and bill_date == fdate:
            bill_date = bill_date + 1

        resline = db_session.query(Resline).filter(
                (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.parent_nr)).first()

        if resline and resline.l_zuordnung[4] != 0:

            master = db_session.query(Master).filter(
                    (Master.resnr == resline.l_zuordnung[4]) &  (Master.active) &  (Master.flag == 0)).first()
        else:

            master = db_session.query(Master).filter(
                    (Master.resnr == bill.resnr) &  (Master.active) &  (Master.flag == 0)).first()

        if master:
            transfer_case = 1

            if (master.umsatzart[0]  and artikel.artart == 8) or (master.umsatzart[1]  and artikel.artart == 9 and artikel.artgrp == 0) or (master.umsatzart[2]  and artikel.umsatzart == 3) or (master.umsatzart[3]  and artikel.umsatzart == 4):
                master_flag = True

            if not master_flag:

                mast_art = db_session.query(Mast_art).filter(
                        (Mast_art.resnr == master.resnr) &  (Mast_art.departement == artikel.departement) &  (Mast_art.artnr == artikel.artnr)).first()

                if mast_art:
                    master_flag = True

        resline = db_session.query(Resline).filter(
                (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.reslinnr)).first()

        if resline and resline.l_zuordnung[1] != 0:
            master_flag = False

        if not master_flag:
            transf_rm = entry(0, resline.memozinr, ";")

            if resline and transf_rm != "" and (transf_rm != resline.zinr):

                resline1 = db_session.query(Resline1).filter(
                        (func.lower(Resline1.zinr) == (transf_rm).lower()) &  (Resline1.resstatus == 6)).first()

                if resline1:
                    master_flag = True
                    transfer_case = 2

        if master_flag:

            if transfer_case == 1:

                mbill = db_session.query(Mbill).filter(
                        (Mbill.resnr == master.resnr) &  (Mbill.reslinnr == 0)).first()
            else:

                mbill = db_session.query(Mbill).filter(
                        (Mbill.resnr == resline1.resnr) &  (Mbill.reslinnr == resline1.reslinnr) &  (Mbillnr == 1)).first()

            if artikel.umsatzart == 1:
                mbill.logisumsatz = mbill.logisumsatz + amount

            elif artikel.umsatzart == 2:
                mbill.argtumsatz = mbill.argtumsatz + amount

            elif artikel.umsatzart == 3:
                mbill.f_b_umsatz = mbill.f_b_umsatz + amount

            elif artikel.umsatzart == 4:
                mbill.sonst_umsatz = mbill.sonst_umsatz + amount

            if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                mbill.gesamtumsatz = mbill.gesamtumsatz + amount
            mbill.rgdruck = 0
            mbill.saldo = mbill.saldo + amount
            mbill.mwst[98] = mbill.mwst[98] + amount_foreign
            mbill.datum = bill_date

            if mbill.rechnr == 0:

                counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
                counters = counters + 1
                mbill.rechnr = counters

                counters = db_session.query(Counters).first()

                master = db_session.query(Master).first()

                if master:
                    master.rechnr = mbill.rechnr

                    master = db_session.query(Master).first()

                if transfer_case == 1:
                    master_str = "Master Bill"
                else:
                    master_str = "Transfer Bill"
                master_rechnr = to_string(mbill.rechnr)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

            if res_line:
                gastnrmember = res_line.gastnrmember
            else:
                gastnrmember = bill.gastnr
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = mbill.rechnr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = qty
            bill_line.fremdwbetrag = amount_foreign
            bill_line.betrag = amount
            bill_line.zinr = curr_room
            bill_line.departement = artikel.departement
            bill_line.zeit = currzeit
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
                bill_line.epreis = price

            if artikel.artart == 9 and res_line:
                bill_line.epreis = res_line.zipreis

            if res_line:
                bill_line.arrangement = res_line.arrangement
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr

            if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()
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

            billjournal.rechnr = mbill.rechnr
            billjournal.zinr = curr_room
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.fremdwaehrng = amount_foreign
            billjournal.bezeich = description
            billjournal.departement = artikel.departement
            billjournal.epreis = price
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if res_line:
                billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)

            if artikel.pricetab:
                billjournal.betrag = amount_foreign
            else:
                billjournal.betrag = amount
            cancel_str = ""

            billjournal = db_session.query(Billjournal).first()

            if artikel.artart == 2 or artikel.artart == 7:
                inv_ar(billart, curr_room, mbill.gastnr, gastnrmember, mbill.rechnr, amount, amount_foreign, htparam.fdate, mbill.name, user_init, "", deptno)

            if artikel.artart == 9 and artikel.artgrp == 0:
                master_taxserv(mbill._recid, currzeit)

            if transfer_case == 1:
                msg_str = "&M" + translateExtended ("Transfered to Master Bill No.", lvcarea, "") + " " + to_string(mbill.rechnr)
            else:
                msg_str = "&M" + translateExtended ("Transfered to Bill No.", lvcarea, "") + " " + to_string(mbill.rechnr) + " - " + translateExtENDed ("RmNo", lvcarea, "") + " " + mbill.zinr

            mbill = db_session.query(Mbill).first()


        return generate_inner_output()

    def master_taxserv(recid_mbill:int, currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

        service:decimal = 0
        vat:decimal = 0
        service_foreign:decimal = 0
        vat_foreign:decimal = 0
        argt_betrag0:decimal = 0
        argt_betrag:decimal = 0
        rest_betrag:decimal = 0
        frate:decimal = 0
        ex_rate:decimal = 0
        p_sign:int = 1
        qty1:int = 0
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        Artikel1 = Artikel
        Mbill = Bill

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 127)).first()
        rm_vat = not htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 128)).first()
        rm_serv = not htparam.flogical

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line.adrflag:
            frate = 1

        elif res_line.reserve_dec != 0:
            frate = res_line.reserve_dec
        else:
            frate = exchg_rate

        mbill = db_session.query(Mbill).filter(
                (Mbill._recid == recid_mbill)).first()
        rest_betrag = amount

        if amount < 0:
            p_sign = -1

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag = round(argt_betrag0 * ex_rate, price_decimal)

            artikel1 = db_session.query(Artikel1).filter(
                    (Artikel1.artnr == argt_line.argt_artnr) &  (Artikel1.departement == argt_line.departement)).first()

            if argt_line.fakt_modus == 1:
                post_it = True

            elif argt_line.fakt_modus == 2:

                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.rechnr == bill.rechnr) &  (Billjournal.artnr == artikel1.artnr) &  (Billjournal.betrag == argt_betrag) &  (Billjournal.departement == artikel1.departement)).first()

                if not billjournal:
                    post_it = True

            elif argt_line.fakt_modus == 3:

                if (res_line.ankunft + 1) == bill_date:
                    post_it = True

            elif argt_line.fakt_modus == 4:

                if get_day(bill_date) == 1:
                    post_it = True

            elif argt_line.fakt_modus == 5:

                if get_day(bill_date + 1) == 1:
                    post_it = True

            if post_it and argt_betrag != 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign
                rest_betrag = rest_betrag - argt_betrag * p_sign

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
                umsatz.betrag = umsatz.betrag + argt_betrag * p_sign
                umsatz.anzahl = umsatz.anzahl + qty1

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng = argt_betrag0 * p_sign
                billjournal.betrag = argt_betrag * p_sign
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit
                billjournal.userinit = userinit
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()

        artikel1 = db_session.query(Artikel1).filter(
                (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == 0)).first()

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

        billjournal.rechnr = mbill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = round(rest_betrag / exchg_rate , 2)
        billjournal.betrag = rest_betrag
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr_room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

        if rm_serv and artikel.service_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                service = htparam.fdecimal

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 133)).first()

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == 0)).first()
                service = service * price / 100
                service_foreign = round(service, 2) * qty

                if double_currency:
                    service = round(service * exchg_rate, price_decimal) * qty
                else:
                    service = round(service, price_decimal) * qty

                if artikel1.umsatzart == 1:
                    bill.logisumsatz = bill.logisumsatz + service

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz = bill.argtumsatz + service

                elif artikel1.umsatzart == 3:
                    bill.f_b_umsatz = bill.f_b_umsatz + service

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz = bill.sonst_umsatz + service

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz = bill.gesamtumsatz + service
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag = service_foreign
                bill_line.betrag = service
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date

                bill_line = db_session.query(Bill_line).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag = umsatz.betrag + service
                umsatz.anzahl = umsatz.anzahl + qty

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng = service_foreign
                billjournal.betrag = service
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()

        if rm_vat and artikel.mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat = htparam.fdecimal

                if (service * qty) < 0:
                    service = - service

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 132)).first()

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == 0)).first()

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat = vat * (price + service_foreign / qty) / 100
                else:
                    vat = vat * price / 100
                vat_foreign = round(vat, 2) * qty

                if double_currency:
                    vat = round(vat * exchg_rate, price_decimal) * qty
                else:
                    vat = round(vat, price_decimal) * qty

                if artikel1.umsatzart == 1:
                    mbill.logisumsatz = mbill.logisumsatz + vat

                elif artikel1.umsatzart == 2:
                    mbill.argtumsatz = mbill.argtumsatz + vat

                elif artikel1.umsatzart == 3:
                    mbill.f_b_umsatz = mbill.f_b_umsatz + vat

                elif artikel1.umsatzart == 4:
                    mbill.sonst_umsatz = mbill.sonst_umsatz + vat

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    mbill.gesamtumsatz = mbill.gesamtumsatz + vat
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag = vat_foreign
                bill_line.betrag = vat
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date

                bill_line = db_session.query(Bill_line).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag = umsatz.betrag + vat
                umsatz.anzahl = umsatz.anzahl + qty

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng = vat_foreign
                billjournal.betrag = vat
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()
        mbill.saldo = mbill.saldo + vat + service
        mbill.mwst[98] = mbill.mwst[98] + vat_foreign + service_foreign

        mbill = db_session.query(Mbill).first()

    def inv_ar(curr_art:int, zinr:str, gastnr:int, gastnrmember:int, rechnr:int, saldo:decimal, saldo_foreign:decimal, bill_date:date, billname:str, userinit:str, voucher_nr:str, dept_nr:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_list, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1


        nonlocal t_bill_line, resline, buf_artikel, buf_bill_line, artikel1, mbill, resline1, debt, debt1, main_res, bill1, bline, guest1
        nonlocal t_bill_line_list

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
        debitor.vesrcod = comment
        debitor.verstat = verstat
        debitor.betriebsnr = dept_nr

        if double_currency or foreign_rate:
            debitor.vesrdep = - saldo_foreign

        if voucher_nr != "":

            if comment != "":
                debitor.vesrcod = voucher_nr + ";" + debitor.vesrcod


            else:
                debitor.vesrcod = voucher_nr


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
    currzeit = get_current_time_in_seconds()
    master_flag = False


    update_bill()

    return generate_output()