#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from models import Bill_line, Res_line, Htparam, Waehrung, Artikel, Bill, Arrangement, Counters, Umsatz, Billjournal, Argt_line, Master, Mast_art, Debitor, Reservation, Guest, Bediener
from functions.next_counter_for_update import next_counter_for_update

def inv_update_billbl(pvilanguage:int, bil_flag:int, invoice_type:string, transdate:date, r_recid:int, 
                      deptno:int, billart:int, qty:int, price:Decimal, amount:Decimal, amount_foreign:Decimal, 
                      description:string, voucher_nr:string, cancel_str:string, user_init:string, billno:int, 
                      master_str:string, master_rechnr:string, balance:Decimal, balance_foreign:Decimal):

    prepare_cache ([Res_line, Htparam, Waehrung, Artikel, Bill, Arrangement, Counters, Umsatz, Billjournal, Argt_line, Master, Reservation, Guest, Bediener])

    master_flag = False
    msg_str = ""
    success_flag = True
    t_bill_line_data = []
    gastnrmember:int = 0
    price_decimal:int = 0
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
    currzeit:int = 0
    bill_date:date = None
    curr_room:string = ""
    lvcarea:string = "fo-invoice"
    bill_line = res_line = htparam = waehrung = artikel = bill = arrangement = counters = umsatz = billjournal = argt_line = master = mast_art = debitor = reservation = guest = bediener = None

    t_bill_line = resline = None

    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})

    Resline = create_buffer("Resline",Res_line)
    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    invoice_type = invoice_type.strip()
    description = description.strip()
    voucher_nr = voucher_nr.strip()
    cancel_str = cancel_str.strip()
    user_init = user_init.strip()
    master_str = master_str.strip()
    master_rechnr = master_rechnr.strip()

    def generate_output():
        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline


        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        return {"billno": billno, "master_str": master_str, "master_rechnr": master_rechnr, "balance": balance, "balance_foreign": balance_foreign, "master_flag": master_flag, "msg_str": msg_str, "success_flag": success_flag, "t-bill-line": t_bill_line_data}

    def update_bill():

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline
        nonlocal last_count, error_lock
        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        buf_artikel = None
        buf_bill_line = None
        skip_it:bool = False
        Buf_artikel =  create_buffer("Buf_artikel",Artikel)
        Buf_bill_line =  create_buffer("Buf_bill_line",Bill_line)

        artikel = get_cache (Artikel, {"artnr": [(eq, billart)],"departement": [(eq, deptno)]})

        if not artikel:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == billart) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag)).first()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        if amount_foreign == None:
            amount_foreign =  to_decimal("0")

        bill = get_cache (Bill, {"_recid": [(eq, r_recid)]})

        if bill:

            if bill.flag == 1 and bil_flag == 0:
                msg_str = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr_unicode(10) + translateExtended ("Bill entry is no longer possible!", lvcarea, "")
                success_flag = False

                return

            if artikel.artart == 9 and artikel.artgrp == 0:
                skip_it = True

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                buf_artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

                buf_bill_line = db_session.query(Buf_bill_line).filter(
                         (Buf_bill_line.departement == 0) & (Buf_bill_line.artnr == buf_artikel.artnr) & (Buf_bill_line.bill_datum == bill_date) & (Buf_bill_line.zinr != "") & (Buf_bill_line.massnr == res_line.resnr) & (Buf_bill_line.billin_nr == res_line.reslinnr)).first()
                skip_it = None != buf_bill_line

                if skip_it:
                    success_flag = False
                    msg_str = translateExtended ("Not possible", lvcarea, "") + chr_unicode(10) + translateExtended ("room Charge Already Posted", lvcarea, "") + " to bill no " + to_string(buf_bill_line.rechnr)

                    return
            pass
            curr_room = bill.zinr
            gastnrmember = bill.gastnr

            if invoice_type.lower()  == ("guest").lower() :

                if bill.flag == 0:
                    master_flag = update_masterbill(currzeit)

                if master_flag:

                    return

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                if res_line:
                    gastnrmember = res_line.gastnrmember

            if artikel.umsatzart == 1:
                bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 2:
                bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)

            elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
                bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(amount)

            elif artikel.umsatzart == 4:
                bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)

            if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)

            if not artikel.autosaldo:
                bill.rgdruck = 0

            if bill.datum < bill_date or bill.datum == None:
                bill.datum = bill_date
            bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)

            if double_currency or foreign_rate:
                bill.mwst[98] = bill.mwst[98] + amount_foreign

            if bill.rechnr == 0:

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                # counters.counter = counters.counter + 1
                # bill.rechnr = counters.counter
                last_count, error_lock = next_counter_for_update(3)
                bill.rechnr = last_count


                if transdate != None:
                    bill.datum = transdate
                pass
            billno = bill.rechnr


            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.massnr = bill.resnr
            bill_line.billin_nr = bill.reslinnr
            bill_line.zinr = curr_room
            bill_line.artnr = billart
            bill_line.anzahl = qty
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.bezeich = description
            bill_line.departement = artikel.departement
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if voucher_nr != "":
                bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr

            if artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
                bill_line.epreis =  to_decimal(price)

            if artikel.artart == 9:

                arrangement = get_cache (Arrangement, {"argt_artikelnr": [(eq, artikel.artnr)]})

                if arrangement and res_line:
                    bill_line.epreis =  to_decimal(res_line.zipreis)

            if res_line:
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement

            if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
                bill_line.bezeich = arrangement.argt_rgbez
            pass
            t_bill_line = T_bill_line()
            t_bill_line_data.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.artart = artikel.artart
            t_bill_line.bl_recid = to_int(bill_line._recid)

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
            billjournal.zinr = curr_room
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.betrag =  to_decimal(amount)
            billjournal.bezeich = description
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(price)
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if voucher_nr != "":
                billjournal.bezeich = billjournal.bezeich + "/" + voucher_nr
            pass

            if artikel.artart == 2 or artikel.artart == 7:

                if invoice_type.lower()  == ("master").lower() :

                    resline = db_session.query(Resline).filter(
                                 (Resline.resnr == bill.resnr) & ((Resline.resstatus == 6) | (Resline.resstatus == 8))).first()

                    if resline:
                        gastnrmember = resline.gastnrmember
                inv_ar(billart, "", bill.gastnr, gastnrmember, bill.rechnr, amount, amount_foreign, bill_date, bill.name, user_init, voucher_nr, deptno)

            elif artikel.artart == 9:

                if artikel.artgrp == 0:
                    rev_bdown(currzeit)
                else:
                    rev_bdown1(currzeit)
            balance =  to_decimal(bill.saldo)

            if double_currency or foreign_rate:
                balance_foreign =  to_decimal(bill.mwst[98])
            pass


    def rev_bdown(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline
        nonlocal last_count, error_lock

        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        service_foreign:Decimal = to_decimal("0.0")
        vat_foreign:Decimal = to_decimal("0.0")
        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        frate:Decimal = to_decimal("0.0")
        ex_rate:Decimal = to_decimal("0.0")
        p_sign:int = 1
        qty1:int = 0
        rm_vat:bool = False
        rm_serv:bool = False
        artikel1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if res_line:

            if res_line.adrflag:
                frate =  to_decimal("1")

            elif res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
        else:
            frate =  to_decimal(exchg_rate)
        rest_betrag =  to_decimal(amount)

        if amount < 0:
            p_sign = -1

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag =  to_decimal(round (argt_betrag) * to_decimal(ex_rate , price_decimal))
            rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag) * to_decimal(p_sign)

            if argt_betrag != 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

                artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement


                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag) * to_decimal(p_sign)
                umsatz.anzahl = umsatz.anzahl + qty1


                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_line.betrag) * to_decimal(p_sign)
                billjournal.betrag =  to_decimal(argt_betrag) * to_decimal(p_sign)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date


                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

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

        if rm_serv and artikel.service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign =  to_decimal(round (service , 2)) * to_decimal(qty)

                if double_currency:
                    service =  to_decimal(round (service) * to_decimal(exchg_rate , price_decimal)) * to_decimal(qty)
                else:
                    service =  to_decimal(round (service , price_decimal)) * to_decimal(qty)

                if artikel1.umsatzart == 1:
                    bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(service)
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

                elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                    bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(service)

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(service)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(service)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date

                if res_line:
                    bill_line.arrangement = res_line.arrangement
                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement


                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty


                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date


                pass

        if rm_vat and artikel.mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign =  to_decimal(round (vat , 2)) * to_decimal(qty)

                if double_currency:
                    vat =  to_decimal(round (vat) * to_decimal(exchg_rate , price_decimal)) * to_decimal(qty)
                else:
                    vat =  to_decimal(round (vat , price_decimal)) * to_decimal(qty)

                if artikel1.umsatzart == 1:
                    bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(vat)
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(vat)

                elif (artikel1.umsatzart == 3 or artikel1.umsatzart == 5 or artikel1.umsatzart == 6):
                    bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(vat)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(vat)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date

                if res_line:
                    bill_line.arrangement = res_line.arrangement
                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement


                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty


                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date


                pass
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(vat) + to_decimal(service)

        if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
            bill.saldo =  to_decimal("0")

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign
        balance =  to_decimal(bill.saldo)

        if double_currency or foreign_rate:
            balance_foreign =  to_decimal(bill.mwst[98])


    def rev_bdown1(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline


        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        p_qty:int = 0
        artikel1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        rest_betrag =  to_decimal(amount)

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

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            if argt_line.betrag != 0:
                argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(p_qty)

                if double_currency or artikel.pricetab:
                    argt_betrag =  to_decimal(round (argt_betrag) * to_decimal(exchg_rate , price_decimal))
            else:
                argt_betrag =  to_decimal(amount) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                argt_betrag =  to_decimal(round (argt_betrag , price_decimal) )


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
            billjournal.zinr = curr_room
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng =  to_decimal(argt_line.betrag)
            billjournal.betrag =  to_decimal(argt_betrag)
            billjournal.bezeich = artikel1.bezeich
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass

        if rest_betrag != 0:

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
            billjournal.zinr = curr_room
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.betrag =  to_decimal(rest_betrag)
            billjournal.bezeich = artikel1.bezeich
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if double_currency:
                billjournal.fremdwaehrng =  to_decimal(round (rest_betrag) / to_decimal(exchg_rate , 6))
            pass


    def update_masterbill(currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline
        nonlocal last_count, error_lock


        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        master_flag = False
        room:string = ""
        transfer_case:int = 0
        na_running:bool = False
        transf_rm:string = ""
        mess_str:string = ""
        mbill = None
        resline = None
        resline1 = None

        def generate_inner_output():
            return (master_flag)

        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)
        Resline1 =  create_buffer("Resline1",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
        na_running = htparam.flogical

        if na_running and bill_date == htparam.fdate:
            bill_date = bill_date + timedelta(days=1)

        resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if resline and resline.l_zuordnung[4] != 0:

            master = get_cache (Master, {"resnr": [(eq, resline.l_zuordnung[4])],"active": [(eq, True)],"flag": [(eq, 0)]})
        else:

            master = get_cache (Master, {"resnr": [(eq, bill.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master:
            transfer_case = 1

            if (master.umsatzart[0]  and artikel.artart == 8) or (master.umsatzart[1]  and artikel.artart == 9 and artikel.artgrp == 0) or (master.umsatzart[2]  and artikel.umsatzart == 3) or (master.umsatzart[3]  and artikel.umsatzart == 4):
                master_flag = True

            if not master_flag:

                mast_art = get_cache (Mast_art, {"resnr": [(eq, master.resnr)],"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)]})

                if mast_art:
                    master_flag = True

        resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        if resline and resline.l_zuordnung[1] != 0:
            master_flag = False

        if not master_flag:
            transf_rm = entry(0, resline.memozinr, ";")

            if resline and transf_rm != "" and (transf_rm != resline.zinr):

                resline1 = get_cache (Res_line, {"zinr": [(eq, transf_rm)],"resstatus": [(eq, 6)]})

                if resline1:
                    master_flag = True
                    transfer_case = 2

        if master_flag:

            if transfer_case == 1:

                mbill = get_cache (Bill, {"resnr": [(eq, master.resnr)],"reslinnr": [(eq, 0)]})
            else:

                mbill = get_cache (Bill, {"resnr": [(eq, resline1.resnr)],"reslinnr": [(eq, resline1.reslinnr)],"billnr": [(eq, 1)]})

            if artikel.umsatzart == 1:
                mbill.logisumsatz =  to_decimal(mbill.logisumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 2:
                mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 3:
                mbill.f_b_umsatz =  to_decimal(mbill.f_b_umsatz) + to_decimal(amount)

            elif artikel.umsatzart == 4:
                mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(amount)

            if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(amount)
            mbill.rgdruck = 0
            mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(amount)
            mbill.mwst[98] = mbill.mwst[98] + amount_foreign
            mbill.datum = bill_date

            if mbill.rechnr == 0:

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                # counters.counter = counters.counter + 1
                # mbill.rechnr = counters.counter

                last_count, error_lock = next_counter_for_update(3)
                mbill.rechnr = last_count

                if master:
                    master.rechnr = mbill.rechnr
                    pass

                if transfer_case == 1:
                    master_str = "Master Bill"
                else:
                    master_str = "Transfer Bill"
                master_rechnr = to_string(mbill.rechnr)

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

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
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.betrag =  to_decimal(amount)
            bill_line.zinr = curr_room
            bill_line.departement = artikel.departement
            bill_line.zeit = currzeit
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date

            if artikel.artart != 2 and artikel.artart != 4 and artikel.artart != 6 and artikel.artart != 7:
                bill_line.epreis =  to_decimal(price)

            if artikel.artart == 9 and res_line:
                bill_line.epreis =  to_decimal(res_line.zipreis)

            if res_line:
                bill_line.arrangement = res_line.arrangement
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr

            if artikel.artart == 9 and artikel.artgrp == 0 and res_line:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
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

            billjournal.rechnr = mbill.rechnr
            billjournal.zinr = curr_room
            billjournal.artnr = billart
            billjournal.anzahl = qty
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = description
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(price)
            billjournal.zeit = currzeit
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if res_line:
                billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)

            if artikel.pricetab:
                billjournal.betrag =  to_decimal(amount_foreign)
            else:
                billjournal.betrag =  to_decimal(amount)
            cancel_str = ""
            pass

            if artikel.artart == 2 or artikel.artart == 7:
                inv_ar(billart, curr_room, mbill.gastnr, gastnrmember, mbill.rechnr, amount, amount_foreign, htparam.fdate, mbill.name, user_init, "", deptno)

            if artikel.artart == 9 and artikel.artgrp == 0:
                master_taxserv(mbill._recid, currzeit)

            if transfer_case == 1:
                msg_str = "&M" + translateExtended ("Transfered to Master Bill No.", lvcarea, "") + " " + to_string(mbill.rechnr)
            else:
                msg_str = "&M" + translateExtended ("Transfered to Bill No.", lvcarea, "") + " " + to_string(mbill.rechnr) + " - " + translateExtended ("RmNo", lvcarea, "") + " " + mbill.zinr
            pass

        return generate_inner_output()


    def master_taxserv(recid_mbill:int, currzeit:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, bill_date, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline


        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        service_foreign:Decimal = to_decimal("0.0")
        vat_foreign:Decimal = to_decimal("0.0")
        argt_betrag0:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        rest_betrag:Decimal = to_decimal("0.0")
        frate:Decimal = to_decimal("0.0")
        ex_rate:Decimal = to_decimal("0.0")
        p_sign:int = 1
        qty1:int = 0
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        artikel1 = None
        mbill = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        Mbill =  create_buffer("Mbill",Bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = not htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = not htparam.flogical

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if res_line.adrflag:
            frate =  to_decimal("1")

        elif res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:
            frate =  to_decimal(exchg_rate)

        mbill = get_cache (Bill, {"_recid": [(eq, recid_mbill)]})
        rest_betrag =  to_decimal(amount)

        if amount < 0:
            p_sign = -1

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag = to_decimal(round(argt_betrag0 * ex_rate , price_decimal))

            artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

            if argt_line.fakt_modus == 1:
                post_it = True

            elif argt_line.fakt_modus == 2:

                billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, artikel1.artnr)],"betrag": [(eq, argt_betrag)],"departement": [(eq, artikel1.departement)]})

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
                rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag) * to_decimal(p_sign)

                artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag) * to_decimal(p_sign)
                umsatz.anzahl = umsatz.anzahl + qty1
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty1
                billjournal.fremdwaehrng =  to_decimal(argt_betrag0) * to_decimal(p_sign)
                billjournal.betrag =  to_decimal(argt_betrag) * to_decimal(p_sign)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

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

        billjournal.rechnr = mbill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = to_decimal(round(rest_betrag / exchg_rate , 2))
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr_room
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = currzeit
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        pass

        if rm_serv and artikel.service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 133)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
                service =  to_decimal(service) * to_decimal(price) / to_decimal("100")
                service_foreign = to_decimal(round(service , 2) * qty)

                if double_currency:
                    service = to_decimal(round(service * exchg_rate , price_decimal) * qty)
                else:
                    service = to_decimal(round(service , price_decimal) * qty)

                if artikel1.umsatzart == 1:
                    bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(service)

                elif artikel1.umsatzart == 2:
                    bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(service)

                elif artikel1.umsatzart == 3:
                    bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(service)

                elif artikel1.umsatzart == 4:
                    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(service)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(service)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(service_foreign)
                bill_line.betrag =  to_decimal(service)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(service)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(service_foreign)
                billjournal.betrag =  to_decimal(service)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass

        if rm_vat and artikel.mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal)

                if (service * qty) < 0:
                    service =  - to_decimal(service)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

                artikel1 = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) * to_decimal((price) + to_decimal(service_foreign) / to_decimal(qty)) / to_decimal("100")
                else:
                    vat =  to_decimal(vat) * to_decimal(price) / to_decimal("100")
                vat_foreign = to_decimal(round(vat , 2) * qty)

                if double_currency:
                    vat = to_decimal(round(vat * exchg_rate , price_decimal) * qty)
                else:
                    vat = to_decimal(round(vat , price_decimal) * qty)

                if artikel1.umsatzart == 1:
                    mbill.logisumsatz =  to_decimal(mbill.logisumsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 2:
                    mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 3:
                    mbill.f_b_umsatz =  to_decimal(mbill.f_b_umsatz) + to_decimal(vat)

                elif artikel1.umsatzart == 4:
                    mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(vat)

                if artikel1.umsatzart >= 1 and artikel1.umsatzart <= 4:
                    mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(vat)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = mbill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = qty
                bill_line.fremdwbetrag =  to_decimal(vat_foreign)
                bill_line.betrag =  to_decimal(vat)
                bill_line.zinr = curr_room
                bill_line.departement = artikel1.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel1.artnr)],"departement": [(eq, artikel1.departement)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(vat)
                umsatz.anzahl = umsatz.anzahl + qty
                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = mbill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = qty
                billjournal.fremdwaehrng =  to_decimal(vat_foreign)
                billjournal.betrag =  to_decimal(vat)
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = curr_room
                billjournal.departement = artikel1.departement
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = cancel_str
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                pass
        mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(vat) + to_decimal(service)
        mbill.mwst[98] = mbill.mwst[98] + vat_foreign + service_foreign
        pass


    def inv_ar(curr_art:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string, voucher_nr:string, dept_nr:int):

        nonlocal master_flag, msg_str, success_flag, t_bill_line_data, price_decimal, exchg_rate, currzeit, curr_room, lvcarea, bill_line, res_line, htparam, waehrung, artikel, bill, arrangement, counters, umsatz, billjournal, argt_line, master, mast_art, debitor, reservation, guest, bediener
        nonlocal pvilanguage, bil_flag, invoice_type, transdate, r_recid, deptno, billart, qty, price, amount, amount_foreign, description, cancel_str, user_init, billno, master_str, master_rechnr, balance, balance_foreign
        nonlocal resline


        nonlocal t_bill_line, resline
        nonlocal t_bill_line_data

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

        debt = db_session.query(Debt).filter(
                 (Debt.artnr == curr_art) & (Debt.rechnr == rechnr) & (Debt.opart == 0) & (Debt.rgdatum == bill_date) & (Debt.counter == 0) & (Debt.saldo == saldo)).first()

        if debt:

            debt1 = db_session.query(Debt1).filter(
                     (Debt1._recid == debt._recid)).first()

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

        bill1 = get_cache (Bill, {"rechnr": [(eq, rechnr)]})

        if bill1 and bill1.resnr != 0:

            resline = get_cache (Res_line, {"resnr": [(eq, bill1.resnr)],"active_flag": [(le, 2)],"resstatus": [(le, 8)],"zipreis": [(ne, 0)]})

            if not resline:

                resline = get_cache (Res_line, {"resnr": [(eq, bill1.resnr)],"active_flag": [(le, 2)],"resstatus": [(le, 8)]})

            if resline:
                currency_nr = resline.betriebsnr

            main_res = get_cache (Reservation, {"resnr": [(eq, bill1.resnr)]})

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
        debitor.vesrcod = comment
        debitor.verstat = verstat
        debitor.betriebsnr = dept_nr

        if double_currency or foreign_rate:
            debitor.vesrdep =  - to_decimal(saldo_foreign)

        if voucher_nr != "":

            if comment != "":
                debitor.vesrcod = voucher_nr + ";" + debitor.vesrcod


            else:
                debitor.vesrcod = voucher_nr


        pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    currzeit = get_current_time_in_seconds()
    master_flag = False


    update_bill()

    return generate_output()