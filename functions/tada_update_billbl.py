#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_restinv_rinv_arbl import ts_restinv_rinv_arbl
from models import Kellner, H_bill, H_bill_line, H_mjourn, H_artikel, Htparam, Queasy, Counters, Hoteldpt, H_umsatz, H_journal, Umsatz, Artikel, Guest, Arrangement, Argt_line, Billjournal

submenu_list_list, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})

def tada_update_billbl(pvilanguage:int, rec_id:int, rec_id_h_artikel:int, deptname:str, transdate:date, h_artart:int, cancel_order:bool, h_artikel_service_code:int, amount:decimal, amount_foreign:decimal, price:decimal, double_currency:bool, qty:int, exchg_rate:decimal, price_decimal:int, order_taker:int, tischnr:int, curr_dept:int, curr_waiter:int, gname:str, pax:int, kreditlimit:decimal, add_zeit:int, billart:int, description:str, change_str:str, cc_comment:str, cancel_str:str, req_str:str, voucher_str:str, hoga_card:str, print_to_kitchen:bool, from_acct:bool, h_artnrfront:int, pay_type:int, guestnr:int, transfer_zinr:str, curedept_flag:bool, foreign_rate:bool, curr_room:str, user_init:str, hoga_resnr:int, hoga_reslinnr:int, submenu_list_list:[Submenu_list]):
    bill_date = None
    cancel_flag = False
    fl_code = 0
    mwst = to_decimal("0.0")
    mwst_foreign = to_decimal("0.0")
    rechnr = 0
    balance = to_decimal("0.0")
    bcol = 0
    balance_foreign = to_decimal("0.0")
    fl_code1 = 0
    fl_code2 = 0
    fl_code3 = 0
    p_88 = False
    closed = False
    t_h_bill_list = []
    t_kellner1_list = []
    lvcarea:str = "TS-restinv"
    tax:decimal = to_decimal("0.0")
    serv:decimal = to_decimal("0.0")
    h_service:decimal = to_decimal("0.0")
    unit_price:decimal = to_decimal("0.0")
    nett_amount_foreign:decimal = to_decimal("0.0")
    h_mwst:decimal = to_decimal("0.0")
    h_mwst_foreign:decimal = to_decimal("0.0")
    h_service_foreign:decimal = to_decimal("0.0")
    nett_amount:decimal = to_decimal("0.0")
    subtotal:decimal = to_decimal("0.0")
    subtotal_foreign:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    service_foreign:decimal = to_decimal("0.0")
    sysdate:date = None
    zeit:int = 0
    condiment:bool = False
    succed:bool = False
    kellner = h_bill = h_bill_line = h_mjourn = h_artikel = htparam = queasy = counters = hoteldpt = h_umsatz = h_journal = umsatz = artikel = guest = arrangement = argt_line = billjournal = None

    t_kellner1 = t_h_bill = submenu_list = h_bline = kellner1 = mjou = bill_guest = None

    t_kellner1_list, T_kellner1 = create_model_like(Kellner)
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    H_bline = create_buffer("H_bline",H_bill_line)
    Kellner1 = create_buffer("Kellner1",Kellner)
    Mjou = create_buffer("Mjou",H_mjourn)
    Bill_guest = create_buffer("Bill_guest",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, t_kellner1_list, lvcarea, tax, serv, h_service, unit_price, nett_amount_foreign, h_mwst, h_mwst_foreign, h_service_foreign, nett_amount, subtotal, subtotal_foreign, service, service_foreign, sysdate, zeit, condiment, succed, kellner, h_bill, h_bill_line, h_mjourn, h_artikel, htparam, queasy, counters, hoteldpt, h_umsatz, h_journal, umsatz, artikel, guest, arrangement, argt_line, billjournal
        nonlocal pvilanguage, rec_id, rec_id_h_artikel, deptname, transdate, h_artart, cancel_order, h_artikel_service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr
        nonlocal h_bline, kellner1, mjou, bill_guest


        nonlocal t_kellner1, t_h_bill, submenu_list, h_bline, kellner1, mjou, bill_guest
        nonlocal t_kellner1_list, t_h_bill_list

        return {"bill_date": bill_date, "cancel_flag": cancel_flag, "fl_code": fl_code, "mwst": mwst, "mwst_foreign": mwst_foreign, "rechnr": rechnr, "balance": balance, "bcol": bcol, "balance_foreign": balance_foreign, "fl_code1": fl_code1, "fl_code2": fl_code2, "fl_code3": fl_code3, "p_88": p_88, "closed": closed, "t-h-bill": t_h_bill_list, "t-kellner1": t_kellner1_list}

    def rev_bdown():

        nonlocal bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, t_kellner1_list, lvcarea, tax, serv, h_service, unit_price, nett_amount_foreign, h_mwst, h_mwst_foreign, h_service_foreign, nett_amount, subtotal, subtotal_foreign, service, service_foreign, sysdate, zeit, condiment, succed, kellner, h_bill, h_bill_line, h_mjourn, h_artikel, htparam, queasy, counters, hoteldpt, h_umsatz, h_journal, umsatz, artikel, guest, arrangement, argt_line, billjournal
        nonlocal pvilanguage, rec_id, rec_id_h_artikel, deptname, transdate, h_artart, cancel_order, h_artikel_service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr
        nonlocal h_bline, kellner1, mjou, bill_guest


        nonlocal t_kellner1, t_h_bill, submenu_list, h_bline, kellner1, mjou, bill_guest
        nonlocal t_kellner1_list, t_h_bill_list

        artikel1 = None
        rest_betrag:decimal = to_decimal("0.0")
        argt_betrag:decimal = to_decimal("0.0")
        Artikel1 =  create_buffer("Artikel1",Artikel)
        rest_betrag =  to_decimal(amount)

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == artikel.artgrp)).first()

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            if argt_line.betrag != 0:
                argt_betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)

                if double_currency or artikel.pricetab:
                    argt_betrag = to_decimal(round(argt_betrag * exchg_rate , price_decimal))
            else:
                argt_betrag =  to_decimal(amount) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                argt_betrag = to_decimal(round(argt_betrag , price_decimal))
            rest_betrag =  to_decimal(rest_betrag) - to_decimal(argt_betrag)

            artikel1 = db_session.query(Artikel1).filter(
                     (Artikel1.artnr == argt_line.argt_artnr) & (Artikel1.departement == argt_line.departement)).first()

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == bill_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artikel1.artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel1.departement
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(argt_betrag)
            umsatz.anzahl = umsatz.anzahl + qty
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = h_bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng =  to_decimal(argt_line.betrag)
            billjournal.betrag =  to_decimal(argt_betrag)
            billjournal.bezeich = artikel1.bezeich +\
                    "<" + to_string(h_bill.departement, "99") + ">"
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

        artikel1 = db_session.query(Artikel1).filter(
                 (Artikel1.artnr == arrangement.artnr_logis) & (Artikel1.departement == arrangement.intervall)).first()

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == artikel1.artnr) & (Umsatz.departement == artikel1.departement) & (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(rest_betrag)
        umsatz.anzahl = umsatz.anzahl + qty
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = h_bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich +\
                "<" + to_string(h_bill.departement, "99") + ">"
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if double_currency:
            billjournal.fremdwaehrng = to_decimal(round(rest_betrag / exchg_rate , 2))


    if rec_id != 0:

        h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == rec_id)).first()

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel._recid == rec_id_h_artikel)).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    if transdate != None:
        bill_date = transdate
    else:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 253)).first()

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)

    if h_bill and h_artart == 0:

        h_bill_line = db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.bill_datum != bill_date)).first()

        if h_bill_line:
            fl_code = 1

            return generate_output()

    if cancel_order:

        h_bline = db_session.query(H_bline).filter(
                 (H_bline._recid == h_bill_line._recid)).first()
    nett_amount =  to_decimal(amount)
    nett_amount_foreign =  to_decimal(amount_foreign)
    h_service =  to_decimal("0")
    h_mwst =  to_decimal("0")
    h_service_foreign =  to_decimal("0")
    h_mwst_foreign =  to_decimal("0")

    if price == 0:

        if double_currency:
            unit_price =  to_decimal(amount_foreign) / to_decimal(qty)
        else:
            unit_price =  to_decimal(amount) / to_decimal(qty)
    else:
        unit_price =  to_decimal(price)

    if h_artart == 0:
        subtotal =  to_decimal(subtotal) + to_decimal(nett_amount)
        subtotal_foreign =  to_decimal(subtotal_foreign) + to_decimal(nett_amount_foreign)

    htparam = db_session.query(Htparam).filter(
             (paramnr == 135)).first()

    if not htparam.flogical and h_artart == 0 and h_artikel and h_artikel_service_code != 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == h_artikel.service_code)).first()

        if htparam.fdecimal != 0:
            serv =  to_decimal(htparam.fdecimal) / to_decimal("100")
            h_service =  to_decimal(unit_price) * to_decimal(htparam.fdecimal) / to_decimal("100")

            if double_currency:
                h_service_foreign = to_decimal(round(h_service , 2))
                h_service = to_decimal(round(h_service * exchg_rate , 2))
                service_foreign =  to_decimal(service_foreign) + to_decimal(h_service_foreign) * to_decimal(qty)


            else:
                h_service = to_decimal(round(h_service , 2))


            service =  to_decimal(service) + to_decimal(h_service) * to_decimal(qty)

    htparam = db_session.query(Htparam).filter(
             (paramnr == 134)).first()

    if not htparam.flogical and h_artart == 0 and h_artikel and h_artikel.mwst_code != 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == h_artikel.mwst_code)).first()

        if htparam.fdecimal != 0:
            tax =  to_decimal(htparam.fdecimal) / to_decimal("100")
            h_mwst =  to_decimal(htparam.fdecimal)

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 479)).first()

            if htparam.flogical:
                tax =  to_decimal(tax) * to_decimal((1) + to_decimal(serv) )
                h_mwst =  to_decimal(unit_price) * to_decimal(tax)


            else:
                h_mwst =  to_decimal(h_mwst) * to_decimal(unit_price) / to_decimal("100")

            if double_currency:
                h_mwst_foreign = to_decimal(round(h_mwst , 2))
                h_mwst =  to_decimal(tax) * to_decimal(unit_price) * to_decimal(exchg_rate)
                h_mwst = to_decimal(round(h_mwst , 2))


            else:
                h_mwst_foreign = to_decimal(round(h_mwst / exchg_rate , 2))
                h_mwst = to_decimal(round(h_mwst , 2))


            mwst =  to_decimal(mwst) + to_decimal(h_mwst) * to_decimal(qty)
            mwst_foreign =  to_decimal(mwst_foreign) + to_decimal(h_mwst_foreign) * to_decimal(qty)


    amount =  to_decimal(amount) + to_decimal((h_service) + to_decimal(h_mwst)) * to_decimal(qty)
    amount = to_decimal(round(amount , price_decimal))
    amount_foreign =  to_decimal(amount_foreign) +\
            (h_service_foreign + to_decimal(h_mwst_foreign)) * to_decimal(qty)

    if h_bill:
        else:
            h_bill = H_bill()
        db_session.add(h_bill)

        h_bill.betriebsnr = order_taker
        h_bill.rgdruck = 1
        h_bill.tischnr = tischnr
        h_bill.departement = curr_dept
        h_bill.kellner_nr = curr_waiter
        h_bill.bilname = gname
        h_bill.belegung = pax

        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 31) & (Queasy.number1 == curr_dept) & (Queasy.number2 == tischnr)).first()

        if queasy:
            queasy.number3 = get_current_time_in_seconds()
            queasy.date1 = get_current_date()

        if hoga_resnr > 0:
            h_bill.resnr = hoga_resnr
            h_bill.reslinnr = hoga_reslinnr

        counters = db_session.query(Counters).filter(
                     (Counters.counter_no == (100 + curr_dept))).first()

        if counters:
            else:

                hoteldpt = db_session.query(Hoteldpt).filter(
                             (Hoteldpt.num == curr_dept)).first()
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 100 + curr_dept
            counters.counter_bez = "Outlet Invoice: " + hoteldpt.depart
        counters.counter = counters.counter + 1

        if counters.counter > 999999:
            counters.counter = 1
        h_bill.rechnr = counters.counter
        rechnr = h_bill.rechnr
        fl_code2 = 1

    if h_bill.bilname == "" and gname != "":
        h_bill.bilname = gname

    kellner1 = db_session.query(Kellner1).filter(
                 (Kellner1.kellner_nr == h_bill.kellner_nr) & (Kellner1.departement == curr_dept)).first()

    if kellner1:
        t_kellner1 = T_kellner1()
        t_kellner1_list.append(t_kellner1)

        buffer_copy(kellner1, t_kellner1)

    if h_artart == 0:
        h_bill.gesamtumsatz =  to_decimal(h_bill.gesamtumsatz) + to_decimal(amount)
    balance =  to_decimal(balance) + to_decimal(amount)

    if balance <= kreditlimit:
        bcol = 2
    h_bill.saldo =  to_decimal(h_bill.saldo) + to_decimal(amount)
    h_bill.mwst[98] = h_bill.mwst[98] + amount_foreign
    balance =  to_decimal(h_bill.saldo)
    balance_foreign =  to_decimal(h_bill.mwst[98])

    if balance != 0:
        h_bill.rgdruck = 0

    if balance <= kreditlimit:
        bcol = 2
    sysdate = get_current_date()
    zeit = get_current_time_in_seconds() + add_zeit

    if billart != 0:

        h_umsatz = db_session.query(H_umsatz).filter(
                     (H_umsatz.artnr == billart) & (H_umsatz.departement == curr_dept) & (H_umsatz.datum == bill_date)).first()

        if h_umsatz:
            else:
                h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = billart
            h_umsatz.datum = bill_date
            h_umsatz.departement = curr_dept
        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(amount)
        h_umsatz.anzahl = h_umsatz.anzahl + qty
        pass
    h_journal = H_journal()
    db_session.add(h_journal)

    h_journal.rechnr = h_bill.rechnr
    h_journal.artnr = billart
    h_journal.anzahl = qty
    h_journal.fremdwaehrng =  to_decimal(amount_foreign)
    h_journal.betrag =  to_decimal(amount)
    h_journal.bezeich = description + change_str + cc_comment
    h_journal.tischnr = tischnr
    h_journal.departement = curr_dept
    h_journal.epreis =  to_decimal(price)
    h_journal.zeit = zeit
    h_journal.stornogrund = cancel_str
    h_journal.aendertext = req_str
    h_journal.kellner_nr = curr_waiter
    h_journal.bill_datum = bill_date
    h_journal.sysdate = sysdate
    h_journal.wabkurz = voucher_str

    if h_artart == 11:
        h_journal.aendertext = gname
        h_journal.segmentcode = billart
    h_bill_line = H_bill_line()
    db_session.add(h_bill_line)

    h_bill_line.rechnr = h_bill.rechnr
    h_bill_line.artnr = billart
    h_bill_line.bezeich = description + change_str + cc_comment
    h_bill_line.anzahl = qty
    h_bill_line.nettobetrag =  to_decimal(nett_amount)
    h_bill_line.fremdwbetrag =  to_decimal(amount_foreign)
    h_bill_line.betrag =  to_decimal(amount)
    h_bill_line.tischnr = tischnr
    h_bill_line.departement = curr_dept
    h_bill_line.epreis =  to_decimal(price)
    h_bill_line.zeit = zeit
    h_bill_line.bill_datum = bill_date
    h_bill_line.sysdate = sysdate

    if h_artikel and h_artikel.artart == 0 and (not print_to_kitchen or from_acct):
        h_bill_line.steuercode = 9999

    if h_artikel and h_artikel.artart == 0 and h_artikel.betriebsnr != 0:

        if not cancel_order:

            for submenu_list in query(submenu_list_list, filters=(lambda submenu_list: submenu_list.nr == h_artikel.betriebsnr and submenu_list.menurecid == menurecid)):
                submenu_list.zeit = zeit
                h_mjourn = H_mjourn()
                db_session.add(h_mjourn)

                h_mjourn.departement = curr_dept
                h_mjourn.rechnr = h_bill.rechnr
                h_mjourn.tischnr = tischnr
                h_mjourn.nr = submenu_list.nr
                h_mjourn.artnr = submenu_list.artnr
                h_mjourn.h_artnr = h_artikel.artnr
                h_mjourn.anzahl = qty
                h_mjourn.zeit = zeit
                h_mjourn.request = submenu_list.request
                h_mjourn.kellner_nr = curr_waiter
                h_mjourn.bill_datum = bill_date
                h_mjourn.sysdate = sysdate
                condiment = True

        else:

            h_journal = db_session.query(H_journal).filter(
                         (H_journal.artnr == h_bline.artnr) & (H_journal.departement == h_bline.departement) & (H_journal.rechnr == h_bline.rechnr) & (H_journal.bill_datum == h_bline.bill_datum) & (H_journal.zeit == h_bline.zeit) & (H_journal.sysdate == h_bline.sysdate)).first()

            if h_journal:

                for mjou in db_session.query(Mjou).filter(
                             (Mjou.departement == h_journal.departement) & (Mjou.h_artnr == h_journal.artnr) & (Mjou.rechnr == h_journal.rechnr) & (Mjou.bill_datum == h_journal.bill_datum) & (Mjou.sysdate == h_journal.sysdate) & (Mjou.zeit == h_journal.zeit)).order_by(Mjou._recid).all():
                    h_mjourn = H_mjourn()
                    db_session.add(h_mjourn)

                    h_mjourn.departement = mjou.departement
                    h_mjourn.rechnr = h_bill.rechnr
                    h_mjourn.tischnr = tischnr
                    h_mjourn.nr = mjou.nr
                    h_mjourn.artnr = mjou.artnr
                    h_mjourn.h_artnr = mjou.h_artnr
                    h_mjourn.anzahl = qty
                    h_mjourn.zeit = zeit
                    h_mjourn.request = mjou.request
                    h_mjourn.kellner_nr = curr_waiter
                    h_mjourn.bill_datum = bill_date
                    h_mjourn.sysdate = sysdate
                    condiment = True

    if h_artikel:
        h_journal.artart = h_artikel.artart
    h_journal.artnrfront = h_artnrfront

    if h_artart == 0 and h_artikel:
        h_journal.gang = h_artikel.gang

    if billart != 0:
        h_journal.artart = h_artart

    if pay_type == 1:
        h_journal.segmentcode = guestnr
        h_journal.bon_nr = h_bill.belegung

    elif pay_type == 2:
        h_journal.zinr = transfer_zinr

    if condiment:
        h_bill_line.betriebsnr = 1
        h_journal.betriebsnr = 1

    if h_artart == 0:
        fl_code3 = 1

        umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == h_artikel.artnrfront) & (Umsatz.departement == curr_dept) & (Umsatz.datum == bill_date)).first()

        if umsatz:
            else:
                umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = curr_dept
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + qty
        pass

        artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artnrfront) & (Artikel.departement == curr_dept)).first()

        if artikel.artart == 9 and artikel.artgrp != 0:
            rev_bdown()

    elif h_artart == 11 or h_artart == 12:

        umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == h_artikel.artnrfront) & (Umsatz.departement == curr_dept) & (Umsatz.datum == bill_date)).first()

        if umsatz:
            else:
                umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = curr_dept
        umsatz.anzahl = umsatz.anzahl + h_bill.belegung
        pass

    elif h_artart == 6:

        umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == h_artikel.artnrfront) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).first()

        if umsatz:
            else:
                umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = 0
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1
        pass
    closed = False

    if h_artart == 2 or h_artart == 7:

        if guestnr == 0:

            htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 867)).first()
            guestnr = htparam.finteger

        bill_guest = db_session.query(Bill_guest).filter(
                     (Bill_guest.gastnr == guestnr)).first()

        artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == 0)).first()

        if foreign_rate and amount_foreign == 0:
            amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
        get_output(ts_restinv_rinv_arbl(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment, deptname))

    if h_artart == 2 or h_artart == 7 or h_artart == 11 or h_artart == 12:

        if balance == 0:
            closed = True
            h_bill.flag = 1

            if h_artart == 11 or h_artart == 12:

                htparam = db_session.query(Htparam).filter(
                             (Htparam.paramnr == 739)).first()

                if htparam.flogical:
                    fl_code1 = 1
    succed = True

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 88)).first()
    p_88 = htparam.flogical
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()