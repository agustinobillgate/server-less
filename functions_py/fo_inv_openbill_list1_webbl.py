# using conversion tools version: 1.0.0.119
"""_yusufwijasena_03/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var declaration
                    - fix python indentation
                    - add import from function_py
                    - changed string to str
                    - fix wrong positional closing bracket
                    - use f"string"
                    - fix converted string
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from sqlalchemy import func
# from functions.fo_invoice_open_bill_cld_2bl import fo_invoice_open_bill_cld_2bl
# from functions.fo_invoice_fill_rescommentbl import fo_invoice_fill_rescommentbl
# from functions.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
# from functions.calc_servtaxesbl import calc_servtaxesbl
# from functions.fo_invoice_disp_bill_line_cldbl import fo_invoice_disp_bill_line_cldbl
from functions_py.fo_invoice_open_bill_cld_2bl import fo_invoice_open_bill_cld_2bl
from functions_py.fo_invoice_fill_rescommentbl import fo_invoice_fill_rescommentbl
from functions_py.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from functions_py.fo_invoice_disp_bill_line_cldbl import fo_invoice_disp_bill_line_cldbl
from models import Bill, Res_line, Bill_line, Htparam, Reslin_queasy, Arrangement, Artikel, Billjournal, Queasy


def fo_inv_openbill_list1_webbl(bil_flag: int, bil_recid: int, room: string, vipflag: bool, fill_co: bool, double_currency: bool, foreign_rate: bool):

    prepare_cache([Htparam, Reslin_queasy, Arrangement, Artikel, Billjournal, Queasy])

    abreise = None
    resname = ""
    res_exrate = to_decimal("0.0")
    zimmer_bezeich = ""
    kreditlimit = to_decimal("0.0")
    master_str = ""
    master_rechnr = ""
    bill_anzahl = 0
    queasy_char1 = ""
    disp_warning = False
    flag_report = False
    rescomment = ""
    printed = ""
    rechnr = 0
    rmrate = to_decimal("0.0")
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    tot_balance = to_decimal("0.0")
    guest_taxcode = ""
    t_res_line_data = []
    t_bill_data = []
    spbill_list_data = []
    t_bill_line_data = []
    datum: date = None
    ci_date: date = None
    fixed_rate: bool = False
    rm_rate = to_decimal("0.0")
    ratecode_qsy = ""
    pax: int = 0
    it_exist: bool = False
    bill_date: date = None
    new_contrate: bool = False
    ebdisc_flag: bool = False
    kbdisc_flag: bool = False
    rate_found: bool = False
    contcode = ""
    curr_zikatnr: int = 0
    early_flag: bool = False
    kback_flag: bool = False
    bonus_array: List[bool] = create_empty_list(999, False)
    curr_i: int = 0
    w_day: int = 0
    curr_artnr: int = 0
    log_artnr: int = 0
    counter: int = 0
    wd_array: List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    serv = to_decimal("0.0")
    vat = to_decimal("0.0")
    netto = to_decimal("0.0")
    repeat_charge: bool = False
    service = to_decimal("0.0")
    tax = to_decimal("0.0")
    tax2 = to_decimal("0.0")
    fact = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    divered_rental: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ar_ledger: int = 0
    bill = res_line = bill_line = htparam = reslin_queasy = arrangement = artikel = billjournal = queasy = None

    t_bill = t_res_line = spbill_list = t_bill_line = p_bill_line = periode_list = mbill_line = bbill_line = None

    t_bill_data, T_bill = create_model_like(Bill)
    t_res_line_data, T_res_line = create_model_like(
        Res_line,
        {
            "guest_name": str
        })
    spbill_list_data, Spbill_list = create_model(
        "Spbill_list",
        {
            "selected": bool,
            "bl_recid": int
        },
        {
            "selected": True
        })
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
            "bjournal": bool
        })
    p_bill_line_data, P_bill_line = create_model_like(
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
            "bjournal": bool
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

    Mbill_line = T_bill_line
    mbill_line_data = t_bill_line_data

    Bbill_line = T_bill_line
    bbill_line_data = t_bill_line_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, datum, ci_date, fixed_rate, rm_rate, ratecode_qsy, pax, it_exist, bill_date, new_contrate, ebdisc_flag, kbdisc_flag, rate_found, contcode, curr_zikatnr, early_flag, kback_flag, bonus_array, curr_i, w_day, curr_artnr, log_artnr, counter, wd_array, serv, vat, netto, repeat_charge, service, tax, tax2, fact, vat2, divered_rental, month_str1, month_str2, ar_ledger, bill, res_line, bill_line, htparam, reslin_queasy, arrangement, artikel, billjournal, queasy
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate
        nonlocal mbill_line, bbill_line
        nonlocal t_bill, t_res_line, spbill_list, t_bill_line, p_bill_line, periode_list, mbill_line, bbill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data, p_bill_line_data, periode_list_data

        return {
            "abreise": abreise,
            "resname": resname,
            "res_exrate": res_exrate,
            "zimmer_bezeich": zimmer_bezeich,
            "kreditlimit": kreditlimit,
            "master_str": master_str,
            "master_rechnr": master_rechnr,
            "bill_anzahl": bill_anzahl,
            "queasy_char1": queasy_char1,
            "disp_warning": disp_warning,
            "flag_report": flag_report,
            "rescomment": rescomment,
            "printed": printed,
            "rechnr": rechnr,
            "rmrate": rmrate,
            "balance": balance,
            "balance_foreign": balance_foreign,
            "tot_balance": tot_balance,
            "guest_taxcode": guest_taxcode,
            "t-res-line": t_res_line_data,
            "t-bill": t_bill_data,
            "spbill-list": spbill_list_data,
            "t-bill-line": t_bill_line_data
        }

    def disp_bill_line():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, datum, ci_date, fixed_rate, rm_rate, ratecode_qsy, pax, it_exist, bill_date, new_contrate, ebdisc_flag, kbdisc_flag, rate_found, contcode, curr_zikatnr, early_flag, kback_flag, bonus_array, curr_i, w_day, curr_artnr, log_artnr, counter, wd_array, serv, vat, netto, repeat_charge, service, tax, tax2, fact, vat2, divered_rental, month_str1, month_str2, ar_ledger, bill, res_line, bill_line, htparam, reslin_queasy, arrangement, artikel, billjournal, queasy
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate
        nonlocal mbill_line, bbill_line
        nonlocal t_bill, t_res_line, spbill_list, t_bill_line, p_bill_line, periode_list, mbill_line, bbill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data, p_bill_line_data, periode_list_data

        p_bill_line_data, spbill_list_data = get_output(
            fo_invoice_disp_bill_line_cldbl(bil_recid, double_currency))

    def calc_periode():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, datum, ci_date, fixed_rate, rm_rate, ratecode_qsy, pax, it_exist, bill_date, new_contrate, ebdisc_flag, kbdisc_flag, rate_found, contcode, curr_zikatnr, early_flag, kback_flag, bonus_array, curr_i, w_day, curr_artnr, log_artnr, wd_array, serv, vat, netto, repeat_charge, service, tax, tax2, fact, vat2, divered_rental, month_str1, month_str2, ar_ledger, bill, res_line, bill_line, htparam, reslin_queasy, arrangement, artikel, billjournal, queasy
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate
        nonlocal mbill_line, bbill_line
        nonlocal t_bill, t_res_line, spbill_list, t_bill_line, p_bill_line, periode_list, mbill_line, bbill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data, p_bill_line_data, periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount = to_decimal("0.0")
        ccount: int = 0
        loop_count: int = 0
        prsv2: date = None
        loopdate: date = None
        pqueasy = None
        mqueasy = None
        Pqueasy = create_buffer("Pqueasy", Queasy)
        Mqueasy = create_buffer("Mqueasy", Queasy)

        mqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, t_res_line.resnr)], "number2": [(eq, t_res_line.reslinnr)], "logi3": [(eq, False)]})

        if mqueasy:
            periode_rsv1 = mqueasy.date2
            periode_rsv2 = mqueasy.date3

        else:
            periode_rsv1 = t_res_line.ankunft
            periode_rsv2 = t_res_line.abreise

        if get_month(periode_rsv1) + 1 > 12:
            periode = date_mdy(1, get_day(periode_rsv1), get_year(periode_rsv1) + timedelta(days=1) - 1)

        elif get_month(periode_rsv1) + 1 == 2:
            if get_day(periode_rsv1) >= 29:
                if get_year(periode_rsv1) % 4 != 0:
                    periode = date_mdy(get_month(periode_rsv1) + 1, month_str1[get_month(periode_rsv1) + 1 - timedelta(days=1), get_year(periode_rsv1)])

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

        pqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, t_res_line.resnr)], "number2": [(eq, t_res_line.reslinnr)], "logi3": [(eq, True)]})

        if pqueasy:
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

            for pqueasy in db_session.query(Pqueasy).filter(
                    (Pqueasy.key == 329) & (Pqueasy.number1 == t_res_line.resnr) & (Pqueasy.number2 == t_res_line.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy._recid).all():
                ccount = ccount + 1

            for pqueasy in db_session.query(Pqueasy).filter(
                    (Pqueasy.key == 329) & (Pqueasy.number1 == t_res_line.resnr) & (Pqueasy.number2 == t_res_line.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy.date2).all():
                periode_rsv1 = pqueasy.date2
                periode_rsv2 = pqueasy.date3
                loop_count = loop_count + 1

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

                if loop_count == ccount:
                    prsv2 = periode_rsv2 - timedelta(days=1)

                else:
                    prsv2 = periode_rsv2

                for loopi in date_range(periode_rsv1, prsv2):
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

        else:
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

            periode_list.diff_day = (periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(curr_amount / periode_list.diff_day)
            periode_list.tamount = to_decimal(periode_list.amt_periode * periode_list.diff_day)

    def usr_prog1(bill_date: date, roomrate: Decimal):
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, datum, ci_date, fixed_rate, rm_rate, ratecode_qsy, pax, it_exist, new_contrate, ebdisc_flag, kbdisc_flag, rate_found, contcode, curr_zikatnr, early_flag, kback_flag, bonus_array, curr_i, w_day, curr_artnr, log_artnr, counter, wd_array, serv, vat, netto, repeat_charge, service, tax, tax2, fact, vat2, divered_rental, month_str1, month_str2, ar_ledger, bill, res_line, bill_line, htparam, reslin_queasy, arrangement, artikel, billjournal, queasy
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate
        nonlocal mbill_line, bbill_line
        nonlocal t_bill, t_res_line, spbill_list, t_bill_line, p_bill_line, periode_list, mbill_line, bbill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data, p_bill_line_data, periode_list_data

        it_exist = False
        prog_str = ""
        i: int = 0

        def generate_inner_output():
            return (roomrate, it_exist)

        # reslin_queasy = get_cache(
        #     Reslin_queasy, {"key": [(eq, "rate-prog")], "number1": [(eq, resnr)], "number2": [(eq, 0)], "char1": [(eq, "")], "reslinnr": [(eq, 1)]})
        reslin_queasy = get_cache(
            Reslin_queasy, {"key": [(eq, "rate-prog")], "number1": [(eq, reslin_queasy.resnr)], "number2": [(eq, 0)], "char1": [(eq, "")], "reslinnr": [(eq, 1)]})

        if reslin_queasy:
            prog_str = reslin_queasy.char3

        # if prog_str != "":
        #     pass

        return generate_inner_output()

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 119)]})

    if htparam:
        log_artnr = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data = get_output(fo_invoice_open_bill_cld_2bl(bil_flag, bil_recid, room, vipflag))

    t_bill = query(t_bill_data, first=True)

    t_res_line = query(t_res_line_data, first=True)
    ebdisc_flag = matches(t_res_line.zimmer_wunsch, ("*ebdisc*"))
    kbdisc_flag = matches(t_res_line.zimmer_wunsch, ("*kbdisc*"))

    if t_res_line.l_zuordnung[0] != 0:
        curr_zikatnr = t_res_line.l_zuordnung[0]
    else:
        curr_zikatnr = t_res_line.zikatnr
    rescomment = get_output(fo_invoice_fill_rescommentbl(bil_recid, fill_co))

    if t_bill.rgdruck == 0:
        printed = ""
    else:
        printed = "*"
    rechnr = t_bill.rechnr
    rmrate = to_decimal("0")

    if t_res_line:
        rmrate = to_decimal(t_res_line.zipreis)
    balance = to_decimal(t_bill.saldo)

    if double_currency or foreign_rate:
        balance_foreign = to_decimal(t_bill.mwst[98])

    if bil_flag == 0:
        tot_balance = to_decimal("0")

        if t_bill.parent_nr == 0:
            tot_balance = to_decimal(t_bill.saldo)
        else:
            tot_balance = get_output(fo_invoice_disp_totbalancebl(bil_recid))
    spbill_list_data.clear()
    disp_bill_line()
    balance = to_decimal(round(balance, 0))
    tot_balance = to_decimal(round(tot_balance, 0))

    if t_bill.billnr == 1:
        calc_periode()

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == t_res_line.resnr) & (Reslin_queasy.reslinnr == t_res_line.reslinnr)).order_by(Reslin_queasy.date1).all():

            periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2), first=True)

            if periode_list:
                t_bill_line = query(t_bill_line_data, filters=(lambda t_bill_line: t_bill_line.bill_datum == periode_list.periode1 and t_bill_line.addserv == False and t_bill_line.addvat == False), first=True)

                if not t_bill_line:
                    t_bill_line = T_bill_line()
                    t_bill_line_data.append(t_bill_line)

                    t_bill_line.bill_datum = periode_list.periode1
                    t_bill_line.rechnr = 0
                    # t_bill_line.bezeich = "Actual Apartment Rental periode " + to_string(periode_list.periode1) + " - " + to_string(periode_list.periode2)
                    t_bill_line.bezeich = f"Actual Apartment Rental periode {periode_list.periode1} - {periode_list.periode2}"
                    t_bill_line.anzahl = 1
                    t_bill_line.zinr = ""

                serv = to_decimal("0")
                vat = to_decimal("0")
                netto = to_decimal("0")
                service = to_decimal("0")
                tax = to_decimal("0")
                tax2 = to_decimal("0")

                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, t_res_line.arrangement)]})

                if arrangement:
                    log_artnr = arrangement.artnr_logis

                artikel = get_cache(
                    Artikel, {"artnr": [(eq, log_artnr)], "departement": [(eq, 0)]})

                if artikel:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, reslin_queasy.date1))
                netto = to_decimal(reslin_queasy.deci1 / fact)
                service = to_decimal(netto * serv)
                tax = to_decimal(netto * vat)
                tax2 = to_decimal(netto * vat2)

                t_bill_line.betrag = to_decimal(t_bill_line.betrag + netto)
                t_bill_line.nettobetrag = to_decimal(t_bill_line.nettobetrag + netto)
                t_bill_line.serv = to_decimal(t_bill_line.serv + service)
                t_bill_line.vat = to_decimal(t_bill_line.vat + tax)
                t_bill_line.netto = to_decimal(t_bill_line.netto + netto)
                balance = to_decimal(balance + reslin_queasy.deci1)
                tot_balance = to_decimal(tot_balance + reslin_queasy.deci1)

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

                mbill_line.betrag = to_decimal(mbill_line.betrag + service)
                mbill_line.nettobetrag = to_decimal(mbill_line.nettobetrag + service)

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

                bbill_line.betrag = to_decimal(bbill_line.betrag + tax)
                bbill_line.nettobetrag = to_decimal(bbill_line.nettobetrag + tax)

    if t_bill.billnr == 1:
        for p_bill_line in query(p_bill_line_data):
            artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == p_bill_line.artnr) & (Artikel.departement == p_bill_line.departement) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7))).first()

            if artikel and artikel.artnr != divered_rental:
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                buffer_copy(p_bill_line, t_bill_line)
                counter = counter + 1
                t_bill_line.counter = counter

            p_bill_line_data.remove(p_bill_line)

        billjournal_obj_list = {}
        billjournal = Billjournal()
        artikel = Artikel()
        for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel, (Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                (matches(Billjournal.bezeich, "*Payment Leasing #*")) & (Billjournal.betrag < 0)).order_by(Billjournal._recid).all():
            if billjournal_obj_list.get(billjournal._recid):
                continue
            else:
                billjournal_obj_list[billjournal._recid] = True

            if num_entries(billjournal.bezeich, "#") > 0 and entry(1, billjournal.bezeich, "#") == to_string(t_bill.resnr) + "]":
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                t_bill_line.bill_datum = billjournal.bill_datum
                t_bill_line.rechnr = 0
                t_bill_line.bezeich = billjournal.bezeich
                t_bill_line.anzahl = 1
                t_bill_line.zinr = t_bill.zinr
                t_bill_line.betrag = to_decimal(t_bill_line.betrag) + to_decimal(billjournal.betrag)
                t_bill_line.nettobetrag = to_decimal(t_bill_line.nettobetrag + billjournal.betrag)
                balance = to_decimal(balance + billjournal.betrag)
                tot_balance = to_decimal(tot_balance + billjournal.betrag)

        billjournal_obj_list = {}
        billjournal = Billjournal()
        artikel = Artikel()
        for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel, (Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                (matches(Billjournal.bezeich, "*Payment Change Rate #*")) & (Billjournal.artnr != ar_ledger)).order_by(Billjournal._recid).all():
            if billjournal_obj_list.get(billjournal._recid):
                continue
            else:
                billjournal_obj_list[billjournal._recid] = True

            if num_entries(billjournal.bezeich, "#") > 0 and entry(1, billjournal.bezeich, "#") == to_string(t_bill.resnr) + "]":
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                t_bill_line.bill_datum = billjournal.bill_datum
                t_bill_line.rechnr = 0
                t_bill_line.bezeich = billjournal.bezeich
                t_bill_line.anzahl = 1
                t_bill_line.zinr = t_bill.zinr
                t_bill_line.betrag = to_decimal(t_bill_line.betrag + billjournal.betrag)
                t_bill_line.nettobetrag = to_decimal(t_bill_line.nettobetrag + billjournal.betrag)
                balance = to_decimal(balance + billjournal.betrag)
                tot_balance = to_decimal(tot_balance + billjournal.betrag)

        billjournal_obj_list = {}
        billjournal = Billjournal()
        artikel = Artikel()
        for billjournal.bill_datum, billjournal.bezeich, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(Billjournal.bill_datum, Billjournal.bezeich, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel, (Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement)).filter(
                (matches(Billjournal.bezeich, "*Refund Change Rate #*")) & (Billjournal.artnr != ar_ledger)).order_by(Billjournal._recid).all():
            if billjournal_obj_list.get(billjournal._recid):
                continue
            else:
                billjournal_obj_list[billjournal._recid] = True

            if num_entries(billjournal.bezeich, "#") > 0 and entry(1, billjournal.bezeich, "#") == to_string(t_bill.resnr) + "]":
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                t_bill_line.bill_datum = billjournal.bill_datum
                t_bill_line.rechnr = 0
                t_bill_line.bezeich = billjournal.bezeich
                t_bill_line.anzahl = 1
                t_bill_line.zinr = t_bill.zinr
                t_bill_line.betrag = to_decimal(t_bill_line.betrag + billjournal.betrag)
                t_bill_line.nettobetrag = to_decimal(t_bill_line.nettobetrag + billjournal.betrag)
                balance = to_decimal(balance + billjournal.betrag)
                tot_balance = to_decimal(tot_balance + billjournal.betrag)

    else:
        for p_bill_line in query(p_bill_line_data):
            t_bill_line = T_bill_line()
            t_bill_line_data.append(t_bill_line)

            buffer_copy(p_bill_line, t_bill_line)
            counter = counter + 1
            t_bill_line.counter = counter

            p_bill_line_data.remove(p_bill_line)

    for t_bill_line in query(t_bill_line_data):
        t_bill_line.betrag = to_decimal(round(t_bill_line.betrag, 0))
        t_bill_line.epreis = to_decimal(round(t_bill_line.epreis, 0))
        t_bill_line.nettobetrag = to_decimal(round(t_bill_line.nettobetrag, 0))
        t_bill_line.serv = to_decimal(round(t_bill_line.serv, 0))
        t_bill_line.vat = to_decimal(round(t_bill_line.vat, 0))
        t_bill_line.netto = to_decimal(round(t_bill_line.netto, 0))

    balance = to_decimal(round(balance, 0))
    tot_balance = to_decimal(round(tot_balance, 0))

    return generate_output()
