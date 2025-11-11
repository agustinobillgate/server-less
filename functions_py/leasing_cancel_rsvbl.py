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
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Artikel, Htparam, Queasy, Res_line, Arrangement, Reslin_queasy, Counters, Reservation, Guest, Bediener, Bill, Bill_line, Debitor, Billjournal, Umsatz, Gl_jouhdr, Gl_journal


def leasing_cancel_rsvbl(qrecid: int, user_init: str):

    prepare_cache([Artikel, Htparam, Queasy, Res_line, Arrangement, Reslin_queasy, Counters,Reservation, Guest, Bediener, Bill, Bill_line, Billjournal, Umsatz, Gl_jouhdr, Gl_journal])

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
    del_mainres: bool = False
    msg_str = ""
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    artikel = htparam = queasy = res_line = arrangement = reslin_queasy = counters = reservation = guest = bediener = bill = bill_line = debitor = billjournal = umsatz = gl_jouhdr = gl_journal = None
    periode_list = bartikel = None

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

    db_session = local_storage.db_session

    def generate_output():
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
        nonlocal periode_list_data

        return {}

    def create_bill():
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
        nonlocal periode_list_data

        billnr: int = 0

        counters = get_cache(Counters, {"counter_no": [(eq, 3)]})

        if not counters:
            counters = Counters()

            counters.counter_no = 3
            counters.counter_bez = "counter for Bill No"

            db_session.add(counters)

        counters.counter = counters.counter + 1
        billnr = counters.counter

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            reservation = get_cache(
                Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
            bill = Bill()
            db_session.add(bill)

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

            create_bill_line(billnr)

    def create_bill_line(billno: int):
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
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
            #     "[" + "Cancel service Apartment #" + \
            #     to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel service Apartment #{queasy.number1}]"

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
            #     "[" + "Cancel service Apartment #" + \
            #     to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Cancel service Apartment #{queasy.number1}]"

            db_session.add(bill_line)

    def create_ar():
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
        nonlocal periode_list_data

        bdebt = None
        Bdebt = create_buffer("Bdebt", Debitor)

        debitor = get_cache(
            Debitor, {"vesrcod": [(eq, queasy.char2)], "zahlkonto": [(eq, 0)]})

        if debitor:
            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
            bdebt = Debitor()
            db_session.add(bdebt)

            bdebt.artnr = ar_ledger
            bdebt.rechnr = to_int(queasy.char2)
            bdebt.rgdatum = bill_date
            bdebt.saldo = - to_decimal(tot_amount)
            bdebt.vesrdep = - to_decimal(tot_amount)
            bdebt.bediener_nr = bediener.nr
            bdebt.vesrdat = get_current_date()
            bdebt.transzeit = get_current_time_in_seconds()
            # bdebt.vesrcod = queasy.char2 + "|Cancel service Apartment"
            bdebt.vesrcod = f"{queasy.char2}|Cancel service Apartment"

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    bdebt.name = guest.name
                    bdebt.gastnr = res_line.gastnr
                    bdebt.gastnrmember = res_line.gastnrmember

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
        #     "[" + "Cancel service Apartment#" + to_string(queasy.number1) + "]"
        billjournal.bezeich = f"{artikel.bezeich}[Cancel service Apartment #{queasy.number1}]"
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
        billjournal.bezeich = artikel.bezeich + \
            "[" + "Cancel service Apartment#" + to_string(queasy.number1) + "]"
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
        umsatz.betrag = to_decimal(umsatz.betrag) + (- to_decimal(tot_amount))

    def create_journal():
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
        nonlocal periode_list_data

        gname: string = ""

        counters = get_cache(Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
        counters.counter = counters.counter + 1

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                gname = guest.name

        gl_jouhdr = Gl_jouhdr()

        gl_jouhdr.jnr = counters.counter
        # gl_jouhdr.refno = "CANCEL-" + \
        #     to_string(queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.refno = f"CANCEL-{queasy.number1}-{bill_date}"
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1

        db_session.add(gl_jouhdr)

        guest = get_cache(Guest, {"gastnr": [(eq, queasy.number2)]})

        if guest:
            # gl_jouhdr.bezeich = "CANCEL-service RESIDENT-" + \
            #     to_string(queasy.number1) + "-" + to_string(bill_date)
            gl_jouhdr.bezeich = f"CANCEL-service RESIDENT-{queasy.number1}-{bill_date}"

        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.credit = to_decimal(tot_amount)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if artikel:
            gl_journal.fibukonto = artikel.fibukonto

        gl_jouhdr.credit = to_decimal(
            gl_jouhdr.credit + gl_journal.credit)
        gl_jouhdr.debit = to_decimal(
            gl_jouhdr.debit + gl_journal.debit)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if artikel:
            div_fibu = artikel.fibukonto

            if artikel.service_code != 0:
                htparam = get_cache(
                    Htparam, {"paramnr": [(eq, artikel.service_code)]})

                if htparam:
                    serv_fibu = entry(0, htparam.fchar, chr_unicode(2))

            if artikel.mwst_code != 0:
                htparam = get_cache(
                    Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                if htparam:
                    vat_fibu = entry(0, htparam.fchar, chr_unicode(2))

            if artikel.prov_code != 0:
                htparam = get_cache(
                    Htparam, {"paramnr": [(eq, artikel.prov_code)]})

                if htparam:
                    vat2_fibu = entry(0, htparam.fchar, chr_unicode(2))
        for loopi in range(1, 3 + 1):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = gl_jouhdr.jnr
            gl_journal.userinit = user_init
            gl_journal.zeit = get_current_time_in_seconds()
            gl_journal.bemerk = gl_jouhdr.bezeich

            if loopi == 1:
                gl_journal.debit = to_decimal(tot_nettamount)
                gl_journal.fibukonto = div_fibu

            elif loopi == 2:
                gl_journal.debit = to_decimal(tot_serv)
                gl_journal.fibukonto = serv_fibu

            elif loopi == 3:
                gl_journal.debit = to_decimal(tot_tax)
                gl_journal.fibukonto = vat_fibu

            gl_jouhdr.credit = to_decimal(
                gl_jouhdr.credit + gl_journal.credit)
            gl_jouhdr.debit = to_decimal(
                gl_jouhdr.debit + gl_journal.debit)

    def calc_periode():
        nonlocal log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, del_mainres, msg_str, month_str1, month_str2, artikel, htparam, queasy, res_line, arrangement, reslin_queasy, counters, reservation, guest, bediener, bill, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, user_init
        nonlocal bartikel
        nonlocal periode_list, bartikel
        nonlocal periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount: Decimal = to_decimal("0.0")
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

        for periode_list in query(periode_list_data):
            curr_amount = to_decimal("0")

            for loopdate in date_range(periode_list.periode1, periode_list.periode2):
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "date1": [(le, loopdate)], "date2": [(le, loopdate)]})

                if reslin_queasy:
                    curr_amount = to_decimal(
                        curr_amount) + to_decimal(reslin_queasy.deci1)

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
        # Artikel, {"artnr": [(eq, finteger)], "departement": [(eq, 0)]})
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
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)], "char2": [(ne, "")], "logi1": [(eq, False)]})

    if queasy:
        calc_periode()

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            arrangement = get_cache(
                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if arrangement:
                log_artnr = arrangement.artnr_logis

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                    (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2)).order_by(Reslin_queasy.date1).all():

                periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2), first=True)

                if periode_list:
                    service = to_decimal("0")
                    tax = to_decimal("0")
                    tax2 = to_decimal("0")
                    netto = to_decimal("0")

                    artikel = get_cache(Artikel, {"artnr": [(eq, log_artnr)]})

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

            tot_nettamount = to_decimal(round(tot_nettamount, 0))
            tot_serv = to_decimal(round(tot_serv, 0))
            tot_tax = to_decimal(round(tot_tax, 0))
            tot_amount = to_decimal(round(tot_amount, 0))

            create_bill()
            create_ar()
            queasy.logi1 = True

    return generate_output()
