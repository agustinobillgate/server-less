from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Artikel, Bill, Htparam, Waehrung, Counters, Bill_line, Umsatz, Billjournal, Master, Mast_art
from functions.next_counter_for_update import next_counter_for_update

def book_article(zinr:str, artnr:int, dept:int, anzahl:int):
    success = False
    amount:decimal = to_decimal("0.0")
    resnr:int = 0
    billno:int = 0
    master_flag:bool = False
    bill_date:date = None
    user_init:str = ""
    bookflag:int = 0
    double_currency:bool = False
    exchg_rate:decimal = 1
    amount_foreign:decimal = to_decimal("0.0")
    res_line = artikel = bill = htparam = waehrung = counters = bill_line = umsatz = billjournal = master = mast_art = None


    db_session = local_storage.db_session
    last_count = 0
    error_lock:str = ""

    def generate_output():
        nonlocal success, amount, resnr, billno, master_flag, bill_date, user_init, bookflag, double_currency, exchg_rate, amount_foreign, res_line, artikel, bill, htparam, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, artnr, dept, anzahl

        return {"success": success}

    def update_masterbill():

        nonlocal success, amount, resnr, billno, master_flag, bill_date, user_init, bookflag, double_currency, exchg_rate, amount_foreign, res_line, artikel, bill, htparam, waehrung, counters, bill_line, umsatz, billjournal, master, mast_art
        nonlocal zinr, artnr, dept, anzahl

        master_flag = False
        bookflag = 1
        mbill = None
        resline = None
        umsart:int = 0

        def generate_inner_output():
            return (master_flag, bookflag)

        Mbill =  create_buffer("Mbill",Bill)
        Resline =  create_buffer("Resline",Res_line)

        master = db_session.query(Master).filter(
                 (Master.resnr == resnr) & (Master.active) & (Master.flag == 0)).first()

        if not master:

            return generate_inner_output()
        umsart = artikel.umsatzart

        if master.umsatzart[umsart - 1] :
            master_flag = True
        else:

            mast_art = db_session.query(Mast_art).filter(
                     (Mast_art.resnr == master.resnr) & (Mast_art.departement == artikel.departement) & (Mast_art.artnr == artikel.artnr)).first()

            if mast_art:
                master_flag = True

        if master_flag:

            mbill = db_session.query(Mbill).filter(
                     (Mbill.resnr == resnr) & (Mbill.reslinnr == 0)).first()

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

                # counters = db_session.query(Counters).filter(
                #          (Counters.counter_no == 3)).first()
                # counters.counter = counters.counter + 1
                # mbill.rechnr = counters.counter
                last_count, error_lock = get_output(next_counter_for_update(3))
                mbill.rechnr = last_count
                master.rechnr = mbill.rechnr
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

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == bill_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = artnr
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement
            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
            umsatz.anzahl = umsatz.anzahl + anzahl
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
        bookflag = 0
        success = True

        return generate_inner_output()

    if anzahl == 0:

        return generate_output()

    res_line = db_session.query(Res_line).filter(
             (Res_line.resstatus == 6) & (func.lower(Res_line.zinr) == (zinr).lower())).first()

    if not res_line:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 13) & (func.lower(Res_line.zinr) == (zinr).lower())).first()

        if not res_line:

            return generate_output()
    resnr = res_line.resnr

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == artnr) & (Artikel.departement == dept)).first()

    if not artikel:

        return generate_output()

    bill = db_session.query(Bill).filter(
             (Bill.zinr == res_line.zinr) & (Bill.reslinnr == res_line.reslinnr) & (Bill.resnr == res_line.resnr)).first()

    if not bill:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 317)).first()
    user_init = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    amount_foreign =  to_decimal(artikel.epreis) * to_decimal(anzahl)
    amount =  to_decimal(amount_foreign) * to_decimal(exchg_rate)
    master_flag, bookflag = update_masterbill()

    if bookflag > 0:

        return generate_output()

    if not master_flag:

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

            # counters = db_session.query(Counters).filter(
            #          (Counters.counter_no == 3)).first()
            # counters.counter = counters.counter + 1
            # bill.rechnr = counters.counter
            last_count, error_lock = get_output(next_counter_for_update(3))
            bill.rechnr = last_count
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.massnr = bill.resnr
        bill_line.billin_nr = bill.reslinnr
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

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == artnr) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artnr
            umsatz.datum = bill_date
            umsatz.departement = 0
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + anzahl
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
        success = True

    return generate_output()