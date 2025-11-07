# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix ("string").lower()
                    - use f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Artikel, Queasy, Htparam, Bediener, Res_history, Res_line, Counters, Reservation, Guest, Bill, Bill_line, Debitor, Billjournal, Umsatz


def leasing_cancel_actual_invoicebl(qrecid: int, user_init: str):
    prepare_cache([Reslin_queasy, Artikel, Queasy, Htparam, Bediener, Res_history, Res_line,Counters, Reservation, Guest, Bill, Bill_line, Debitor, Billjournal, Umsatz])

    error_flag = 0
    success_flag = False
    ar_ledger: int = 0
    divered_rental: int = 0
    bill_date: date = None
    tot_amount = to_decimal("0.0")
    inv_no: int = 0
    reslin_queasy = artikel = queasy = htparam = bediener = res_history = res_line = counters = reservation = guest = bill = bill_line = debitor = billjournal = umsatz = None
    breslin = bartikel = treslin = pqueasy = mreslin = None

    Breslin = create_buffer("Breslin", Reslin_queasy)
    Bartikel = create_buffer("Bartikel", Artikel)
    Treslin = create_buffer("Treslin", Reslin_queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)
    Mreslin = create_buffer("Mreslin", Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin

        return {
            "error_flag": error_flag,
            "success_flag": success_flag
        }

    def create_log():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin

        bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        # res_history.aenderung = "Cancel Actual Invoice - Reservation no : " + \
        #     to_string(queasy.number1)
        res_history.aenderung = f"Cancel Actual Invoice - Reservation no : {queasy.number1}"
        res_history.action = "Service Apartment"
        
        db_session.add(res_history)

        treslin = Reslin_queasy()

        treslin.key = "ResChanges"
        treslin.resnr = queasy.number1
        treslin.reslinnr = queasy.number2
        treslin.date2 = get_current_date()
        treslin.number2 = get_current_time_in_seconds()
        
        db_session.add(treslin)

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            treslin.char3 = to_string(res_line.ankunft) + ";" +\
                to_string(res_line.ankunft) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.zimmeranz) + ";" +\
                to_string(res_line.zimmeranz) + ";" +\
                to_string(res_line.erwachs) + ";" +\
                to_string(res_line.erwachs) + ";" +\
                to_string(res_line.kind1) + ";" +\
                to_string(res_line.kind1) + ";" +\
                to_string(res_line.gratis) + ";" +\
                to_string(res_line.gratis) + ";" +\
                to_string(res_line.zikatnr) + ";" +\
                to_string(res_line.zikatnr) + ";" +\
                to_string(res_line.zinr) + ";" +\
                to_string(res_line.zinr) + ";" +\
                to_string(res_line.arrangement) + ";" +\
                to_string(res_line.arrangement) + ";" +\
                to_string(res_line.zipreis) + ";" +\
                to_string(res_line.zipreis) + ";" +\
                " " + ";" +\
                to_string(user_init) + ";" +\
                to_string(get_current_date()) + ";" +\
                to_string(get_current_time_in_seconds()) + ";" +\
                to_string("Service Apartement - Cancel Actual Invoice : ") + ";" +\
                to_string(res_line.resnr) + ";" +\
                to_string("NO", "x(3)") + ";" +\
                to_string("NO", "x(3)") + ";"

        pqueasy = get_cache(
            Queasy, {"key": [(eq, 375)], "number1": [(eq, 2)], "number2": [(eq, queasy.number1)], "number3": [(eq, queasy.number2)]})

        if not pqueasy:
            pqueasy = Queasy()

            pqueasy.key = 375
            pqueasy.number1 = 2
            pqueasy.number2 = queasy.number1
            pqueasy.number3 = queasy.number2
            pqueasy.date1 = get_current_date()
            pqueasy.char1 = to_string(
                get_current_time_in_seconds(), "HH:MM:SS")
            pqueasy.char2 = user_init
            pqueasy.logi1 = True
            
            db_session.add(pqueasy)

        else:
            pqueasy.date1 = get_current_date()
            pqueasy.char1 = to_string(
                get_current_time_in_seconds(), "HH:MM:SS")
            pqueasy.char2 = user_init
            pqueasy.logi1 = True

    def create_bill():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin

        billnr: int = 0

        counters = get_cache(Counters, {"counter_no": [(eq, 3)]})

        if not counters:
            counters = Counters()

            counters.counter_no = 3
            counters.counter_bez = "Counter for Bill No"

            db_session.add(counters)
            
        counters.counter = counters.counter + 1
        billnr = counters.counter

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            reservation = get_cache(
                Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache(
                Guest, {"gastnr": [(eq, res_line.gastnr)]})

            bediener = get_cache(
                Bediener, {"userinit": [(eq, user_init)]})
            bill = Bill()

            bill.flag = 1
            bill.billnr = 1
            bill.rgdruck = 1
            bill.zinr = res_line.zinr
            bill.gastnr = res_line.gastnrpay
            bill.resnr = res_line.resnr
            bill.reslinnr = res_line.reslinnr
            bill.parent_nr = res_line.reslinnr
            bill.name = guest.name
            bill.kontakt_nr = bediener.nr
            bill.segmentcode = reservation.segmentcode
            bill.datum = bill_date
            bill.rechnr = billnr

            db_session.add(bill)

            create_bill_line(billnr)

    def create_bill_line(billno: int):
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin

        bartikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if bartikel:
            bill_line = Bill_line()

            bill_line.rechnr = billno
            bill_line.artnr = divered_rental
            bill_line.anzahl = 1
            bill_line.betrag = - to_decimal(tot_amount)
            bill_line.bezeich = bartikel.bezeich
            bill_line.departement = bartikel.departement
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            # bill_line.bezeich = bill_line.bezeich + \
            #     "[" + "Cancel Actual Invoice #" + \
            #     to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel Actual Invoice #{queasy.number1}]"

            db_session.add(bill_line)

        bartikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if bartikel:
            bill_line = Bill_line()

            bill_line.rechnr = billno
            bill_line.artnr = ar_ledger
            bill_line.anzahl = 1
            bill_line.betrag = to_decimal(tot_amount)
            bill_line.bezeich = bartikel.bezeich
            bill_line.departement = bartikel.departement
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            # bill_line.bezeich = bill_line.bezeich + \
            #     "[" + "Cancel Actual Invoice #" + \
            #     to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel Actual Invoice #{queasy.number1}]"

            db_session.add(bill_line)

    def create_ar():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin
        nonlocal breslin, bartikel, treslin, pqueasy, mreslin

        bediener = get_cache(
            Bediener, {"userinit": [(eq, user_init)]})
        debitor = Debitor()

        debitor.artnr = ar_ledger
        debitor.rechnr = inv_no
        debitor.rgdatum = bill_date
        debitor.saldo = - to_decimal(tot_amount)
        debitor.vesrdep = - to_decimal(tot_amount)
        debitor.bediener_nr = bediener.nr
        debitor.vesrdat = get_current_date()
        debitor.transzeit = get_current_time_in_seconds()
        debitor.vesrcod = to_string(inv_no)

        db_session.add(debitor)

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                debitor.name = guest.name
                debitor.gastnr = res_line.gastnr
                debitor.gastnrmember = res_line.gastnrmember

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = ar_ledger
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = to_decimal(tot_amount)
        billjournal.betrag = to_decimal(tot_amount)
        # billjournal.bezeich = artikel.bezeich + \
        #     "[" + "Cancel Actual Invoice#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Cancel Actual Invoice #{queasy.number1}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        db_session.add(billjournal)

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = ar_ledger
            umsatz.datum = bill_date

            db_session.add(umsatz)

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = to_decimal(umsatz.betrag + tot_amount)
        artikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if not artikel:

            return
        billjournal = Billjournal()

        billjournal.artnr = divered_rental
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - to_decimal(tot_amount)
        billjournal.betrag = - to_decimal(tot_amount)
        # billjournal.bezeich = artikel.bezeich + \
        #     "[" + "Cancel Actual Invoice#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Cancel Actual Invoice #{queasy.number1}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        db_session.add(billjournal)

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = divered_rental
            umsatz.datum = bill_date

            db_session.add(umsatz)

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = to_decimal(umsatz.betrag - tot_amount)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        if queasy.logi2 and queasy.deci2 != 0:
            error_flag = 1

            return generate_output()

        pqueasy = get_cache(
            Queasy, {"key": [(eq, 375)], "number1": [(eq, 2)], "number2": [(eq, queasy.number1)], "number3": [(eq, queasy.number2)], "logi1": [(eq, True)]})

        if pqueasy:
            error_flag = 2

            return generate_output()

        mreslin = get_cache(
            Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "char1": [(eq, "")]})

        if mreslin:
            error_flag = 3

            return generate_output()

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2)).order_by(Reslin_queasy._recid).all():
            tot_amount = to_decimal(tot_amount + reslin_queasy.deci1)

        inv_no = to_int(queasy.char2)
        tot_amount = to_decimal(round(tot_amount, 0))

        create_bill()
        create_ar()
        create_log()
        success_flag = True
    return generate_output()
