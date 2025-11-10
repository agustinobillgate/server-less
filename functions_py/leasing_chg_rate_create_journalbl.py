#using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - using f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Artikel, Billjournal, Umsatz, Bediener, Debitor, Res_line, Guest

def leasing_chg_rate_create_journalbl(resnr:int, reslinnr:int, user_init:str):

    prepare_cache ([Htparam, Queasy, Artikel, Billjournal, Umsatz, Bediener, Debitor, Res_line, Guest])

    bill_date:date = None
    refund_div:int = 0
    add_rmcharge:int = 0
    divered_rental:int = 0
    price_decimal:int = 0
    ar_ledger:int = 0
    amount = to_decimal("0.0")
    billno:int = 0
    htparam = queasy = artikel = billjournal = umsatz = bediener = debitor = res_line = guest = None
    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, amount, billno, htparam, queasy, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal resnr, reslinnr, user_init
        nonlocal bqueasy
        nonlocal bqueasy

        return {}

    def create_bill_line():
        nonlocal bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, amount, billno, htparam, queasy, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal resnr, reslinnr, user_init
        nonlocal bqueasy
        nonlocal bqueasy

        if amount < 0:
            artikel = get_cache(
                Artikel, {"artnr": [(eq, divered_rental)],"departement": [(eq, 0)]})

            if artikel:
                billjournal = Billjournal()

                billjournal.rechnr = billno
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng =  - to_decimal(amount)
                billjournal.betrag =  - to_decimal(amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + to_string(billno) + ": Adjustment Rate - Service Apartment"
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(billno)}: Adjustment Rate - Service Apartment"
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(round(billjournal.fremdwaehrng , price_decimal))
                billjournal.betrag = to_decimal(round(billjournal.betrag , price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache (
                    Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(- to_decimal(amount) )
                umsatz.betrag = to_decimal(round(umsatz.betrag , price_decimal))

            artikel = get_cache(
                Artikel, {"artnr": [(eq, ar_ledger)],"departement": [(eq, 0)]})

            if artikel:
                billjournal = Billjournal()

                billjournal.rechnr = billno
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng =  to_decimal(amount)
                billjournal.betrag =  to_decimal(amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + to_string(billno) + ": Adjustment Rate - Service Apartment"
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(billno)}: Adjustment Rate - Service Apartment"
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(round(billjournal.fremdwaehrng , price_decimal))
                billjournal.betrag = to_decimal(round(billjournal.betrag , price_decimal))


                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag =  to_decimal(umsatz.betrag + amount)
                umsatz.betrag = to_decimal(round(umsatz.betrag , price_decimal))

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, user_init)]})
                debitor = Debitor()

                debitor.artnr = artikel.artnr
                debitor.rechnr = billno
                debitor.rgdatum = bill_date
                debitor.saldo =  - to_decimal(amount)
                debitor.vesrdep =  - to_decimal(amount)
                debitor.bediener_nr = bediener.nr
                debitor.vesrdat = get_current_date()
                debitor.transzeit = get_current_time_in_seconds()
                debitor.vesrcod = to_string(billno)
                debitor.vesrcod = to_string(billno)
                debitor.saldo = to_decimal(round(debitor.saldo , price_decimal))
                debitor.vesrdep = to_decimal(round(debitor.vesrdep , price_decimal))

                db_session.add(debitor)

                res_line = get_cache(
                    Res_line, {"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

                if res_line:
                    guest = get_cache(
                        Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        debitor.name = guest.name
                        debitor.gastnr = res_line.gastnr
                        debitor.gastnrmember = res_line.gastnrmember

            else:
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, divered_rental)],"departement": [(eq, 0)]})

                if artikel:
                    billjournal = Billjournal()

                    billjournal.rechnr = billno
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng =  - to_decimal(amount)
                    billjournal.betrag =  - to_decimal(amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + to_string(billno) + ": Adjustment Rate - Service Apartment"
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(billno)}: Adjustment Rate - Service Apartment"
                    billjournal.epreis =  to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date
                    billjournal.fremdwaehrng = to_decimal(round(billjournal.fremdwaehrng , price_decimal))
                    billjournal.betrag = to_decimal(round(billjournal.betrag , price_decimal))

                    db_session.add(billjournal)

                    umsatz = get_cache (
                        Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag =  (- to_decimal(amount)) + to_decimal(umsatz.betrag)  
                    umsatz.betrag = to_decimal(round(umsatz.betrag , price_decimal))

                artikel = get_cache (
                    Artikel, {"artnr": [(eq, ar_ledger)],"departement": [(eq, 0)]})

                if artikel:
                    billjournal = Billjournal()

                    billjournal.rechnr = billno
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng =  to_decimal(amount)
                    billjournal.betrag =  to_decimal(amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + to_string(billno) + ": Adjustment Rate - Service Apartment"
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(billno)}: Adjustment Rate - Service Apartment"
                    billjournal.epreis =  to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date
                    billjournal.fremdwaehrng = to_decimal(round(billjournal.fremdwaehrng , price_decimal))
                    billjournal.betrag = to_decimal(round(billjournal.betrag , price_decimal))

                    db_session.add(billjournal)

                    umsatz = get_cache (
                        Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag =  to_decimal(umsatz.betrag + amount)
                    umsatz.betrag = to_decimal(round(umsatz.betrag , price_decimal))

                    bediener = get_cache (
                        Bediener, {"userinit": [(eq, user_init)]})
                    debitor = Debitor()
                    db_session.add(debitor)

                    debitor.artnr = artikel.artnr
                    debitor.rechnr = billno
                    debitor.rgdatum = bill_date
                    debitor.saldo =  - to_decimal(amount)
                    debitor.vesrdep =  - to_decimal(amount)
                    debitor.bediener_nr = bediener.nr
                    debitor.vesrdat = get_current_date()
                    debitor.transzeit = get_current_time_in_seconds()
                    debitor.vesrcod = to_string(billno)
                    debitor.vesrcod = to_string(billno)
                    debitor.saldo = to_decimal(round(debitor.saldo , price_decimal))
                    debitor.vesrdep = to_decimal(round(debitor.vesrdep , price_decimal))

                    res_line = get_cache (
                        Res_line, {"resnr": [(eq, queasy.number1)],"reslinnr": [(eq, queasy.number2)]})

                    if res_line:
                        guest = get_cache (
                            Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if guest:
                            debitor.name = guest.name
                            debitor.gastnr = res_line.gastnr
                            debitor.gastnrmember = res_line.gastnrmember

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 356) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr)).order_by(Queasy.date1.desc(), Queasy.number3.desc()).all():
        bqueasy = get_cache (
            Queasy, {"key": [(eq, 329)],"number1": [(eq, queasy.number1)],"number2": [(eq, queasy.number2)]})

        if bqueasy:
            amount =  to_decimal(queasy.deci1 - queasy.deci2)
            billno = to_int(bqueasy.char2)

            if queasy.deci2 != 0:
                create_bill_line()
        break

    return generate_output()