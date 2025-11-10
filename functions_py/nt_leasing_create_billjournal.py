#using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - only convert
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Billjournal, Htparam, Artikel, Umsatz

def nt_leasing_create_billjournal():

    prepare_cache ([Billjournal, Htparam, Artikel, Umsatz])

    bill_date:date = None
    ar_ledger:int = 0
    billjournal = htparam = artikel = umsatz = None

    bjournal = None

    Bjournal = create_buffer("Bjournal",Billjournal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, ar_ledger, billjournal, htparam, artikel, umsatz
        nonlocal bjournal
        nonlocal bjournal

        return {}

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    billjournal = get_cache (
        Billjournal, {"artnr": [(eq, ar_ledger)],"departement": [(eq, 0)],"bill_datum": [(eq, bill_date)]})

    if billjournal:
        artikel = get_cache (
            Artikel, {"artnr": [(eq, ar_ledger)],"departement": [(eq, 0)]})

        if not artikel:
            return generate_output()
        bjournal = Billjournal()

        bjournal.artnr = artikel.artnr
        bjournal.anzahl = 1
        bjournal.fremdwaehrng =  - to_decimal(billjournal.fremdwaehrng)
        bjournal.betrag =  - to_decimal(billjournal.betrag)
        bjournal.bezeich = billjournal.bezeich
        bjournal.epreis =  to_decimal("0")
        bjournal.zeit = get_current_time_in_seconds()
        bjournal.billjou_ref = artikel.artnr
        bjournal.userinit = "**"
        bjournal.bill_datum = bill_date

        db_session.add(bjournal)

        umsatz = get_cache (
            Umsatz, {"artnr": [(eq, ar_ledger)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = ar_ledger
            umsatz.datum = bill_date

            db_session.add(umsatz)

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + (- to_decimal(billjournal.betrag))

    return generate_output()