# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - fix closing braket on timedelta(days=1)
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Reslin_queasy, Htparam, Res_line, Guest

def leasing_reminder_actual_invoicebl(gname: str):

    prepare_cache([Queasy, Reslin_queasy, Htparam, Res_line, Guest])

    output_list_data = []
    bill_date: date = None
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    queasy = reslin_queasy = htparam = res_line = guest = None

    output_list = periode_list = bqueasy = rqueasy = tqueasy = None

    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "resno": int,
            "gname": string,
            "reserv_name": string,
            "amount": Decimal,
            "arrival": date,
            "departure": date,
            "invoice_no": string,
            "installment": int,
            "due_date": date,
            "queasy_recid": int,
            "prev_payment": bool,
            "actual_invoice": bool
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

    Bqueasy = create_buffer("Bqueasy", Queasy)
    Rqueasy = create_buffer("Rqueasy", Reslin_queasy)
    Tqueasy = create_buffer("Tqueasy", Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, bill_date, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, queasy, reslin_queasy, htparam, res_line, guest
        nonlocal gname
        nonlocal bqueasy, rqueasy, tqueasy
        nonlocal output_list, periode_list, bqueasy, rqueasy, tqueasy
        nonlocal output_list_data, periode_list_data

        return {
            "output-list": output_list_data
        }

    def calc_periode():
        nonlocal output_list_data, bill_date, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, queasy, reslin_queasy, htparam, res_line, guest
        nonlocal gname
        nonlocal bqueasy, rqueasy, tqueasy
        nonlocal output_list, periode_list, bqueasy, rqueasy, tqueasy
        nonlocal output_list_data, periode_list_data

        periode_rsv1: date = None
        periode_rsv2: date = None
        counter: int = 0
        periode: date = None
        loopi: date = None
        curr_amount = to_decimal("0.0")
        loopdate: date = None
        breslin = None
        Breslin = create_buffer("Breslin", Reslin_queasy)
        periode_rsv1 = bqueasy.date2
        periode_rsv2 = bqueasy.date3

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
                    curr_amount = to_decimal(
                        curr_amount + breslin.deci1)

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount / periode_list.diff_day)
            periode_list.tamount = to_decimal(
                periode_list.amt_periode * periode_list.diff_day)

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    reslin_queasy_obj_list = {}
    reslin_queasy = Reslin_queasy()
    res_line = Res_line()
    for reslin_queasy.resnr, reslin_queasy.date2, reslin_queasy.number1, reslin_queasy.logi2, reslin_queasy.reslinnr, reslin_queasy.logi3, reslin_queasy.number2, reslin_queasy.logi1, reslin_queasy._recid, reslin_queasy.deci1, reslin_queasy.date1, res_line.ankunft, res_line.abreise, res_line.gastnrmember, res_line.gastnr, res_line._recid in db_session.query(Reslin_queasy.resnr, Reslin_queasy.date2, Reslin_queasy.number1, Reslin_queasy.logi2, Reslin_queasy.reslinnr, Reslin_queasy.logi3, Reslin_queasy.number2, Reslin_queasy.logi1, Reslin_queasy._recid, Reslin_queasy.deci1, Reslin_queasy.date1, Res_line.ankunft, Res_line.abreise, Res_line.gastnrmember, Res_line.gastnr, Res_line._recid).join(Res_line, (Res_line.resnr == Reslin_queasy.resnr) & (Res_line.reslinnr == Reslin_queasy.reslinnr) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10)).filter(
            (Reslin_queasy.key == ("actual-invoice").lower()) & ((Reslin_queasy.logi1) | ((Reslin_queasy.logi1 == False) & (Reslin_queasy.logi2 == False) & (Reslin_queasy.logi3 == False))) & (Reslin_queasy.char1 == "")).order_by(Reslin_queasy._recid).all():
        if reslin_queasy_obj_list.get(reslin_queasy._recid):
            continue
        else:
            reslin_queasy_obj_list[reslin_queasy._recid] = True

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.resno = reslin_queasy.resnr
        output_list.due_date = reslin_queasy.date2
        output_list.installment = reslin_queasy.number1

        if reslin_queasy.logi1:
            output_list.actual_invoice = False

        elif reslin_queasy.logi1 == False and reslin_queasy.logi2 == False:
            output_list.actual_invoice = True

        tqueasy = get_cache(
            Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)], "number1": [(eq, reslin_queasy.number1 - 1)]})

        if tqueasy:
            output_list.prev_payment = reslin_queasy.logi3

        output_list.arrival = res_line.ankunft
        output_list.departure = res_line.abreise

        guest = get_cache(
            Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            output_list.gname = guest.name + "," + guest.vorname1

        guest = get_cache(
            Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if guest:
            output_list.reserv_name = guest.name + "," + guest.vorname1

        bqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, reslin_queasy.resnr)], "number2": [(eq, reslin_queasy.reslinnr)]})

        if bqueasy:
            periode_list_data.clear()
            tot_periode = 0

            calc_periode()
            output_list.invoice_no = bqueasy.char2
            output_list.queasy_recid = bqueasy._recid

            for periode_list in query(periode_list_data):
                tot_periode = tot_periode + 1

            v_cicilanke = reslin_queasy.number1
            v_percount = tot_periode / reslin_queasy.number2
            v_start = ((v_cicilanke - 1) * v_percount) + 1
            v_end = v_cicilanke * v_percount

            rqueasy_obj_list = {}
            for rqueasy in db_session.query(Rqueasy).filter(
                    (Rqueasy.key == "arrangement") & (Rqueasy.resnr == reslin_queasy.resnr) & (Rqueasy.reslinnr == reslin_queasy.reslinnr)).order_by(Rqueasy.date1).all():
                periode_list = query(periode_list_data, (lambda periode_list: rqueasy.date1 >= periode_list.periode1 and rqueasy.date1 <= periode_list.periode2 and periode_list.counter >= v_start and periode_list.counter <= v_end), first=True)
                if not periode_list:
                    continue

                if rqueasy_obj_list.get(rqueasy._recid):
                    continue
                else:
                    rqueasy_obj_list[rqueasy._recid] = True

                output_list.amount = to_decimal(
                    output_list.amount + rqueasy.deci1)

    for output_list in query(output_list_data):
        output_list.amount = to_decimal(round(output_list.amount, 0))

    return generate_output()
