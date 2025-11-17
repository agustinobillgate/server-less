# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        remark: - fix python indentation 
                - fix ("string").lower()
                - fix closing bracket on timedelta(days)
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Queasy, Htparam, Reslin_queasy, Billjournal, Umsatz, Debitor, Bediener, Res_line, Guest, Counters, Gl_jouhdr, Gl_journal


def leasing_pay_deposit_1bl(qrecid: int, pinvoice_no: str, artikel_no: int, pay_amount: Decimal, user_init: str, voucher_no: str):

    prepare_cache([Artikel, Queasy, Htparam, Reslin_queasy, Billjournal, Umsatz, Bediener, Res_line, Guest, Counters, Gl_jouhdr, Gl_journal])

    success_flag = False
    bill_date: date = None
    ar_ledger: int = 0
    div_fibu = ""
    extendflag: int = 0
    amount: Decimal = to_decimal("0.0")
    installment: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    artikel = queasy = htparam = reslin_queasy = billjournal = umsatz = debitor = bediener = res_line = guest = counters = gl_jouhdr = gl_journal = None

    periode_list = bart = bartikel = tqueasy = None

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

    Bart = create_buffer("Bart", Artikel)
    Bartikel = create_buffer("Bartikel", Artikel)
    Tqueasy = create_buffer("Tqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        return {
            "success_flag": success_flag
        }

    def create_queasy():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        tqueasy = get_cache(
            Queasy, {"key": [(eq, 355)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)], "number3": [(eq, artikel_no)]})

        if not tqueasy:
            tqueasy = Queasy()
            db_session.add(tqueasy)

            tqueasy.key = 355
            tqueasy.number1 = queasy.number1
            tqueasy.number2 = queasy.number2
            tqueasy.number3 = artikel_no
            tqueasy.deci1 = to_decimal(pay_amount)
            tqueasy.char1 = user_init
            tqueasy.date1 = bill_date
            tqueasy.deci2 = to_decimal(get_current_time_in_seconds)()
            tqueasy.char2 = to_string(get_current_date(
            )) + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        else:
            tqueasy.deci1 = to_decimal(
                tqueasy.deci1) + to_decimal(pay_amount)
            tqueasy.char1 = user_init
            tqueasy.date1 = bill_date
            tqueasy.deci2 = to_decimal(get_current_time_in_seconds)()
            tqueasy.char2 = to_string(get_current_date(
            )) + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    def check_amount():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        curr_amount = to_decimal("0.0")

        def generate_inner_output():
            return (curr_amount)

        calc_periode()

        if queasy.char2 != "":
            reslin_queasy = get_cache(
                Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "betriebsnr": [(eq, qrecid)], "logi1": [(eq, False)], "logi2": [(eq, False)], "logi3": [(eq, False)]})

            if reslin_queasy:
                for periode_list in query(periode_list_data):
                    tot_periode = tot_periode + 1

                installment = reslin_queasy.number2
                v_cicilanke = reslin_queasy.number1
                v_percount = tot_periode / reslin_queasy.number2
                v_start = ((v_cicilanke - 1) * v_percount) + 1
                v_end = v_cicilanke * v_percount

                for periode_list in query(periode_list_data, filters=(lambda periode_list: periode_list.counter >= v_start and periode_list.counter <= v_end)):
                    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            ((Reslin_queasy.key).lower == "arrangement") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2) & (Reslin_queasy.date1 >= periode_list.periode1) & (Reslin_queasy.date1 <= periode_list.periode2)).order_by(Reslin_queasy.date1).all():
                        curr_amount = to_decimal(
                            curr_amount) + to_decimal(reslin_queasy.deci1)

        return generate_inner_output()

    def calc_periode():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
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
                        curr_amount) + to_decimal(reslin_queasy.deci1)

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount) / to_decimal(periode_list.diff_day)
            periode_list.tamount = to_decimal(
                periode_list.amt_periode) * to_decimal(periode_list.diff_day)

    def create_turnover():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = to_decimal(pay_amount)
        billjournal.betrag = to_decimal(pay_amount)
        billjournal.bezeich = f"{artikel.bezeich}-{voucher_no}- Invoice No : {pinvoice_no}[Payment Leasing #{to_string(queasy.number1)}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.kassabuch_nr = qrecid

        if v_cicilanke != 0:
            billjournal.billin_nr = v_cicilanke

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = ar_ledger
            umsatz.datum = bill_date

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = to_decimal(umsatz.betrag) + to_decimal(pay_amount)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

        if not artikel:
            return
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - to_decimal(pay_amount)
        billjournal.betrag = - to_decimal(pay_amount)
        billjournal.bezeich = f"{artikel.bezeich}-{voucher_no}- Invoice No : {pinvoice_no}[Payment Leasing #{to_string(queasy.number1)}]"
        billjournal.epreis = to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = queasy.number1
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.kassabuch_nr = qrecid

        if v_cicilanke != 0:
            billjournal.billin_nr = v_cicilanke

        umsatz = get_cache(
            Umsatz, {"artnr": [(eq, artikel.artnr)], "departement": [(eq, 0)], "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date

        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = to_decimal(umsatz.betrag) + \
            to_decimal(- to_decimal(pay_amount))

    def create_ar():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        bdebt = None
        Bdebt = create_buffer("Bdebt", Debitor)

        debitor = get_cache(
            Debitor, {"vesrcod": [(eq, pinvoice_no)], "zahlkonto": [(eq, 0)]})

        if debitor:
            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

            bart = db_session.query(Bart).filter(
                (Bart.artnr == artikel_no) & (Bart.departement == 0) & ((Bart.artart == 2) | (Bart.artart == 7))).first()

            if bart:
                bdebt = Debitor()
                db_session.add(bdebt)

                bdebt.artnr = artikel_no
                bdebt.rechnr = to_int(pinvoice_no)
                bdebt.rgdatum = bill_date
                bdebt.saldo = to_decimal(pay_amount)
                bdebt.vesrdep = to_decimal(pay_amount)
                bdebt.bediener_nr = bediener.nr
                bdebt.vesrdat = get_current_date()
                bdebt.transzeit = get_current_time_in_seconds()
                bdebt.vesrcod = f"{pinvoice_no}-{voucher_no}|PAYMENT DEPOSIT"

                res_line = get_cache(
                    Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

                if res_line:
                    guest = get_cache(
                        Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        bdebt.name = guest.name
                        bdebt.gastnr = res_line.gastnr
                        bdebt.gastnrmember = res_line.gastnrmember

            bdebt = Debitor()
            db_session.add(bdebt)

            bdebt.artnr = ar_ledger
            bdebt.rechnr = to_int(pinvoice_no)
            bdebt.rgdatum = bill_date
            bdebt.saldo = - to_decimal(pay_amount)
            bdebt.vesrdep = - to_decimal(pay_amount)
            bdebt.bediener_nr = bediener.nr
            bdebt.vesrdat = get_current_date()
            bdebt.transzeit = get_current_time_in_seconds()
            bdebt.vesrcod = f"{pinvoice_no}-{voucher_no}|VOID PAYMENT DEPOSIT"

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    bdebt.name = guest.name
                    bdebt.gastnr = res_line.gastnr
                    bdebt.gastnrmember = res_line.gastnrmember

    def create_journal():
        nonlocal success_flag, bill_date, ar_ledger, div_fibu, extendflag, amount, installment, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, artikel, queasy, htparam, reslin_queasy, billjournal, umsatz, debitor, bediener, res_line, guest, counters, gl_jouhdr, gl_journal
        nonlocal qrecid, pinvoice_no, artikel_no, pay_amount, user_init, voucher_no
        nonlocal bart, bartikel, tqueasy
        nonlocal periode_list, bart, bartikel, tqueasy
        nonlocal periode_list_data

        counters = get_cache(Counters, {"counter_no": [(eq, 25)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
        counters.counter = counters.counter + 1
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.refno = "Payment Deposit - " + pinvoice_no
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1

        guest = get_cache(Guest, {"gastnr": [(eq, queasy.number2)]})

        if guest:
            gl_jouhdr.bezeich = pinvoice_no + "-Leasing-" + guest.name

        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.debit = to_decimal(pay_amount)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, artikel_no)], "departement": [(eq, 0)]})

        if artikel:
            gl_journal.fibukonto = artikel.fibukonto

        gl_jouhdr.credit = to_decimal(
            gl_jouhdr.credit) + to_decimal(gl_journal.credit)
        gl_jouhdr.debit = to_decimal(
            gl_jouhdr.debit) + to_decimal(gl_journal.debit)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if artikel:
            div_fibu = artikel.fibukonto

        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.credit = to_decimal(pay_amount)
        gl_journal.fibukonto = div_fibu

        gl_jouhdr.credit = to_decimal(
            gl_jouhdr.credit) + to_decimal(gl_journal.credit)
        gl_jouhdr.debit = to_decimal(
            gl_jouhdr.debit) + to_decimal(gl_journal.debit)

    htparam = get_cache(Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    queasy = get_cache(Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

    if queasy:
        amount = check_amount()
        amount = to_decimal(round(amount, 0))

        if amount != 0:
            if pay_amount != amount:
                success_flag = False
                return generate_output()

        if queasy.logi3:
            extendflag = 1

        else:
            extendflag = 0

        artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == artikel_no) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 6))).first()

        if artikel:
            if artikel.artart == 2 or artikel.artart == 7:
                create_ar()
        create_turnover()
        create_queasy()
        queasy.logi2 = True
        queasy.deci2 = to_decimal(queasy.deci2) + to_decimal(pay_amount)

        reslin_queasy = db_session.query(Reslin_queasy).filter(
            ((Reslin_queasy.key).lower() == "actual-invoice") & (Reslin_queasy.resnr == queasy.number1) & (Reslin_queasy.reslinnr == queasy.number2) & (Reslin_queasy.deci1 == extendflag) & (Reslin_queasy.betriebsnr == qrecid) & ((Reslin_queasy.logi2) | ((Reslin_queasy.logi1 == False) & (Reslin_queasy.logi2 == False))) & (Reslin_queasy.logi3 == False)).first()

        if reslin_queasy:
            reslin_queasy.logi3 = True

        success_flag = True

    return generate_output()
