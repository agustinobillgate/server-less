#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Waehrung, Reservation, Bediener, Debitor, Umsatz, Billjournal

def deposit_pay_btn_exitbl(pvilanguage:int, resnr:int, artnr:int, depositgef:Decimal, payment:Decimal, deposit_exrate:Decimal, voucher_str:string, user_init:string):

    prepare_cache ([Htparam, Artikel, Waehrung, Reservation, Bediener, Debitor, Umsatz, Billjournal])

    msg_str = ""
    error_flag = False
    deposit_pay = to_decimal("0.0")
    exchg_rate:Decimal = 1
    foreign_payment:Decimal = to_decimal("0.0")
    local_payment:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    depoart:int = 0
    deposit_balance:Decimal = to_decimal("0.0")
    lvcarea:string = "deposit-pay"
    htparam = artikel = waehrung = reservation = bediener = debitor = umsatz = billjournal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, deposit_balance, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal
        nonlocal pvilanguage, resnr, artnr, depositgef, payment, deposit_exrate, voucher_str, user_init

        return {"msg_str": msg_str, "error_flag": error_flag, "deposit_pay": deposit_pay}

    def calculate_amount(amount:Decimal):

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, deposit_balance, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal
        nonlocal pvilanguage, resnr, artnr, depositgef, payment, deposit_exrate, voucher_str, user_init

        avrg_kurs:Decimal = 1
        pay_exrate:Decimal = 1

        def generate_inner_output():
            return (amount)


        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                pay_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


        deposit_pay = to_decimal(- round(amount * pay_exrate / deposit_exrate , 2))

        if artikel.pricetab:
            foreign_payment =  to_decimal(amount)
            amount =  to_decimal(amount) * to_decimal(exchg_rate)
            amount = to_decimal(round(amount , price_decimal))


        else:
            foreign_payment =  to_decimal(amount) / to_decimal(exchg_rate)
        local_payment =  to_decimal(amount)

        return generate_inner_output()


    def deposit_payment1():

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, deposit_balance, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal
        nonlocal pvilanguage, resnr, artnr, depositgef, payment, deposit_exrate, voucher_str, user_init

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate
        reservation.depositgef =  to_decimal(depositgef)
        reservation.depositbez =  to_decimal(deposit_pay)
        reservation.zahldatum = bill_date
        reservation.zahlkonto = artikel.artnr


        create_journal(bill_date)


    def deposit_payment2():

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, deposit_balance, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal
        nonlocal pvilanguage, resnr, artnr, depositgef, payment, deposit_exrate, voucher_str, user_init

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate
        reservation.depositgef =  to_decimal(depositgef)
        reservation.depositbez2 =  to_decimal(reservation.depositbez2) + to_decimal(deposit_pay)
        reservation.zahldatum2 = bill_date
        reservation.zahlkonto2 = artikel.artnr


        create_journal(bill_date)


    def create_journal(bill_date:date):

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, deposit_balance, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal
        nonlocal pvilanguage, resnr, artnr, depositgef, payment, deposit_exrate, voucher_str, user_init

        if artikel.artart == 2 or artikel.artart == 7:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo =  - to_decimal(local_payment)
            debitor.vesrdep =  - to_decimal(foreign_payment)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


            debitor.vesrcod = translateExtended ("Deposit payment - ResNo:", lvcarea, "") + " " + to_string(resnr)

            if voucher_str != "":
                debitor.vesrcod = debitor.vesrcod + "; " + voucher_str
            pass

        umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, artikel.artnr)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(local_payment)


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(foreign_payment)
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = reservation.resnr


        billjournal.bezeich = artikel.bezeich + "[" + translateExtended ("Deposit", lvcarea, "") + " #" + to_string(reservation.resnr) + "]" + voucher_str
        billjournal.betrag =  to_decimal(local_payment)
        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date


        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(local_payment)
        umsatz.anzahl = umsatz.anzahl + 1


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  - to_decimal(foreign_payment)
        billjournal.betrag =  - to_decimal(local_payment)
        billjournal.bezeich = artikel.bezeich +\
                " [#" + to_string(reservation.resnr) + " " + artikel.bezeich + "]" + voucher_str


        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

    if not artikel or artikel.artart != 5:
        error_flag = True
        msg_str = translateExtended ("Deposit article not defined.", lvcarea, "")

        return generate_output()
    depoart = artikel.artnr

    artikel = db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.artnr == artnr)).first()

    if not artikel:
        error_flag = True
        msg_str = translateExtended ("payment article not defined.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    payment = calculate_amount(payment)

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:

        if reservation.depositbez != 0:

            if reservation.depositbez2 != 0:
                deposit_balance =  to_decimal(depositgef) - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)
            else:
                deposit_balance =  to_decimal(depositgef) - to_decimal(reservation.depositbez)

            if deposit_balance == 0:

                return generate_output()

        if reservation.depositbez == 0:
            deposit_payment1()
        else:
            deposit_payment2()
        pass

    return generate_output()