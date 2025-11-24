# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix ("string").lower()
                    - use f"string"
"""
#------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Artikel, Queasy, Htparam, Bediener, Res_history, Res_line, Counters, Reservation, Guest, Bill, Bill_line, Debitor, Billjournal, Umsatz
from functions.next_counter_for_update import next_counter_for_update


def leasing_cancel_installmentbl(qrecid: int, user_init: str):
    prepare_cache([Reslin_queasy, Artikel, Queasy, Htparam, Bediener, Res_history, Res_line, Counters, Reservation, Guest, Bill, Bill_line, Debitor, Billjournal, Umsatz])

    error_flag = 0
    success_flag = False
    ar_ledger: int = 0
    divered_rental: int = 0
    bill_date: date = None
    tot_amount = to_decimal("0.0")
    inv_no: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    installment: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    reslin_queasy = artikel = queasy = htparam = bediener = res_history = res_line = counters = reservation = guest = bill = bill_line = debitor = billjournal = umsatz = None
    periode_list = breslin = bartikel = treslin = pqueasy = None

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

    Breslin = create_buffer("Breslin", Reslin_queasy)
    Bartikel = create_buffer("Bartikel", Artikel)
    Treslin = create_buffer("Treslin", Reslin_queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)

    db_session = local_storage.db_session
    last_count = 0
    error_lock: str = ""


    def generate_output():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

        return {
            "error_flag": error_flag,
            "success_flag": success_flag
        }

    def create_log():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

        bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        # res_history.aenderung = "Cancel installment - Reservation no : " + \
        #     to_string(queasy.number1)
        res_history.aenderung = f"Cancel installment - Reservation no : {queasy.number1}"
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
                to_string("Service Apartement - Cancel installment : ") + ";" +\
                to_string(res_line.resnr) + ";" +\
                to_string("NO", "x(3)") + ";" +\
                to_string("NO", "x(3)") + ";"

    def create_bill():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

        billnr: int = 0

        # counters = get_cache(Counters, {"counter_no": [(eq, 3)]})

        # if not counters:
        #     counters = Counters()

        #     counters.counter_no = 3
        #     counters.counter_bez = "counter for Bill No"

        #     db_session.add(counters)

        # counters.counter = counters.counter + 1
        # billnr = counters.counter
        
        last_count, error_lock = get_output(next_counter_for_update(3))
        billnr = last_count

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            reservation = get_cache(
                Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
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
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

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
            #     "[" + "Cancel installment #" + to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel Installment #{queasy.number1}]"

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
            #     "[" + "Cancel installment #" + to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel Installment #{queasy.number1}]"

            db_session.add(bill_line)

    def create_ar():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

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
        billjournal.fremdwaehrng = to_decimal(tot_amount)
        billjournal.betrag = to_decimal(tot_amount)
        # billjournal.bezeich = artikel.bezeich + \
        #     "[" + "Cancel installment#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Cancel Installment #{queasy.number1}]"
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
        umsatz.betrag = to_decimal(umsatz.betrag) + to_decimal(tot_amount)

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
        #     "[" + "Cancel installment#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Cancel Installment #{queasy.number1}]"
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

    def calc_periode():
        nonlocal error_flag, success_flag, ar_ledger, divered_rental, bill_date, tot_amount, inv_no, tot_periode, v_cicilanke, v_percount, v_start, v_end, installment, month_str1, month_str2, reslin_queasy, artikel, queasy, htparam, bediener, res_history, res_line, counters, reservation, guest, bill, bill_line, debitor, billjournal, umsatz
        nonlocal qrecid, user_init
        nonlocal breslin, bartikel, treslin, pqueasy
        nonlocal periode_list, breslin, bartikel, treslin, pqueasy
        nonlocal periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount = to_decimal("0.0")
        loopdate: date = None
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
                periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

        else:
            periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

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
                        periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

                else:
                    periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1), get_day(periode_rsv1), get_year(periode_rsv1)) - 1

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
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "date1": [(le, loopdate)], "date2": [(le, loopdate)]})

                if reslin_queasy:
                    curr_amount = to_decimal(
                        curr_amount + reslin_queasy.deci1)

            periode_list.diff_day = (periode_list.periode2 - periode_list.periode1) + 1
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

    periode_list_data.clear()

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        reslin_queasy = get_cache(
            Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "logi3": [(eq, True)]})

        if reslin_queasy:
            error_flag = 1

            return generate_output()
        calc_periode()

        for periode_list in query(periode_list_data):
            tot_periode = tot_periode + 1

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "actual-invoice") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2) & (Reslin_queasy.logi1 == False) & (Reslin_queasy.logi2 == False)).order_by(Reslin_queasy._recid).all():
            installment = reslin_queasy.number2
            v_cicilanke = reslin_queasy.number1
            v_percount = tot_periode / reslin_queasy.number2
            v_start = ((v_cicilanke - 1) * v_percount) + 1
            v_end = v_cicilanke * v_percount

            breslin_obj_list = {}
            for breslin in db_session.query(Breslin).filter(
                    (Breslin.key == "arrangement") & (Breslin.resnr == queasy.number1) & (Breslin.reslinnr == queasy.number2)).order_by(Breslin.date1).all():
                periode_list = query(periode_list_data, (lambda periode_list: breslin.date1 >= periode_list.periode1 and breslin.date1 <= periode_list.periode2 and periode_list.counter >= v_start and periode_list.counter <= v_end), first=True)
                if not periode_list:
                    continue

                if breslin_obj_list.get(breslin._recid):
                    continue
                else:
                    breslin_obj_list[breslin._recid] = True

                tot_amount = to_decimal(tot_amount + breslin.deci1)

        for breslin in db_session.query(Breslin).filter(
                (Breslin.key == "actual-invoice") & (Breslin.resnr == queasy.number1) & (Breslin.reslinnr == queasy.number2)).order_by(Breslin._recid).all():
            breslin.char1 = "1|" + user_init + "|" + \
                to_string(bill_date) + "|" + \
                to_string(get_current_time_in_seconds())

        inv_no = to_int(queasy.char2)

        if tot_amount != 0:
            create_bill()
            create_ar()
        create_log()
        success_flag = True

    return generate_output()
