# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - add import from function_py
                    - fix closing braket on timedelta(days=1)
                    - using f"string"
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Guest, Htparam, Queasy, Artikel


def leasing_print_proforma_invoicebl(qrecid: int):

    prepare_cache([Guest, Htparam, Queasy, Artikel])

    balance = to_decimal("0.0")
    tot_balance = to_decimal("0.0")
    header_list_data = []
    t_bill_line_data = []
    datum: date = None
    log_artnr: int = 0
    serv = to_decimal("0.0")
    vat = to_decimal("0.0")
    netto = to_decimal("0.0")
    counter: int = 0
    bill_date: date = None
    service = to_decimal("0.0")
    tax = to_decimal("0.0")
    tax2 = to_decimal("0.0")
    fact = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    bill_line = guest = htparam = queasy = artikel = None

    t_bill_line = periode_list = header_list = mbill_line = bbill_line = bguest = None

    t_bill_line_data, T_bill_line = create_model_like(
        Bill_line,
        {
            "rec_id": int,
            "serv": Decimal,
            "vat": Decimal,
            "netto": Decimal,
            "art_type": int,
            "counter": int,
            "addserv": bool,
            "addvat": bool
        })
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
    header_list_data, Header_list = create_model(
        "Header_list",
        {
            "reserv_no": int,
            "company_name": string,
            "company_addr": string,
            "arrival": date,
            "depart": date,
            "guest_name": string,
            "pinvoice_no": string
        })

    Mbill_line = T_bill_line
    mbill_line_data = t_bill_line_data

    Bbill_line = T_bill_line
    bbill_line_data = t_bill_line_data

    Bguest = create_buffer("Bguest", Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, tot_balance, header_list_data, t_bill_line_data, datum, log_artnr, serv, vat, netto, counter, bill_date, service, tax, tax2, fact, vat2, month_str1, month_str2, bill_line, guest, htparam, queasy, artikel
        nonlocal qrecid
        nonlocal mbill_line, bbill_line, bguest
        nonlocal t_bill_line, periode_list, header_list, mbill_line, bbill_line, bguest
        nonlocal t_bill_line_data, periode_list_data, header_list_data

        return {
            "balance": balance,
            "tot_balance": tot_balance,
            "header-list": header_list_data,
            "t-bill-line": t_bill_line_data
        }

    def calc_periode():
        nonlocal balance, tot_balance, header_list_data, t_bill_line_data, datum, log_artnr, serv, vat, netto, bill_date, service, tax, tax2, fact, vat2, month_str1, month_str2, bill_line, guest, htparam, queasy, artikel
        nonlocal qrecid
        nonlocal mbill_line, bbill_line, bguest
        nonlocal t_bill_line, periode_list, header_list, mbill_line, bbill_line, bguest
        nonlocal t_bill_line_data, periode_list_data, header_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
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
            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                round(queasy.deci1 / periode_list.diff_day, 3))
            periode_list.tamount = to_decimal(
                periode_list.amt_periode * periode_list.diff_day)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 119)]})

    if htparam:
        log_artnr = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        header_list = query(header_list_data, filters=(
            lambda header_list: header_list.reserv_no == queasy.number3), first=True)

        if not header_list:
            header_list = Header_list()
            header_list_data.append(header_list)

            header_list.reserv_no = queasy.number3
            header_list.arrival = queasy.date2
            header_list.depart = queasy.date3
            # header_list.pinvoice_no = "PINV/" + to_string(get_month(bill_date)) + "/" + to_string(get_year(bill_date)) + "/" + to_string(queasy.number3, "999999")
            header_list.pinvoice_no = f"PINV/{to_string(get_month(bill_date))}/{to_string(get_year(bill_date))}/{to_string(queasy.number3, "999999")}"

            guest = get_cache(
                Guest, {"gastnr": [(eq, queasy.number2)]})

            if guest:
                header_list.company_name = guest.name
                header_list.company_addr = guest.adresse1 + " " + guest.adresse2

            bguest = get_cache(
                Guest, {"gastnr": [(eq, queasy.number1)]})

            if bguest:
                header_list.guest_name = bguest.name + "," + bguest.vorname1

        calc_periode()
        for datum in date_range(queasy.date2, (queasy.date3 - 1)):
            periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.datum >= periode_list.periode1 and datum <= periode_list.periode2), first=True)

            if periode_list:
                t_bill_line = query(t_bill_line_data, filters=(lambda t_bill_line: t_bill_line.bill_datum == periode_list.periode1 and t_bill_line.addserv == False and t_bill_line.addvat == False), first=True)

                if not t_bill_line:
                    t_bill_line = T_bill_line()
                    t_bill_line_data.append(t_bill_line)

                    t_bill_line.bill_datum = periode_list.periode1
                    t_bill_line.rechnr = 0
                    # t_bill_line.bezeich = "Actual Apartment Rental periode " + to_string(periode_list.periode1) + " - " +\
                    #     to_string(periode_list.periode2)
                    t_bill_line.bezeich = f"Actual Apartment Rental periode {to_string(periode_list.periode1)} - {to_string(periode_list.periode2)}" 
                    t_bill_line.anzahl = 1
                    t_bill_line.zinr = ""

                serv = to_decimal("0")
                vat = to_decimal("0")
                netto = to_decimal("0")
                service = to_decimal("0")
                tax = to_decimal("0")
                tax2 = to_decimal("0")

                artikel = get_cache(
                    Artikel, {"artnr": [(eq, log_artnr)], "departement": [(eq, 0)]})

                if artikel:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                        1, artikel.artnr, artikel.departement, datum))
                netto = to_decimal(periode_list.amt_periode / fact)
                service = to_decimal(netto * serv)
                tax = to_decimal(netto * vat)
                tax2 = to_decimal(netto * vat2)

                t_bill_line.betrag = to_decimal(
                    t_bill_line.betrag + netto)
                t_bill_line.nettobetrag = to_decimal(
                    t_bill_line.nettobetrag + netto)
                t_bill_line.serv = to_decimal(
                    t_bill_line.serv + service)
                t_bill_line.vat = to_decimal(
                    t_bill_line.vat + tax)
                t_bill_line.netto = to_decimal(
                    t_bill_line.netto + netto)
                balance = to_decimal(
                    balance + periode_list.amt_periode)
                tot_balance = to_decimal(
                    tot_balance + periode_list.amt_periode)

                mbill_line = query(mbill_line_data, filters=(lambda mbill_line: mbill_line.bill_datum == periode_list.periode1 and mbill_line.addserv and mbill_line.addvat == False), first=True)

                if not mbill_line:
                    mbill_line = Mbill_line()
                    mbill_line_data.append(mbill_line)

                    counter = counter + 1
                    mbill_line.counter = counter
                    mbill_line.bill_datum = periode_list.periode1
                    mbill_line.rechnr = 0
                    mbill_line.bezeich = "Service Charge"
                    mbill_line.addserv = True
                    mbill_line.anzahl = 1
                    mbill_line.zinr = " "

                mbill_line.betrag = to_decimal(
                    mbill_line.betrag + service)
                mbill_line.nettobetrag = to_decimal(
                    mbill_line.nettobetrag + service)

                bbill_line = query(bbill_line_data, filters=(lambda bbill_line: bbill_line.bill_datum == periode_list.periode1 and bbill_line.addserv == False and bbill_line.addvat), first=True)

                if not bbill_line:
                    bbill_line = Bbill_line()
                    bbill_line_data.append(bbill_line)

                    counter = counter + 1
                    bbill_line.counter = counter
                    bbill_line.bill_datum = periode_list.periode1
                    bbill_line.rechnr = 0
                    bbill_line.bezeich = "VAT Rental"
                    bbill_line.addvat = True
                    bbill_line.anzahl = 1
                    bbill_line.zinr = " "

                bbill_line.betrag = to_decimal(
                    bbill_line.betrag + tax)
                bbill_line.nettobetrag = to_decimal(
                    bbill_line.nettobetrag + tax)

    for t_bill_line in query(t_bill_line_data, sort_by=[("bill_datum", False)]):
        t_bill_line.betrag = to_decimal(round(t_bill_line.betrag, 0))
        t_bill_line.nettobetrag = to_decimal(round(t_bill_line.nettobetrag, 0))
        t_bill_line.serv = to_decimal(round(t_bill_line.serv, 0))
        t_bill_line.vat = to_decimal(round(t_bill_line.vat, 0))
        t_bill_line.netto = to_decimal(round(t_bill_line.netto, 0))

    return generate_output()
