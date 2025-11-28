#using conversion tools version: 1.0.0.119
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_newbillbl import create_newbillbl
from models import Bill, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal

def bookcall2bl(pvilanguage:int, zinr:string, calldate:date, calltime:int, destination:string, duration:int, 
                rufnummer:string, amount:Decimal, user_init:string):

    prepare_cache ([Bill, Res_line, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal])

    success = False
    rechnr = 0
    lvcarea:string = "bookcall2"
    bil_recid:int = 0
    epreis:Decimal = to_decimal("0.0")
    artnr:int = 0
    resnr:int = 0
    billno:int = 0
    master_flag:bool = False
    bill_date:date = None
    usr_init:string = ""
    bookflag:int = 0
    price_decimal:int = 0
    foreign_rate:bool = False
    double_currency:bool = False
    exchg_rate:Decimal = 1
    amount_foreign:Decimal = to_decimal("0.0")
    calls_type:int = 0
    bill = res_line = htparam = artikel = waehrung = counters = bill_line = umsatz = billjournal = None

    bill1 = None

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session
    zinr = zinr.strip()
    destination = destination.strip()
    rufnummer = rufnummer.strip()
    last_count:int = 0
    error_lock:string = ""


    def generate_output():
        nonlocal success, rechnr, lvcarea, bil_recid, epreis, artnr, resnr, billno, master_flag, bill_date, usr_init, bookflag, price_decimal, foreign_rate, double_currency, exchg_rate, amount_foreign, calls_type, bill, res_line, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal
        nonlocal pvilanguage, zinr, calldate, calltime, destination, duration, rufnummer, amount, user_init
        nonlocal bill1


        nonlocal bill1

        return {"success": success, "rechnr": rechnr}


    if zinr == "":

        return generate_output()

    res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, zinr)]})

    if not res_line:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 13)],"zinr": [(eq, zinr)]})

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    if substring(rufnummer, 0, 2) == ("00").lower() :
        calls_type = 2

    elif substring(rufnummer, 0, 1) == ("0").lower() :
        calls_type = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 113)]})
    artnr = htparam.finteger

    artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, 0)]})

    if not artikel:

        return generate_output()

    if calls_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 114)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

        if artikel:
            artnr = htparam.finteger

    elif calls_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 115)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

        if artikel:
            artnr = htparam.finteger
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 114)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)],"artart": [(eq, 0)]})

            if artikel:
                artnr = htparam.finteger

    bill1 = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"reslinnr": [(eq, res_line.reslinnr)],"resnr": [(eq, res_line.resnr)]})

    if not bill1:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 335)]})
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 317)]})
    usr_init = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 559)]})

    if htparam.flogical and length(rufnummer) > 3:
        rufnummer = substring(rufnummer, 0, length(rufnummer) - 3)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    amount_foreign =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if foreign_rate or double_currency:

        if artikel.pricetab and artikel.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)],"ankauf": [(ne, 0)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if double_currency:
        amount_foreign =  to_decimal(amount)
        amount =  to_decimal(amount) * to_decimal(exchg_rate)

    elif foreign_rate:
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)
    amount =  to_decimal(round (amount , price_decimal))

    if billno > 1:

        bill = get_cache (Bill, {"resnr": [(eq, bill1.resnr)],"parent_nr": [(eq, bill1.parent_nr)],"billnr": [(eq, billno)],"flag": [(eq, 0)],"zinr": [(eq, bill1.zinr)]})

        if not bill:
            bil_recid = get_output(create_newbillbl(res_line._recid, bill1.parent_nr, billno))

            # bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
            bill = db_session.query(Bill).filter(Bill._recid == bil_recid).with_for_update().first()
    else:

        # bill = get_cache (Bill, {"_recid": [(eq, bill1._recid)]})
        bill = db_session.query(Bill).filter(Bill._recid == bill1._recid).with_for_update().first()

    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)
    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
    bill.rgdruck = 0
    bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
    bill.mwst[98] = bill.mwst[98] + amount_foreign
    bill.datum = bill_date

    if bill.rechnr == 0:

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()
        counters.counter = counters.counter + 1
        bill.rechnr = counters.counter
 
    bill_line = Bill_line()
    db_session.add(bill_line)

    bill_line.rechnr = bill.rechnr
    bill_line.massnr = bill.resnr
    bill_line.billin_nr = bill.reslinnr
    bill_line.artnr = artnr
    bill_line.bezeich = artikel.bezeich + " - " +\
            substring(rufnummer, 0, length(rufnummer))
    bill_line.anzahl = 1
    bill_line.betrag =  to_decimal(amount)
    bill_line.fremdwbetrag =  to_decimal(amount_foreign)
    bill_line.zinr = zinr
    bill_line.departement = artikel.departement
    bill_line.epreis =  to_decimal(epreis)
    bill_line.zeit = get_current_time_in_seconds()
    bill_line.userinit = usr_init
    bill_line.arrangement = res_line.arrangement
    bill_line.bill_datum = bill_date
    bill_line.origin_id = "CALLS" + " " + to_string(calldate) + ";" +\
            to_string(calltime, "HH:MM") + ";" + rufnummer + ";" +\
            destination + ";" + to_string(duration, "HH:MM:SS") + ";"


    pass

    # umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})
    umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artnr) &
                (Umsatz.departement == 0) &
                (Umsatz.datum == bill_date)).with_for_update().first()

    if not umsatz:
        umsatz = Umsatz()
        db_session.add(umsatz)

        umsatz.artnr = artnr
        umsatz.datum = bill_date
        umsatz.departement = 0
    umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
    umsatz.anzahl = umsatz.anzahl + 1
    pass
    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill.rechnr
    billjournal.artnr = artnr
    billjournal.anzahl = 1
    billjournal.betrag =  to_decimal(amount)
    billjournal.fremdwaehrng =  to_decimal(amount_foreign)
    billjournal.bezeich = artikel.bezeich + " - " + substring(rufnummer, 0, length(rufnummer))
    billjournal.zinr = zinr
    billjournal.departement = artikel.departement
    billjournal.epreis =  to_decimal(epreis)
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date
    pass
    pass
    success = True
    rechnr = bill.rechnr

    return generate_output()