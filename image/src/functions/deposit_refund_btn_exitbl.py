from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Reservation, Artikel, Htparam, Umsatz, Billjournal, Bediener, Debitor

def deposit_refund_btn_exitbl(pvilanguage:int, resnr:int, artnr:int, payment:decimal, deposit_pay:decimal, user_init:str, depoart:int, depobezeich:str):
    balance = 0
    t_reservation_list = []
    lvcarea:str = "deposit_refund"
    reservation = artikel = htparam = umsatz = billjournal = bediener = debitor = None

    t_reservation = None

    t_reservation_list, T_reservation = create_model_like(Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, t_reservation_list, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor


        nonlocal t_reservation
        nonlocal t_reservation_list
        return {"balance": balance, "t-reservation": t_reservation_list}

    def deposit_payment1():

        nonlocal balance, t_reservation_list, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor


        nonlocal t_reservation
        nonlocal t_reservation_list

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate
        reservation.depositbez = reservation.depositbez - payment
        reservation.zahldatum = None
        reservation.zahlkonto = 0

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + deposit_pay

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag = deposit_pay
        billjournal.bezeich = artikel.bezeich + "  " + to_string(reservation.resnr)
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == depoart) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date
        umsatz.betrag = umsatz.betrag - deposit_pay
        umsatz.anzahl = umsatz.anzahl + 1

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag = - deposit_pay
        billjournal.bezeich = depobezeich + "  " + to_string(reservation.resnr)
        billjournal.epreis = 0
        billjournal.billjou_ref = artikel.artnr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

        if artikel.artart == 7:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo = - deposit_pay
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


    def deposit_payment2():

        nonlocal balance, t_reservation_list, lvcarea, reservation, artikel, htparam, umsatz, billjournal, bediener, debitor


        nonlocal t_reservation
        nonlocal t_reservation_list

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if payment > reservation.depositbez2:
            reservation.depositbez = reservation.depositbez - payment + reservation.depositbez2
            reservation.depositbez2 = 0
        else:
            reservation.depositbez2 = reservation.depositbez2 - payment
        reservation.zahldatum = None
        reservation.zahldatum2 = None
        reservation.zahlkonto2 = 0

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + deposit_pay

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag = deposit_pay
        billjournal.bezeich = artikel.bezeich + " [" + translateExtended ("Refund", lvcarea, "") + " #" + to_string(reservation.resnr) + "]"
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = reservation.resnr

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == depoart) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date
        umsatz.betrag = umsatz.betrag - deposit_pay
        umsatz.anzahl = umsatz.anzahl + 1

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag = - deposit_pay
        billjournal.bezeich = depobezeich + "  " + to_string(reservation.resnr)
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

        if artikel.artart == 7:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            debitor = Debitor()
            db_session.add(debitor)

            debitor.artnr = artikel.artnr
            debitor.gastnr = reservation.gastnr
            debitor.gastnrmember = reservation.gastnr
            debitor.saldo = - deposit_pay
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = reservation.name


            debitor.vesrcod = translateExtended ("Deposit Refund - ResNo:", lvcarea, "") + " " + to_string(resnr)


    artikel = db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  ((Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag) &  (Artikel.artnr == artnr)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    reservation = db_session.query(Reservation).first()

    if reservation.depositbez == 0:
        deposit_payment1()
    else:
        deposit_payment2()

    reservation = db_session.query(Reservation).first()
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)

    return generate_output()