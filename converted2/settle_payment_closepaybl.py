#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Bediener, Umsatz, Billjournal, Artikel

def settle_payment_closepaybl(user_init:string, artnr:int, p_betrag:Decimal, f_amt:Decimal, bill_date:date):

    prepare_cache ([Debitor, Bediener, Umsatz, Billjournal, Artikel])

    debitor = bediener = umsatz = billjournal = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debitor, bediener, umsatz, billjournal, artikel
        nonlocal user_init, artnr, p_betrag, f_amt, bill_date

        return {}

    def settle_payment():

        nonlocal debitor, bediener, umsatz, billjournal, artikel
        nonlocal user_init, artnr, p_betrag, f_amt, bill_date

        saldo_i:Decimal = to_decimal("0.0")
        count:int = 0
        anzahl:int = 0
        supplier:string = ""
        debitor1 = None
        Debitor1 =  create_buffer("Debitor1",Debitor)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        debitor1 = Debitor()
        db_session.add(debitor1)

        debitor1.gastnr = debitor.gastnr
        debitor1.opart = 2
        debitor1.name = debitor.name
        debitor1.rechnr = debitor.rechnr
        debitor1.gastnr = debitor.gastnr
        debitor1.zahlkonto = artnr
        debitor1.saldo =  to_decimal(p_betrag)
        debitor1.vesrdep =  to_decimal(f_amt)
        debitor1.betrieb_gastmem = artikel.betriebsnr
        debitor1.counter = debitor.counter
        debitor1.rgdatum = bill_date
        debitor1.bediener_nr = bediener.nr

        umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, artnr)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

        umsatz.datum = bill_date
        umsatz.artnr = artnr
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(debitor.saldo)
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)


        artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, 0)]})
        billjournal.rechnr = debitor.rechnr
        billjournal.bill_datum = bill_date
        billjournal.artnr = artnr
        billjournal.betrag =  to_decimal(p_betrag)
        billjournal.bezeich = artikel.bezeich
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.bediener_nr = bediener.nr
        billjournal.userinit = user_init
        pass


    settle_payment()

    return generate_output()