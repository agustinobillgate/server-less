#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, H_bill, H_bill_line, Queasy, Htparam, H_umsatz, Artikel, Kellner, Kellne1, Umsatz, H_compli, Arrangement, Argt_line, Billjournal

def ts_restinv_btn_transfer_paytype56bl(rec_id:int, guestnr:int, curr_dept:int, balance_foreign:Decimal, balance:Decimal, pay_type:int, transdate:date, double_currency:bool, exchg_rate:Decimal, price_decimal:int, user_init:string):

    prepare_cache ([H_bill, Queasy, Htparam, H_umsatz, Artikel, Umsatz, H_compli, Arrangement, Argt_line, Billjournal])

    payment_exist = False
    p_artnr = 0
    billart = 0
    qty = 0
    description = ""
    price = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    bill_date = None
    fl_code = 0
    t_h_artikel_list = []
    h_artikel = h_bill = h_bill_line = queasy = htparam = h_umsatz = artikel = kellner = kellne1 = umsatz = h_compli = arrangement = argt_line = billjournal = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        return {"payment_exist": payment_exist, "p_artnr": p_artnr, "billart": billart, "qty": qty, "description": description, "price": price, "amount_foreign": amount_foreign, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-artikel": t_h_artikel_list}

    def check_payment():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        h_bline = None
        h_art = None
        fdisc:int = 0
        bdisc:int = 0
        odisc:int = 0
        tot_disc:Decimal = to_decimal("0.0")
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)

        h_bline = db_session.query(H_bline).filter(
                 (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == h_bill.departement)).first()
        while None != h_bline:

            if h_bline.artnr == 0:
                payment_exist = True
            else:

                h_art = db_session.query(H_art).filter(
                         (H_art.artnr == h_bline.artnr) & (H_art.departement == h_bline.departement)).first()

                if h_art.artart != 0:
                    payment_exist = True

                if (h_bline.artnr == fdisc or h_bline.artnr == bdisc or h_bline.artnr == odisc):
                    tot_disc =  to_decimal(tot_disc) + to_decimal(h_bline.betrag)

            curr_recid = h_bline._recid
            h_bline = db_session.query(H_bline).filter(
                     (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == h_bill.departement) & (H_bline._recid > curr_recid)).first()

        if payment_exist:
            fl_code = 1

            return

        if tot_disc != 0:
            fl_code = 2
            payment_exist = True


    def release_tbplan():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, h_bill.departement)],"number2": [(eq, h_bill.tischnr)]})

        if queasy:
            pass
            queasy.number3 = 0
            queasy.date1 = None


            pass
            pass


    def fill_mcoupon(dept:int, artno:int):

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, artno)],"departement": [(eq, - dept)],"betriebsnr": [(eq, dept)],"datum": [(eq, bill_date)]})

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = artno
            h_umsatz.departement = - dept
            h_umsatz.betriebsnr = dept
            h_umsatz.datum = bill_date


        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung
        pass
        pass


    def adjust_complito():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        h_mwst:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst_foreign:Decimal = to_decimal("0.0")
        h_service_foreign:Decimal = to_decimal("0.0")
        epreis:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        amount_foreign:Decimal = to_decimal("0.0")
        cost:Decimal = to_decimal("0.0")
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        f_eknr:int = 0
        b_eknr:int = 0
        f_disc:int = 0
        b_disc:int = 0
        o_disc:int = 0
        h_bline = None
        h_art = None
        fr_art = None
        kellner1 = None
        kellne1 = None
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        Kellner1 =  create_buffer("Kellner1",Kellner)
        Kellne1 =  create_buffer("Kellne1",Kellner)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        f_disc = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
        b_disc = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
        o_disc = htparam.finteger

        kellner1 = db_session.query(Kellner1).filter(
                 (Kellner1.kellner_nr == h_bill.kellner_nr) & (Kellner1.departement == curr_dept)).first()

        kellne1 = get_cache (Kellne1, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, curr_dept)]})

        h_bline = db_session.query(H_bline).filter(
                 (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == curr_dept)).first()
        while None != h_bline:

            h_art = db_session.query(H_art).filter(
                     (H_art.artnr == h_bline.artnr) & (H_art.departement == h_bline.departement)).first()

            if h_art and h_art.artart == 0:
                h_service =  to_decimal("0")
                h_mwst =  to_decimal("0")
                h_service_foreign =  to_decimal("0")
                h_mwst_foreign =  to_decimal("0")
                amount =  to_decimal("0")
                amount_foreign =  to_decimal("0")

                artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, h_art.departement)]})

                if artikel.artart == 9 and artikel.artgrp != 0:
                    adjust_revbdown(h_bline.bill_datum, - h_bline.betrag, - h_bline.anzahl)

                h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})

                if h_umsatz and pay_type == 5:
                    h_umsatz.betrag =  to_decimal(h_umsatz.betrag) - to_decimal(h_bline.betrag)
                    h_umsatz.anzahl = h_umsatz.anzahl - h_bline.anzahl
                    pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})

                if umsatz:
                    umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(h_bline.betrag)
                    umsatz.anzahl = umsatz.anzahl - h_bline.anzahl
                    pass
                pass
                h_bill.gesamtumsatz =  to_decimal(h_bill.gesamtumsatz) - to_decimal(h_bline.betrag)
                h_bill.mwst[98] = h_bill.mwst[98] - (h_service_foreign + h_mwst_foreign) * h_bline.anzahl
                h_bill.saldo =  to_decimal(h_bill.saldo) - to_decimal((h_service) + to_decimal(h_mwst)) * to_decimal(h_bline.anzahl)
                pass
            balance_foreign =  to_decimal(h_bill.mwst[98])
            balance =  to_decimal(h_bill.saldo)

            if pay_type == 5:
                h_compli = H_compli()
                db_session.add(h_compli)

                h_compli.datum = h_bline.bill_datum
                h_compli.departement = h_bline.departement
                h_compli.rechnr = h_bline.rechnr
                h_compli.artnr = h_bline.artnr
                h_compli.anzahl = h_bline.anzahl
                h_compli.epreis =  to_decimal(h_bline.epreis)
                h_compli.p_artnr = p_artnr
                pass

            curr_recid = h_bline._recid
            h_bline = db_session.query(H_bline).filter(
                     (H_bline.rechnr == h_bill.rechnr) & (H_bline.departement == curr_dept) & (H_bline._recid > curr_recid)).first()


    def adjust_revbdown(bill_date:date, amount:Decimal, qty:int):

        nonlocal payment_exist, p_artnr, billart, description, price, amount_foreign, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal rec_id, guestnr, curr_dept, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, price_decimal, user_init


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

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
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    if h_bill.kellner_nr != to_int(user_init):
        h_bill.kellner_nr = to_int(user_init)
    check_payment()

    if payment_exist:

        return generate_output()
    p_artnr = guestnr
    adjust_complito()

    h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, p_artnr)]})
    billart = h_artikel.artnr
    qty = h_bill.belegung
    description = h_artikel.bezeich
    price =  to_decimal("0")
    amount_foreign =  - to_decimal(balance_foreign)
    amount =  - to_decimal(balance)

    if pay_type == 6:
        fill_mcoupon(curr_dept, p_artnr)
    release_tbplan()

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

    return generate_output()