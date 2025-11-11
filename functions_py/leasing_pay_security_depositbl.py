# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - using f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Artikel, Res_line, Bediener, Debitor, Umsatz, Billjournal


def leasing_pay_security_depositbl(qrecid: int, artikel_no: int, deposit: Decimal, user_init: str, voucher_str: str):

    prepare_cache([Queasy, Htparam, Artikel, Res_line,Bediener, Debitor, Umsatz, Billjournal])

    success_flag = False
    bill_date: date = None
    art_security: int = 0
    queasy = htparam = artikel = res_line = bediener = debitor = umsatz = billjournal = None
    bqueasy = None

    Bqueasy = create_buffer("Bqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill_date, art_security, queasy, htparam, artikel, res_line, bediener, debitor, umsatz, billjournal
        nonlocal qrecid, artikel_no, deposit, user_init, voucher_str
        nonlocal bqueasy
        nonlocal bqueasy

        return {
            "success_flag": success_flag
        }

    def create_journal(bill_date: date):
        nonlocal success_flag, art_security, queasy, htparam, artikel, res_line, bediener, debitor, umsatz, billjournal
        nonlocal qrecid, artikel_no, deposit, user_init, voucher_str
        nonlocal bqueasy
        nonlocal bqueasy

        bartikel = None
        Bartikel = create_buffer("Bartikel", Artikel)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

        if artikel:
            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                if artikel.artart == 2 or artikel.artart == 7:
                    bediener = get_cache(
                        Bediener, {"userinit": [(eq, user_init)]})
                    debitor = Debitor()

                    debitor.artnr = artikel.artnr
                    debitor.gastnr = res_line.gastnr
                    debitor.gastnrmember = res_line.gastnrmember
                    debitor.saldo = to_decimal(deposit)
                    debitor.vesrdep = to_decimal(deposit)
                    debitor.transzeit = get_current_time_in_seconds()
                    debitor.rgdatum = bill_date
                    debitor.bediener_nr = bediener.nr
                    debitor.name = res_line.name
                    # debitor.vesrcod = "Security deposit - ResNo:" + \
                    #     " " + to_string(res_line.resnr)
                    debitor.vesrcod = f"Security deposit - ResNo: {to_string(res_line.resnr)}"

                    db_session.add(debitor)

                    if voucher_str != "":
                        debitor.vesrcod = debitor.vesrcod + "; " + voucher_str
                    pass

                umsatz = get_cache(
                    Umsatz, {"departement": [(eq, 0)], "artnr": [(eq, artikel.artnr)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag - deposit)

                billjournal = Billjournal()

                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - to_decimal(deposit)
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.billjou_ref = res_line.resnr
                billjournal.betrag = - to_decimal(deposit)
                # billjournal.bezeich = artikel.bezeich + \
                #     "[" + "Security deposit #" + \
                #     to_string(res_line.resnr) + "]" + voucher_str
                billjournal.bezeich = f"{artikel.bezeich}[Security deposit #{to_string(res_line.resnr)}]{voucher_str}"
                
                db_session.add(billjournal)
                
                bartikel = get_cache(
                    Artikel, {"artnr": [(eq, art_security)], "departement": [(eq, 0)]})

                if bartikel:
                    umsatz = get_cache(Umsatz, {"artnr": [(eq, bartikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = bartikel.artnr
                        umsatz.datum = bill_date
                        
                        db_session.add(umsatz)

                    umsatz.betrag = to_decimal(
                        umsatz.betrag + deposit)
                    umsatz.anzahl = umsatz.anzahl + 1

                    billjournal = Billjournal()

                    billjournal.artnr = bartikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = to_decimal(deposit)
                    billjournal.betrag = to_decimal(deposit)
                    # billjournal.bezeich = bartikel.bezeich + \
                    #     "[" + "Security deposit #" + \
                    #     to_string(res_line.resnr) + "]" + voucher_str
                    billjournal.bezeich = f"{bartikel.bezeich}[Security deposit #{to_string(res_line.resnr)}]{voucher_str}"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = bartikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date

                    db_session.add(billjournal)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1053)]})

    if htparam:
        art_security = htparam.finteger

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        bqueasy = get_cache(
            Queasy, {"key": [(eq, 349)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

        if not bqueasy:
            bqueasy = Queasy()

            bqueasy.key = 349
            bqueasy.number1 = queasy.number1
            bqueasy.number2 = queasy.number2
            bqueasy.number3 = artikel_no
            bqueasy.deci1 = to_decimal(deposit)
            bqueasy.char1 = user_init
            bqueasy.date1 = bill_date
            bqueasy.deci2 = to_decimal(get_current_time_in_seconds)()
            bqueasy.char2 = to_string(get_current_date(
            )) + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

            db_session.add(bqueasy)

        else:
            bqueasy.deci1 = to_decimal(bqueasy.deci1) + to_decimal(deposit)
            bqueasy.char1 = user_init
            bqueasy.date1 = bill_date
            bqueasy.deci2 = to_decimal(get_current_time_in_seconds)()
            bqueasy.char2 = to_string(get_current_date(
            )) + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        create_journal(bill_date)

    return generate_output()
