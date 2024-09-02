from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Artikel, Waehrung, Reservation, Bediener, Debitor, Umsatz, Billjournal

def deposit_pay_btn_exitbl(pvilanguage:int, resnr:int, artnr:int, depositgef:decimal, payment:decimal, deposit_exrate:decimal, voucher_str:str, user_init:str):
    msg_str = ""
    error_flag = False
    deposit_pay = 0
    exchg_rate:decimal = 1
    foreign_payment:decimal = 0
    local_payment:decimal = 0
    price_decimal:int = 0
    depoart:int = 0
    lvcarea:str = "deposit_pay"
    htparam = artikel = waehrung = reservation = bediener = debitor = umsatz = billjournal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal


        return {"msg_str": msg_str, "error_flag": error_flag, "deposit_pay": deposit_pay}

    def calculate_amount(amount:decimal):

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal

        avrg_kurs:decimal = 1
        pay_exrate:decimal = 1

        if artikel.pricetab:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if waehrung:
                pay_exrate = waehrung.ankauf / waehrung.einheit


        deposit_pay = - round(amount * pay_exrate / deposit_exrate, 2)

        if artikel.pricetab:
            foreign_payment = amount
            amount = amount * exchg_rate
            amount = round(amount, price_decimal)


        else:
            foreign_payment = amount / exchg_rate
        local_payment = amount

    def deposit_payment1():

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate
        reservation.depositgef = depositgef
        reservation.depositbez = deposit_pay
        reservation.zahldatum = bill_date
        reservation.zahlkonto = artikel.artnr


        create_journal(bill_date)

    def deposit_payment2():

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate
        reservation.depositgef = depositgef
        reservation.depositbez2 = reservation.depositbez2 + deposit_pay
        reservation.zahldatum2 = bill_date
        reservation.zahlkonto2 = artikel.artnr


        create_journal(bill_date)

    def create_journal(bill_date:date):

        nonlocal msg_str, error_flag, deposit_pay, exchg_rate, foreign_payment, local_payment, price_decimal, depoart, lvcarea, htparam, artikel, waehrung, reservation, bediener, debitor, umsatz, billjournal

        if artikel.artart == 2 or artikel.artart == 7:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo = - local_payment
            debitor.vesrdep = - foreign_payment
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


            debitor.vesrcod = translateExtended ("Deposit payment - ResNo:", lvcarea, "") + " " + to_string(resnr)

            if voucher_str != "":
                debitor.vesrcod = debitor.vesrcod + "; " + voucher_str


        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + local_payment

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = foreign_payment
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = reservation.resnr


        billjournal.bezeich = artikel.bezeich + "[" + translateExtended ("Deposit", lvcarea, "") + " #" + to_string(reservation.resnr) + "]" + voucher_str
        billjournal.betrag = local_payment

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == depoart) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date


        umsatz.betrag = umsatz.betrag - local_payment
        umsatz.anzahl = umsatz.anzahl + 1


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - foreign_payment
        billjournal.betrag = - local_payment
        billjournal.bezeich = artikel.bezeich +\
                " [#" + to_string(reservation.resnr) + " " + artikel.bezeich + "]" + voucher_str


        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

    pass

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

    if not artikel or artikel.artart != 5:
        error_flag = True
        msg_str = translateExtended ("Deposit article not defined.", lvcarea, "")

        return generate_output()
    depoart = artikel.artnr

    artikel = db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  ((Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.artnr == artnr)).first()

    if not artikel:
        error_flag = True
        msg_str = translateExtended ("payment article not defined.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    payment = calculate_amount(payment)

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    if reservation.depositbez == 0:
        deposit_payment1()
    else:
        deposit_payment2()

    reservation = db_session.query(Reservation).first()

    return generate_output()