# using conversion tools version: 1.0.0.119
"""_yusufwijasena_11/11/2025

    Ticket ID: F6D79E
        _remark_:   - update ITA: Program terkait feature service apartement
                    - import from function_py
                    - fix python indentation
                    - fix timedelta(days=1)
"""
#------------------------------------------
# Rd, 25/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
# from functions.ratecode_rate import ratecode_rate
from functions_py.ratecode_rate import ratecode_rate
from models import Res_line, Waehrung, Htparam, Bediener, Arrangement, Guest, Guest_pr, Queasy, Reslin_queasy, Ratecode

reslin_list_data, Reslin_list = create_model_like(Res_line)


def res_rmrate_view_repeat_chargebl(pvilanguage: int, user_init: string, reslin_list_data: list[Reslin_list]):

    prepare_cache([Res_line, Waehrung, Htparam, Bediener, Arrangement, Queasy, Reslin_queasy, Ratecode])

    rate_found = False
    ci_date = None
    output_list_data = []
    p_list_data = []
    curr_add_last_data = []
    t_waehrung_data = []
    q2_reslin_queasy_data = []
    ratecode_list_data = []
    rate_flag = False
    split_price = False
    price_decimal: int = 0
    exchg_rate: Decimal = 1
    ct: string = ""
    curr_wabnr: int = 0
    datum: date = None
    bill_date: date = None
    co_date: date = None
    ebdisc_flag: bool = False
    kbdisc_flag: bool = False
    early_flag: bool = False
    kback_flag: bool = False
    curr_zikatnr: int = 0
    rm_rate: Decimal = to_decimal("0.0")
    # ITA: Program terkait feature service apartement
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    lvcarea: str = "prepare-res-rmrate"
    found: bool = False
    curr_time: int = 0
    res_line = waehrung = htparam = bediener = arrangement = guest = guest_pr = queasy = reslin_queasy = ratecode = None

    dynarate_list = ratecode_list = output_list = t_waehrung = q2_reslin_queasy = curr_add_last = p_list = periode_list = reslin_list = waehrung2 = waehrung1 = None

    dynarate_list_data, Dynarate_list = create_model(
        "Dynarate_list",
        {
            "rcode": str,
            "fr_room": int,
            "to_room": int,
            "days1": int,
            "days2": int,
            "s_recid": int,
            "rmtype": str
        })
    ratecode_list_data, Ratecode_list = create_model(
        "Ratecode_list",
        {
            "rcode_str": str
        })
    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "foreign_rate": bool,
            "double_currency": bool,
            "curr_foreign": str,
            "local_nr": int,
            "msg_str": str,
            "foreign_nr": int,
            "max_rate": Decimal,
            "long_digit": bool,
            "selected": bool,
            "contcode": str,
            "currency_add_first": str,
            "zimmer_wunsch": str,
            "btn_chgart": bool,
            "fact1": Decimal,
            "betriebsnr": int,
            "zipreis": Decimal,
            "adrflag": bool,
            "recid_resline": int
        })
    t_waehrung_data, T_waehrung = create_model(
        "T_waehrung",
        {
            "wabkurz": str,
            "bezeich": str,
            "betriebsnr": int,
            "waehrungsnr": int,
            "exrate": Decimal
        })
    q2_reslin_queasy_data, Q2_reslin_queasy = create_model(
        "Q2_reslin_queasy",
        {
            "date1": date,
            "date2": date,
            # ITA: Program terkait feature service apartement
            "date3": date,
            "deci1": Decimal,
            "char1": str,
            "number3": int,
            "char2": str,
            "char3": str,
            # ITA: Program terkait feature service apartement
            "recid_reslin": int,
            "printed_actual": bool
        })
    curr_add_last_data, Curr_add_last = create_model(
        "Curr_add_last",
        {
            "bezeich": str
        })
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

    Waehrung2 = create_buffer("Waehrung2", Waehrung)
    Waehrung1 = create_buffer("Waehrung1", Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        return {
            "rate_found": rate_found,
            "ci_date": ci_date,
            "output-list": output_list_data,
            "p-list": p_list_data,
            "curr-add-last": curr_add_last_data,
            "t-waehrung": t_waehrung_data,
            "q2-reslin-queasy": q2_reslin_queasy_data,
            "ratecode-list": ratecode_list_data,
            "rate_flag": rate_flag,
            "split_price": split_price
        }

    # ITA: leasing Feature
    def calc_periode():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount: Decimal = to_decimal("0.0")
        ccount: int = 0
        loop_count: int = 0
        prsv2: date = None
        loopdate: date = None
        pqueasy = None
        mqueasy = None
        Pqueasy = create_buffer("Pqueasy", Queasy)
        Mqueasy = create_buffer("Mqueasy", Queasy)

        mqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, reslin_list.resnr)], "number2": [(eq, reslin_list.reslinnr)], "logi3": [(eq, False)]})

        if mqueasy:
            periode_rsv1 = mqueasy.date2
            periode_rsv2 = mqueasy.date3

        else:
            periode_rsv1 = reslin_list.ankunft
            periode_rsv2 = reslin_list.abreise

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

        pqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, reslin_list.resnr)], "number2": [(eq, reslin_list.reslinnr)], "logi3": [(eq, True)]})

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
                    (Pqueasy.key == 329) & (Pqueasy.number1 == reslin_list.resnr) & (Pqueasy.number2 == reslin_list.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy._recid).all():
                ccount = ccount + 1

            for pqueasy in db_session.query(Pqueasy).filter(
                    (Pqueasy.key == 329) & (Pqueasy.number1 == reslin_list.resnr) & (Pqueasy.number2 == reslin_list.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy.date2).all():
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
            if reslin_list.resstatus == 6 and reslin_list.abreise > res_line.abreise:
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

                periode_rsv1 = res_line.abreise
                periode_rsv2 = reslin_list.abreise

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

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount) / to_decimal(periode_list.diff_day)
            periode_list.tamount = to_decimal(
                periode_list.amt_periode) * to_decimal(periode_list.diff_day)

    def disp_query():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        output_list.fact1 = to_decimal(
            waehrung1.ankauf) / to_decimal(waehrung1.einheit)

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == reslin_list.resnr) & (Reslin_queasy.reslinnr == reslin_list.reslinnr)).order_by(Reslin_queasy.date1).all():

            periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.reslin_queasy.date1 >= periode_list.periode1 and reslin_queasy.date1 <= periode_list.periode2), first=True)

            if periode_list:
                # ITA: Program terkait feature service apartement
                q2_reslin_queasy = query(q2_reslin_queasy_data, filters=(lambda q2_reslin_queasy: q2_reslin_queasy.date1 == periode_list.periode1 and q2_reslin_queasy.date3 == periode_list.periode2), first=True)

                if not q2_reslin_queasy:
                    q2_reslin_queasy = Q2_reslin_queasy()
                    q2_reslin_queasy_data.append(q2_reslin_queasy)

                    q2_reslin_queasy.date1 = periode_list.periode1
                    # ITA: Program terkait feature service apartement
                    q2_reslin_queasy.date3 = periode_list.periode2
                    q2_reslin_queasy.char1 = reslin_queasy.char1
                    q2_reslin_queasy.number3 = reslin_queasy.number3
                    q2_reslin_queasy.char2 = reslin_queasy.char2
                    q2_reslin_queasy.char3 = reslin_queasy.char3
                    q2_reslin_queasy.recid_reslin = reslin_queasy._recid

                    # ITA: Program terkait feature service apartement
                    queasy = get_cache(
                        Queasy, {"key": [(eq, 329)], "number1": [(eq, reslin_list.resnr)], "number2": [(eq, reslin_list.reslinnr)]})

                    if queasy:
                        q2_reslin_queasy.printed_actual = True

                # ITA: Program terkait feature service apartement
                q2_reslin_queasy.deci1 = to_decimal(
                    q2_reslin_queasy.deci1) + to_decimal(reslin_queasy.deci1)
                q2_reslin_queasy.date2 = reslin_queasy.date1

        for q2_reslin_queasy in query(q2_reslin_queasy_data):
            q2_reslin_queasy.deci1 = to_decimal(
                round(q2_reslin_queasy.deci1, 0))

    def fill_p_list():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        if reslin_queasy:
            p_list.betrag = to_decimal(reslin_queasy.deci1)
            p_list.date1 = reslin_queasy.date1
            p_list.date2 = reslin_queasy.date2
            p_list.argt = reslin_queasy.char1
            p_list.pax = reslin_queasy.number3
            p_list.rcode = reslin_queasy.char2

    def assign_it():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        curr_add_last = Curr_add_last()
        curr_add_last_data.append(curr_add_last)

        curr_add_last.bezeich = waehrung1.bezeich

    def create_dynarate_list():
        nonlocal rate_found, ci_date, output_list_data, p_list_data, curr_add_last_data, t_waehrung_data, q2_reslin_queasy_data, ratecode_list_data, rate_flag, split_price, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, month_str1, month_str2, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal pvilanguage, user_init
        nonlocal waehrung2, waehrung1
        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, periode_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_data, ratecode_list_data, output_list_data, t_waehrung_data, q2_reslin_queasy_data, curr_add_last_data, p_list_data, periode_list_data

        i: int = 0
        tokcounter: int = 0
        iftask = ""
        mestoken = ""
        mesvalue = ""
        occ_rooms: int = 0
        use_it: bool = False

        for ratecode in db_session.query(Ratecode).filter(
                (Ratecode.code == guest_pr.code)).order_by(Ratecode._recid).all():
            dynarate_list = Dynarate_list()
            dynarate_list_data.append(dynarate_list)

            dynarate_list.s_recid = ratecode._recid

            iftask = ratecode.char1[4]
            for tokcounter in range(1, num_entries(iftask, ";") - 1 + 1):
                mestoken = substring(entry(tokcounter - 1, iftask, ";"), 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";"), 2)

                if mestoken == "RT":
                    dynarate_list.rmtype = mesvalue
                elif mestoken == "FR":
                    dynarate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynarate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynarate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynarate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynarate_list.rcode = mesvalue

        for dynarate_list in query(dynarate_list_data, sort_by=[("rcode", False)]):
            ratecode_list = query(ratecode_list_data, filters=(
                lambda ratecode_list: ratecode_list.rcode_str == dynarate_list.rcode), first=True)

            if not ratecode_list:
                ratecode_list = Ratecode_list()
                ratecode_list_data.append(ratecode_list)

                ratecode_list.rcode_str = dynarate_list.rcode

    htparam = get_cache(Htparam, {"paramnr": [(eq, 90)]})
    split_price = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    reslin_list = query(reslin_list_data, first=True)

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
        t_waehrung = T_waehrung()
        t_waehrung_data.append(t_waehrung)

        t_waehrung.wabkurz = waehrung.wabkurz
        t_waehrung.bezeich = waehrung.bezeich
        t_waehrung.betriebsnr = waehrung.betriebsnr
        t_waehrung.waehrungsnr = waehrung.waehrungsnr
        t_waehrung.exrate = to_decimal(
            waehrung.ankauf) / to_decimal(waehrung.einheit)

    output_list = Output_list()
    output_list_data.append(output_list)

    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

    arrangement = get_cache(
        Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 143)]})
    output_list.foreign_rate = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 240)]})
    output_list.double_currency = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})
    output_list.curr_foreign = htparam.fchar

    htparam = get_cache(Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache(Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        output_list.msg_str = output_list.msg_str + chr_unicode(2) + translateExtended(
            "Local Currency Code incorrect! (Param 152 / Grp 7).", lvcarea, "")

        return generate_output()
    output_list.local_nr = waehrung.waehrungsnr

    if output_list.foreign_rate:
        htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache(Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if not waehrung:
            output_list.msg_str = output_list.msg_str + chr_unicode(2) + translateExtended(
                "Foreign Currency Code incorrect! (Param 144 / Grp 7).", lvcarea, "")

            return generate_output()
        output_list.foreign_nr = waehrung.waehrungsnr

    # htparam = get_cache(Htparam, {"paramnr": [(eq, 1108)]})
    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 1108).with_for_update().first()

    if htparam.feldtyp == 1:
        htparam.feldtyp = 2
        htparam.fdecimal = to_decimal(htparam.finteger)
        htparam.finteger = 0

    output_list.max_rate = to_decimal(htparam.fdecimal)

    htparam = get_cache(Htparam, {"paramnr": [(eq, 494)]})
    rate_flag = htparam.flogical

    res_line = get_cache(
        Res_line, {"resnr": [(eq, reslin_list.resnr)], "reslinnr": [(eq, reslin_list.reslinnr)]})
    output_list.betriebsnr = reslin_list.betriebsnr
    output_list.zipreis = to_decimal(reslin_list.zipreis)
    output_list.adrflag = reslin_list.adrflag
    output_list.recid_resline = res_line._recid

    guest = get_cache(Guest, {"gastnr": [(eq, reslin_list.gastnr)]})

    if guest.notizen[2] != "":
        waehrung2 = get_cache(Waehrung, {"wabkurz": [(eq, guest.notizen[2])]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 246)]})
    output_list.long_digit = htparam.flogical

    if output_list.foreign_rate or output_list.double_currency:

        htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache(Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate = to_decimal(waehrung.ankauf) / \
                to_decimal(waehrung.einheit)

    guest_pr = get_cache(Guest_pr, {"gastnr": [(eq, reslin_list.gastnr)]})

    if guest_pr:
        output_list.contcode = guest_pr.code
        ct = reslin_list.zimmer_wunsch

        if matches(ct, r"*$CODE$*"):
            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
            output_list.contcode = substring(ct, 0, get_index(ct, ";") - 1)
    p_list = P_list()
    p_list_data.append(p_list)

    if arrangement:
        output_list.selected = True
        fill_p_list()
    ebdisc_flag = matches(reslin_list.zimmer_wunsch, ("*ebdisc*"))
    kbdisc_flag = matches(reslin_list.zimmer_wunsch, ("*kbdisc*"))

    if reslin_list.l_zuordnung[0] != 0:
        curr_zikatnr = reslin_list.l_zuordnung[0]
    else:
        curr_zikatnr = reslin_list.zikatnr
    co_date = reslin_list.abreise

    if co_date > reslin_list.ankunft:
        co_date = co_date - timedelta(days=1)
    for datum in date_range(reslin_list.ankunft, co_date):
        bill_date = datum

        guest_pr = get_cache(Guest_pr, {"gastnr": [(eq, reslin_list.gastnr)]})

        if guest_pr:

            queasy = get_cache(
                Queasy, {"key": [(eq, 18)], "number1": [(eq, reslin_list.reserve_int)]})

            if queasy and queasy.logi3:
                bill_date = reslin_list.ankunft
            rate_found, rm_rate, early_flag, kback_flag = get_output(
                ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, guest_pr.code, None, bill_date, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

            if rate_found:
                break

    if reslin_list.resstatus == 8:
        pass

    elif reslin_list.reserve_char != "" and substring(bediener.permissions, 42, 1) < "2":
        output_list.btn_chgart = True
    else:
        output_list.btn_chgart = False

    output_list = query(output_list_data, first=True)

    if reslin_list.betriebsnr != 0:
        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != reslin_list.betriebsnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
            assign_it()

        waehrung1 = get_cache(
            Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})

    elif waehrung2:
        curr_wabnr = waehrung2.waehrungsnr

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != curr_wabnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
            assign_it()

        waehrung1 = get_cache(Waehrung, {"waehrungsnr": [(eq, curr_wabnr)]})

    elif reslin_list.betriebsnr == 0 and not reslin_list.adrflag:
        if guest_pr:
            if reslin_list.reserve_int != 0:
                queasy = get_cache(
                    Queasy, {"key": [(eq, 18)], "number1": [(eq, reslin_list.reserve_int)]})

                if not queasy or (queasy and queasy.char3 == ""):
                    queasy = get_cache(
                        Queasy, {"key": [(eq, 2)], "char1": [(eq, output_list.contcode)]})
            else:
                queasy = get_cache(
                    Queasy, {"key": [(eq, 2)], "char1": [(eq, output_list.contcode)]})

            if queasy:
                if queasy.key == 18:
                    waehrung1 = get_cache(
                        Waehrung, {"wabkurz": [(eq, queasy.char3)]})
                else:
                    waehrung1 = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                if waehrung1:
                    found = True
                    curr_wabnr = waehrung1.waehrungsnr

                    for waehrung1 in db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr != curr_wabnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                        assign_it()

                    waehrung1 = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, curr_wabnr)]})

        if not found:
            if output_list.foreign_rate:
                for waehrung1 in db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr != output_list.foreign_nr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                    assign_it()

                waehrung1 = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, output_list.foreign_nr)]})
            else:
                for waehrung1 in db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr != output_list.local_nr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                    assign_it()

                waehrung1 = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, output_list.local_nr)]})

    elif reslin_list.betriebsnr == 0 and reslin_list.adrflag:
        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != output_list.local_nr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
            assign_it()

        waehrung1 = get_cache(
            Waehrung, {"waehrungsnr": [(eq, output_list.local_nr)]})
    output_list.currency_add_first = waehrung1.bezeich
    calc_periode()
    disp_query()
    output_list.zimmer_wunsch = reslin_list.zimmer_wunsch
    
    # ITA: Program terkait feature service apartement
    for q2_reslin_queasy in query(q2_reslin_queasy_data):
        q2_reslin_queasy.deci1 = to_decimal(q2_reslin_queasy.deci1)

    curr_time = get_current_time_in_seconds()

    guest_pr = get_cache(Guest_pr, {"gastnr": [(eq, reslin_list.gastnr)]})
    
    while guest_pr is not None:
        queasy = get_cache(
            Queasy, {"key": [(eq, 2)], "char1": [(eq, guest_pr.code)]})

        if queasy:
            if not queasy.logi2:
                ratecode_list = query(ratecode_list_data, filters=(
                    lambda ratecode_list: ratecode_list.rcode_str == guest_pr.code), first=True)

                if not ratecode_list:
                    ratecode_list = Ratecode_list()
                    ratecode_list_data.append(ratecode_list)
                    
                    ratecode_list.rcode_str = guest_pr.code

            else:
                dynarate_list_data.clear()
                create_dynarate_list()

        curr_recid = guest_pr._recid
        guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == reslin_list.gastnr) & (Guest_pr._recid > curr_recid)).first()
    curr_time = get_current_time_in_seconds() - curr_time

    return generate_output()
