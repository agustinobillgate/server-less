from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, H_bill, H_bill_line, Queasy, Htparam, H_umsatz, Artikel, Kellner, Kellne1, Umsatz, H_compli, Arrangement, Argt_line, Billjournal

def ts_restinv_btn_transfer_paytype56bl(rec_id:int, guestnr:int, curr_dept:int, balance_foreign:decimal, balance:decimal, pay_type:int, transdate:date, double_currency:bool, exchg_rate:decimal, price_decimal:int, user_init:str):
    payment_exist = False
    p_artnr = 0
    billart = 0
    qty = 0
    description = ""
    price = 0
    amount_foreign = 0
    amount = 0
    bill_date = None
    fl_code = 0
    t_h_artikel_list = []
    h_artikel = h_bill = h_bill_line = queasy = htparam = h_umsatz = artikel = kellner = kellne1 = umsatz = h_compli = arrangement = argt_line = billjournal = None

    t_h_artikel = h_bline = h_art = fr_art = kellner1 = kellne1 = artikel1 = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_bline = H_bill_line
    H_art = H_artikel
    Fr_art = Artikel
    Kellner1 = Kellner
    Kellne1 = Kellner
    Artikel1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list
        return {"payment_exist": payment_exist, "p_artnr": p_artnr, "billart": billart, "qty": qty, "description": description, "price": price, "amount_foreign": amount_foreign, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-artikel": t_h_artikel_list}

    def check_payment():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list

        fdisc:int = 0
        bdisc:int = 0
        odisc:int = 0
        tot_disc:decimal = 0
        H_bline = H_bill_line
        H_art = H_artikel

        h_bline = db_session.query(H_bline).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == h_bill.departement)).first()
        while None != h_bline:

            if h_bline.artnr == 0:
                payment_exist = True
            else:

                h_art = db_session.query(H_art).filter(
                        (H_art.artnr == h_bline.artnr) &  (H_art.departement == h_bline.departement)).first()

                if h_art.artart != 0:
                    payment_exist = True

                if (h_bline.artnr == fdisc or h_bline.artnr == bdisc or h_bline.artnr == odisc):
                    tot_disc = tot_disc + h_bline.betrag

            h_bline = db_session.query(H_bline).filter(
                    (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == h_bill.departement)).first()

        if payment_exist:
            fl_code = 1

            return

        if tot_disc != 0:
            fl_code = 2
            payment_exist = True

    def release_tbplan():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == h_bill.departement) &  (Queasy.number2 == h_bill.tischnr)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.number3 = 0
            queasy.date1 = None

            queasy = db_session.query(Queasy).first()


    def fill_mcoupon(dept:int, artno:int):

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list

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

        h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == artno) &  (H_umsatz.departement == - dept) &  (H_umsatz.betriebsnr == dept) &  (H_umsatz.datum == bill_date)).first()

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = artno
            h_umsatz.departement = - dept
            h_umsatz.betriebsnr = dept
            h_umsatz.datum = bill_date


        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung

        h_umsatz = db_session.query(H_umsatz).first()

    def adjust_complito():

        nonlocal payment_exist, p_artnr, billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list

        h_mwst:decimal = 0
        h_service:decimal = 0
        h_mwst_foreign:decimal = 0
        h_service_foreign:decimal = 0
        epreis:decimal = 0
        amount:decimal = 0
        amount_foreign:decimal = 0
        cost:decimal = 0
        f_cost:decimal = 0
        b_cost:decimal = 0
        f_eknr:int = 0
        b_eknr:int = 0
        f_disc:int = 0
        b_disc:int = 0
        o_disc:int = 0
        H_bline = H_bill_line
        H_art = H_artikel
        Fr_art = Artikel
        Kellner1 = Kellner
        Kellne1 = Kellner

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()
        f_disc = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 596)).first()
        b_disc = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 556)).first()
        o_disc = htparam.finteger

        kellner1 = db_session.query(Kellner1).filter(
                (Kellner1.kellner_nr == h_bill.kellner_nr) &  (Kellner1.departement == curr_dept)).first()

        kellne1 = db_session.query(Kellne1).filter(
                (Kellne1.kellner_nr == h_bill.kellner_nr) &  (Kellne1.departement == curr_dept)).first()

        h_bline = db_session.query(H_bline).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == curr_dept)).first()
        while None != h_bline:

            h_art = db_session.query(H_art).filter(
                    (H_art.artnr == h_bline.artnr) &  (H_art.departement == h_bline.departement)).first()

            if h_art and h_art.artart == 0:
                h_service = 0
                h_mwst = 0
                h_service_foreign = 0
                h_mwst_foreign = 0
                amount = 0
                amount_foreign = 0

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == h_art.departement)).first()

                if artikel.artart == 9 and artikel.artgrp != 0:
                    adjust_revbdown(h_bline.bill_datum, - h_bline.betrag, - h_bline.anzahl)

                h_umsatz = db_session.query(H_umsatz).filter(
                        (H_umsatz.artnr == h_art.artnr) &  (H_umsatz.departement == h_art.departement) &  (H_umsatz.datum == h_bline.bill_datum)).first()

                if h_umsatz and pay_type == 5:
                    h_umsatz.betrag = h_umsatz.betrag - h_bline.betrag
                    h_umsatz.anzahl = h_umsatz.anzahl - h_bline.anzahl

                    h_umsatz = db_session.query(H_umsatz).first()

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == h_art.artnrfront) &  (Umsatz.departement == h_art.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()

            if umsatz:
                umsatz.betrag = umsatz.betrag - h_bline.betrag
                umsatz.anzahl = umsatz.anzahl - h_bline.anzahl

                umsatz = db_session.query(Umsatz).first()

            h_bill = db_session.query(H_bill).first()
            h_bill.gesamtumsatz = h_bill.gesamtumsatz - h_bline.betrag
            h_bill.mwst[98] = h_bill.mwst[98] - (h_service_foreign + h_mwst_foreign) * h_bline.anzahl
            h_bill.saldo = h_bill.saldo - (h_service + h_mwst) * h_bline.anzahl

            h_bill = db_session.query(H_bill).first()
        balance_foreign = h_bill.mwst[98]
        balance = h_bill.saldo

        if pay_type == 5:
            h_compli = H_compli()
            db_session.add(h_compli)

            h_compli.datum = h_bline.bill_datum
            h_compli.departement = h_bline.departement
            h_compli.rechnr = h_bline.rechnr
            h_compli.artnr = h_bline.artnr
            h_compli.anzahl = h_bline.anzahl
            h_compli.epreis = h_bline.epreis
            h_compli.p_artnr = p_artnr

            h_compli = db_session.query(H_compli).first()

        h_bline = db_session.query(H_bline).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == curr_dept)).first()

    def adjust_revbdown(bill_date:date, amount:decimal, qty:int):

        nonlocal payment_exist, p_artnr, billart, description, price, amount_foreign, bill_date, fl_code, t_h_artikel_list, h_artikel, h_bill, h_bill_line, queasy, htparam, h_umsatz, artikel, kellner, kellne1, umsatz, h_compli, arrangement, argt_line, billjournal
        nonlocal h_bline, h_art, fr_art, kellner1, kellne1, artikel1


        nonlocal t_h_artikel, h_bline, h_art, fr_art, kellner1, kellne1, artikel1
        nonlocal t_h_artikel_list

        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
        Artikel1 = Artikel
        rest_betrag = amount

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == artikel.artgrp)).first()

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr)).all():

            if argt_line.betrag != 0:
                argt_betrag = argt_line.betrag * qty

                if double_currency or artikel.pricetab:
                    argt_betrag = round(argt_betrag * exchg_rate, price_decimal)
            else:
                argt_betrag = amount * argt_line.vt_percnt / 100
                argt_betrag = round(argt_betrag, price_decimal)
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

            billjournal.rechnr = h_bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = qty
            billjournal.fremdwaehrng = argt_line.betrag
            billjournal.betrag = argt_betrag
            billjournal.bezeich = artikel1.bezeich +\
                    "<" + to_string(h_bill.departement, "99") + ">"
            billjournal.departement = artikel1.departement
            billjournal.epreis = 0
            billjournal.zeit = get_current_time_in_seconds()
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

        billjournal.rechnr = h_bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = qty
        billjournal.betrag = rest_betrag
        billjournal.bezeich = artikel1.bezeich +\
                "<" + to_string(h_bill.departement, "99") + ">"
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    if h_bill.kellner_nr != to_int(user_init):
        h_bill.kellner_nr = to_int(user_init)
    check_payment()

    if payment_exist:

        return generate_output()
    p_artnr = guestnr
    adjust_complito()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  (H_artikel.artnr == p_artnr)).first()
    billart = h_artikel.artnr
    qty = h_bill.belegung
    description = h_artikel.bezeich
    price = 0
    amount_foreign = - balance_foreign
    amount = - balance

    if pay_type == 6:
        fill_mcoupon(curr_dept, p_artnr)
    release_tbplan()

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

    return generate_output()