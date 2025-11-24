# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix ("string").lower()
                    - use f"string"
"""
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Reslin_queasy, Waehrung, Res_line, Htparam, Bediener, Arrangement, Guest_pr, Ratecode, Pricecod, Katpreis, Queasy, Artikel, Debitor, Guest, Counters, Gl_jouhdr, Gl_journal, Bresline
from functions.next_counter_for_update import next_counter_for_update

p_list_data, P_list = create_model(
    "P_list",
    {
        "betrag": Decimal,
        "date1": date,
        "date2": date,
        "argt": str,
        "pax": int,
        "rcode": str
    })


def leasing_btn_go_res_rmrate_webbl(pvilanguage: int, curr_select: str, max_rate: Decimal, fact1: Decimal, 
                                    inp_wahrnr: int, inp_zikatnr: int, user_init: str, resnr: int, reslinnr: int, 
                                    recid_reslin: int, contcode: str, repeat_charge: bool, p_list_data: P_list):

    prepare_cache([Waehrung, Res_line, Htparam, Bediener, Arrangement, Bresline, Guest_pr, Katpreis, Queasy, Artikel, Debitor, Guest, Counters, Gl_jouhdr, Gl_journal])

    msg_str = ""
    error_found1 = False
    error_code = 0
    t_reslin_queasy_data = []
    lvcarea: str = "chk-btn-go-res-rmrate"
    error_found: bool = False
    log_artnr: int = 0
    ar_ledger: int = 0
    divered_rental: int = 0
    tot_amount = to_decimal("0.0")
    tot_nettamount = to_decimal("0.0")
    tot_serv = to_decimal("0.0")
    tot_tax = to_decimal("0.0")
    serv_acctno = ""
    vat_acctno = ""
    vat_fibu = ""
    vat2_fibu = ""
    serv_fibu = ""
    div_fibu = ""
    amount_periode = to_decimal("0.0")
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    exrate2 = 1
    wd_array: List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    bill_date: date = None
    pinvoice = ""
    reslin_queasy = waehrung = res_line = htparam = bediener = arrangement = guest_pr = ratecode = pricecod = katpreis = queasy = artikel = debitor = guest = counters = gl_jouhdr = gl_journal = bresline = None
    t_reslin_queasy = p_list = periode_list = brq = waehrung1 = breslin = preslin = None

    t_reslin_queasy_data, T_reslin_queasy = create_model(
        "T_reslin_queasy",
        {
            "date1": date,
            "date2": date,
            "deci1": Decimal,
            "char1": string,
            "number3": int,
            "char2": string,
            "char3": string,
            "recid_reslin": int
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

    Brq = create_buffer("Brq", Reslin_queasy)
    Waehrung1 = create_buffer("Waehrung1", Waehrung)
    Breslin = create_buffer("Breslin", Reslin_queasy)
    Preslin = create_buffer("Preslin", Res_line)
    db_session = local_storage.db_session
    last_count = 0
    error_lock: str = ""
    curr_select = curr_select.strip()
    contcode = contcode.strip()

    def generate_output():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        return {
            "msg_str": msg_str,
            "error_found1": error_found1,
            "error_code": error_code,
            "t-reslin-queasy": t_reslin_queasy_data
        }

    def lastday(d: date):
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        return add_interval(date_mdy(get_month(d), 1, get_year(d)), 1, "month") - 1

    def calc_periode():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_last: int = 0
        amount_periode = to_decimal(p_list.betrag)
        periode_rsv1 = p_list.date1
        periode_rsv2 = p_list.date2

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
            curr_last = get_day(lastday(periode_list.periode1))

            if periode_list.diff_day < curr_last:
                periode_list.amt_periode = to_decimal(
                    round((amount_periode * 12 / 365), 3))

            else:
                periode_list.amt_periode = to_decimal(
                    round(amount_periode / periode_list.diff_day, 3))

            periode_list.tamount = to_decimal(
                round(periode_list.amt_periode * periode_list.diff_day, 0))

    def proc_repeat():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        loopdate: date = None
        tot_days: int = 0
        curr_amount = to_decimal("0.0")
        curr_date: date = None
        co_date: date = None
        curr_date1: date = None
        curr_amount1 = to_decimal("0.0")
        bresline = None
        Bresline = create_buffer("Bresline", Res_line)

        bresline = get_cache(
            Res_line, {"resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)]})

        if bresline:
            co_date = bresline.abreise

        if curr_select.lower() == "add":
            if res_line.active_flag == 0:
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "fixrate-trace-record")], "resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)]})

                if not reslin_queasy:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "fixrate-trace-record"
                    reslin_queasy.resnr = resnr
                    reslin_queasy.reslinnr = reslinnr
                    reslin_queasy.date1 = get_current_date()
                    reslin_queasy.number1 = get_current_time_in_seconds()
                    reslin_queasy.char3 = ""

            for loopdate in date_range(p_list.date1, p_list.date2):
                periode_list = query(periode_list_data, filters=(
                    lambda periode_list: periode_list.periode1 <= loopdate and periode_list.periode2 >= loopdate), first=True)

                if periode_list:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "arrangement"
                    reslin_queasy.resnr = resnr
                    reslin_queasy.reslinnr = reslinnr
                    reslin_queasy.date1 = loopdate
                    reslin_queasy.date2 = loopdate
                    reslin_queasy.deci1 = to_decimal(periode_list.amt_periode)
                    reslin_queasy.char1 = p_list.argt
                    reslin_queasy.char2 = p_list.rcode
                    reslin_queasy.char3 = user_init
                    reslin_queasy.number3 = p_list.pax
                    reslin_queasy.number2 = get_current_time_in_seconds()
                    reslin_queasy.date3 = get_current_date()

                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                    buffer_copy(reslin_queasy, t_reslin_queasy)
                    t_reslin_queasy.recid_reslin = reslin_queasy._recid

                    res_line = get_cache(
                        Res_line, {"resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)]})
                    res_changes_chg()

        elif curr_select.lower() == "chg":
            if res_line.active_flag == 0:
                reslin_queasy = get_cache(
                    Reslin_queasy, {"key": [(eq, "fixrate-trace-record")], "resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)]})

                if not reslin_queasy:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "fixrate-trace-record"
                    reslin_queasy.resnr = resnr
                    reslin_queasy.reslinnr = reslinnr
                    reslin_queasy.date1 = get_current_date()
                    reslin_queasy.number1 = get_current_time_in_seconds()
                    reslin_queasy.char3 = ""

            if p_list.date2 == co_date:
                curr_date = p_list.date2 - timedelta(days=1)

            else:
                curr_date = p_list.date2
            curr_date1 = p_list.date1

            reslin_queasy = get_cache(
                Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)], "date1": [(le, bill_date)], "date2": [(le, bill_date)]})

            if reslin_queasy:
                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr) & (Reslin_queasy.date1 < bill_date) & (Reslin_queasy.date2 < bill_date)).order_by(Reslin_queasy._recid).all():
                    curr_date1 = curr_date1 + timedelta(days=1)
                    curr_amount1 = to_decimal(
                        curr_amount1 + reslin_queasy.deci1)

                if curr_amount1 != 0:
                    p_list.betrag = to_decimal(
                        p_list.betrag - curr_amount1)

                    proc_delete_journal()
            tot_days = (curr_date - curr_date1) + 1
            curr_amount = to_decimal(p_list.betrag / tot_days)

            for loopdate in date_range(curr_date1, curr_date):
                # if loopdate == co_date:
                #     pass
                # else:
                if loopdate != co_date:
                    reslin_queasy = get_cache(
                        Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)], "date1": [(eq, loopdate)], "date2": [(eq, loopdate)]})

                    if not reslin_queasy:
                        reslin_queasy = Reslin_queasy()
                        db_session.add(reslin_queasy)

                        reslin_queasy.key = "arrangement"
                        reslin_queasy.resnr = resnr
                        reslin_queasy.reslinnr = reslinnr
                        reslin_queasy.date1 = loopdate
                        reslin_queasy.date2 = loopdate
                        reslin_queasy.deci1 = to_decimal(curr_amount)
                        reslin_queasy.char1 = p_list.argt
                        reslin_queasy.char2 = p_list.rcode
                        reslin_queasy.char3 = user_init
                        reslin_queasy.number3 = p_list.pax
                        reslin_queasy.number2 = get_current_time_in_seconds()
                        reslin_queasy.date3 = get_current_date()

                        t_reslin_queasy = T_reslin_queasy()
                        t_reslin_queasy_data.append(t_reslin_queasy)

                        buffer_copy(reslin_queasy, t_reslin_queasy)
                        t_reslin_queasy.recid_reslin = reslin_queasy._recid

                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)]})
                        res_changes_chg()

                    elif reslin_queasy:
                        reslin_queasy.date1 = loopdate
                        reslin_queasy.date2 = loopdate
                        reslin_queasy.deci1 = to_decimal(curr_amount)
                        reslin_queasy.char1 = p_list.argt
                        reslin_queasy.char2 = p_list.rcode
                        reslin_queasy.char3 = user_init
                        reslin_queasy.number3 = p_list.pax
                        reslin_queasy.number2 = get_current_time_in_seconds()
                        reslin_queasy.date3 = get_current_date()

                        t_reslin_queasy = T_reslin_queasy()
                        t_reslin_queasy_data.append(t_reslin_queasy)

                        buffer_copy(reslin_queasy, t_reslin_queasy)
                        t_reslin_queasy.recid_reslin = reslin_queasy._recid


                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)]})
                        res_changes_chg()
            proc_create_journal()

    def get_rackrate(erwachs: int, kind1: int, kind2: int):
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        rate = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate = to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate = to_decimal(rate + kind1) * to_decimal(
            katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate

    def check_rate():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        error_found = False
        i: int = 0
        n: int = 0
        val = to_decimal("0.0")
        max_disc = to_decimal("0.0")
        tol_value = to_decimal("0.0")
        rack_rate = to_decimal("0.0")
        datum: date = None
        exrate1 = 1

        def generate_inner_output():
            return (error_found)

        if bediener.char1 == "":
            return generate_inner_output()

        if max_rate != 0 and p_list.betrag * fact1 > max_rate:
            msg_str = msg_str + chr_unicode(2) + translateExtended(
                "Room rate incorrect / too large! Check currency.", lvcarea, "")
            error_found = True

            return generate_inner_output()

        guest_pr = get_cache(
            Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})
        if guest_pr:
            ratecode = get_cache(
                Ratecode, {"code": [(eq, guest_pr.code)]})
            if ratecode:
                return generate_inner_output()

            pricecod = get_cache(
                Pricecod, {"code": [(eq, guest_pr.code)]})

            if pricecod:
                return generate_inner_output()
        n = num_entries(bediener.char1, ";")
        for i in range(1, n + 1):
            val = to_decimal(
                to_int(entry(i) - to_decimal(1, bediener.char1, ";"))) / to_decimal("100")

            if max_disc < val:
                max_disc = to_decimal(val)
        max_disc = to_decimal(max_disc / 100)

        if max_disc == 0:
            return generate_inner_output()

        htparam = get_cache(
            Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache(
            Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exrate1 = to_decimal(waehrung.ankauf / waehrung.einheit)

        waehrung = get_cache(
            Waehrung, {"waehrungsnr": [(eq, inp_wahrnr)]})

        if waehrung:
            exrate2 = to_decimal(waehrung.ankauf / waehrung.einheit)
        for datum in date_range(p_list.date1, p_list.date2):
            rack_rate = to_decimal("0")

            katpreis = get_cache(
                Katpreis, {"zikatnr": [(eq, inp_zikatnr)], "argtnr": [(eq, arrangement.argtnr)], "startperiode": [(le, datum)], "endperiode": [(ge, datum)], "betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

            if not katpreis:
                katpreis = get_cache(
                    Katpreis, {"zikatnr": [(eq, inp_zikatnr)], "argtnr": [(eq, arrangement.argtnr)], "startperiode": [(le, datum)], "endperiode": [(ge, datum)], "betriebsnr": [(eq, 0)]})

            if katpreis:
                rack_rate = to_decimal(get_rackrate(
                    res_line.erwachs, res_line.kind1, res_line.kind2))
            rack_rate = to_decimal(rack_rate * exrate1 / exrate2)

            if truncate(rack_rate, 0) != rack_rate:
                rack_rate = to_decimal(round(rack_rate + 0.5, 0))

            if rack_rate * (1 - max_disc) > p_list.betrag:
                msg_str = msg_str + chr_unicode(2) + translateExtended("Over discounted rate)", lvcarea,"") + " " + translateExtended("for date =", lvcarea, "") + " " + to_string(datum)
                error_found = True

                return generate_inner_output()
        return generate_inner_output()
    def check_currency():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        reslin_queasy = get_cache(
            Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)]})

        if not reslin_queasy:
            # if not guest_pr:
            #     return

            queasy = get_cache(
                Queasy, {"key": [(eq, 2)], "char1": [(eq, contcode)]})

            if queasy and queasy.number1 != 0:
                waehrung1 = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:
                    res_line.betriebsnr = waehrung1.waehrungsnr
                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended("No AdHoc Rates found; set back the currency code", lvcarea, "") + chr_unicode(
                        10) + translateExtended("to", lvcarea, "") + " " + waehrung1.bezeich + " " + translateExtended("as defined in the contract rates.", lvcarea, "")

    def res_changes_add():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        cid = ""
        cdate = " "
        rqy = None
        Rqy = create_buffer("Rqy", Reslin_queasy)

        # if not res_line:
        #     return

        # if res_line.active_flag == 2:
        #     return

        if res_line.changed is not None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()

        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + \
            to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + \
            ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("ADD Fixrate:") + ";" + to_string(
                reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

    def res_changes_chg():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        cid = ""
        cdate = " "
        rqy = None
        Rqy = create_buffer("Rqy", Reslin_queasy)

        # if not res_line:
        #     return

        # if res_line.active_flag == 2 and res_line.resstatus != 12:
        #     return

        if res_line.changed is not None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()

        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(
            res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate FR:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        
        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()

        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + \
            to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(
                user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate TO:") + ";" + to_string(p_list.date1) + "-" + to_string(p_list.betrag) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

    def proc_delete_journal():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        netto = to_decimal("0.0")
        service = to_decimal("0.0")
        tax = to_decimal("0.0")
        tax2 = to_decimal("0.0")
        serv = to_decimal("0.0")
        vat = to_decimal("0.0")
        vat2 = to_decimal("0.0")
        fact = to_decimal("0.0")
        loopi: int = 0
        datum: date = None

        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)], "char2": [(ne, "")]})

        if queasy:
            preslin = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if preslin:
                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, preslin.arrangement)]})

                if arrangement:
                    log_artnr = arrangement.artnr_logis

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

                        tot_nettamount = to_decimal(tot_nettamount + netto)
                        tot_serv = to_decimal(tot_serv + service)
                        tot_tax = to_decimal(tot_tax + tax)
                        tot_amount = to_decimal(tot_amount + reslin_queasy.deci1)

                tot_amount = to_decimal(round(tot_amount, 0))

                pinvoice = queasy.char2

                create_ar()
                cancel_journal()

    def create_ar():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        bdebt = None
        tresline = None
        Bdebt = create_buffer("Bdebt", Debitor)
        Tresline = create_buffer("Tresline", Res_line)

        debitor = get_cache(
            Debitor, {"vesrcod": [(eq, pinvoice)], "zahlkonto": [(eq, 0)]})

        if debitor:
            bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
            bdebt = Debitor()
            db_session.add(bdebt)

            bdebt.artnr = ar_ledger
            bdebt.rechnr = to_int(pinvoice)
            bdebt.rgdatum = bill_date
            bdebt.saldo = - to_decimal(tot_amount)
            bdebt.vesrdep = - to_decimal(tot_amount)
            bdebt.bediener_nr = bediener.nr
            bdebt.vesrdat = get_current_date()
            bdebt.transzeit = get_current_time_in_seconds()
            bdebt.vesrcod = pinvoice + "|Cancel"

            tresline = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if tresline:
                guest = get_cache(
                    Guest, {"gastnr": [(eq, tresline.gastnr)]})

                if guest:
                    bdebt.name = guest.name
                    bdebt.gastnr = tresline.gastnr
                    bdebt.gastnrmember = tresline.gastnrmember

    def cancel_journal():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        gname = ""
        loopi: int = 0

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
        db_session.add(gl_jouhdr)

        # gl_jouhdr.jnr = counters.counter
        gl_jouhdr.jnr = last_count


        # gl_jouhdr.refno = "CANCEL-" + \
        #     to_string(queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.refno = f"CANCEL-{queasy.number1}-{bill_date}"
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1

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

    def proc_create_journal():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        netto = to_decimal("0.0")
        service = to_decimal("0.0")
        tax = to_decimal("0.0")
        tax2 = to_decimal("0.0")
        serv = to_decimal("0.0")
        vat = to_decimal("0.0")
        vat2 = to_decimal("0.0")
        fact = to_decimal("0.0")
        loopi: int = 0
        datum: date = None

        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)], "char2": [(ne, "")]})

        if queasy:
            preslin = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if preslin:
                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, preslin.arrangement)]})

                if arrangement:
                    log_artnr = arrangement.artnr_logis

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

                tot_amount = to_decimal(round(tot_amount, 0))

                pinvoice = queasy.char2

                create_ar1()
                create_journal()

    def create_ar1():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
        debitor = Debitor()
        db_session.add(debitor)

        debitor.artnr = ar_ledger
        debitor.rechnr = to_int(pinvoice)
        debitor.rgdatum = bill_date
        debitor.saldo = to_decimal(tot_amount)
        debitor.vesrdep = to_decimal(tot_amount)
        debitor.bediener_nr = bediener.nr
        debitor.vesrdat = get_current_date()
        debitor.transzeit = get_current_time_in_seconds()
        debitor.vesrcod = to_string(pinvoice)

        res_line = get_cache(
            Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

        if res_line:
            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest:
                debitor.name = guest.name
                debitor.gastnr = res_line.gastnr
                debitor.gastnrmember = res_line.gastnrmember

    def create_journal():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, log_artnr, ar_ledger, divered_rental, tot_amount, tot_nettamount, tot_serv, tot_tax, serv_acctno, vat_acctno, vat_fibu, vat2_fibu, serv_fibu, div_fibu, amount_periode, month_str1, month_str2, exrate2, wd_array, bill_date, pinvoice, reslin_queasy, waehrung, res_line, htparam, bediener, arrangement, guest_pr, ratecode, pricecod, katpreis, queasy, artikel, debitor, guest, counters, gl_jouhdr, gl_journal, bresline
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode, repeat_charge
        nonlocal brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy, p_list, periode_list, brq, waehrung1, breslin, preslin
        nonlocal t_reslin_queasy_data, periode_list_data

        gname = ""
        loopi: int = 0

        # counters = get_cache(
        #     Counters, {"counter_no": [(eq, 25)]})

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
        
        # gl_jouhdr.refno = to_string(
        #     queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.refno = f"{queasy.number1}-{bill_date}"
        gl_jouhdr.datum = bill_date
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 1
        # gl_jouhdr.bezeich = "service RESIDENT-" + \
        #     to_string(queasy.number1) + "-" + to_string(bill_date)
        gl_jouhdr.bezeich = f"service RESIDENT-{queasy.number1}-{bill_date}"

        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = gl_jouhdr.bezeich
        gl_journal.debit = to_decimal(tot_amount)

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

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 119)]})

    if htparam:
        log_artnr = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    p_list = query(p_list_data, first=True)

    res_line = get_cache(
        Res_line, {"resnr": [(eq, resnr)], "reslinnr": [(eq, reslinnr)]})

    bediener = get_cache(
        Bediener, {"userinit": [(eq, user_init)]})

    reslin_queasy = get_cache(
        Reslin_queasy, {"_recid": [(eq, recid_reslin)]})

    if p_list.argt != "":
        arrangement = get_cache(
            Arrangement, {"arrangement": [(eq, p_list.argt)]})

        if not arrangement:
            msg_str = msg_str + chr_unicode(2) + translateExtended("Arrangement Code incorrect.", lvcarea, "")
            error_code = 1

            return generate_output()

    if repeat_charge:
        calc_periode()
        proc_repeat()

        return generate_output()
    return generate_output()
