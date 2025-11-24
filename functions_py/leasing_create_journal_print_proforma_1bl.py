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
#-------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#-------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Artikel, Queasy, Htparam, Res_line, Arrangement, Reslin_queasy, Bill, Counters, Reservation, Guest, Bediener, Bill_line, Debitor, Billjournal, Umsatz, Gl_jouhdr, Gl_journal
from functions.next_counter_for_update import next_counter_for_update


def leasing_create_journal_print_proforma_1bl(qrecid: int, pinvoice_no: str, user_init: str, installment: int):

    prepare_cache([Artikel, Queasy, Htparam, Res_line, Arrangement, Reslin_queasy, Bill, Counters,Reservation, Guest, Bediener, Bill_line, Debitor, Billjournal, Umsatz, Gl_jouhdr, Gl_journal])

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
    prev_tax = to_decimal("0.0")
    prev_serv = to_decimal("0.0")
    prev_amount_debit = to_decimal("0.0")
    prev_amount_credit = to_decimal("0.0")
    curr_due: date = None
    loopj: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    artikel = queasy = htparam = res_line = arrangement = reslin_queasy = bill = counters = reservation = guest = bediener = bill_line = debitor = billjournal = umsatz = gl_jouhdr = gl_journal = None

    periode_list = bartikel = bqueasy = pqueasy = tqueasy = None

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
    Tqueasy = create_buffer("Tqueasy", Queasy)

    db_session = local_storage.db_session
    pinvoice_no = pinvoice_no.strip()
    last_count = 0
    error_lock: str = ""


    def generate_output():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list_data

        return {
            "success_flag": success_flag
        }

    def endofmonth(pdate: date):
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
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
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
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
        # nd = MINIMUM(d, get_day(nlast))
        nd = min(d, get_day(nlast))

        return date_mdy(nm, nd, ny)

    def create_bill():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list_data

        billnr: int = 0

        # counters = get_cache(
        #     Counters, {"counter_no": [(eq, 3)]})

        # if not counters:
        #     counters = Counters()

        #     counters.counter_no = 3
        #     counters.counter_bez = "Counter for Bill No"

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
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
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
            # bill_line.bezeich = bill_line.bezeich + \
            #     "[" + "Create Actual Invoice #" + \
            #     to_string(queasy.number1) + "]"
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
            # bill_line.bezeich = bill_line.bezeich + \
            #     "[" + "Create Actual Invoice #" + \
            #     to_string(queasy.number1) + "]"
            bill_line.bezeich = f"{bill_line.bezeich}[Create Actual Invoice #{to_string(queasy.number1)}]"

            db_session.add(bill_line)

    def create_ar():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list_data

        bediener = get_cache(
            Bediener, {"userinit": [(eq, user_init)]})

        debitor = get_cache(
            Debitor, {"rechnr": [(eq, rechnr)], "zahlkonto": [(eq, 0)]})

        if not debitor:
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

        elif debitor.saldo != tot_amount:
            debitor.saldo = to_decimal(tot_amount)
            debitor.vesrdep = to_decimal(tot_amount)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()

        billjournal.artnr = ar_ledger
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - to_decimal(tot_amount)
        billjournal.betrag = - to_decimal(tot_amount)
        # billjournal.bezeich = artikel.bezeich + \
        #     "[" + "Print actual Invoice#" + to_string(queasy.number1) + "]"
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

    def create_journal():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list_data

        gname: string = ""
        bjouhdr = None
        bjournal = None
        tjournal = None
        Bjouhdr = create_buffer("Bjouhdr", Gl_jouhdr)
        Bjournal = create_buffer("Bjournal", Gl_journal)
        Tjournal = create_buffer("Tjournal", Gl_journal)
        prev_amount_debit = to_decimal("0")
        prev_amount_credit = to_decimal("0")
        prev_serv = to_decimal("0")
        prev_tax = to_decimal("0")

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

        bjouhdr = db_session.query(Bjouhdr).filter(
            (num_entries(Bjouhdr.bezeich, "-") == 4) & (entry(3, Bjouhdr.bezeich, "-") == to_string(rechnr))).first()

        if bjouhdr:

            tjournal = get_cache(
                Gl_journal, {"jnr": [(eq, gl_jouhdr.jnr)], "debit": [(ne, 0), (ne, tot_amount)]})

            if tjournal:
                for bjournal in db_session.query(Bjournal).filter(
                        (Bjournal.jnr == gl_jouhdr.jnr)).order_by(Bjournal._recid).all():

                    if bjournal.debit != 0:
                        prev_amount_debit = to_decimal(bjournal.debit)

                    else:
                        if bjournal.fibukonto.lower() == (serv_fibu).lower():
                            prev_serv = to_decimal(bjournal.credit)

                        elif bjournal.fibukonto.lower() == (vat_fibu).lower():
                            prev_tax = to_decimal(bjournal.credit)

                        else:
                            prev_amount_credit = to_decimal(bjournal.credit)

                cancel_journal()

        # counters = get_cache(Counters, {"counter_no": [(eq, 25)]})

        # if not counters:
        #     counters = Counters()
        #     db_session.add(counters)

        #     counters.counter_no = 25
        #     counters.counter_bez = "G/L Transaction Journal"
        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(25))


        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                gname = guest.name

        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        # gl_jouhdr.jnr = counters.counter
        gl_jouhdr.jnr = last_count

        gl_jouhdr.refno = to_string(queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1
        # gl_jouhdr.bezeich = "service RESIDENT-" + \
        #     to_string(queasy.number1) + "-" + \
        #     to_string(bill_date) + "-" + to_string(rechnr)
        gl_jouhdr.bezeich = f"SERVICE RESIDENT-{to_string(queasy.number1)}-{to_string(bill_date)}-{to_string(rechnr)}"

        gl_journal = Gl_journal()

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.debit = to_decimal(tot_amount)

        db_session.add(gl_journal)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if artikel:
            gl_journal.fibukonto = artikel.fibukonto

        gl_jouhdr.credit = to_decimal(
            gl_jouhdr.credit + gl_journal.credit)
        gl_jouhdr.debit = to_decimal(
            gl_jouhdr.debit + gl_journal.debit)

        for loopi in range(1, 3 + 1):
            gl_journal = Gl_journal()

            gl_journal.jnr = gl_jouhdr.jnr
            gl_journal.userinit = user_init
            gl_journal.zeit = get_current_time_in_seconds()
            gl_journal.bemerk = gl_jouhdr.bezeich

            db_session.add(gl_journal)

            if loopi == 1:
                gl_journal.credit = to_decimal(tot_nettamount)
                gl_journal.fibukonto = div_fibu

            elif loopi == 2:
                gl_journal.credit = to_decimal(tot_serv)
                gl_journal.fibukonto = serv_fibu

            elif loopi == 3:
                gl_journal.credit = to_decimal(tot_tax)
                gl_journal.fibukonto = vat_fibu

            gl_jouhdr.credit = to_decimal(
                gl_jouhdr.credit + gl_journal.credit)
            gl_jouhdr.debit = to_decimal(
                gl_jouhdr.debit + gl_journal.debit)

    def cancel_journal():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, loopi, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list_data

        gname = ""

        # counters = get_cache(Counters, {"counter_no": [(eq, 25)]})

        # if not counters:
        #     counters = Counters()
        #     db_session.add(counters)

        #     counters.counter_no = 25
        #     counters.counter_bez = "G/L Transaction Journal"
        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(25))


        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(
                Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                gname = guest.name

        gl_jouhdr = Gl_jouhdr()

        # gl_jouhdr.jnr = counters.counter
        gl_jouhdr.jnr = last_count

        # gl_jouhdr.refno = "CANCEL-" + \
        #     to_string(queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.refno = f"CANCEL-{to_string(queasy.number1)}-{to_string(bill_date)}"
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1

        db_session.add(gl_jouhdr)

        guest = get_cache(Guest, {"gastnr": [(eq, queasy.number2)]})

        if guest:
            # gl_jouhdr.bezeich = "CANCEL-service RESIDENT-" + \
            #     to_string(queasy.number1) + "-" + \
            #     to_string(bill_date) + "-" + to_string(rechnr)
            gl_jouhdr.bezeich = f"CANCEL-SERVICE RESIDENT-{to_string(queasy.number1)}-{to_string(bill_date)}-{to_string(rechnr)}"

        gl_journal = Gl_journal()

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.credit = to_decimal(prev_amount_debit)

        db_session.add(gl_journal)

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

            gl_journal.jnr = gl_jouhdr.jnr
            gl_journal.userinit = user_init
            gl_journal.zeit = get_current_time_in_seconds()
            gl_journal.bemerk = gl_jouhdr.bezeich

            db_session.add(gl_journal)

            if loopi == 1:
                gl_journal.debit = to_decimal(prev_amount_credit)
                gl_journal.fibukonto = div_fibu

            elif loopi == 2:
                gl_journal.debit = to_decimal(prev_serv)
                gl_journal.fibukonto = serv_fibu

            elif loopi == 3:
                gl_journal.debit = to_decimal(prev_tax)
                gl_journal.fibukonto = vat_fibu

            gl_jouhdr.credit = to_decimal(
                gl_jouhdr.credit + gl_journal.credit)
            gl_jouhdr.debit = to_decimal(
                gl_jouhdr.debit + gl_journal.debit)

    def calc_periode():
        nonlocal success_flag, log_artnr, ar_ledger, divered_rental, bill_date, tot_amount, tot_nettamount, tot_serv, tot_tax, datum, netto, service, tax, tax2, serv, vat, vat2, fact, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, rechnr, prev_tax, prev_serv, prev_amount_debit, prev_amount_credit, curr_due, loopj, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, res_line, arrangement, reslin_queasy, bill, counters, reservation, guest, bediener, bill_line, debitor, billjournal, umsatz, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, user_init, installment
        nonlocal bartikel, bqueasy, pqueasy, tqueasy
        nonlocal periode_list, bartikel, bqueasy, pqueasy, tqueasy
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

    htparam = get_cache(Htparam, {"paramnr": [(eq, 133)]})

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
    tot_nettamount = to_decimal("0")
    tot_serv = to_decimal("0")
    tot_tax = to_decimal("0")
    tot_amount = to_decimal("0")

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        calc_periode()

        tqueasy = get_cache(
            Queasy, {"key": [(eq, 346)], "number1": [(eq, queasy.number1)]})

        if tqueasy:
            curr_due = queasy.date1

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            arrangement = get_cache(
                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if arrangement:
                log_artnr = arrangement.artnr_logis

            if installment > 1:
                tot_nettamount = to_decimal("0")
                tot_serv = to_decimal("0")
                tot_tax = to_decimal("0")
                tot_amount = to_decimal("0")

                for periode_list in query(periode_list_data):
                    tot_periode = tot_periode + 1

                v_cicilanke = 1
                v_percount = tot_periode / installment
                v_start = ((v_cicilanke - 1) * v_percount) + 1
                v_end = v_cicilanke * v_percount

                reslin_queasy_obj_list = {}
                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2)).order_by(Reslin_queasy.date1).all():
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

                    artikel = get_cache(Artikel, {"artnr": [(eq, log_artnr)]})

                    if artikel:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                            1, artikel.artnr, artikel.departement, datum))
                    netto = to_decimal(reslin_queasy.deci1 / fact)
                    service = to_decimal(netto) * to_decimal(serv)
                    tax = to_decimal(netto) * to_decimal(vat)
                    tax2 = to_decimal(netto) * to_decimal(vat2)

                    tot_nettamount = to_decimal(
                        tot_nettamount) + to_decimal(netto)
                    tot_serv = to_decimal(tot_serv) + to_decimal(service)
                    tot_tax = to_decimal(tot_tax) + to_decimal(tax)
                    tot_amount = to_decimal(
                        tot_amount) + to_decimal(reslin_queasy.deci1)

                tot_nettamount = to_decimal(round(tot_nettamount, 0))
                tot_serv = to_decimal(round(tot_serv, 0))
                tot_tax = to_decimal(round(tot_tax, 0))
                tot_amount = to_decimal(round(tot_amount, 0))

                bill = get_cache(
                    Bill, {"resnr": [(eq, queasy.number1)], "parent_nr": [(eq, queasy.number2)], "billnr": [(eq, 1)]})

                if bill:
                    rechnr = bill.rechnr

                else:
                    # counters = get_cache(
                    #     Counters, {"counter_no": [(eq, 3)]})

                    # if not counters:
                    #     counters = Counters()
                    #     db_session.add(counters)

                    #     counters.counter_no = 3
                    #     counters.counter_bez = "Counter for Bill No"

                    # counters.counter = counters.counter + 1
                    # rechnr = counters.counter
                    last_count, error_lock = get_output(next_counter_for_update(3))
                    rechnr = last_count


                create_bill()
                create_ar()
                for loopj in range(1, installment + 1):
                    reslin_queasy = get_cache(
                        Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "number1": [(eq, loopj)], "betriebsnr": [(eq, qrecid)], "char1": [(eq, "")]})

                    if not reslin_queasy:
                        reslin_queasy = Reslin_queasy()

                        reslin_queasy.key = "actual-invoice"
                        reslin_queasy.resnr = queasy.number1
                        reslin_queasy.reslinnr = queasy.number2
                        reslin_queasy.number1 = loopj
                        reslin_queasy.number2 = installment
                        reslin_queasy.date1 = curr_due
                        reslin_queasy.date2 = add_interval(
                            curr_due, 1, "Month")
                        reslin_queasy.betriebsnr = qrecid
                        curr_due = reslin_queasy.date2
                        
                        db_session.add(reslin_queasy)

                        if queasy.logi3:
                            reslin_queasy.deci1 = to_decimal("1")

                        if loopj > 1:
                            reslin_queasy.logi1 = True

                        elif loopj == 1:
                            reslin_queasy.logi2 = True
                            reslin_queasy.date3 = bill_date

            else:
                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2)).order_by(Reslin_queasy.date1).all():

                    periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2), first=True)

                    if periode_list:
                        service = to_decimal("0")
                        tax = to_decimal("0")
                        tax2 = to_decimal("0")
                        netto = to_decimal("0")

                        artikel = get_cache(
                            Artikel, {"artnr": [(eq, log_artnr)]})

                        if artikel:
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                                1, artikel.artnr, artikel.departement, datum))
                        netto = to_decimal(
                            reslin_queasy.deci1 / fact)
                        service = to_decimal(netto * serv)
                        tax = to_decimal(netto * vat)
                        tax2 = to_decimal(netto * vat2)

                        tot_nettamount = to_decimal(
                            tot_nettamount + netto)
                        tot_serv = to_decimal(tot_serv + service)
                        tot_tax = to_decimal(tot_tax + tax)
                        tot_amount = to_decimal(
                            tot_amount + reslin_queasy.deci1)

                tot_nettamount = to_decimal(round(tot_nettamount, 0))
                tot_serv = to_decimal(round(tot_serv, 0))
                tot_tax = to_decimal(round(tot_tax, 0))
                tot_amount = to_decimal(round(tot_amount, 0))

                bill = get_cache(
                    Bill, {"resnr": [(eq, queasy.number1)], "parent_nr": [(eq, queasy.number2)], "billnr": [(eq, 1)]})

                if bill:
                    rechnr = bill.rechnr

                else:
                    # counters = get_cache(
                    #     Counters, {"counter_no": [(eq, 3)]})

                    # if not counters:
                    #     counters = Counters()

                    #     counters.counter_no = 3
                    #     counters.counter_bez = "counter for Bill No"

                    #     db_session.add(counters)

                    # counters.counter = counters.counter + 1
                    # rechnr = counters.counter
                    last_count, error_lock = get_output(next_counter_for_update(3))
                    rechnr = last_count
                    

                create_bill()
                create_ar()

            pqueasy = get_cache(
                Queasy, {"key": [(eq, 375)], "number2": [(eq, queasy.number1)], "number3": [(eq, queasy.number2)], "number1": [(eq, 2)], "logi1": [(eq, True)]})

            if pqueasy:
                pqueasy.logi1 = False

            queasy.char3 = "*|" + to_string(bill_date) + "|" + to_string(
                get_current_time_in_seconds(), "HH:MM:SS") + "|" + user_init
            queasy.char2 = to_string(rechnr)

            success_flag = True

    return generate_output()
