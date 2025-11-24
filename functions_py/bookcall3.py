#using conversion tools version: 1.0.0.119
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal
from functions.next_counter_for_update import next_counter_for_update

def bookcall3(bil_recid:int, calldate:date, calltime:int, destination:string, duration:int, rufnummer:string, amount:Decimal):

    prepare_cache ([Bill, Htparam, Artikel, Waehrung, Counters, Bill_line, Umsatz, Billjournal])

    success = False
    rechno = 0
    variable = None
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
    bill = htparam = artikel = waehrung = counters = bill_line = umsatz = billjournal = None

    bill1 = None

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session
    last_count:int = 0
    error_lock:string = ""


    def generate_output():
        nonlocal success, rechno, variable, epreis, artnr, resnr, billno, master_flag, bill_date, usr_init, bookflag, price_decimal, foreign_rate, double_currency, exchg_rate, amount_foreign, calls_type, bill, htparam, artikel, waehrung, counters, bill_line, umsatz, billjournal
        nonlocal bil_recid, calldate, calltime, destination, duration, rufnummer, amount
        nonlocal bill1


        nonlocal bill1

        return {"success": success, "rechno": rechno}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 113)]})
    artnr = htparam.finteger

    artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, 0)]})

    if not artikel:

        return generate_output()

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

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()

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
    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)
    bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
    bill.rgdruck = 0
    bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
    bill.mwst[98] = bill.mwst[98] + amount_foreign
    bill.datum = bill_date

    if bill.rechnr == 0:

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        # counters.counter = counters.counter + 1
        # bill.rechnr = counters.counter
        last_count, error_lock = get_output(next_counter_for_update(3))
        bill.rechnr = last_count
        
        pass
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
    bill_line.zinr = bill.zinr
    bill_line.departement = artikel.departement
    bill_line.epreis =  to_decimal(epreis)
    bill_line.zeit = get_current_time_in_seconds()
    bill_line.userinit = usr_init
    bill_line.bill_datum = bill_date
    bill_line.origin_id = "CALLS" + " " + to_string(calldate) + ";" +\
            to_string(calltime, "HH:MM") + ";" + rufnummer + ";" +\
            destination + ";" + to_string(duration, "HH:MM:SS") + ";"


    pass

    umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

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
    billjournal.bezeich = artikel.bezeich + " - " +\
            substring(rufnummer, 0, length(rufnummer))
    billjournal.departement = artikel.departement
    billjournal.epreis =  to_decimal(epreis)
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date


    pass
    pass
    rechno = bill.rechnr
    success = True

    return generate_output()