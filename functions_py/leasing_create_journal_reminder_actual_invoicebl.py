# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - added import from function_py
                    - fix MINIMUM func to min func in python
                    - using f"string"
                    - fix closing on timedelta(days=1)
                    - fix ("string").lower()
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Artikel, Queasy, Reslin_queasy, Htparam, Res_line, Arrangement, Counters, Reservation, Guest, Bediener, Bill, Bill_line, Debitor, Billjournal, Umsatz


def leasing_create_journal_reminder_actual_invoicebl(qrecid: int, pinvoice_no: str, user_init: str, installment: int):

    prepare_cache([Artikel, Queasy, Reslin_queasy, Htparam, Res_line, Arrangement, Counters, Reservation, Guest, Bediener, Bill, Bill_line, Debitor, Billjournal, Umsatz])

    success_flag = False
    log_artnr: int = 0
    ar_ledger: int = 0
    divered_rental: int = 0
    bill_date: date = None
    tot_amount = to_decimal("0.0")
    tot_nettamount = to_decimal("0.0")
    tot_serv = to_decimal("0.0")
    tot_tax = to_decimal("0.0")
    datum: date = None
    netto = to_decimal("0.0")
    service = to_decimal("0.0")
    tax = to_decimal("0.0")
    tax2 = to_decimal("0.0")
    serv = to_decimal("0.0")
    vat = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    fact = to_decimal("0.0")
    loopi: int = 0
    serv_acctno = ""
    vat_acctno = ""
    vat_fibu = ""
    vat2_fibu = ""
    serv_fibu = ""
    div_fibu = ""
    rechnr: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    prev_tax = to_decimal("0.0")
    prev_serv = to_decimal("0.0")
    prev_amount_debit = to_decimal("0.0")
    prev_amount_credit = to_decimal("0.0")
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    artikel = queasy = reslin_queasy = htparam = res_line = arrangement = counters = reservation = guest = bediener = bill = bill_line = debitor = billjournal = umsatz = None

    periode_list = bartikel = bqueasy = pqueasy = rqueasy = None

    periode_list_data, Periode_list = create_model(
        "Periode_list",
        {
            "counter": int,
            "periode1": date,
            "periode2": date,
            "diff_day": int,
            "amt_periode": Decimal,
            "tamount": Decimal
        })

    Bartikel = create_buffer("Bartikel", Artikel)
    Bqueasy = create_buffer("Bqueasy", Queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)
    Rqueasy = create_buffer("Rqueasy", Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy

        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        return {
            "success_flag": success_flag
        }

    def endofmonth(pdate: date):
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        y: int = 0
        m: int = 0
        y = get_year(pdate)
        m = get_month(pdate)

        if m == 12:
            return date_mdy(1, 1, y + 1) - 1
        else:
            return date_mdy(m + 1, 1, y) - 1

    def addmonths(pdate: date, pmonths: int):
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        y: int = 0
        m: int = 0
        d: int = 0
        ny: int = 0
        nm: int = 0
        nlast: date = None
        nd: int = 0
        y = get_year(pdate)
        m = get_month(pdate)
        d = get_day(pdate)

        ny = y + to_int((m - 1 + pmonths) / 12)
        nm = ((m - 1 + pmonths) % 12) + 1

        if nm == 12:
            nlast = date_mdy(1, 1, ny + timedelta(days=1)) - timedelta(days=1)
        else:
            nlast = date_mdy(nm + 1, 1, ny) - timedelta(days=1)
        # nd = MINIMUM (d, get_day(nlast))
        nd = min(d, get_day(nlast))

        return date_mdy(nm, nd, ny)

    def create_bill():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        billnr: int = 0
        counters = get_cache(
            Counters, {"counter_no": [(eq, 3)]})

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
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        bartikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if bartikel:
            bill_line = Bill_line()

            bill_line.rechnr = billno
            bill_line.artnr = divered_rental
            bill_line.anzahl = 1
            bill_line.betrag = to_decimal(tot_amount)
            bill_line.bezeich = bartikel.bezeich
            bill_line.departement = bartikel.departement
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            # bill_line.bezeich = bill_line.bezeich + "[" + "Create Actual Invoice #" + to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Create Actual Invoice #{to_string(queasy.number1)}]"

            db_session.add(bill_line)

        bartikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if bartikel:
            bill_line = Bill_line()

            bill_line.rechnr = billno
            bill_line.artnr = ar_ledger
            bill_line.anzahl = 1
            bill_line.betrag = - to_decimal(tot_amount)
            bill_line.bezeich = bartikel.bezeich
            bill_line.departement = bartikel.departement
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            # bill_line.bezeich = bill_line.bezeich + "[" + "Create Actual Invoice #" + to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Create Actual Invoice #{to_string(queasy.number1)}]"

            db_session.add(bill_line)

    def create_ar():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        bediener = get_cache(
            Bediener, {"userinit": [(eq, user_init)]})
        debitor = Debitor()

        debitor.artnr = ar_ledger
        debitor.rechnr = rechnr
        debitor.rgdatum = bill_date
        debitor.saldo = to_decimal(tot_amount)
        debitor.vesrdep = to_decimal(tot_amount)
        debitor.bediener_nr = bediener.nr
        debitor.vesrdat = get_current_date()
        debitor.transzeit = get_current_time_in_seconds()
        debitor.vesrcod = to_string(rechnr)

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

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = ar_ledger
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - to_decimal(tot_amount)
        billjournal.betrag = - to_decimal(tot_amount)
        # billjournal.bezeich = artikel.bezeich + "[" + "Print actual Invoice#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Print actual Invoice #{to_string(queasy.number1)}]"
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
        umsatz.betrag = to_decimal(umsatz.betrag) + (- to_decimal(tot_amount))

        artikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = divered_rental
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = to_decimal(tot_amount)
        billjournal.betrag = to_decimal(tot_amount)
        billjournal.bezeich = artikel.bezeich + \
            "[" + "Print actual Invoice#" + to_string(queasy.number1) + "]"
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
        umsatz.betrag = to_decimal(umsatz.betrag + tot_amount)

    def calc_periode():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, month_str1, month_str2, artikel, queasy, reslin_queasy, htparam, res_line, arrangement, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, rqueasy
        nonlocal periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount = to_decimal("0.0")
        loopdate: date = None
        breslin = None
        Breslin = create_buffer("Breslin", Reslin_queasy)
        periode_rsv1 = queasy.date2
        periode_rsv2 = queasy.date3

        if get_month(periode_rsv1) + 1 > 12:
            periode = date_mdy(1, get_day(periode_rsv1), get_year(
                periode_rsv1) + timedelta(days=1) - 1)

        elif get_month(periode_rsv1) + 1 == 2:
            if get_day(periode_rsv1) >= 29:
                if get_year(periode_rsv1) % 4 != 0:
                    periode = date_mdy(get_month(periode_rsv1) + 1, month_str1[get_month(
                        periode_rsv1) + 1 - timedelta(days=1), get_year(periode_rsv1)])

                elif get_year(periode_rsv1) % 4 == 0:
                    periode = date_mdy(get_month(periode_rsv1) + 1, month_str2[get_month(
                        periode_rsv1) + 1 - timedelta(days=1), get_year(periode_rsv1)])

            else:
                periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1),
                                   get_day(periode_rsv1), get_year(periode_rsv1)) - 1

        else:
            periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1),
                               get_day(periode_rsv1), get_year(periode_rsv1)) - 1

        for loopi in date_range(periode_rsv1, periode_rsv2 - 1):
            if loopi > periode:
                periode_rsv1 = loopi

                if get_month(periode_rsv1) + 1 > 12:
                    periode = date_mdy(1, get_day(periode_rsv1), get_year(
                        periode_rsv1) + timedelta(days=1) - 1)

                elif get_month(periode_rsv1) + 1 == 2:
                    if get_day(periode_rsv1) >= 29:
                        if get_year(periode_rsv1) % 4 != 0:
                            periode = date_mdy(get_month(periode_rsv1) + 1, month_str1[get_month(
                                periode_rsv1) + 1 - timedelta(days=1), get_year(periode_rsv1)])

                        elif get_year(periode_rsv1) % 4 == 0:
                            periode = date_mdy(get_month(periode_rsv1) + 1, month_str2[get_month(
                                periode_rsv1) + 1 - timedelta(days=1), get_year(periode_rsv1)])

                    else:
                        periode = date_mdy(get_month(
                            periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

                else:
                    periode = date_mdy(get_month(
                        periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

            if loopi <= periode:
                periode_list = query(periode_list_data, filters=(
                    lambda periode_list: periode_list.periode1 == periode_rsv1), first=True)

                if not periode_list:
                    periode_list = Periode_list()
                    periode_list_data.append(periode_list)

                    periode_list.periode1 = periode_rsv1
                    counter = counter + 1
                    periode_list.counter = counter

                periode_list.periode2 = loopi

        for periode_list in query(periode_list_data, sort_by=[("periode1", False)]):
            curr_amount = to_decimal("0")

            for loopdate in date_range(periode_list.periode1, periode_list.periode2):
                breslin = get_cache(
                    Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "date1": [(le, loopdate)], "date2": [(le, loopdate)]})

                if breslin:
                    curr_amount = to_decimal(curr_amount + breslin.deci1)

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount / periode_list.diff_day)
            periode_list.tamount = to_decimal(
                periode_list.amt_periode * periode_list.diff_day)

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

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 119)]})

    if htparam:
        log_artnr = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 133)]})

    artikel = get_cache(
        Artikel, {"artnr": [(eq, htparam.finteger)], "departement": [(eq, 0)]})

    if artikel:
        serv_acctno = artikel.fibukonto

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 132)]})

    artikel = get_cache(
        Artikel, {"artnr": [(eq, htparam.finteger)], "departement": [(eq, 0)]})

    if artikel:
        vat_acctno = artikel.fibukonto
    periode_list_data.clear()

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        calc_periode()
        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            arrangement = get_cache(
                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if arrangement:
                log_artnr = arrangement.artnr_logis

            rqueasy = get_cache(
                Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "number1": [(eq, installment)]})

            if rqueasy:
                for periode_list in query(periode_list_data):
                    tot_periode = tot_periode + 1

                v_cicilanke = installment
                v_percount = tot_periode / rqueasy.number2
                v_start = ((v_cicilanke - 1) * v_percount) + 1
                v_end = v_cicilanke * v_percount

                reslin_queasy_obj_list = {}
                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == rqueasy.resnr) & (Reslin_queasy.reslinnr == rqueasy.reslinnr)).order_by(Reslin_queasy.date1).all():
                    periode_list = query(periode_list_data, (lambda periode_list: reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2 and periode_list.counter >= v_start and periode_list.counter <= v_end), first=True)
                    if not periode_list:
                        continue

                    if reslin_queasy_obj_list.get(reslin_queasy._recid):
                        continue
                    else:
                        reslin_queasy_obj_list[reslin_queasy._recid] = True

                    service = to_decimal("0")
                    tax = to_decimal("0")
                    tax2 = to_decimal("0")
                    netto = to_decimal("0")

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, log_artnr)]})

                    if artikel:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                            1, artikel.artnr, artikel.departement, datum))
                    netto = to_decimal(reslin_queasy.deci1 / fact)
                    service = to_decimal(netto * serv)
                    tax = to_decimal(netto * vat)
                    tax2 = to_decimal(netto * vat2)

                    tot_nettamount = to_decimal(tot_nettamount + netto)
                    tot_serv = to_decimal(tot_serv + service)
                    tot_tax = to_decimal(tot_tax + tax)
                    tot_amount = to_decimal(tot_amount + reslin_queasy.deci1)

                rqueasy.logi1 = False
                rqueasy.logi2 = True
                rqueasy.date3 = bill_date

            tot_nettamount = to_decimal(round(tot_nettamount, 0))
            tot_serv = to_decimal(round(tot_serv, 0))
            tot_tax = to_decimal(round(tot_tax, 0))
            tot_amount = to_decimal(round(tot_amount, 0))

            rechnr = to_int(pinvoice_no)

            create_bill()
            create_ar()
            success_flag = True

    return generate_output()
