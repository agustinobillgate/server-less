# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - using f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bill, Queasy, Artikel, Debitor, Bediener, Res_line, Guest, Bill_line, Billjournal, Umsatz


def leasing_payment_chg_ratebl(bill_no: int, resnr: int, reslinnr: int, artikel_no: int, amount: Decimal, remark: str, user_init: str):

    prepare_cache([Htparam, Bill, Queasy, Artikel, Bediener, Res_line, Guest, Billjournal, Umsatz])

    err_msg = ""
    bill_date: date = None
    ar_ledger: int = 0
    htparam = bill = queasy = artikel = debitor = bediener = res_line = guest = bill_line = billjournal = umsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_msg, bill_date, ar_ledger, htparam, bill, queasy, artikel, debitor, bediener, res_line, guest, bill_line, billjournal, umsatz
        nonlocal bill_no, resnr, reslinnr, artikel_no, amount, remark, user_init

        return {
            "err_msg": err_msg
        }

    def create_ar():
        nonlocal err_msg, bill_date, ar_ledger, htparam, bill, queasy, artikel, debitor, bediener, res_line, guest, bill_line, billjournal, umsatz
        nonlocal bill_no, resnr, reslinnr, artikel_no, amount, remark, user_init

        bdebt = None
        Bdebt = create_buffer("Bdebt", Debitor)

        bediener = get_cache(
            Bediener, {"userinit": [(eq, user_init)]})
        bdebt = Debitor()

        bdebt.artnr = artikel_no
        bdebt.rechnr = bill_no
        bdebt.rgdatum = bill_date
        bdebt.saldo = - to_decimal(amount)
        bdebt.vesrdep = - to_decimal(amount)
        bdebt.bediener_nr = bediener.nr
        bdebt.vesrdat = get_current_date()
        bdebt.transzeit = get_current_time_in_seconds()
        bdebt.vesrcod = to_string(bill_no)

        db_session.add(bdebt)

        if amount < 0:
            # bdebt.vesrcod = to_string(bill_no) + "|PAYMENT CHANGED RATE"
            bdebt.vesrcod = f"{to_string(bill_no)}|PAYMENT CHANGED RATE"

        else:
            # bdebt.vesrcod = to_string(bill_no) + "|REFUND CHANGED RATE"
            bdebt.vesrcod = f"{to_string(bill_no)}|REFUND CHANGED RATE"

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                bdebt.name = guest.name
                bdebt.gastnr = res_line.gastnr
                bdebt.gastnrmember = res_line.gastnrmember

    def create_bill_line():
        nonlocal err_msg, bill_date, ar_ledger, htparam, bill, queasy, artikel, debitor, bediener, res_line, guest, bill_line, billjournal, umsatz
        nonlocal bill_no, resnr, reslinnr, artikel_no, amount, remark, user_init

        div_amt: Decimal = to_decimal("0.0")
        bline = None
        Bline = create_buffer("Bline", Bill_line)

        if amount < 0:
            artikel = get_cache(
                Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

            if artikel:
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(amount)
                billjournal.betrag = to_decimal(amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(
                #         bill.rechnr) + "[Payment Change Rate #" + to_string(queasy.number1) + "]"
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)}[Payment Change Rate #{to_string(queasy.number1)}]"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag + amount)

            artikel = get_cache(
                Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

            if artikel:
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - to_decimal(amount)
                billjournal.betrag = - to_decimal(amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(
                #         bill.rechnr) + "[Payment Change Rate #" + to_string(queasy.number1) + "]"
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)}[Payment Change Rate #{to_string(queasy.number1)}]"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag) + (- to_decimal(amount))

            else:
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

                if artikel:
                    billjournal = Billjournal()

                    billjournal.rechnr = bill.rechnr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = to_decimal(amount)
                    billjournal.betrag = to_decimal(amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    #     to_string(
                    #         bill.rechnr) + "[Refund Change Rate #" + to_string(queasy.number1) + "]"
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)}[Refund Change Rate #{to_string(queasy.number1)}]"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date

                    db_session.add(billjournal)

                    umsatz = get_cache(
                        Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag = to_decimal(umsatz.betrag + amount)

                artikel = get_cache(
                    Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

                if artikel:
                    billjournal = Billjournal()

                    billjournal.rechnr = bill.rechnr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = - to_decimal(amount)
                    billjournal.betrag = - to_decimal(amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    #     to_string(
                    #         bill.rechnr) + "[Refund Change Rate #" + to_string(queasy.number1) + "]"
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)}[Refund Change Rate #{to_string(queasy.number1)}]"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date

                    db_session.add(billjournal)

                    umsatz = get_cache(
                        Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag = to_decimal(umsatz.betrag) + (- to_decimal(amount))

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    bill = get_cache(
        Bill, {"rechnr": [(eq, bill_no)]})

    if bill and bill.billnr != 1:
        err_msg = "The refund/payment process is not permitted. This bill is not the main invoice."

        return generate_output()

    elif bill and bill.billnr == 1:
        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)]})

        if queasy:
            create_bill_line()

            artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artikel_no) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7))).first()

            if artikel:
                create_ar()

    return generate_output()
