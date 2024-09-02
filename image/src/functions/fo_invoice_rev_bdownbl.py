from functions.additional_functions import *
import decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from models import Artikel, Bill, Arrangement, Htparam, Res_line, Argt_line, Umsatz, Billjournal, Bill_line

def fo_invoice_rev_bdownbl(bil_recid:int, currzeit:int, exchg_rate:decimal, amount:decimal, t_artnr:int, t_dept:int, arran_argtnr:int, price_decimal:int, bill_date:date, curr_room:str, cancel_str:str, user_init:str, curr_department:int, qty:int, double_currency:bool, foreign_rate:bool, price:decimal, balance_foreign:decimal):
    balance = 0
    rm_vat:bool = False
    rm_serv:bool = False
    service:decimal = 0
    vat:decimal = 0
    service_foreign:decimal = 0
    vat_foreign:decimal = 0
    rest_betrag:decimal = 0
    argt_betrag:decimal = 0
    frate:decimal = 0
    p_sign:int = 1
    qty1:int = 0
    ex_rate:decimal = 0
    artikel = bill = arrangement = htparam = res_line = argt_line = umsatz = billjournal = bill_line = None

    artikel1 = None

    Artikel1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, rm_vat, rm_serv, service, vat, service_foreign, vat_foreign, rest_betrag, argt_betrag, frate, p_sign, qty1, ex_rate, artikel, bill, arrangement, htparam, res_line, argt_line, umsatz, billjournal, bill_line
        nonlocal artikel1


        nonlocal artikel1
        return {"balance": balance}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == t_artnr) &  (Artikel.departement == t_dept)).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement.argtnr == arran_argtnr)).first()

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

            if argt_line.vt_percnt == 0:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.erwachs * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

            elif argt_line.vt_percnt == 1:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind1 * p_sign
                else:
                    qty1 = argt_line.betriebsnr * p_sign

            elif argt_line.vt_percnt == 2:

                if argt_line.betriebsnr == 0:
                    qty1 = res_line.kind2 * p_sign
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
            (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == curr_department)).first()

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
                    (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == curr_department)).first()
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
                    (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == curr_department)).first()

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

    return generate_output()