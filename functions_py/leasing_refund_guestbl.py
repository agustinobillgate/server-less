# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - fix closing braket on timedelta(days=1)
                    - using f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Bill, Bill_line, Artikel, Billjournal, Umsatz, Bediener, Debitor, Res_line, Guest


def leasing_refund_guestbl(bill_no: int, resnr: int, reslinnr: int, additional_amount: Decimal, refund_artikel: int, refund_amount: Decimal, remark: str, avail_pay: bool, user_init: str):

    prepare_cache([Queasy, Htparam, Bill, Bill_line, Artikel, Billjournal, Umsatz, Bediener, Debitor, Res_line, Guest])

    err_msg = ""
    bill_date: date = None
    refund_div: int = 0
    add_rmcharge: int = 0
    divered_rental: int = 0
    price_decimal: int = 0
    ar_ledger: int = 0
    queasy = htparam = bill = bill_line = artikel = billjournal = umsatz = bediener = debitor = res_line = guest = None

    tqueasy = None

    Tqueasy = create_buffer("Tqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        return {
            "err_msg": err_msg
        }

    def create_queasy():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        tqueasy = get_cache(
            Queasy, {"key": [(eq, 358)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

        if not tqueasy:
            tqueasy = Queasy()

            tqueasy.key = 358
            tqueasy.number1 = queasy.number1
            tqueasy.number2 = queasy.number2

            db_session.add(tqueasy)

    def create_bill_line():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        div_amt = to_decimal("0.0")
        bline = None
        Bline = create_buffer("Bline", Bill_line)

        for bline in db_session.query(Bline).filter(
                (Bline.rechnr == bill.rechnr) & (Bline.artnr == divered_rental)).order_by(Bline._recid).all():
            div_amt = to_decimal(div_amt + bline.betrag)

        if div_amt != 0:

            artikel = get_cache(
                Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = - (to_decimal(queasy.deci1 + div_amt))
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - (to_decimal(queasy.deci1 + div_amt))
                billjournal.betrag = - (to_decimal(queasy.deci1 + div_amt))
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(
                    round(billjournal.fremdwaehrng, price_decimal))
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)
                    
                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + (- to_decimal(queasy.deci1 + to_decimal(div_amt)))
                umsatz.betrag = to_decimal(round(umsatz.betrag, price_decimal))

            artikel = get_cache(
                Artikel, {"artnr": [(eq, add_rmcharge)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(additional_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(additional_amount)
                billjournal.betrag = to_decimal(additional_amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
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
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + to_decimal(additional_amount)

            artikel = get_cache(
                Artikel, {"artnr": [(eq, refund_artikel)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(refund_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(refund_amount)
                billjournal.betrag = to_decimal(refund_amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(
                    round(billjournal.fremdwaehrng, price_decimal))
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag + ((queasy.deci1 + div_amt) - additional_amount))
                umsatz.betrag = to_decimal(round(umsatz.betrag, 0))

            if artikel.artart == 2 or artikel.artart == 7:
                bediener = get_cache(
                    Bediener, {"userinit": [(eq, user_init)]})
                debitor = Debitor()

                debitor.artnr = artikel.artnr
                debitor.rechnr = bill.rechnr
                debitor.rgdatum = bill_date
                debitor.saldo = - to_decimal(refund_amount)
                debitor.vesrdep = - to_decimal(refund_amount)
                debitor.bediener_nr = bediener.nr
                debitor.vesrdat = get_current_date()
                debitor.transzeit = get_current_time_in_seconds()
                debitor.vesrcod = to_string(bill_no)

                db_session.add(debitor)

                if refund_amount < 0:
                    # debitor.vesrcod = to_string(
                    #     bill.rechnr) + "|PAYMENT EARLY C/O"
                    debitor.vesrcod = f"{to_string(bill.rechnr)}|PAYMENT EARLY C/O"

                else:
                    # debitor.vesrcod = to_string(
                    #     bill.rechnr) + "|REFUND EARLY C/O"
                    debitor.vesrcod = f"{to_string(bill.rechnr)}|REFUND EARLY C/O"

                res_line = get_cache(
                    Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                if res_line:

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        debitor.name = guest.name
                        debitor.gastnr = res_line.gastnr
                        debitor.gastnrmember = res_line.gastnrmember

    def create_bill_line3():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        div_amt = to_decimal("0.0")
        bline = None
        Bline = create_buffer("Bline", Bill_line)

        for bline in db_session.query(Bline).filter(
                (Bline.rechnr == bill.rechnr) & (Bline.artnr == divered_rental)).order_by(Bline._recid).all():
            div_amt = to_decimal(div_amt + bline.betrag)

        if div_amt != 0:
            artikel = get_cache(
                Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = - (to_decimal(queasy.deci1 + div_amt))
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)
                
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - (to_decimal(queasy.deci1 + div_amt))
                billjournal.betrag = - (to_decimal(queasy.deci1 + div_amt))
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(
                    round(billjournal.fremdwaehrng, price_decimal))
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag + (queasy.deci1 + div_amt))
                umsatz.betrag = to_decimal(round(umsatz.betrag, price_decimal))

            artikel = get_cache(
                Artikel, {"artnr": [(eq, add_rmcharge)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()
                
                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(additional_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(additional_amount)
                billjournal.betrag = to_decimal(additional_amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
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
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + to_decimal(additional_amount)

            artikel = get_cache(
                Artikel, {"artnr": [(eq, refund_artikel)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(refund_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)
                
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(refund_amount)
                billjournal.betrag = to_decimal(refund_amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(
                    round(billjournal.fremdwaehrng, price_decimal))
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + to_decimal(refund_amount)
                umsatz.betrag = to_decimal(round(umsatz.betrag, 0))

                if artikel.artart == 2 or artikel.artart == 7:
                    bediener = get_cache(
                        Bediener, {"userinit": [(eq, user_init)]})
                    debitor = Debitor()

                    debitor.artnr = artikel.artnr
                    debitor.rechnr = bill.rechnr
                    debitor.rgdatum = bill_date
                    debitor.saldo = - to_decimal(refund_amount)
                    debitor.vesrdep = - to_decimal(refund_amount)
                    debitor.bediener_nr = bediener.nr
                    debitor.vesrdat = get_current_date()
                    debitor.transzeit = get_current_time_in_seconds()
                    debitor.vesrcod = to_string(bill_no)

                    db_session.add(debitor)

                    if refund_amount < 0:
                        # debitor.vesrcod = to_string(
                        #     bill.rechnr) + "|PAYMENT EARLY C/O"
                        debitor.vesrcod = f"{to_string(bill.rechnr)}|PAYMENT EARLY C/O"

                    else:
                        # debitor.vesrcod = to_string(
                        #     bill.rechnr) + "|REFUND EARLY C/O"
                        debitor.vesrcod = f"{to_string(bill.rechnr)}|REFUND EARLY C/O"

                    res_line = get_cache(
                        Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                    if res_line:
                        guest = get_cache(
                            Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if guest:
                            debitor.name = guest.name
                            debitor.gastnr = res_line.gastnr
                            debitor.gastnrmember = res_line.gastnrmember

            artikel = get_cache(
                Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal((queasy.deci1 - additional_amount - refund_amount) + div_amt)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                # billjournal.fremdwaehrng = (to_decimal(queasy.deci1) - to_decimal(
                #     additional_amount) - to_decimal(refund_amount)) + to_decimal(div_amt)
                # billjournal.betrag = (to_decimal(queasy.deci1) - to_decimal(
                #     additional_amount) - to_decimal(refund_amount)) + to_decimal(div_amt)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.fremdwaehrng = to_decimal((queasy.deci1 - additional_amount - refund_amount) + div_amt)
                billjournal.betrag = to_decimal((queasy.deci1 - additional_amount - refund_amount) + div_amt)
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.fremdwaehrng = to_decimal(
                    round(billjournal.fremdwaehrng, price_decimal))
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(umsatz.betrag + ((queasy.deci1 - additional_amount - refund_amount) + div_amt))
                umsatz.betrag = to_decimal(round(umsatz.betrag, price_decimal))

    def create_bill_line2():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        div_amt = to_decimal("0.0")
        bline = None
        Bline = create_buffer("Bline", Bill_line)

        for bline in db_session.query(Bline).filter(
                (Bline.rechnr == bill.rechnr) & (Bline.artnr == divered_rental)).order_by(Bline._recid).all():
            div_amt = to_decimal(div_amt + bline.betrag)

        if div_amt != 0:
            artikel = get_cache(
                Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = - (to_decimal(queasy.deci1) - to_decimal(div_amt))
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)
                
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - (to_decimal(queasy.deci1) - to_decimal(div_amt))
                billjournal.betrag = - (to_decimal(queasy.deci1) - to_decimal(div_amt))
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(
                    umsatz.betrag) - to_decimal((queasy.deci1) - to_decimal(div_amt))
                umsatz.betrag = to_decimal(round(umsatz.betrag, price_decimal))

            artikel = get_cache(
                Artikel, {"artnr": [(eq, add_rmcharge)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(additional_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark
                bill_line.betrag = to_decimal(
                    round(bill_line.betrag, price_decimal))

                db_session.add(bill_line)
                
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(additional_amount)
                billjournal.betrag = to_decimal(additional_amount)
                billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    to_string(bill.rechnr) + " - " + remark
                billjournal.epreis = to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.billjou_ref = artikel.artnr
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date
                billjournal.betrag = to_decimal(
                    round(billjournal.betrag, price_decimal))

                db_session.add(billjournal)

                umsatz = get_cache(
                    Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date

                    db_session.add(umsatz)

                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + to_decimal(additional_amount)
                umsatz.betrag = to_decimal(round(umsatz.betrag, price_decimal))

            if refund_amount != 0:
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, refund_artikel)], "departement": [(eq, 0)]})

                if artikel:
                    bill_line = Bill_line()

                    bill_line.rechnr = bill.rechnr
                    bill_line.artnr = artikel.artnr
                    bill_line.anzahl = 1
                    bill_line.betrag = - to_decimal(refund_amount)
                    bill_line.bezeich = artikel.bezeich
                    bill_line.departement = artikel.departement
                    bill_line.zeit = get_current_time_in_seconds()
                    bill_line.userinit = user_init
                    bill_line.bill_datum = bill_date
                    bill_line.bezeich = bill_line.bezeich + " - " + remark
                    bill_line.betrag = to_decimal(
                        round(bill_line.betrag, price_decimal))

                    db_session.add(bill_line)
                    
                    billjournal = Billjournal()

                    billjournal.rechnr = bill.rechnr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = - to_decimal(refund_amount)
                    billjournal.betrag = - to_decimal(refund_amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    #     to_string(bill.rechnr) + " - " + remark
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date
                    billjournal.fremdwaehrng = to_decimal(
                        round(billjournal.fremdwaehrng, price_decimal))
                    billjournal.betrag = to_decimal(
                        round(billjournal.betrag, price_decimal))

                    db_session.add(billjournal)

                    umsatz = get_cache(
                        Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag = to_decimal(
                        umsatz.betrag) - to_decimal(refund_amount)
                    umsatz.betrag = to_decimal(
                        round(umsatz.betrag, price_decimal))

                    if artikel.artart == 2 or artikel.artart == 7:
                        bediener = get_cache(
                            Bediener, {"userinit": [(eq, user_init)]})
                        debitor = Debitor()

                        debitor.artnr = artikel.artnr
                        debitor.rechnr = bill.rechnr
                        debitor.rgdatum = bill_date
                        debitor.saldo = to_decimal(refund_amount)
                        debitor.vesrdep = to_decimal(refund_amount)
                        debitor.bediener_nr = bediener.nr
                        debitor.vesrdat = get_current_date()
                        debitor.transzeit = get_current_time_in_seconds()
                        debitor.vesrcod = to_string(bill_no)

                        db_session.add(debitor)

                        if refund_amount < 0:
                            # debitor.vesrcod = to_string(
                            #     bill.rechnr) + "|PAYMENT EARLY C/O"
                            debitor.vesrcod = f"{to_string(bill.rechnr)}|PAYMENT EARLY C/O"

                        else:
                            debitor.vesrcod = to_string(
                                bill.rechnr) + "|REFUND EARLY C/O"
                            debitor.vesrcod = f"{to_string(bill.rechnr)}|REFUND EARLY C/O"

                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                        if res_line:
                            guest = get_cache(
                                Guest, {"gastnr": [(eq, res_line.gastnr)]})

                            if guest:
                                debitor.name = guest.name
                                debitor.gastnr = res_line.gastnr
                                debitor.gastnrmember = res_line.gastnrmember

                artikel = get_cache(
                    Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

                if artikel:
                    bill_line = Bill_line()

                    bill_line.rechnr = bill.rechnr
                    bill_line.artnr = artikel.artnr
                    bill_line.anzahl = 1
                    bill_line.betrag = to_decimal(queasy.deci1)
                    bill_line.bezeich = artikel.bezeich
                    bill_line.departement = artikel.departement
                    bill_line.zeit = get_current_time_in_seconds()
                    bill_line.userinit = user_init
                    bill_line.bill_datum = bill_date
                    bill_line.bezeich = bill_line.bezeich + " - " + remark
                    bill_line.betrag = to_decimal(
                        round(bill_line.betrag, price_decimal))

                    db_session.add(bill_line)
                    
                    billjournal = Billjournal()

                    billjournal.rechnr = bill.rechnr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = to_decimal(queasy.deci1)
                    billjournal.betrag = to_decimal(queasy.deci1)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    #     to_string(bill.rechnr) + " - " + remark
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date
                    billjournal.fremdwaehrng = to_decimal(
                        round(billjournal.fremdwaehrng, price_decimal))
                    billjournal.betrag = to_decimal(
                        round(billjournal.betrag, price_decimal))

                    db_session.add(billjournal)

                    umsatz = get_cache(
                        Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag = to_decimal(
                        umsatz.betrag) + to_decimal(queasy.deci1)
                    umsatz.betrag = to_decimal(
                        round(umsatz.betrag, price_decimal))

                    bediener = get_cache(
                        Bediener, {"userinit": [(eq, user_init)]})
                    debitor = Debitor()

                    debitor.artnr = artikel.artnr
                    debitor.rechnr = bill.rechnr
                    debitor.rgdatum = bill_date
                    debitor.saldo = - to_decimal(queasy.deci1)
                    debitor.vesrdep = - to_decimal(queasy.deci1)
                    debitor.bediener_nr = bediener.nr
                    debitor.vesrdat = get_current_date()
                    debitor.transzeit = get_current_time_in_seconds()
                    debitor.vesrcod = to_string(bill_no)
                    debitor.vesrcod = to_string(bill.rechnr)
                    debitor.saldo = to_decimal(
                        round(debitor.saldo, price_decimal))
                    debitor.vesrdep = to_decimal(
                        round(debitor.vesrdep, price_decimal))

                    db_session.add(debitor)

                    res_line = get_cache(
                        Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                    if res_line:
                        guest = get_cache(
                            Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if guest:
                            debitor.name = guest.name
                            debitor.gastnr = res_line.gastnr
                            debitor.gastnrmember = res_line.gastnrmember

    def create_bill_line4():
        nonlocal err_msg, bill_date, refund_div, add_rmcharge, divered_rental, price_decimal, ar_ledger, queasy, htparam, bill, bill_line, artikel, billjournal, umsatz, bediener, debitor, res_line, guest
        nonlocal bill_no, resnr, reslinnr, additional_amount, refund_artikel, refund_amount, remark, avail_pay, user_init
        nonlocal tqueasy
        nonlocal tqueasy

        div_amt = to_decimal("0.0")
        bline = None
        Bline = create_buffer("Bline", Bill_line)

        for bline in db_session.query(Bline).filter(
                (Bline.rechnr == bill.rechnr) & (Bline.artnr == divered_rental)).order_by(Bline._recid).all():
            div_amt = to_decimal(div_amt) + to_decimal(bline.betrag)

        if div_amt != 0:
            artikel = get_cache(
                Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = - to_decimal(div_amt)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark

                db_session.add(bill_line)

                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = - to_decimal(div_amt)
                billjournal.betrag = - to_decimal(div_amt)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
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
                umsatz.betrag = to_decimal(umsatz.betrag) - to_decimal(div_amt)

            artikel = get_cache(
                Artikel, {"artnr": [(eq, add_rmcharge)], "departement": [(eq, 0)]})

            if artikel:
                bill_line = Bill_line()

                bill_line.rechnr = bill.rechnr
                bill_line.artnr = artikel.artnr
                bill_line.anzahl = 1
                bill_line.betrag = to_decimal(additional_amount)
                bill_line.bezeich = artikel.bezeich
                bill_line.departement = artikel.departement
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.bezeich = bill_line.bezeich + " - " + remark

                db_session.add(bill_line)
                
                billjournal = Billjournal()

                billjournal.rechnr = bill.rechnr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = to_decimal(additional_amount)
                billjournal.betrag = to_decimal(additional_amount)
                # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                #     to_string(bill.rechnr) + " - " + remark
                billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
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
                umsatz.betrag = to_decimal(
                    umsatz.betrag) + to_decimal(additional_amount)

            if refund_amount != 0:
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, refund_artikel)], "departement": [(eq, 0)]})

                if artikel:
                    bill_line = Bill_line()

                    bill_line.rechnr = bill.rechnr
                    bill_line.artnr = artikel.artnr
                    bill_line.anzahl = 1
                    bill_line.betrag = - to_decimal(refund_amount)
                    bill_line.bezeich = artikel.bezeich
                    bill_line.departement = artikel.departement
                    bill_line.zeit = get_current_time_in_seconds()
                    bill_line.userinit = user_init
                    bill_line.bill_datum = bill_date
                    bill_line.bezeich = bill_line.bezeich + " - " + remark
                    bill_line.betrag = to_decimal(
                        round(bill_line.betrag, price_decimal))

                    db_session.add(bill_line)

                    billjournal = Billjournal()

                    billjournal.rechnr = bill.rechnr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng = - to_decimal(refund_amount)
                    billjournal.betrag = - to_decimal(refund_amount)
                    # billjournal.bezeich = artikel.bezeich + "- Invoice No : " + \
                    #     to_string(bill.rechnr) + " - " + remark
                    billjournal.bezeich = f"{artikel.bezeich}- Invoice No : {to_string(bill.rechnr)} - {remark}"
                    billjournal.epreis = to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.billjou_ref = artikel.artnr
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date
                    billjournal.fremdwaehrng = to_decimal(
                        round(billjournal.fremdwaehrng, price_decimal))
                    billjournal.betrag = to_decimal(
                        round(billjournal.betrag, price_decimal))

                    db_session.add(billjournal)

                    umsatz = get_cache(
                        Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date

                        db_session.add(umsatz)

                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag = to_decimal(
                        umsatz.betrag) - to_decimal(refund_amount)
                    umsatz.betrag = to_decimal(
                        round(umsatz.betrag, price_decimal))

                    if artikel.artart == 2 or artikel.artart == 7:
                        bediener = get_cache(
                            Bediener, {"userinit": [(eq, user_init)]})
                        debitor = Debitor()

                        debitor.artnr = artikel.artnr
                        debitor.rechnr = bill.rechnr
                        debitor.rgdatum = bill_date
                        debitor.saldo = - to_decimal(refund_amount)
                        debitor.vesrdep = - to_decimal(refund_amount)
                        debitor.bediener_nr = bediener.nr
                        debitor.vesrdat = get_current_date()
                        debitor.transzeit = get_current_time_in_seconds()
                        debitor.vesrcod = to_string(bill_no)

                        db_session.add(debitor)

                        if refund_amount < 0:
                            # debitor.vesrcod = to_string(
                            #     bill.rechnr) + "|PAYMENT EARLY C/O"
                            debitor.vesrcod = f"{to_string(bill.rechnr)}|PAYMENT EARLY C/O"

                        else:
                            # debitor.vesrcod = to_string(
                            #     bill.rechnr) + "|REFUND EARLY C/O"
                            debitor.vesrcod = f"{to_string(bill.rechnr)}|REFUND EARLY C/O"

                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                        if res_line:
                            guest = get_cache(
                                Guest, {"gastnr": [(eq, res_line.gastnr)]})

                            if guest:
                                debitor.name = guest.name
                                debitor.gastnr = res_line.gastnr
                                debitor.gastnrmember = res_line.gastnrmember

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1369)]})

    if htparam:
        refund_div = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1365)]})

    if htparam:
        add_rmcharge = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    if remark == None:
        remark = " "

    bill = get_cache(Bill, {"rechnr": [(eq, bill_no)]})

    if bill and bill.billnr != 1:
        err_msg = "The refund process is not permitted. This bill is not the main invoice."

        return generate_output()

    elif bill and bill.billnr == 1:
        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)]})

        if queasy:
            if avail_pay:
                if round(queasy.deci1, price_decimal) == queasy.deci2:
                    create_bill_line()

                elif queasy.deci2 < queasy.deci1:
                    create_bill_line3()

            elif avail_pay == False:
                if queasy.char2 != "":
                    create_bill_line2()
                else:
                    create_bill_line4()
            create_queasy()

    return generate_output()

