# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - import from function_py
"""
# ============================
# Rd, 24/11/2025, update last_count for counter update
# ============================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.create_newbillbl import create_newbillbl
from functions_py.create_newbillbl import create_newbillbl
from models import Htparam, Queasy, Res_line, Waehrung, Exrate, Artikel, Bill, Counters, Bill_line, Umsatz, Billjournal
from functions.next_counter_for_update import next_counter_for_update


def nt_postdefferedrental():

    prepare_cache([Htparam, Res_line, Waehrung, Exrate, Artikel, Bill, Counters, Bill_line, Umsatz, Billjournal])

    art_deposit: int = 0
    user_init: str = ""
    new_contrate: bool = False
    billno: int = 0
    userinit: str = ""
    bill_date: date = None
    exchg_rate = 1
    ex_rate = to_decimal("0.0")
    frate = to_decimal("0.0")
    price_decimal: int = 0
    bil_recid: int = 0
    billart: int = 0
    qty: int = 0
    double_currency: bool = False
    foreign_rate: bool = False
    master_str: str = ""
    master_exist: bool = False
    master_rechnr: str = ""
    curr_posting: str = ""
    department: int = ""
    description: str = ""
    amount_foreign = to_decimal("0.0")
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    htparam = queasy = res_line = waehrung = exrate = artikel = bill = counters = bill_line = umsatz = billjournal = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock = ""


    def generate_output():
        nonlocal art_deposit, user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, department, description, amount_foreign, price, amount, htparam, queasy, res_line, waehrung, exrate, artikel, bill, counters, bill_line, umsatz, billjournal

        return {}

    def deff_charge():
        nonlocal art_deposit, user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, bil_recid, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, department, description, amount_foreign, price, amount, htparam, queasy, res_line, waehrung, exrate, artikel, bill, counters, bill_line, umsatz, billjournal

        currzeit: int = 0
        i: int = 0
        n: int = 0
        currzeit = get_current_time_in_seconds() - 3

        res_line_obj_list = {}
        for res_line, queasy in db_session.query(Res_line, Queasy).join(Queasy, (Queasy.key == 301) & (Queasy.number1 == Res_line.resnr) & (Queasy.logi1)).filter(
                (Res_line.active_flag == 1) & (Res_line.zinr != "") & (Res_line.ankunft <= bill_date) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resnr, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            frate = to_decimal(res_line.reserve_dec)

            if res_line.reserve_dec != 0:
                if res_line.ankunft == bill_date:
                    waehrung = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        frate = to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                else:
                    exrate = get_cache(
                        Exrate, {"datum": [(eq, res_line.ankunft)], "artnr": [(eq, res_line.betriebsnr)]})

                    if exrate:
                        frate = to_decimal(exrate.betrag)

            elif res_line.betriebsnr != 0:
                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                frate = to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:

                if res_line.adrflag:
                    frate = to_decimal("1")
                else:
                    frate = to_decimal(exchg_rate)

            if res_line.zipreis == 0 and res_line.resstatus == 6:
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, art_deposit)]})

                if artikel:
                    price = to_decimal(res_line.zipreis)
                    description = artikel.bezeich
                    qty = 1
                    department = artikel.departement
                    billart = artikel.artnr

                    if foreign_rate or double_currency:
                        if not res_line.adrflag:
                            amount_foreign = to_decimal(price)
                        else:
                            amount_foreign = to_decimal(
                                price) / to_decimal(exchg_rate)
                    else:
                        amount_foreign = to_decimal("0")
                    amount = to_decimal(
                        round(price) * to_decimal(frate, price_decimal))

                    if foreign_rate and price_decimal == 0:
                        htparam = get_cache(Htparam, {"paramnr": [(eq, 145)]})

                        if htparam.finteger != 0:
                            n = 1
                            for i in range(1, htparam.finteger + 1):
                                n = n * 10
                            amount = to_decimal(round(amount / n, 0) * n)
                    currzeit = currzeit + 3

                    update_bill(currzeit)

    def update_bill(currzeit: int):
        nonlocal art_deposit, user_init, new_contrate, billno, userinit, bill_date, exchg_rate, ex_rate, frate, price_decimal, billart, qty, double_currency, foreign_rate, master_str, master_exist, master_rechnr, curr_posting, department, description, amount_foreign, price, amount, htparam, queasy, res_line, waehrung, exrate, artikel, bill, counters, bill_line, umsatz, billjournal

        master_flag: bool = False
        bil_recid: int = 0
        bill1 = None
        Bill1 = create_buffer("Bill1", Bill)

        bill = get_cache(
            Bill, {"zinr": [(eq, res_line.zinr)], "resnr": [(eq, res_line.resnr)], "billtyp": [(eq, 0)], "parent_nr": [(eq, res_line.reslinnr)], "billnr": [(eq, billno)], "flag": [(eq, 0)]})

        if not bill:
            bill1 = get_cache(
                Bill, {"zinr": [(eq, res_line.zinr)], "gastnr": [(eq, res_line.gastnrpay)], "resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "billtyp": [(eq, 0)], "billnr": [(eq, 1)], "flag": [(eq, 0)]})
            bil_recid = get_output(create_newbillbl(
                res_line.resnr, res_line.reslinnr, bill1.parent_nr, billno))

            bill = get_cache(
                Bill, {"_recid": [(eq, bil_recid)]})
        bill.argtumsatz = to_decimal(bill.argtumsatz) + to_decimal(amount)
        bill.gesamtumsatz = to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        bill.rgdruck = 0
        bill.datum = bill_date
        bill.saldo = to_decimal(bill.saldo) + to_decimal(amount)
        bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.rechnr == 0:
            # counters = get_cache(
            #     Counters, {"counter_no": [(eq, 3)]})
            # counters.counter = counters.counter + 1
            # bill.rechnr = counters.counter
            last_count, error_lock = get_output(next_counter_for_update(3))
            bill.rechnr = last_count
            
        bill_line = Bill_line()

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = billart
        bill_line.bezeich = description
        bill_line.anzahl = qty
        bill_line.betrag = to_decimal(amount)
        bill_line.fremdwbetrag = to_decimal(amount_foreign)
        bill_line.zinr = res_line.zinr
        bill_line.departement = department
        bill_line.epreis = to_decimal(price)
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr
        bill_line.zeit = currzeit
        bill_line.userinit = userinit
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date

        db_session.add(bill_line)

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, billart)], "departement": [(eq, department)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = billart
            umsatz.datum = bill_date
            umsatz.departement = department

            db_session.add(umsatz)

        umsatz.betrag = to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + qty

        billjournal = Billjournal()

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = billart
        billjournal.anzahl = qty
        billjournal.betrag = to_decimal(amount)
        billjournal.fremdwaehrng = to_decimal(amount_foreign)
        billjournal.bezeich = description
        billjournal.zinr = res_line.zinr
        billjournal.departement = department
        billjournal.epreis = to_decimal(price)
        billjournal.zeit = currzeit
        billjournal.userinit = userinit
        billjournal.bill_datum = bill_date
        billjournal.comment = to_string(res_line.resnr) + ";" +\
            to_string(res_line.reslinnr)

        db_session.add(billjournal)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 84)]})
    billno = htparam.finteger

    if billno == 0:
        billno = 1

    if billno > 2:
        billno = 2

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:
        art_deposit = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 104)]})
    user_init = htparam.fchar
    deff_charge()

    return generate_output()
