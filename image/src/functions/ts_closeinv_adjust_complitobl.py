from functions.additional_functions import *
import decimal
from models import H_bill, Artikel, H_bill_line, H_artikel, Kellner, Htparam, H_umsatz, Umsatz, Arrangement, Argt_line, Billjournal, H_journal, H_compli

def ts_closeinv_adjust_complitobl(rec_h_bill:int, p_sign:int, p_artnr:int, h_artart:int, curr_dept:int, pay_type:int, double_currency:bool, exchg_rate:decimal, price_decimal:int, user_init:str):
    balance_foreign = 0
    balance = 0
    t_h_bill_list = []
    h_bill = artikel = h_bill_line = h_artikel = kellner = htparam = h_umsatz = umsatz = arrangement = argt_line = billjournal = h_journal = h_compli = None

    t_h_bill = artikel1 = h_bline = h_art = fr_art = kellner1 = kellne1 = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Artikel1 = Artikel
    H_bline = H_bill_line
    H_art = H_artikel
    Fr_art = Artikel
    Kellner1 = Kellner
    Kellne1 = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance_foreign, balance, t_h_bill_list, h_bill, artikel, h_bill_line, h_artikel, kellner, htparam, h_umsatz, umsatz, arrangement, argt_line, billjournal, h_journal, h_compli
        nonlocal artikel1, h_bline, h_art, fr_art, kellner1, kellne1


        nonlocal t_h_bill, artikel1, h_bline, h_art, fr_art, kellner1, kellne1
        nonlocal t_h_bill_list
        return {"balance_foreign": balance_foreign, "balance": balance, "t-h-bill": t_h_bill_list}

    def adjust_complito():

        nonlocal balance_foreign, balance, t_h_bill_list, h_bill, artikel, h_bill_line, h_artikel, kellner, htparam, h_umsatz, umsatz, arrangement, argt_line, billjournal, h_journal, h_compli
        nonlocal artikel1, h_bline, h_art, fr_art, kellner1, kellne1


        nonlocal t_h_bill, artikel1, h_bline, h_art, fr_art, kellner1, kellne1
        nonlocal t_h_bill_list

        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
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
        Artikel1 = Artikel
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

                h_umsatz = db_session.query(H_umsatz).filter(
                        (H_umsatz.artnr == h_art.artnr) &  (H_umsatz.departement == h_art.departement) &  (H_umsatz.datum == h_bline.bill_datum)).first()

                if h_umsatz and pay_type == 5:
                    h_umsatz.betrag = h_umsatz.betrag - p_sign * h_bline.betrag
                    h_umsatz.anzahl = h_umsatz.anzahl - p_sign * h_bline.anzahl

                    h_umsatz = db_session.query(H_umsatz).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == h_art.artnrfront) &  (Umsatz.departement == h_art.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()

                if umsatz:
                    umsatz.betrag = umsatz.betrag - p_sign * h_bline.betrag
                    umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl

                    umsatz = db_session.query(Umsatz).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == umsatz.artnr) &  (Artikel.departement == umsatz.departement)).first()

                if artikel.artart == 9:
                    amount = p_sign * h_bline.betrag
                    rest_betrag = amount

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.argtnr == artikel.artgrp)).first()

                    for argt_line in db_session.query(Argt_line).filter(
                            (Argt_line.argtnr == arrangement.argtnr)).all():

                        if argt_line.betrag != 0:
                            argt_betrag = p_sign * argt_line.betrag * h_bline.anzahl

                            if double_currency or artikel.pricetab:
                                argt_betrag = round(argt_betrag * exchg_rate, price_decimal)
                        else:
                            argt_betrag = amount * argt_line.vt_percnt / 100
                            argt_betrag = round(argt_betrag, price_decimal)


                        rest_betrag = rest_betrag - argt_betrag

                        artikel1 = db_session.query(Artikel1).filter(
                                (Artikel1.artnr == argt_line.argt_artnr) &  (Artikel1.departement == argt_line.departement)).first()

                        umsatz = db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()

                        if not umsatz:
                            umsatz = Umsatz()
                            db_session.add(umsatz)

                            umsatz.artnr = artikel1.artnr
                            umsatz.datum = h_bline.bill_datum
                            umsatz.departement = artikel1.departement


                        umsatz.betrag = umsatz.betrag - argt_betrag
                        umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl

                        umsatz = db_session.query(Umsatz).first()
                        billjournal = Billjournal()
                        db_session.add(billjournal)

                        billjournal.rechnr = h_bline.rechnr
                        billjournal.artnr = artikel1.artnr
                        billjournal.anzahl = - p_sign * h_bline.anzahl
                        billjournal.betrag = - argt_betrag
                        billjournal.bezeich = artikel1.bezeich +\
                                "<" + to_string(h_bline.departement, "99") + ">"
                        billjournal.departement = artikel1.departement
                        billjournal.epreis = 0
                        billjournal.zeit = get_current_time_in_seconds()
                        billjournal.userinit = user_init
                        billjournal.bill_datum = h_bline.bill_datum

                        billjournal = db_session.query(Billjournal).first()

                    artikel1 = db_session.query(Artikel1).filter(
                            (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == arrangement.intervall)).first()

                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()

                    if not umsatz:
                        umsatz = Umsatz()
                        db_session.add(umsatz)

                        umsatz.artnr = artikel1.artnr
                        umsatz.datum = h_bline.bill_datum
                        umsatz.departement = artikel1.departement


                    umsatz.betrag = umsatz.betrag - rest_betrag
                    umsatz.anzahl = umsatz.anzahl - p_sign * h_bline.anzahl

                    umsatz = db_session.query(Umsatz).first()
                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = h_bline.rechnr
                    billjournal.artnr = artikel1.artnr
                    billjournal.anzahl = - p_sign * h_bline.anzahl
                    billjournal.betrag = - rest_betrag
                    billjournal.bezeich = artikel1.bezeich +\
                            "<" + to_string(h_bline.departement, "99") + ">"
                    billjournal.departement = artikel1.departement
                    billjournal.epreis = 0
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.userinit = user_init
                    billjournal.bill_datum = h_bline.bill_datum

                    billjournal = db_session.query(Billjournal).first()

                if h_bline.artnr != f_disc and h_bline.artnr != b_disc and h_bline.artnr != o_disc:

                    h_journal = db_session.query(H_journal).filter(
                            (H_journal.bill_datum == h_bline.bill_datum) &  (H_journal.zeit == h_bline.zeit) &  (H_journal.sysdate == h_bline.sysdate) &  (H_journal.artnr == h_bline.artnr) &  (H_journal.departement == h_bline.departement)).first()
                    h_journal.fremdwaehrng = h_bline.fremdwbetrag
                    h_journal.betrag = h_bline.betrag

                    h_journal = db_session.query(H_journal).first()

                h_bill = db_session.query(H_bill).first()
                h_bill.gesamtumsatz = h_bill.gesamtumsatz - p_sign * h_bline.betrag
                h_bill.mwst[98] = h_bill.mwst[98] - p_sign * (h_service_foreign + h_mwst_foreign) * h_bline.anzahl
                h_bill.saldo = h_bill.saldo - p_sign * (h_service + h_mwst) * h_bline.anzahl

                h_bill = db_session.query(H_bill).first()
                balance_foreign = h_bill.mwst[98]
                balance = h_bill.saldo

                if h_artart == 11:
                    h_compli = H_compli()
                    db_session.add(h_compli)

                    h_compli.datum = h_bline.bill_datum
                    h_compli.departement = h_bline.departement
                    h_compli.rechnr = h_bline.rechnr
                    h_compli.artnr = h_bline.artnr
                    h_compli.anzahl = p_sign * h_bline.anzahl
                    h_compli.epreis = h_bline.epreis
                    h_compli.p_artnr = p_artnr

                    h_compli = db_session.query(H_compli).first()

            h_bline = db_session.query(H_bline).filter(
                    (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == curr_dept)).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_h_bill)).first()
    adjust_complito()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_h_bill)).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()