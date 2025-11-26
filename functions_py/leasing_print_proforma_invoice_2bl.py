# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - add import from function_py
                    - fix closing braket on timedelta(days=1)
                    - using f"string"
                    - fix ("string").lower()
"""
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Guest, Queasy, Reslin_queasy, Htparam, Res_line, Arrangement, Billjournal, Artikel, Argt_line, Guest_pr


def leasing_print_proforma_invoice_2bl(qrecid: int, user_init: str, instalment: int):

    prepare_cache([Guest, Queasy, Reslin_queasy, Htparam, Res_line, Arrangement, Billjournal, Artikel, Argt_line])

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
    loopdate: date = None
    show_tax: bool = False
    show_package: bool = False
    netto_argt = to_decimal("0.0")
    service_argt = to_decimal("0.0")
    tax_argt = to_decimal("0.0")
    tax2_argt = to_decimal("0.0")
    serv_argt = to_decimal("0.0")
    vat_argt = to_decimal("0.0")
    vat2_argt = to_decimal("0.0")
    fact_argt = to_decimal("0.0")
    add_it: bool = False
    qty: int = 0
    argt_rate = to_decimal("0.0")
    argt_rate2 = to_decimal("0.0")
    argt_defined: bool = False
    contcode = ""
    price_decimal: int = 0
    installment: int = 0
    n_install: int = 0
    curr_periode: int = 0
    amount_install = to_decimal("0.0")
    curr_resnr: int = 0
    curr_reslinnr: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    tot_periode1: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    bill_line = guest = queasy = reslin_queasy = htparam = res_line = arrangement = billjournal = artikel = argt_line = guest_pr = None

    t_bill_line = periode_list = header_list = mbill_line = bbill_line = cbill_line = bguest = bqueasy = breslin_queasy = treslin_queasy = pqueasy = None

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
            "addvat": bool,
            "package": bool,
            "periode": int
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
            "pinvoice_no": string,
            "total_amount": Decimal,
            "payment": Decimal,
            "total_vat": Decimal,
            "balance": Decimal,
            "printed_date": date,
            "duedate": date,
            "roomno": string
        })

    Mbill_line = T_bill_line
    mbill_line_data = t_bill_line_data

    Bbill_line = T_bill_line
    bbill_line_data = t_bill_line_data

    Cbill_line = T_bill_line
    cbill_line_data = t_bill_line_data

    Bguest = create_buffer("Bguest", Guest)
    Bqueasy = create_buffer("Bqueasy", Queasy)
    Breslin_queasy = create_buffer("Breslin_queasy", Reslin_queasy)
    Treslin_queasy = create_buffer("Treslin_queasy", Reslin_queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance, tot_balance, header_list_data, t_bill_line_data, datum, log_artnr, serv, vat, netto, counter, bill_date, service, tax, tax2, fact, vat2, loopdate, show_tax, show_package, netto_argt, service_argt, tax_argt, tax2_argt, serv_argt, vat_argt, vat2_argt, fact_argt, add_it, qty, argt_rate, argt_rate2, argt_defined, contcode, price_decimal, installment, n_install, curr_periode, amount_install, curr_resnr, curr_reslinnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, tot_periode1, month_str1, month_str2, bill_line, guest, queasy, reslin_queasy, htparam, res_line, arrangement, billjournal, artikel, argt_line, guest_pr
        nonlocal qrecid, user_init, instalment
        nonlocal mbill_line, bbill_line, cbill_line, bguest, bqueasy, breslin_queasy, treslin_queasy, pqueasy
        nonlocal t_bill_line, periode_list, header_list, mbill_line, bbill_line, cbill_line, bguest, bqueasy, breslin_queasy, treslin_queasy, pqueasy
        nonlocal t_bill_line_data, periode_list_data, header_list_data

        return {
            "balance": balance,
            "tot_balance": tot_balance,
            "header-list": header_list_data,
            "t-bill-line": t_bill_line_data
        }

    def calc_periode():
        nonlocal balance, tot_balance, header_list_data, t_bill_line_data, datum, log_artnr, serv, vat, netto, bill_date, service, tax, tax2, fact, vat2, loopdate, show_tax, show_package, netto_argt, service_argt, tax_argt, tax2_argt, serv_argt, vat_argt, vat2_argt, fact_argt, add_it, qty, argt_rate, argt_rate2, argt_defined, contcode, price_decimal, installment, n_install, curr_periode, amount_install, curr_resnr, curr_reslinnr, tot_periode, v_cicilanke, v_percount, v_start, v_end, tot_periode1, month_str1, month_str2, bill_line, guest, queasy, reslin_queasy, htparam, res_line, arrangement, billjournal, artikel, argt_line, guest_pr
        nonlocal qrecid, user_init, instalment
        nonlocal mbill_line, bbill_line, cbill_line, bguest, bqueasy, breslin_queasy, treslin_queasy, pqueasy
        nonlocal t_bill_line, periode_list, header_list, mbill_line, bbill_line, cbill_line, bguest, bqueasy, breslin_queasy, treslin_queasy, pqueasy
        nonlocal t_bill_line_data, periode_list_data, header_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount: Decimal = to_decimal("0.0")
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
            if get_day(periode_rsv1) >= 31:
                periode = date_mdy(get_month(
                    periode_rsv1) + 1, month_str1[get_month(periode_rsv1) + 1 - 1], get_year(periode_rsv1)) - 1

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
                    if get_day(periode_rsv1) >= 31:
                        periode = date_mdy(get_month(
                            periode_rsv1) + 1, month_str1[get_month(periode_rsv1) + 1 - 1], get_year(periode_rsv1)) - 1

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
                        curr_amount + reslin_queasy.deci1)

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount / periode_list.diff_day)
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

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    # queasy = get_cache(
    #     Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})
    queasy = db_session.query(Queasy).filter(
        (Queasy.key == 329) & (Queasy._recid == qrecid)).with_for_update().first()
    
    if queasy:
        curr_resnr = queasy.number1
        curr_reslinnr = queasy.number2

        header_list = query(header_list_data, filters=(
            lambda header_list: header_list.reserv_no == queasy.number1), first=True)

        if not header_list:
            header_list = Header_list()
            header_list_data.append(header_list)

            header_list.reserv_no = queasy.number1
            header_list.arrival = queasy.date2
            header_list.depart = queasy.date3
            header_list.pinvoice_no = queasy.char2
            header_list.printed_date = get_current_date()
            header_list.duedate = header_list.printed_date + timedelta(days=14)

            bqueasy = get_cache(
                Queasy, {"key": [(eq, 346)], "number1": [(eq, queasy.number1)]})

            if bqueasy:
                header_list.duedate = bqueasy.date1
                show_tax = bqueasy.logi1
                show_package = bqueasy.logi2

            if instalment != 0:
                header_list.pinvoice_no = header_list.pinvoice_no + "-" + to_string(instalment)

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                header_list.roomno = res_line.zinr

                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:
                    log_artnr = arrangement.artnr_logis

                guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    header_list.company_name = guest.name
                    header_list.company_addr = guest.adresse1 + " " + guest.adresse2

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bguest:
                    header_list.guest_name = bguest.name + "," + bguest.vorname1

            for billjournal in db_session.query(Billjournal).filter(
                    (matches(Billjournal.bezeich, "*Payment Leasing*")) & (to_int(entry(0, entry(1, Billjournal.bezeich, "#"), "]")) == queasy.number1) & (Billjournal.kassabuch_nr == qrecid) & (Billjournal.billin_nr == instalment)).order_by(Billjournal._recid).all():
                header_list.payment = to_decimal(
                    header_list.payment) + to_decimal(- to_decimal(billjournal.betrag))

        calc_periode()
        tot_periode1 = 0

        for periode_list in query(periode_list_data):
            tot_periode1 = tot_periode1 + 1

        curr_periode = 0

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2)).order_by(Reslin_queasy.date1).all():

            periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2), first=True)

            if periode_list:
                if show_tax:
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
                        curr_periode = curr_periode + 1
                        t_bill_line.periode = curr_periode

                        if curr_periode == tot_periode1:
                            # t_bill_line.bezeich = "Actual Apartment Rental periode " + to_string(periode_list.periode1) + " - " +\
                            #     to_string(periode_list.periode2 + 1)
                            t_bill_line.bezeich = f"Actual Apartment Rental periode {to_string(periode_list.periode1)} - {to_string(periode_list.periode2)}"

                    serv = to_decimal("0")
                    vat = to_decimal("0")
                    vat2 = to_decimal("0")
                    netto = to_decimal("0")
                    service = to_decimal("0")
                    tax = to_decimal("0")
                    tax2 = to_decimal("0")

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, log_artnr)], "departement": [(eq, 0)]})

                    if artikel:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                            1, artikel.artnr, artikel.departement, datum))
                    netto = to_decimal(reslin_queasy.deci1 / fact)
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
                    balance = to_decimal(balance) + \
                        to_decimal(reslin_queasy.deci1)
                    tot_balance = to_decimal(
                        tot_balance + reslin_queasy.deci1)

                    if show_package:
                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                        if res_line:
                            arrangement = get_cache(
                                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                            if arrangement:
                                if reslin_queasy.deci1 != 0:
                                    for argt_line in db_session.query(Argt_line).filter(
                                            (Argt_line.argtnr == arrangement.argtnr) & not_(Argt_line.kind2)).order_by(Argt_line._recid).all():
                                        add_it = False

                                        if argt_line.vt_percnt == 0:
                                            if argt_line.betriebsnr == 0:
                                                qty = res_line.erwachs
                                            else:
                                                qty = argt_line.betriebsnr

                                        elif argt_line.vt_percnt == 1:
                                            qty = res_line.kind1

                                        elif argt_line.vt_percnt == 2:
                                            qty = res_line.kind2

                                        if qty > 0:
                                            if argt_line.fakt_modus == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 2:

                                                if res_line.ankunft == reslin_queasy.date1:
                                                    add_it = True

                                            elif argt_line.fakt_modus == 3:

                                                if (res_line.ankunft + 1) == reslin_queasy.date1:
                                                    add_it = True

                                            elif argt_line.fakt_modus == 4 and get_day(reslin_queasy.date1) == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 6:

                                                if (res_line.ankunft + (argt_line.intervall - 1)) >= reslin_queasy.date1:
                                                    add_it = True

                                        if add_it:
                                            artikel = get_cache(
                                                Artikel, {"artnr": [(eq, argt_line.argt_artnr)], "departement": [(eq, argt_line.departement)]})
                                            argt_rate = to_decimal("0")
                                            argt_rate2 = to_decimal(
                                                argt_line.betrag)
                                            argt_defined = False

                                            breslin_queasy = get_cache(
                                                Reslin_queasy, {"key": [(eq, "fargt-line")], "char1": [(eq, "")], "number1": [(eq, argt_line.departement)], "number2": [(eq, argt_line.argtnr)], "resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "number3": [(eq, argt_line.argt_artnr)], "date1": [(le, reslin_queasy.date1)], "date2": [(ge, reslin_queasy.date1)]})

                                            if breslin_queasy:
                                                for breslin_queasy in db_session.query(Breslin_queasy).filter(
                                                        (Breslin_queasy.key == "fargt-line") & (Breslin_queasy.char1 == "") & (Breslin_queasy.number1 == argt_line.departement) & (Breslin_queasy.number2 == argt_line.argtnr) & (Breslin_queasy.resnr == res_line.resnr) & (Breslin_queasy.reslinnr == res_line.reslinnr) & (Breslin_queasy.number3 == argt_line.argt_artnr) & (reslin_queasy.date1 >= Breslin_queasy.date1) & (reslin_queasy.date1 <= Breslin_queasy.date2)).order_by(Breslin_queasy._recid).all():
                                                    argt_defined = True

                                                    if breslin_queasy.char2.lower() != "" and breslin_queasy.char2.lower() != "0":
                                                        argt_rate = reslin_queasy.deci1 * to_int(breslin_queasy.char2) / 100
                                                    else:
                                                        if breslin_queasy.deci1 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci1)

                                                        elif breslin_queasy.deci2 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci2)

                                                        elif breslin_queasy.deci3 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci3)
                                                    serv_argt = to_decimal("0")
                                                    vat_argt = to_decimal("0")
                                                    vat2_argt = to_decimal("0")
                                                    netto_argt = to_decimal("0")
                                                    service_argt = to_decimal("0")
                                                    tax_argt = to_decimal("0")
                                                    tax2_argt = to_decimal("0")

                                                    serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                        calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                                    netto_argt = to_decimal(
                                                        argt_rate / fact_argt)
                                                    service_argt = to_decimal(
                                                        netto * serv_argt)
                                                    tax_argt = to_decimal(
                                                        netto * vat_argt)
                                                    tax2_argt = to_decimal(
                                                        netto * vat2_argt)

                                                    if argt_rate > 0:
                                                        argt_rate = to_decimal(
                                                            netto_argt * qty)
                                                    else:
                                                        argt_rate = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                            netto_argt) / to_decimal(100))) * to_decimal(qty)

                                                    if argt_rate != 0:
                                                        cbill_line = query(cbill_line_data, filters=(
                                                            lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                        if not cbill_line:
                                                            cbill_line = Cbill_line()
                                                            cbill_line_data.append(
                                                                cbill_line)

                                                            counter = counter + 1
                                                            cbill_line.counter = counter
                                                            cbill_line.bill_datum = periode_list.periode1
                                                            cbill_line.rechnr = 0
                                                            cbill_line.artnr = artikel.artnr
                                                            # cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                            cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                            cbill_line.package = True
                                                            cbill_line.anzahl = qty
                                                            cbill_line.zinr = " "
                                                            cbill_line.periode = curr_periode

                                                        cbill_line.betrag = to_decimal(
                                                            cbill_line.betrag) + to_decimal(argt_rate)
                                                        cbill_line.nettobetrag = to_decimal(
                                                            cbill_line.nettobetrag) + to_decimal(argt_rate)

                                            guest_pr = get_cache(
                                                Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                            if guest_pr and not argt_defined:
                                                treslin_queasy = get_cache(
                                                    Reslin_queasy, {"key": [(eq, "argt-line")], "char1": [(eq, contcode)], "number1": [(eq, res_line.reserve_int)], "number2": [(eq, arrangement.argtnr)], "reslinnr": [(eq, res_line.zikatnr)], "number3": [(eq, argt_line.argt_artnr)], "resnr": [(eq, argt_line.departement)], "date1": [(le, reslin_queasy.date1)], "date2": [(ge, reslin_queasy.date1)]})

                                                if treslin_queasy:
                                                    for treslin_queasy in db_session.query(Treslin_queasy).filter(
                                                            (Treslin_queasy.key == "argt-line") & (Treslin_queasy.char1 == (contcode).lower()) & (Treslin_queasy.number1 == res_line.reserve_int) & (Treslin_queasy.number2 == arrangement.argtnr) & (Treslin_queasy.reslinnr == res_line.zikatnr) & (Treslin_queasy.number3 == argt_line.argt_artnr) & (Treslin_queasy.resnr == argt_line.departement) & (reslin_queasy.date1 >= Treslin_queasy.date1) & (reslin_queasy.date1 <= Treslin_queasy.date2)).order_by(Treslin_queasy._recid).all():
                                                        argt_defined = True

                                                        if argt_line.vt_percnt == 0:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci1)

                                                        elif argt_line.vt_percnt == 1:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci2)

                                                        elif argt_line.vt_percnt == 2:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci3)
                                                        serv_argt = to_decimal("0")
                                                        vat_argt = to_decimal("0")
                                                        vat2_argt = to_decimal("0")
                                                        netto_argt = to_decimal("0")
                                                        service_argt = to_decimal("0")
                                                        tax_argt = to_decimal("0")
                                                        tax2_argt = to_decimal("0")

                                                        serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                            calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                                        netto_argt = to_decimal(
                                                            argt_rate / fact_argt)
                                                        service_argt = to_decimal(
                                                            netto * serv_argt)
                                                        tax_argt = to_decimal(
                                                            netto * vat_argt)
                                                        tax2_argt = to_decimal(
                                                            netto * vat2_argt)

                                                        if argt_rate > 0:
                                                            argt_rate = to_decimal(
                                                                netto_argt * qty)
                                                        else:
                                                            argt_rate = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                                netto_argt) / to_decimal(100))) * to_decimal(qty)

                                                        if argt_rate != 0:
                                                            cbill_line = query(cbill_line_data, filters=(
                                                                lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                            if not cbill_line:
                                                                cbill_line = Cbill_line()
                                                                cbill_line_data.append(
                                                                    cbill_line)

                                                                counter = counter + 1
                                                                cbill_line.counter = counter
                                                                cbill_line.bill_datum = periode_list.periode1
                                                                cbill_line.rechnr = 0
                                                                cbill_line.artnr = artikel.artnr
                                                                # cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                                cbill_line.bezeich = f"Incl. {artikel.bezeich}"
                                                                cbill_line.package = True
                                                                cbill_line.anzahl = qty
                                                                cbill_line.zinr = " "
                                                                cbill_line.periode = curr_periode

                                                            cbill_line.betrag = to_decimal(
                                                                cbill_line.betrag + argt_rate)
                                                            cbill_line.nettobetrag = to_decimal(
                                                                cbill_line.nettobetrag + argt_rate)

                                            serv_argt = to_decimal("0")
                                            vat_argt = to_decimal("0")
                                            vat2_argt = to_decimal("0")
                                            netto_argt = to_decimal("0")
                                            service_argt = to_decimal("0")
                                            tax_argt = to_decimal("0")
                                            tax2_argt = to_decimal("0")

                                            serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                            netto_argt = to_decimal(
                                                argt_rate2 / fact_argt)
                                            service_argt = to_decimal(
                                                netto * serv_argt)
                                            tax_argt = to_decimal(
                                                netto * vat_argt)
                                            tax2_argt = to_decimal(
                                                netto * vat2_argt)

                                            if argt_rate2 > 0:
                                                argt_rate2 = to_decimal(
                                                    netto_argt * qty)
                                            else:
                                                argt_rate2 = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                    netto_argt) / to_decimal(100))) * to_decimal(qty)

                                            if argt_rate == 0:
                                                cbill_line = query(cbill_line_data, filters=(
                                                    lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                if not cbill_line:
                                                    cbill_line = Cbill_line()
                                                    cbill_line_data.append(
                                                        cbill_line)

                                                    counter = counter + 1
                                                    cbill_line.counter = counter
                                                    cbill_line.bill_datum = periode_list.periode1
                                                    cbill_line.rechnr = 0
                                                    cbill_line.artnr = artikel.artnr
                                                    cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                    cbill_line.package = True
                                                    cbill_line.anzahl = qty
                                                    cbill_line.zinr = " "
                                                    cbill_line.periode = curr_periode

                                                cbill_line.betrag = to_decimal(
                                                    cbill_line.betrag + argt_rate2)
                                                cbill_line.nettobetrag = to_decimal(
                                                    cbill_line.nettobetrag + argt_rate2)

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
                        mbill_line.periode = curr_periode

                    mbill_line.betrag = to_decimal(
                        mbill_line.betrag) + to_decimal(service)
                    mbill_line.nettobetrag = to_decimal(
                        mbill_line.nettobetrag) + to_decimal(service)

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
                        bbill_line.periode = curr_periode

                    bbill_line.betrag = to_decimal(
                        bbill_line.betrag + tax)
                    bbill_line.nettobetrag = to_decimal(
                        bbill_line.nettobetrag + tax)

                elif show_tax == False:
                    t_bill_line = query(t_bill_line_data, filters=(
                        lambda t_bill_line: t_bill_line.bill_datum == periode_list.periode1), first=True)

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
                        curr_periode = curr_periode + 1
                        t_bill_line.periode = curr_periode

                    t_bill_line.betrag = to_decimal(
                        t_bill_line.betrag + reslin_queasy.deci1)
                    t_bill_line.nettobetrag = to_decimal(
                        t_bill_line.nettobetrag + reslin_queasy.deci1)
                    t_bill_line.netto = to_decimal(
                        t_bill_line.netto + reslin_queasy.deci1)
                    balance = to_decimal(
                        balance + reslin_queasy.deci1)
                    tot_balance = to_decimal(
                        tot_balance + reslin_queasy.deci1)

                    if show_package:
                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                        if res_line:
                            arrangement = get_cache(
                                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                            if arrangement:
                                if reslin_queasy.deci1 != 0:
                                    for argt_line in db_session.query(Argt_line).filter(
                                            (Argt_line.argtnr == arrangement.argtnr) & not_(Argt_line.kind2)).order_by(Argt_line._recid).all():
                                        add_it = False

                                        if argt_line.vt_percnt == 0:
                                            if argt_line.betriebsnr == 0:
                                                qty = res_line.erwachs
                                            else:
                                                qty = argt_line.betriebsnr

                                        elif argt_line.vt_percnt == 1:
                                            qty = res_line.kind1

                                        elif argt_line.vt_percnt == 2:
                                            qty = res_line.kind2

                                        if qty > 0:
                                            if argt_line.fakt_modus == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 2:

                                                if res_line.ankunft == reslin_queasy.date1:
                                                    add_it = True

                                            elif argt_line.fakt_modus == 3:
                                                if (res_line.ankunft + 1) == reslin_queasy.date1:
                                                    add_it = True

                                            elif argt_line.fakt_modus == 4 and get_day(reslin_queasy.date1) == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                                                add_it = True

                                            elif argt_line.fakt_modus == 6:
                                                if (res_line.ankunft + (argt_line.intervall - 1)) >= reslin_queasy.date1:
                                                    add_it = True

                                        if add_it:
                                            artikel = get_cache(
                                                Artikel, {"artnr": [(eq, argt_line.argt_artnr)], "departement": [(eq, argt_line.departement)]})
                                            argt_rate = to_decimal("0")
                                            argt_rate2 = to_decimal(
                                                argt_line.betrag)
                                            argt_defined = False

                                            breslin_queasy = get_cache(
                                                Reslin_queasy, {"key": [(eq, "fargt-line")], "char1": [(eq, "")], "number1": [(eq, argt_line.departement)], "number2": [(eq, argt_line.argtnr)], "resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "number3": [(eq, argt_line.argt_artnr)], "date1": [(le, reslin_queasy.date1)], "date2": [(ge, reslin_queasy.date1)]})

                                            if breslin_queasy:
                                                for breslin_queasy in db_session.query(Breslin_queasy).filter(
                                                        (Breslin_queasy.key == "fargt-line") & (Breslin_queasy.char1 == "") & (Breslin_queasy.number1 == argt_line.departement) & (Breslin_queasy.number2 == argt_line.argtnr) & (Breslin_queasy.resnr == res_line.resnr) & (Breslin_queasy.reslinnr == res_line.reslinnr) & (Breslin_queasy.number3 == argt_line.argt_artnr) & (reslin_queasy.date1 >= Breslin_queasy.date1) & (reslin_queasy.date1 <= Breslin_queasy.date2)).order_by(Breslin_queasy._recid).all():
                                                    argt_defined = True

                                                    if breslin_queasy.char2.lower() != "" and breslin_queasy.char2.lower() != "0":
                                                        argt_rate = reslin_queasy.deci1 * to_int(breslin_queasy.char2) / 100
                                                    else:
                                                        if breslin_queasy.deci1 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci1)

                                                        elif breslin_queasy.deci2 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci2)

                                                        elif breslin_queasy.deci3 != 0:
                                                            argt_rate = to_decimal(
                                                                breslin_queasy.deci3)
                                                    serv_argt = to_decimal("0")
                                                    vat_argt = to_decimal("0")
                                                    vat2_argt = to_decimal("0")
                                                    netto_argt = to_decimal("0")
                                                    service_argt = to_decimal("0")
                                                    tax_argt = to_decimal("0")
                                                    tax2_argt = to_decimal("0")

                                                    serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                        calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                                    netto_argt = to_decimal(
                                                        argt_rate / fact_argt)
                                                    service_argt = to_decimal(
                                                        netto * serv_argt)
                                                    tax_argt = to_decimal(
                                                        netto * vat_argt)
                                                    tax2_argt = to_decimal(
                                                        netto * vat2_argt)

                                                    if argt_rate > 0:
                                                        argt_rate = to_decimal(
                                                            netto_argt * qty)
                                                    else:
                                                        argt_rate = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                            netto_argt) / to_decimal(100))) * to_decimal(qty)

                                                    if argt_rate != 0:
                                                        cbill_line = query(cbill_line_data, filters=(
                                                            lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                        if not cbill_line:
                                                            cbill_line = Cbill_line()
                                                            cbill_line_data.append(
                                                                cbill_line)

                                                            counter = counter + 1
                                                            cbill_line.counter = counter
                                                            cbill_line.bill_datum = periode_list.periode1
                                                            cbill_line.rechnr = 0
                                                            cbill_line.artnr = artikel.artnr
                                                            # cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                            cbill_line.bezeich = f"Incl. {artikel.bezeich}"
                                                            cbill_line.package = True
                                                            cbill_line.anzahl = qty
                                                            cbill_line.zinr = " "
                                                            cbill_line.periode = curr_periode

                                                        cbill_line.betrag = to_decimal(
                                                            cbill_line.betrag + argt_rate)
                                                        cbill_line.nettobetrag = to_decimal(
                                                            cbill_line.nettobetrag + argt_rate)

                                            guest_pr = get_cache(
                                                Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                            if guest_pr and not argt_defined:
                                                treslin_queasy = get_cache(
                                                    Reslin_queasy, {"key": [(eq, "argt-line")], "char1": [(eq, contcode)], "number1": [(eq, res_line.reserve_int)], "number2": [(eq, arrangement.argtnr)], "reslinnr": [(eq, res_line.zikatnr)], "number3": [(eq, argt_line.argt_artnr)], "resnr": [(eq, argt_line.departement)], "date1": [(le, reslin_queasy.date1)], "date2": [(ge, reslin_queasy.date1)]})

                                                if treslin_queasy:
                                                    for treslin_queasy in db_session.query(Treslin_queasy).filter(
                                                            (Treslin_queasy.key == "argt-line") & (Treslin_queasy.char1 == (contcode).lower()) & (Treslin_queasy.number1 == res_line.reserve_int) & (Treslin_queasy.number2 == arrangement.argtnr) & (Treslin_queasy.reslinnr == res_line.zikatnr) & (Treslin_queasy.number3 == argt_line.argt_artnr) & (Treslin_queasy.resnr == argt_line.departement) & (reslin_queasy.date1 >= Treslin_queasy.date1) & (reslin_queasy.date1 <= Treslin_queasy.date2)).order_by(Treslin_queasy._recid).all():
                                                        argt_defined = True

                                                        if argt_line.vt_percnt == 0:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci1)

                                                        elif argt_line.vt_percnt == 1:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci2)

                                                        elif argt_line.vt_percnt == 2:
                                                            argt_rate = to_decimal(
                                                                treslin_queasy.deci3)
                                                        serv_argt = to_decimal("0")
                                                        vat_argt = to_decimal("0")
                                                        vat2_argt = to_decimal("0")
                                                        netto_argt = to_decimal("0")
                                                        service_argt = to_decimal("0")
                                                        tax_argt = to_decimal("0")
                                                        tax2_argt = to_decimal("0")

                                                        serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                            calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                                        netto_argt = to_decimal(
                                                            argt_rate / fact_argt)
                                                        service_argt = to_decimal(
                                                            netto * serv_argt)
                                                        tax_argt = to_decimal(
                                                            netto * vat_argt)
                                                        tax2_argt = to_decimal(
                                                            netto * vat2_argt)

                                                        if argt_rate > 0:
                                                            argt_rate = to_decimal(
                                                                netto_argt * qty)
                                                        else:
                                                            argt_rate = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                                netto_argt) / to_decimal(100))) * to_decimal(qty)

                                                        if argt_rate != 0:
                                                            cbill_line = query(cbill_line_data, filters=(
                                                                lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                            if not cbill_line:
                                                                cbill_line = Cbill_line()
                                                                cbill_line_data.append(
                                                                    cbill_line)

                                                                counter = counter + 1
                                                                cbill_line.counter = counter
                                                                cbill_line.bill_datum = periode_list.periode1
                                                                cbill_line.rechnr = 0
                                                                cbill_line.artnr = artikel.artnr
                                                                # cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                                cbill_line.bezeich = f"Incl. {artikel.bezeich}"
                                                                cbill_line.package = True
                                                                cbill_line.anzahl = qty
                                                                cbill_line.zinr = " "
                                                                cbill_line.periode = curr_periode

                                                            cbill_line.betrag = to_decimal(
                                                                cbill_line.betrag + argt_rate)
                                                            cbill_line.nettobetrag = to_decimal(
                                                                cbill_line.nettobetrag + argt_rate)

                                            serv_argt = to_decimal("0")
                                            vat_argt = to_decimal("0")
                                            vat2_argt = to_decimal("0")
                                            netto_argt = to_decimal("0")
                                            service_argt = to_decimal("0")
                                            tax_argt = to_decimal("0")
                                            tax2_argt = to_decimal("0")

                                            serv_argt, vat_argt, vat2_argt, fact_argt = get_output(
                                                calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                            netto_argt = to_decimal(
                                                argt_rate2 / fact_argt)
                                            service_argt = to_decimal(
                                                netto * serv_argt)
                                            tax_argt = to_decimal(
                                                netto * vat_argt)
                                            tax2_argt = to_decimal(
                                                netto * vat2_argt)

                                            if argt_rate2 > 0:
                                                argt_rate2 = to_decimal(
                                                    netto_argt * qty)
                                            else:
                                                argt_rate2 = (to_decimal(reslin_queasy.deci1) * to_decimal(- to_decimal(
                                                    netto_argt) / to_decimal(100))) * to_decimal(qty)

                                            if argt_rate == 0:
                                                cbill_line = query(cbill_line_data, filters=(
                                                    lambda cbill_line: cbill_line.bill_datum == periode_list.periode1 and cbill_line.package and cbill_line.artnr == artikel.artnr), first=True)

                                                if not cbill_line:
                                                    cbill_line = Cbill_line()
                                                    cbill_line_data.append(
                                                        cbill_line)

                                                    counter = counter + 1
                                                    cbill_line.counter = counter
                                                    cbill_line.bill_datum = periode_list.periode1
                                                    cbill_line.rechnr = 0
                                                    cbill_line.artnr = artikel.artnr
                                                    # cbill_line.bezeich = "Incl. " + artikel.bezeich
                                                    cbill_line.bezeich = f"Incl. {artikel.bezeich}"
                                                    cbill_line.package = True
                                                    cbill_line.anzahl = qty
                                                    cbill_line.zinr = " "
                                                    cbill_line.periode = curr_periode

                                                cbill_line.betrag = to_decimal(
                                                    cbill_line.betrag + argt_rate2)
                                                cbill_line.nettobetrag = to_decimal(
                                                    cbill_line.nettobetrag + argt_rate2)

        if queasy.char2 != "":
            if instalment == 0:
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, curr_resnr)], "reslinnr": [(eq, curr_reslinnr)], "logi2": [(eq, True)], "betriebsnr": [(eq, qrecid)]})

                if reslin_queasy:
                    for periode_list in query(periode_list_data):
                        tot_periode = tot_periode + 1

                    installment = reslin_queasy.number2
                    v_cicilanke = reslin_queasy.number1
                    v_percount = tot_periode / reslin_queasy.number2
                    v_start = ((v_cicilanke - 1) * v_percount) + 1
                    v_end = v_cicilanke * v_percount

                    reslin_queasy.logi2 = False

            else:
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, curr_resnr)], "reslinnr": [(eq, curr_reslinnr)], "number1": [(eq, instalment)], "betriebsnr": [(eq, qrecid)]})

                if reslin_queasy:
                    for periode_list in query(periode_list_data):
                        tot_periode = tot_periode + 1

                    installment = reslin_queasy.number2
                    v_cicilanke = reslin_queasy.number1
                    v_percount = tot_periode / reslin_queasy.number2
                    v_start = ((v_cicilanke - 1) * v_percount) + 1
                    v_end = v_cicilanke * v_percount

                    reslin_queasy.logi2 = False

        queasy.char1 = "*|" + to_string(bill_date) + "|" + to_string(
            get_current_time_in_seconds(), "HH:MM:SS") + "|" + user_init

    for t_bill_line in query(t_bill_line_data, filters=(lambda t_bill_line: t_bill_line.addserv == False and t_bill_line.addvat == False and t_bill_line.package == False)):
        for cbill_line in query(cbill_line_data, filters=(lambda cbill_line: cbill_line.package and cbill_line.bill_datum == t_bill_line.bill_datum)):
            t_bill_line.betrag = to_decimal(
                t_bill_line.betrag - cbill_line.betrag)
            t_bill_line.nettobetrag = to_decimal(
                t_bill_line.nettobetrag - cbill_line.nettobetrag)

    for t_bill_line in query(t_bill_line_data, sort_by=[("bill_datum", False)]):
        if installment != 0:
            if t_bill_line.periode >= v_start and t_bill_line.periode <= v_end:
                t_bill_line.betrag = to_decimal(
                    round(t_bill_line.betrag, price_decimal))
                t_bill_line.nettobetrag = to_decimal(
                    round(t_bill_line.nettobetrag, price_decimal))
                t_bill_line.serv = to_decimal(
                    round(t_bill_line.serv, price_decimal))
                t_bill_line.vat = to_decimal(
                    round(t_bill_line.vat, price_decimal))
                t_bill_line.netto = to_decimal(
                    round(t_bill_line.netto, price_decimal))

                header_list = query(header_list_data, first=True)

                if header_list:
                    header_list.total_amount = to_decimal(
                        header_list.total_amount) + to_decimal(t_bill_line.betrag)
                    header_list.total_vat = to_decimal(
                        header_list.total_vat) + to_decimal(t_bill_line.vat)
                    header_list.balance = to_decimal(
                        header_list.balance) + to_decimal(t_bill_line.betrag)

            else:
                t_bill_line_data.remove(t_bill_line)
        else:
            t_bill_line.betrag = to_decimal(
                round(t_bill_line.betrag, price_decimal))
            t_bill_line.nettobetrag = to_decimal(
                round(t_bill_line.nettobetrag, price_decimal))
            t_bill_line.serv = to_decimal(
                round(t_bill_line.serv, price_decimal))
            t_bill_line.vat = to_decimal(round(t_bill_line.vat, price_decimal))
            t_bill_line.netto = to_decimal(
                round(t_bill_line.netto, price_decimal))

            header_list = query(header_list_data, first=True)

            if header_list:
                header_list.total_amount = to_decimal(
                    header_list.total_amount + t_bill_line.betrag)
                header_list.total_vat = to_decimal(
                    header_list.total_vat + t_bill_line.vat)
                header_list.balance = to_decimal(
                    header_list.balance + t_bill_line.betrag)

    header_list = query(header_list_data, first=True)

    if header_list:
        header_list.total_amount = to_decimal(
            round(header_list.total_amount, price_decimal))
        header_list.total_vat = to_decimal(
            round(header_list.total_vat, price_decimal))
        header_list.balance = to_decimal(
            round(header_list.balance, price_decimal))
        header_list.balance = to_decimal(
            header_list.balance - header_list.payment)

    return generate_output()
