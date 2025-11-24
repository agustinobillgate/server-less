#using conversion tools version: 1.0.0.119
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Htparam, Artikel, Waehrung, Bill, Counters, Bill_line, Umsatz, Billjournal, Master, Mast_art
from functions.next_counter_for_update import next_counter_for_update
def bookmini(zinr:string, artnr:int, dept:int, anzahl:int, amount:Decimal):

    prepare_cache ([Res_line, Htparam, Artikel, Waehrung, Bill, Counters, Bill_line, Umsatz, Billjournal, Master])

    billno = 0
    success = False
    resnr:int = 0
    master_flag:bool = False
    bill_date:date = None
    user_init:string = ""
    bookflag:int = 0
    double_currency:bool = False
    exchg_rate:Decimal = 1
    amount_foreign:Decimal = to_decimal("0.0")
    res_line = htparam = artikel = waehrung = bill = counters = bill_line = umsatz = billjournal = master = mast_art = None

    db_session = local_storage.db_session
    zinr = zinr.strip()
    last_count:int = 0
    error_lock:string = ""

    def generate_output():
        nonlocal billno, success, resnr, master_flag, bill_date, user_init, bookflag, double_currency, exchg_rate, amount_foreign, res_line, htparam, artikel, waehrung, bill, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, artnr, dept, anzahl, amount

        return {"billno": billno, "success": success}

    def update_masterbill():

        nonlocal billno, success, resnr, master_flag, bill_date, user_init, bookflag, double_currency, exchg_rate, amount_foreign, res_line, htparam, artikel, waehrung, bill, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, artnr, dept, anzahl, amount

        master_flag = False
        bookflag = -1
        umsart:int = 0
        mbill = None
        resline = None

        def generate_inner_output():
            return (master_flag, bookflag)

        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)

        master = get_cache (Master, {"resnr": [(eq, resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if not master:

            return generate_inner_output()

        mast_art = get_cache (Mast_art, {"resnr": [(eq, master.resnr)],"departement": [(eq, artikel.departement)],"artnr": [(eq, artikel.artnr)]})

        if mast_art:
            master_flag = True

        if master_flag:

            mbill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)]})

            if not mbill:

                return generate_inner_output()

            if artikel.umsatzart == 1:
                mbill.logisumsatz =  to_decimal(mbill.logisumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 2:
                mbill.argtumsatz =  to_decimal(mbill.argtumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 3:
                mbill.f_b_umsatz =  to_decimal(mbill.f_b_umsatz) + to_decimal(amount)

            elif artikel.umsatzart == 4:
                mbill.sonst_umsatz =  to_decimal(mbill.sonst_umsatz) + to_decimal(amount)
            mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(amount)
            mbill.rgdruck = 0
            mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(amount)
            mbill.mwst[98] = mbill.mwst[98] + amount_foreign
            mbill.datum = bill_date

            if mbill.rechnr == 0:

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                # counters.counter = counters.counter + 1
                # mbill.rechnr = counters.counter
                last_count, error_lock = get_output(next_counter_for_update(3))
                mbill.rechnr = last_count

                pass
                pass
                master.rechnr = mbill.rechnr
                pass
            billno = mbill.rechnr
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = mbill.rechnr
            bill_line.artnr = artnr
            bill_line.bezeich = artikel.bezeich
            bill_line.anzahl = anzahl
            bill_line.betrag =  to_decimal(amount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = zinr
            bill_line.departement = artikel.departement
            bill_line.epreis =  to_decimal(artikel.epreis)
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.arrangement = res_line.arrangement
            bill_line.bill_datum = bill_date


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + anzahl
            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = mbill.rechnr
            billjournal.artnr = artnr
            billjournal.anzahl = anzahl
            billjournal.betrag =  to_decimal(amount)
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = zinr
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(artikel.epreis)
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date


            pass
            pass
        bookflag = 0
        success = True

        return generate_inner_output()

    res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, zinr)]})

    if not res_line:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 13)],"zinr": [(eq, zinr)]})

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    if anzahl == 0:
        anzahl = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 570)]})
    dept = htparam.finteger

    artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, dept)]})

    if not artikel:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 317)]})
    user_init = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    elif artikel.pricetab:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if artikel.epreis == 0:
        amount =  to_decimal(anzahl)
        anzahl = 1
    else:
        amount =  to_decimal(anzahl) * to_decimal(artikel.epreis)
    amount_foreign =  to_decimal(amount)
    amount =  to_decimal(amount_foreign) * to_decimal(exchg_rate)
    master_flag, bookflag = update_masterbill()

    if bookflag > 0:

        return generate_output()

    if not master_flag:

        bill = get_cache (Bill, {"zinr": [(eq, res_line.zinr)],"reslinnr": [(eq, res_line.reslinnr)],"resnr": [(eq, res_line.resnr)]})

        if not bill:

            return generate_output()

        if artikel.umsatzart == 1:
            bill.logisumsatz =  to_decimal(bill.logisumsatz) + to_decimal(amount)

        elif artikel.umsatzart == 2:
            bill.argtumsatz =  to_decimal(bill.argtumsatz) + to_decimal(amount)

        elif artikel.umsatzart == 3:
            bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(amount)

        elif artikel.umsatzart == 4:
            bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(amount)

        if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
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
        billno = bill.rechnr
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artnr
        bill_line.bezeich = artikel.bezeich
        bill_line.anzahl = anzahl
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.zinr = zinr
        bill_line.departement = artikel.departement
        bill_line.epreis =  to_decimal(artikel.epreis)
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date


        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artnr
            umsatz.datum = bill_date
            umsatz.departement = dept


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + anzahl
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artnr
        billjournal.anzahl = anzahl
        billjournal.betrag =  to_decimal(amount)
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.bezeich = artikel.bezeich
        billjournal.zinr = zinr
        billjournal.departement = artikel.departement
        billjournal.epreis =  to_decimal(artikel.epreis)
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        pass
        pass
        success = True

    return generate_output()