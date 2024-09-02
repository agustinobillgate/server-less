from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Debitor, Bediener, Umsatz, Billjournal, Artikel

def settle_payment_closepaybl(user_init:str, artnr:int, p_betrag:decimal, f_amt:decimal, bill_date:date):
    debitor = bediener = umsatz = billjournal = artikel = None

    debitor1 = None

    Debitor1 = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debitor, bediener, umsatz, billjournal, artikel
        nonlocal debitor1


        nonlocal debitor1
        return {}

    def settle_payment():

        nonlocal debitor, bediener, umsatz, billjournal, artikel
        nonlocal debitor1


        nonlocal debitor1

        saldo_i:decimal = 0
        count:int = 0
        anzahl:int = 0
        supplier:str = ""
        Debitor1 = Debitor

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        debitor1 = Debitor1()
        db_session.add(debitor1)

        debitor1.gastnr = debitor.gastnr
        debitor1.opart = 2
        debitor1.name = debitor.name
        debitor1.rechnr = debitor.rechnr
        debitor1.gastnr = debitor.gastnr
        debitor1.zahlkonto = artnr
        debitor1.saldo = p_betrag
        debitor1.vesrdep = f_amt
        debitor1.betrieb_gastmem = artikel.betriebsnr
        debitor1.counter = debitor.counter
        debitor1.rgdatum = bill_date
        debitor1.bediener_nr = bediener.nr

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
        db_session.add(umsatz)

        umsatz.datum = bill_date
        umsatz.artnr = artnr
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + debitor.saldo

        billjournal = Billjournal()
        db_session.add(billjournal)


        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artnr) &  (Artikel.departement == 0)).first()
        billjournal.rechnr = debitor.rechnr
        billjournal.bill_datum = bill_date
        billjournal.artnr = artnr
        billjournal.betrag = p_betrag
        billjournal.bezeich = artikel.bezeich
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = user_init


    settle_payment()

    return generate_output()