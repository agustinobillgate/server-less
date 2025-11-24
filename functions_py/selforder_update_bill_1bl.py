#using conversion tools version: 1.0.0.117

# ========================
# Rulita, 31-10-2025
# - Recompile program
# ========================
# ============================
# Rd, 24/11/2025, update last_count for counter update
# ============================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_restinv_rinv_arbl import ts_restinv_rinv_arbl
from models import Kellner, H_bill, H_bill_line, H_mjourn, H_artikel, Htparam, Queasy, Guest, Counters, Hoteldpt, H_umsatz, H_journal, Umsatz, Artikel, Arrangement, Argt_line, Billjournal
from functions.next_counter_for_update import next_counter_for_update

submenu_list_data, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})

def selforder_update_bill_1bl(pvilanguage:int, rec_id:int, rec_id_h_artikel:int, deptname:string, 
                              transdate:date, h_artart:int, cancel_order:bool, h_artikel_service_code:int, 
                              amount:Decimal, amount_foreign:Decimal, price:Decimal, double_currency:bool, qty:int, 
                              exchg_rate:Decimal, price_decimal:int, order_taker:int, tischnr:int, curr_dept:int, 
                              curr_waiter:int, gname:string, pax:int, kreditlimit:Decimal, add_zeit:int, 
                              billart:int, description:string, change_str:string, cc_comment:string, 
                              cancel_str:string, req_str:string, voucher_str:string, hoga_card:string, 
                              print_to_kitchen:bool, from_acct:bool, h_artnrfront:int, pay_type:int, guestnr:int, 
                              transfer_zinr:string, curedept_flag:bool, foreign_rate:bool, curr_room:string, 
                              user_init:string, hoga_resnr:int, hoga_reslinnr:int, submenu_list_data:[Submenu_list]):

    prepare_cache ([H_bill_line, H_mjourn, H_artikel, Htparam, Queasy, Guest, Counters, Hoteldpt, H_umsatz, H_journal, Umsatz, Artikel, Arrangement, Argt_line, Billjournal])

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
    t_h_bill_data = []
    t_kellner1_data = []
    lvcarea:string = "TS-restinv"
    incl_vat:bool = False
    get_price:int = 0
    mc_str:string = ""
    tax:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    h_service:Decimal = to_decimal("0.0")
    unit_price:Decimal = to_decimal("0.0")
    nett_amount_foreign:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    h_mwst_foreign:Decimal = to_decimal("0.0")
    h_service_foreign:Decimal = to_decimal("0.0")
    nett_amount:Decimal = to_decimal("0.0")
    subtotal:Decimal = to_decimal("0.0")
    subtotal_foreign:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    service_foreign:Decimal = to_decimal("0.0")
    recid_h_bill_line:int = 0
    sysdate:date = None
    zeit:int = 0
    condiment:bool = False
    succed:bool = False
    kellner = h_bill = h_bill_line = h_mjourn = h_artikel = htparam = queasy = guest = counters = hoteldpt = h_umsatz = h_journal = umsatz = artikel = arrangement = argt_line = billjournal = None

    t_kellner1 = t_h_bill = submenu_list = h_bline = kellner1 = bbill = mjou = bill_guest = None

    t_kellner1_data, T_kellner1 = create_model_like(Kellner)
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    H_bline = create_buffer("H_bline",H_bill_line)
    Kellner1 = create_buffer("Kellner1",Kellner)
    Bbill = create_buffer("Bbill",H_bill)
    Mjou = create_buffer("Mjou",H_mjourn)
    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session
    last_count:int = 0
    error_lock = ""
    deptname = deptname.strip()
    gname = gname.strip()
    description = description.strip()
    change_str = change_str.strip()
    cc_comment = cc_comment.strip()
    cancel_str = cancel_str.strip()
    req_str = req_str.strip()
    voucher_str = voucher_str.strip()
    hoga_card = hoga_card.strip()
    transfer_zinr = transfer_zinr.strip()
    curr_room = curr_room.strip()

    
    def generate_output():
        nonlocal bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, t_kellner1_data, lvcarea, incl_vat, get_price, mc_str, tax, serv, h_service, unit_price, nett_amount_foreign, h_mwst, h_mwst_foreign, h_service_foreign, nett_amount, subtotal, subtotal_foreign, service, service_foreign, recid_h_bill_line, sysdate, zeit, condiment, succed, kellner, h_bill, h_bill_line, h_mjourn, h_artikel, htparam, queasy, guest, counters, hoteldpt, h_umsatz, h_journal, umsatz, artikel, arrangement, argt_line, billjournal
        nonlocal pvilanguage, rec_id, rec_id_h_artikel, deptname, transdate, h_artart, cancel_order, h_artikel_service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr
        nonlocal h_bline, kellner1, bbill, mjou, bill_guest


        nonlocal t_kellner1, t_h_bill, submenu_list, h_bline, kellner1, bbill, mjou, bill_guest
        nonlocal t_kellner1_data, t_h_bill_data

        return {"bill_date": bill_date, "cancel_flag": cancel_flag, "fl_code": fl_code, "mwst": mwst, "mwst_foreign": mwst_foreign, "rechnr": rechnr, "balance": balance, "bcol": bcol, "balance_foreign": balance_foreign, "fl_code1": fl_code1, "fl_code2": fl_code2, "fl_code3": fl_code3, "p_88": p_88, "closed": closed, "t-h-bill": t_h_bill_data, "t-kellner1": t_kellner1_data}

    def rev_bdown():

        nonlocal bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, t_kellner1_data, lvcarea, incl_vat, get_price, mc_str, tax, serv, h_service, unit_price, nett_amount_foreign, h_mwst, h_mwst_foreign, h_service_foreign, nett_amount, subtotal, subtotal_foreign, service, service_foreign, recid_h_bill_line, sysdate, zeit, condiment, succed, kellner, h_bill, h_bill_line, h_mjourn, h_artikel, htparam, queasy, guest, counters, hoteldpt, h_umsatz, h_journal, umsatz, artikel, arrangement, argt_line, billjournal
        nonlocal pvilanguage, rec_id, rec_id_h_artikel, deptname, transdate, h_artart, cancel_order, h_artikel_service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr
        nonlocal h_bline, kellner1, bbill, mjou, bill_guest


        nonlocal t_kellner1, t_h_bill, submenu_list, h_bline, kellner1, bbill, mjou, bill_guest
        nonlocal t_kellner1_data, t_h_bill_data

        artikel1 = None
        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        Artikel1 =  create_buffer("Artikel1",Artikel)
        rest_betrag =  to_decimal(amount)

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, artikel.artgrp)]})

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
        pass


    if rec_id != 0:

        h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_id_h_artikel)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    if transdate != None:
        bill_date = transdate
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)

    if h_bill and h_artart == 0:

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)],"bill_datum": [(ne, bill_date)]})

        if h_bill_line:
            fl_code = 1

            return generate_output()

    if cancel_order:

        h_bline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

    if not htparam.flogical and h_artart == 0 and h_artikel and h_artikel_service_code != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, h_artikel.service_code)]})

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

    if not htparam.flogical and h_artart == 0 and h_artikel and h_artikel.mwst_code != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, h_artikel.mwst_code)]})

        if htparam.fdecimal != 0:
            tax =  to_decimal(htparam.fdecimal) / to_decimal("100")
            h_mwst =  to_decimal(htparam.fdecimal)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

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


    pass

    if h_bill:
        pass
    else:

        bbill = db_session.query(Bbill).filter(
                     (Bbill.tischnr == tischnr) & (Bbill.departement == curr_dept) & (Bbill.flag == 0)).first()

        if bbill:
            fl_code = 2

            return generate_output()
        h_bill = H_bill()
        db_session.add(h_bill)

        h_bill.betriebsnr = order_taker
        h_bill.rgdruck = 1
        h_bill.tischnr = tischnr
        h_bill.departement = curr_dept
        h_bill.kellner_nr = curr_waiter
        h_bill.bilname = gname
        h_bill.belegung = pax

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

        if queasy:
            pass
            queasy.number3 = get_current_time_in_seconds()
            queasy.date1 = get_current_date()


            pass
            pass

        if hoga_resnr > 0:
            h_bill.resnr = hoga_resnr
            h_bill.reslinnr = hoga_reslinnr

        if hoga_reslinnr == 0 and gname != "":

            guest = get_cache (Guest, {"vorname1": [(eq, gname)]})

            if guest:
                h_bill.resnr = guest.gastnr
                h_bill.reslinnr = 0

        # counters = get_cache (Counters, {"counter_no": [(eq, (100 + curr_dept))]})
        counters = db_session.query(Counters).filter(
            Counters.counter_no == (100 + curr_dept)
        ).with_for_update(nowait=False).first()

        if counters:
            pass
        else:

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
            counters = Counters()
            db_session.add(counters)
            db_session.flush()
            counters.counter_no = 100 + curr_dept
            counters.counter_bez = "Outlet Invoice: " + hoteldpt.depart


        counters.counter = counters.counter + 1

        if counters.counter > 999999:
            counters.counter = 1
        
        db_session.commit()
        h_bill.rechnr = counters.counter
        rechnr = h_bill.rechnr
        fl_code2 = 1
        pass

    if gname != "":
        h_bill.bilname = gname

    kellner1 = db_session.query(Kellner1).filter(
                 (Kellner1.kellner_nr == h_bill.kellner_nr) & (Kellner1.departement == curr_dept)).first()

    if kellner1:
        t_kellner1 = T_kellner1()
        t_kellner1_data.append(t_kellner1)

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

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, billart)],"departement": [(eq, curr_dept)],"datum": [(eq, bill_date)]})

        if h_umsatz:
            pass
        else:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = billart
            h_umsatz.datum = bill_date
            h_umsatz.departement = curr_dept
        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(amount)
        h_umsatz.anzahl = h_umsatz.anzahl + qty
        pass
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

        if mc_str != " ":

            queasy = get_cache (Queasy, {"key": [(eq, 197)],"char1": [(eq, mc_str)],"date1": [(eq, bill_date)],"number1": [(eq, billart)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 197
                queasy.char1 = mc_str
                queasy.date1 = bill_date
                queasy.deci1 =  to_decimal(amount)
                queasy.number1 = billart


            else:
                pass
                queasy.deci1 =  to_decimal(queasy.deci1) + to_decimal(amount)


                pass
                pass
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
    recid_h_bill_line = h_bill_line._recid
    h_journal.schankbuch = recid_h_bill_line

    if h_artikel and h_artikel.artart == 0 and (not print_to_kitchen or from_acct):
        h_bill_line.steuercode = 9999

    if h_artikel and h_artikel.artart == 0 and h_artikel.betriebsnr != 0:

        if not cancel_order:

            for submenu_list in query(submenu_list_data, filters=(lambda submenu_list: submenu_list.nr == h_artikel.betriebsnr and submenu_list.menurecid == menurecid)):
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
                pass
                condiment = True

        else:

            h_journal = get_cache (H_journal, {"artnr": [(eq, h_bline.artnr)],"departement": [(eq, h_bline.departement)],"rechnr": [(eq, h_bline.rechnr)],"bill_datum": [(eq, h_bline.bill_datum)],"zeit": [(eq, h_bline.zeit)],"sysdate": [(eq, h_bline.sysdate)]})

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
                    pass
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


    pass
    pass

    if h_artart == 0:
        fl_code3 = 1

        umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)],"datum": [(eq, bill_date)]})

        if umsatz:
            pass
        else:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = curr_dept
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + qty
        pass
        pass

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artnrfront)],"departement": [(eq, curr_dept)]})

        if artikel.artart == 9 and artikel.artgrp != 0:
            rev_bdown()

    elif h_artart == 11 or h_artart == 12:

        umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)],"datum": [(eq, bill_date)]})

        if umsatz:
            pass
        else:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = curr_dept
        umsatz.anzahl = umsatz.anzahl + h_bill.belegung
        pass
        pass

    elif h_artart == 6:

        umsatz = get_cache (Umsatz, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if umsatz:
            pass
        else:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = h_artikel.artnrfront
            umsatz.datum = bill_date
            umsatz.departement = 0
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1
        pass
        pass
    pass
    closed = False

    if h_artart == 2 or h_artart == 7:

        if guestnr == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})
            guestnr = htparam.finteger

        bill_guest = get_cache (Guest, {"gastnr": [(eq, guestnr)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

        if foreign_rate and amount_foreign == 0:
            amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
        get_output(ts_restinv_rinv_arbl(artikel.artnr, curr_dept, curr_room, bill_guest.gastnr, bill_guest.gastnr, h_bill.rechnr, amount, amount_foreign, bill_date, bill_guest.name, user_init, cc_comment, deptname))

    if h_artart == 2 or h_artart == 7 or h_artart == 11 or h_artart == 12:

        if balance == 0:
            closed = True
            pass
            h_bill.flag = 1

            if h_artart == 11 or h_artart == 12:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 739)]})

                if htparam.flogical:
                    fl_code1 = 1
            pass
    succed = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 88)]})
    p_88 = htparam.flogical
    pass
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()