from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_newbillbl import create_newbillbl
from models import Bill, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal

def bookcall2bl(pvilanguage:int, zinr:str, calldate:date, calltime:int, destination:str, duration:int, rufnummer:str, amount:decimal, user_init:str):
    success = False
    rechnr = 0
    lvcarea:str = "bookcall2"
    bil_recid:int = 0
    epreis:decimal = 0
    artnr:int = 0
    resnr:int = 0
    billno:int = 0
    master_flag:bool = False
    bill_date:date = None
    usr_init:str = ""
    bookflag:int = 0
    price_decimal:int = 0
    foreign_rate:bool = False
    double_currency:bool = False
    exchg_rate:decimal = 1
    amount_foreign:decimal = 0
    calls_type:int = 0
    bill = res_line = htparam = artikel = waehrung = counters = bill_line = umsatz = billjournal = None

    bill1 = None

    Bill1 = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, rechnr, lvcarea, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, usr_init, bookflag, price_decimal, foreign_rate, double_currency, exchg_rate, amount_foreign, calls_type, bill, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal
        nonlocal bill1


        nonlocal bill1
        return {"success": success, "rechnr": rechnr}


    if zinr == "":

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resstatus == 6) &  (func.lower(Res_line.zinr) == (zinr).lower())).first()

    if not res_line:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 13) &  (func.lower(Res_line.zinr) == (zinr).lower())).first()

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    if substring(rufnummer, 0, 2) == "00":
        calls_type = 2

    elif substring(rufnummer, 0, 1) == "0":
        calls_type = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 113)).first()
    artnr = htparam.finteger

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == artnr) &  (Artikel.departement == 0)).first()

    if not artikel:

        return generate_output()

    if calls_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 114)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0) &  (Artikel.artart == 0)).first()

        if artikel:
            artnr = htparam.finteger

    elif calls_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 115)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0) &  (Artikel.artart == 0)).first()

        if artikel:
            artnr = htparam.finteger
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 114)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0) &  (Artikel.artart == 0)).first()

            if artikel:
                artnr = htparam.finteger

    bill1 = db_session.query(Bill1).filter(
            (Bill1.zinr == res_line.zinr) &  (Bill1.reslinnr == res_line.reslinnr) &  (Bill1.resnr == res_line.resnr)).first()

    if not bill1:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 335)).first()
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 317)).first()
    usr_init = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 559)).first()

    if htparam.flogical and len(rufnummer) > 3:
        rufnummer = substring(rufnummer, 0, len(rufnummer) - 3)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    amount_foreign = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if foreign_rate or double_currency:

        if artikel.pricetab and artikel.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.waehrungsnr == artikel.betriebsnr) &  (Waehrung.ankauf != 0)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit

    if double_currency:
        amount_foreign = amount
        amount = amount * exchg_rate

    elif foreign_rate:
        amount_foreign = amount / exchg_rate
    amount = round (amount, price_decimal)

    if billno > 1:

        where = query(where_list, filters=(lambda where :bill.resnr == bill1.resnr and bill.parent_nr == bill1.parent_nr and bill.billnr == billno and bill.flag == 0 and bill.zinr == bill1.zinr), bill=True)

        if not bill:
            bil_recid = get_output(create_newbillbl(res_line._recid, bill1.parent_nr, billno))

            bill = db_session.query(Bill).filter(
                        (Bill._recid == bil_recid)).first()
    else:

        bill = db_session.query(Bill).filter(
                    (Bill._recid == bill1._recid)).first()
    bill.sonst_umsatz = bill.sonst_umsatz + amount
    bill.gesamtumsatz = bill.gesamtumsatz + amount
    bill.rgdruck = 0
    bill.saldo = bill.saldo + amount
    bill.mwst[98] = bill.mwst[98] + amount_foreign
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
    bill_line.massnr = bill.resnr
    bill_line.billin_nr = bill.reslinnr
    bill_line.artnr = artnr
    bill_line.bezeich = artikel.bezeich + " - " +\
            substring(rufnummer, 0, len(rufnummer))
    bill_line.anzahl = 1
    bill_line.betrag = amount
    bill_line.fremdwbetrag = amount_foreign
    bill_line.zinr = zinr
    bill_line.departement = artikel.departement
    bill_line.epreis = epreis
    bill_line.zeit = get_current_time_in_seconds()
    bill_line.userinit = usr_init
    bill_line.arrangement = res_line.arrangement
    bill_line.bill_datum = bill_date
    bill_line.origin_id = "CALLS" + " " + to_string(calldate) + ";" +\
            to_string(calltime, "HH:MM") + ";" + rufnummer + ";" +\
            destination + ";" + to_string(duration, "HH:MM:SS") + ";"

    bill_line = db_session.query(Bill_line).first()

    umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artnr) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

    if not umsatz:
        umsatz = Umsatz()
        db_session.add(umsatz)

        umsatz.artnr = artnr
        umsatz.datum = bill_date
        umsatz.departement = 0
    umsatz.betrag = umsatz.betrag + amount
    umsatz.anzahl = umsatz.anzahl + 1

    umsatz = db_session.query(Umsatz).first()
    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill.rechnr
    billjournal.artnr = artnr
    billjournal.anzahl = 1
    billjournal.betrag = amount
    billjournal.fremdwaehrng = amount_foreign
    billjournal.bezeich = artikel.bezeich + " - " + substring(rufnummer, 0, len(rufnummer))
    billjournal.zinr = zinr
    billjournal.departement = artikel.departement
    billjournal.epreis = epreis
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date

    billjournal = db_session.query(Billjournal).first()

    bill = db_session.query(Bill).first()
    success = True
    rechnr = bill.rechnr

    return generate_output()