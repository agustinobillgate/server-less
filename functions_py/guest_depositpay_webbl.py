#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Waehrung, Billjournal, Umsatz, Bediener, Debitor

def guest_depositpay_webbl(pvilanguage:int, user_init:string, guest_number:int, guest_name:string, deposit_pay_num:int, deposit_pay_desc:string, deposit_pay_amt:Decimal, voucher_number:string):

    prepare_cache ([Htparam, Artikel, Waehrung, Billjournal, Umsatz, Bediener, Debitor])

    error_desc = ""
    lvcarea:string = "guest-depositPay-web"
    exchg_rate:Decimal = 1
    foreign_payment:Decimal = to_decimal("0.0")
    deposit_amount:Decimal = to_decimal("0.0")
    deposit_foreign:Decimal = to_decimal("0.0")
    local_depo_pay:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    bill_date:date = None
    depoart:int = 0
    depobez:string = ""
    sys_id:string = ""
    htparam = artikel = waehrung = billjournal = umsatz = bediener = debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_desc, lvcarea, exchg_rate, foreign_payment, deposit_amount, deposit_foreign, local_depo_pay, price_decimal, bill_date, depoart, depobez, sys_id, htparam, artikel, waehrung, billjournal, umsatz, bediener, debitor
        nonlocal pvilanguage, user_init, guest_number, guest_name, deposit_pay_num, deposit_pay_desc, deposit_pay_amt, voucher_number

        return {"error_desc": error_desc}

    def calculate_amount(amount:Decimal):

        nonlocal error_desc, lvcarea, exchg_rate, foreign_payment, deposit_amount, deposit_foreign, local_depo_pay, price_decimal, bill_date, depoart, depobez, sys_id, htparam, artikel, waehrung, billjournal, umsatz, bediener, debitor
        nonlocal pvilanguage, user_init, guest_number, guest_name, deposit_pay_num, deposit_pay_desc, deposit_pay_amt, voucher_number

        pay_exrate:Decimal = 1

        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                pay_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if artikel.pricetab:
            foreign_payment =  to_decimal(amount)
            deposit_foreign =  - to_decimal(amount)
            amount =  to_decimal(amount) * to_decimal(exchg_rate)
            amount = to_decimal(round(amount , price_decimal))


        else:
            foreign_payment =  to_decimal(amount) / to_decimal(exchg_rate)
            deposit_foreign =  - to_decimal(foreign_payment)
        local_depo_pay =  to_decimal(amount)
        deposit_amount =  - to_decimal(amount)


    def create_journal():

        nonlocal error_desc, lvcarea, exchg_rate, foreign_payment, deposit_amount, deposit_foreign, local_depo_pay, price_decimal, bill_date, depoart, depobez, sys_id, htparam, artikel, waehrung, billjournal, umsatz, bediener, debitor
        nonlocal pvilanguage, user_init, guest_number, guest_name, deposit_pay_num, deposit_pay_desc, deposit_pay_amt, voucher_number


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(deposit_foreign)
        billjournal.betrag =  to_decimal(deposit_amount)
        billjournal.bezeich = depobez +\
                " [GuestNo#" + to_string(guest_number) + " " + artikel.bezeich + "]" + voucher_number
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        pass
        pass

        # umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == depoart) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).with_for_update().with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit_amount)


        pass
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(foreign_payment)
        billjournal.betrag =  to_decimal(local_depo_pay)
        billjournal.bezeich = artikel.bezeich +\
                "[" + translateExtended ("Guest Deposit #", lvcarea, "") + to_string(guest_number) + "]" + voucher_number
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = guest_number
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        pass
        pass

        # umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).with_for_update().with_for_update().with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(local_depo_pay)


        pass
        pass

        if artikel.artart == 2 or artikel.artart == 7:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = guest_number
            debitor.gastnrmember = guest_number
            debitor.saldo =  to_decimal(deposit_amount)
            debitor.vesrdep =  to_decimal(deposit_foreign)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = guest_name
            debitor.vesrcod = translateExtended ("Guest Deposit Payment - GuestNo:", lvcarea, "") +\
                    " " + to_string(guest_number)

            if voucher_number != "":
                debitor.vesrcod = debitor.vesrcod + "; " + voucher_number
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_desc = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart = artikel.artnr
        depobez = artikel.bezeich

    artikel = db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.artnr == deposit_pay_num)).first()

    if not artikel:
        error_desc = translateExtended ("Payment article not defined.", lvcarea, "")

        return generate_output()

    if guest_number == None or guest_number == 0:
        error_desc = translateExtended ("Guest number is not yet defined. Please save the guest card first.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    deposit_pay_amt =  to_decimal(deposit_pay_amt)
    calculate_amount(deposit_pay_amt)
    create_journal()

    return generate_output()
