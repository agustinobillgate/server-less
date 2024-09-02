from functions.additional_functions import *
import decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from models import Htparam, Res_line, Waehrung, Arrangement, Artikel, Bill, Counters, Bill_line, Umsatz, Billjournal, Argt_line

def post_dayuse(resnr:int, reslinnr:int):
    user_init:str = ""
    master_flag:bool = False
    gastnrmember:int = 0
    amount:decimal = 0
    amount_foreign:decimal = 0
    description:str = ""
    bill_date:date = None
    price_decimal:int = 0
    exchg_rate:decimal = 1
    ex_rate:decimal = 0
    double_currency:bool = False
    foreign_rate:bool = False
    billart:int = 0
    qty:int = 1
    curr_room:str = ""
    cancel_str:str = ""
    master_str:str = ""
    master_rechnr:str = ""
    curr_department:int = 0
    price:decimal = 0
    currzeit:int = 0
    i:int = 0
    n:int = 1
    htparam = res_line = waehrung = arrangement = artikel = bill = counters = bill_line = umsatz = billjournal = argt_line = None

    artikel1 = None

    Artikel1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, master_flag, gastnrmember, amount, amount_foreign, description, bill_date, price_decimal, exchg_rate, ex_rate, double_currency, foreign_rate, billart, qty, curr_room, cancel_str, master_str, master_rechnr, curr_department, price, currzeit, i, n, htparam, res_line, waehrung, arrangement, artikel, bill, counters, bill_line, umsatz, billjournal, argt_line
        nonlocal artikel1


        nonlocal artikel1
        return {}

    def tax_service(currzeit:int):

        nonlocal user_init, master_flag, gastnrmember, amount, amount_foreign, description, bill_date, price_decimal, exchg_rate, ex_rate, double_currency, foreign_rate, billart, qty, curr_room, cancel_str, master_str, master_rechnr, curr_department, price, currzeit, i, n, htparam, res_line, waehrung, arrangement, artikel, bill, counters, bill_line, umsatz, billjournal, argt_line
        nonlocal artikel1


        nonlocal artikel1

        service:decimal = 0
        vat:decimal = 0
        service_foreign:decimal = 0
        vat_foreign:decimal = 0
        argt_betrag0:decimal = 0
        argt_betrag:decimal = 0
        rest_betrag:decimal = 0
        rm_vat:bool = False
        rm_serv:bool = False
        post_it:bool = False
        Artikel1 = Artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 127)).first()
        rm_vat = not htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 128)).first()
        rm_serv = not htparam.flogical
        rest_betrag = amount

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():
            post_it = False
            argt_betrag0, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
            argt_betrag = round (argt_betrag0 * ex_rate, price_decimal)

            artikel1 = db_session.query(Artikel1).filter(
                    (Artikel1.artnr == argt_line.argt_artnr) &  (Artikel1.departement == argt_line.departement)).first()

            if argt_line.fakt_modus == 1:
                post_it = True

            elif argt_line.fakt_modus == 2 or argt_line.fakt_modus == 3:

                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.rechnr == bill.rechnr) &  (Billjournal.artnr == artikel1.artnr) &  (Billjournal.betrag == argt_betrag) &  (Billjournal.departement == artikel1.departement)).first()

                if not billjournal:
                    post_it = True

            elif argt_line.fakt_modus == 4:

                if get_day(bill_date) == 1:
                    post_it = True

            elif argt_line.fakt_modus == 5:

                if get_day(bill_date + 1) == 1:
                    post_it = True

            if post_it and argt_betrag != 0:
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
                billjournal.fremdwaehrng = argt_betrag0
                billjournal.betrag = argt_betrag
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()

        artikel1 = db_session.query(Artikel1).filter(
                (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == artikel.departement)).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement
        umsatz.betrag = umsatz.betrag + rest_betrag
        umsatz.anzahl = umsatz.anzahl + 1

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = round (rest_betrag / exchg_rate , 2)
        billjournal.betrag = rest_betrag
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currzeit
        billjournal.stornogrund = ""
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
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == artikel.departement)).first()
                service = service * amount_foreign / 100
                service_foreign = round (service, 2)

                if double_currency:
                    service = round (service * exchg_rate, price_decimal)
                else:
                    service = round (service, price_decimal)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = 1
                bill_line.fremdwbetrag = service_foreign
                bill_line.betrag = service
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 1
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr

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
                umsatz.anzahl = umsatz.anzahl + 1

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = service_foreign
                billjournal.betrag = service
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 1
                billjournal.stornogrund = ""
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
                        (Artikel1.artnr == htparam.finteger) &  (Artikel1.departement == artikel.departement)).first()

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat = vat * (amount_foreign + service_foreign) / 100
                else:
                    vat = vat * amount_foreign / 100
                vat_foreign = round (vat, 2)

                if double_currency:
                    vat = round (vat * exchg_rate, price_decimal)
                else:
                    vat = round (vat, price_decimal)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel1.artnr
                bill_line.bezeich = artikel1.bezeich
                bill_line.anzahl = 1
                bill_line.fremdwbetrag = vat_foreign
                bill_line.betrag = vat
                bill_line.zinr = res_line.zinr
                bill_line.departement = artikel1.departement
                bill_line.epreis = 0
                bill_line.zeit = currzeit + 2
                bill_line.userinit = user_init
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr

                bill_line = db_session.query(Bill_line).first()

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel1.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = artikel1.departement
                umsatz.betrag = umsatz.betrag + vat
                umsatz.anzahl = umsatz.anzahl + 1

                umsatz = db_session.query(Umsatz).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel1.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = vat_foreign
                billjournal.betrag = vat
                billjournal.bezeich = artikel1.bezeich
                billjournal.zinr = res_line.zinr
                billjournal.departement = artikel1.departement
                billjournal.epreis = 0
                billjournal.zeit = currzeit + 2
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                billjournal = db_session.query(Billjournal).first()
        bill.saldo = bill.saldo + vat + service
        bill.mwst[98] = bill.mwst[98] + vat_foreign + service_foreign


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 104)).first()
    user_init = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    gastnrmember = res_line.gastnrmember
    price = res_line.zipreis
    amount = res_line.zipreis
    curr_room = res_line.zinr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if double_currency or foreign_rate or res_line.betriebsnr != 0:

        if res_line.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == res_line.betriebsnr)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

            if res_line.adrflag and res_line.betriebsnr == 0:
                exchg_rate = 1
            amount_foreign = res_line.zipreis
            amount = round (res_line.zipreis * exchg_rate, price_decimal)

            if foreign_rate and price_decimal == 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 145)).first()

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,finteger + 1) :
                        n = n * 10
                    amount = round(amount / n, 0) * n

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_line.arrangement)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  (Artikel.artnr == arrangement.argt_artikelnr)).first()
    billart = artikel.artnr
    description = arrangement.argt_rgbez

    bill = db_session.query(Bill).filter(
            (Bill.resnr == resnr) &  (Bill.reslinnr == reslinnr) &  (Bill.zinr == res_line.zinr) &  (Billnr == 1)).first()
    currzeit = get_current_time_in_seconds()
    master_flag = update_masterbill(currzeit)

    if not master_flag:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        bill = db_session.query(Bill).filter(
                (Bill.resnr == resnr) &  (Bill.reslinnr == reslinnr) &  (Bill.zinr == res_line.zinr) &  (Billnr == 1)).first()

        if artikel.umsatzart == 1:
            bill.logisumsatz = bill.logisumsatz + amount

        elif artikel.umsatzart == 2:
            bill.argtumsatz = bill.argtumsatz + amount

        elif artikel.umsatzart == 3:
            bill.f_b_umsatz = bill.f_b_umsatz + amount

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz = bill.sonst_umsatz + amount

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
            bill.gesamtumsatz = bill.gesamtumsatz + amount
        bill.rgdruck = 0
        bill.saldo = bill.saldo + amount
        bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.datum < bill_date:
            bill.datum = bill_date

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()
            counters = counters + 1
            bill.rechnr = counters

            counters = db_session.query(Counters).first()
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artikel.artnr
        bill_line.bezeich = description
        bill_line.anzahl = 1
        bill_line.betrag = amount
        bill_line.fremdwbetrag = amount_foreign
        bill_line.zinr = res_line.zinr
        bill_line.departement = artikel.departement
        bill_line.zeit = currzeit
        bill_line.userinit = user_init
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr

        if double_currency:
            bill_line.epreis = amount_foreign
        else:
            bill_line.epreis = amount

        bill_line = db_session.query(Bill_line).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement
        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + 1

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag = amount
        billjournal.fremdwaehrng = amount_foreign
        billjournal.bezeich = description
        billjournal.zinr = res_line.zinr
        billjournal.departement = artikel.departement

        if double_currency:
            billjournal.epreis = amount_foreign
        else:
            billjournal.epreis = amount
        billjournal.zeit = currzeit
        billjournal.stornogrund = ""
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()
        tax_service(currzeit)

        bill = db_session.query(Bill).first()

    return generate_output()