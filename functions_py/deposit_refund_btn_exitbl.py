#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Artikel, Htparam, Umsatz, Billjournal, Bediener, Debitor

def deposit_refund_btn_exitbl(pvilanguage:int, resnr:int, artnr:int, payment:Decimal, deposit_pay:Decimal, user_init:string, depoart:int, depobezeich:string):

    prepare_cache ([Artikel, Htparam, Umsatz, Billjournal, Bediener, Debitor])

    balance = to_decimal("0.0")
    t_reservation_data = []
    lvcarea:string = "deposit-refund"
    reservation = artikel = htparam = umsatz = billjournal = bediener = debitor = None

    t_reservation = None

    t_reservation_data, T_reservation = create_model_like(Reservation)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, t_reservation_data, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor
        nonlocal pvilanguage, resnr, artnr, payment, deposit_pay, user_init, depoart, depobezeich


        nonlocal t_reservation
        nonlocal t_reservation_data

        return {"balance": balance, "t-reservation": t_reservation_data}

    def deposit_payment1():

        nonlocal balance, t_reservation_data, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor
        nonlocal pvilanguage, resnr, artnr, payment, deposit_pay, user_init, depoart, depobezeich


        nonlocal t_reservation
        nonlocal t_reservation_data

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate
        reservation.depositbez =  to_decimal(reservation.depositbez) - to_decimal(payment)
        reservation.zahldatum = None
        reservation.zahlkonto = 0

        umsatz = db_session.query(Umsatz).filter(
            (Umsatz.departement == 0) & (Umsatz.artnr == artikel.artnr) & (Umsatz.datum == bill_date)
        ).with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)
            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit_pay)
        billjournal = Billjournal()
        db_session.add(billjournal)
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(deposit_pay)
        billjournal.bezeich = artikel.bezeich + " " + to_string(reservation.resnr)
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        umsatz = db_session.query(Umsatz).filter(
            (Umsatz.artnr == depoart) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)
        ).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)
            umsatz.artnr = depoart
            umsatz.datum = bill_date

        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(deposit_pay)
        umsatz.anzahl = umsatz.anzahl + 1
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag =  - to_decimal(deposit_pay)
        billjournal.bezeich = depobezeich + " " + to_string(reservation.resnr)
        billjournal.epreis =  to_decimal("0")
        billjournal.billjou_ref = artikel.artnr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        if artikel.artart == 7:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo =  - to_decimal(deposit_pay)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


    def deposit_payment2():

        nonlocal balance, t_reservation_data, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor
        nonlocal pvilanguage, resnr, artnr, payment, deposit_pay, user_init, depoart, depobezeich


        nonlocal t_reservation
        nonlocal t_reservation_data

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if payment > reservation.depositbez2:
            reservation.depositbez =  to_decimal(reservation.depositbez) - to_decimal(payment) + to_decimal(reservation.depositbez2)
            reservation.depositbez2 =  to_decimal("0")
        else:
            reservation.depositbez2 =  to_decimal(reservation.depositbez2) - to_decimal(payment)
        reservation.zahldatum = None
        reservation.zahldatum2 = None
        reservation.zahlkonto2 = 0

        umsatz = db_session.query(Umsatz).filter(
            (Umsatz.departement == 0) & (Umsatz.artnr == artikel.artnr) & (Umsatz.datum == bill_date)
        ).with_for_update().first()
        
        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)
            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit_pay)
        
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(deposit_pay)
        billjournal.bezeich = artikel.bezeich + " [" + translateExtended ("Refund", lvcarea, "") + " #" + to_string(reservation.resnr) + "]"
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = reservation.resnr

        umsatz = db_session.query(Umsatz).filter(
            (Umsatz.artnr == depoart) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)
        ).first()
        
        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date
        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(deposit_pay)
        umsatz.anzahl = umsatz.anzahl + 1

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag =  - to_decimal(deposit_pay)
        billjournal.bezeich = depobezeich + " " + to_string(reservation.resnr)
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if artikel.artart == 7:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo =  - to_decimal(deposit_pay)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


            debitor.vesrcod = translateExtended ("Deposit Refund - ResNo:", lvcarea, "") + " " + to_string(resnr)


    artikel = db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag) & (Artikel.artnr == artnr)).first()

    reservation = db_session.query(Reservation).filter(Reservation.resnr == resnr).with_for_update().first() 

    if reservation.depositbez == 0:
        deposit_payment1()
    else:
        deposit_payment2()

    t_reservation = T_reservation()
    t_reservation_data.append(t_reservation)
    buffer_copy(reservation, t_reservation)

    return generate_output()