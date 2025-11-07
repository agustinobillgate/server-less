# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix closing bracket position
                    - fix string.lower()
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import Bill_line, Queasy, Htparam, Res_line, Waehrung, Reslin_queasy, Arrangement, Zimkateg, Guest, Bill, Artikel


def deferred_rentalbl(fdate: date, tdate: date, sorttype: int, exclude_tax: bool):
    prepare_cache([Bill_line, Queasy, Htparam, Res_line,Reslin_queasy, Arrangement, Zimkateg, Guest, Bill, Artikel])

    output_list_data = []
    loop_date: date = None
    ci_date: date = None
    rstatus: List[str] = create_empty_list(99, "")
    doit: bool = False
    netto = to_decimal("0.0")
    service = to_decimal("0.0")
    tax = to_decimal("0.0")
    tax2 = to_decimal("0.0")
    serv = to_decimal("0.0")
    vat = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    fact = to_decimal("0.0")
    log_artnr: int = 0
    flag_sort: int = 0
    curr_sort: int = 0
    tot_revenue = to_decimal("0.0")
    tot_deffrental = to_decimal("0.0")
    tot_diff = to_decimal("0.0")
    tot_amount = to_decimal("0.0")
    tot_rmrate = to_decimal("0.0")
    gtot_revenue = to_decimal("0.0")
    gtot_deffrental = to_decimal("0.0")
    gtot_diff = to_decimal("0.0")
    gtot_amount = to_decimal("0.0")
    gtot_rmrate = to_decimal("0.0")
    divered_rental: int = 0
    tot_periode: int = 0
    v_cicilanke: int = 0
    v_percount: int = 0
    v_start: int = 0
    v_end: int = 0
    month_str1: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_str2: List[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    bill_line = queasy = htparam = res_line = waehrung = reslin_queasy = arrangement = zimkateg = guest = bill = artikel = None

    output_list = output_list1 = periode_list = tbill_line = bqueasy = pqueasy = None

    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "resnr": int,
            "reslinnr": int,
            "ankunft": date,
            "abreise": date,
            "roomtype": str,
            "roomnr": str,
            "accountnumber": str,
            "guestname": str,
            "resstatus": str,
            "start_date": date,
            "end_date": date,
            "invoiceno": str,
            "rental_amount": Decimal,
            "rmrate": Decimal,
            "periodbilling": int,
            "consumed": int,
            "remainbilling": int,
            "deffrental": Decimal,
            "revenue": Decimal,
            "diff": Decimal,
            "type_flag": int,
            "logis": int,
            "extend_rsv": bool
        })
    output_list1_data, Output_list1 = create_model_like(Output_list)
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

    Tbill_line = create_buffer("Tbill_line", Bill_line)
    Bqueasy = create_buffer("Bqueasy", Queasy)
    Pqueasy = create_buffer("Pqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, loop_date, ci_date, rstatus, doit, netto, service, tax, tax2, serv, vat, vat2, fact, log_artnr, flag_sort, curr_sort, tot_revenue, tot_deffrental, tot_diff, tot_amount, tot_rmrate, gtot_revenue, gtot_deffrental, gtot_diff, gtot_amount, gtot_rmrate, divered_rental, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, bill_line, queasy, htparam, res_line, waehrung, reslin_queasy, arrangement, zimkateg, guest, bill, artikel
        nonlocal fdate, tdate, sorttype, exclude_tax
        nonlocal tbill_line, bqueasy, pqueasy
        nonlocal output_list, output_list1, periode_list, tbill_line, bqueasy, pqueasy
        nonlocal output_list_data, output_list1_data, periode_list_data

        return {
            "output-list": output_list_data
        }

    def calc_periode():
        nonlocal output_list_data, loop_date, ci_date, rstatus, doit, netto, service, tax, tax2, serv, vat, vat2, fact, log_artnr, flag_sort, curr_sort, tot_revenue, tot_deffrental, tot_diff, tot_amount, tot_rmrate, gtot_revenue, gtot_deffrental, gtot_diff, gtot_amount, gtot_rmrate, divered_rental, tot_periode, v_cicilanke, v_percount, v_start, v_end, month_str1, month_str2, bill_line, queasy, htparam, res_line, waehrung, reslin_queasy, arrangement, zimkateg, guest, bill, artikel
        nonlocal fdate, tdate, sorttype, exclude_tax
        nonlocal tbill_line, bqueasy, pqueasy
        nonlocal output_list, output_list1, periode_list, tbill_line, bqueasy, pqueasy
        nonlocal output_list_data, output_list1_data, periode_list_data

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
        breslin = None
        Pqueasy = create_buffer("Pqueasy", Queasy)
        Mqueasy = create_buffer("Mqueasy", Queasy)
        Breslin = create_buffer("Breslin", Reslin_queasy)

        mqueasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number1": [(eq, res_line.resnr)], "number2": [(eq, res_line.reslinnr)], "logi3": [(eq, False)]})

        if mqueasy:
            periode_rsv1 = mqueasy.date2
            periode_rsv2 = mqueasy.date3

        else:
            periode_rsv1 = res_line.ankunft
            periode_rsv2 = res_line.abreise

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
            Queasy, {"key": [(eq, 329)], "number1": [(eq, res_line.resnr)], "number2": [(eq, res_line.reslinnr)], "logi3": [(eq, True)]})

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
                    (Pqueasy.key == 329) & (Pqueasy.number1 == res_line.resnr) & (Pqueasy.number2 == res_line.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy._recid).all():
                ccount = ccount + 1

            for pqueasy in db_session.query(Pqueasy).filter(
                    (Pqueasy.key == 329) & (Pqueasy.number1 == res_line.resnr) & (Pqueasy.number2 == res_line.reslinnr) & (Pqueasy.logi3)).order_by(Pqueasy.date2).all():
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
                breslin = get_cache(
                    Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "date1": [(le, loopdate)], "date2": [(le, loopdate)]})

                if breslin:
                    curr_amount = to_decimal(
                        curr_amount) + to_decimal(breslin.deci1)

            periode_list.diff_day = (
                periode_list.periode2 - periode_list.periode1) + 1
            periode_list.amt_periode = to_decimal(
                curr_amount / periode_list.diff_day)
            periode_list.tamount = to_decimal(
                periode_list.amt_periode * periode_list.diff_day)

    rstatus[0] = "GUARANTEED"
    rstatus[1] = "6 PM"
    rstatus[2] = "TENTATIVE"
    rstatus[3] = "WAITING LIST"
    rstatus[4] = "ORAL CONFIRM"
    rstatus[5] = "INHOUSE"
    rstatus[7] = "CHECK OUT"
    rstatus[8] = "CANCEL"
    rstatus[9] = "NO SHOW"
    rstatus[10] = "ROOM SHARER"
    rstatus[11] = "ADD BILL"
    rstatus[12] = "ROOM SHARER (INHOUSE)"
    rstatus[98] = "DELETE"

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1052)]})

    if htparam:
        divered_rental = htparam.finteger

    reslin_queasy_obj_list = {}
    for reslin_queasy, res_line, waehrung, queasy in db_session.query(Reslin_queasy, Res_line, Waehrung, Queasy).join(Res_line, (Res_line.resnr == Reslin_queasy.resnr) & (Res_line.reslinnr == Reslin_queasy.reslinnr) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 8) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Waehrung, (Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Queasy, (Queasy.key == 329) & (Queasy.number1 == Reslin_queasy.resnr) & (Queasy.number2 == Reslin_queasy.reslinnr) & (Queasy._recid == Reslin_queasy.betriebsnr)).filter(
            (Reslin_queasy.key == "actual-invoice") & (Reslin_queasy.date3 <= fdate)).order_by(Reslin_queasy._recid).all():
        if reslin_queasy_obj_list.get(reslin_queasy._recid):
            continue
        else:
            reslin_queasy_obj_list[reslin_queasy._recid] = True

        doit = False
        if sorttype == 0:
            doit = True

            if res_line.resstatus == 6:
                if queasy.char2 != "":
                    flag_sort = 1

                elif queasy.char2 == "":
                    flag_sort = 2

            elif res_line.resstatus != 6:
                if queasy.char2 != "":
                    flag_sort = 3

                elif queasy.char2 == "":
                    flag_sort = 4

        elif sorttype == 1:
            if res_line.resstatus == 6:
                if queasy.char2 != "":
                    doit = True
                    flag_sort = 1

        elif sorttype == 2:
            if res_line.resstatus == 6:
                if queasy.char2 == "":
                    doit = True
                    flag_sort = 2

        elif sorttype == 3:
            if res_line.resstatus != 6:
                if queasy.char2 != "":
                    doit = True
                    flag_sort = 3

        elif sorttype == 4:
            if res_line.resstatus != 6:
                if queasy.char2 == "":
                    doit = True
                    flag_sort = 4

        if doit:
            periode_list_data.clear()
            calc_periode()
            tot_periode = 0

            for periode_list in query(periode_list_data):
                tot_periode = tot_periode + 1

            v_cicilanke = reslin_queasy.number1
            v_percount = tot_periode / reslin_queasy.number2
            v_start = ((v_cicilanke - 1) * v_percount) + 1
            v_end = v_cicilanke * v_percount

            for periode_list in query(periode_list_data, filters=(lambda periode_list: periode_list.counter >= v_start and periode_list.counter <= v_end)):
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.resnr = res_line.resnr
                output_list1.reslinnr = res_line.reslinnr
                output_list1.ankunft = res_line.ankunft
                output_list1.abreise = res_line.abreise
                output_list1.roomnr = res_line.zinr
                output_list1.roomnr = res_line.zinr
                output_list1.resstatus = rstatus[res_line.resstatus - 1]
                output_list1.start_date = periode_list.periode1
                output_list1.end_date = periode_list.periode2
                output_list1.periodbilling = (
                    periode_list.periode2 - periode_list.periode1) + 1
                output_list1.type_flag = flag_sort
                output_list1.extend_rsv = queasy.logi3
                output_list1.invoiceno = queasy.char2

                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:
                    output_list1.logis = arrangement.argt_artikelnr

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    output_list1.roomtype = zimkateg.kurzbez

                guest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    # output_list1.guestname = guest.name + ", " + \
                    #     guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    output_list1.guestname = f"{guest.name}, {guest.vorname1}{guest.anredefirma} {guest.anrede1}"

    queasy_obj_list = {}
    for queasy, res_line, waehrung in db_session.query(Queasy, Res_line, Waehrung).join(Res_line, (Res_line.resnr == Queasy.number1) & (Res_line.reslinnr == Queasy.number2) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 8) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Waehrung, (Waehrung.waehrungsnr == Res_line.betriebsnr)).filter(
            (Queasy.key == 329) & (Queasy.char3 != "")).order_by(Queasy._recid).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True

        doit = False
        if date_mdy(entry(1, queasy.char3, "|")) <= fdate:
            doit = True

        if doit:
            if sorttype == 0:
                doit = True

                if res_line.resstatus == 6:
                    if queasy.char2 != "":
                        flag_sort = 1

                    elif queasy.char2 == "":
                        flag_sort = 2

                elif res_line.resstatus != 6:
                    if queasy.char2 != "":
                        flag_sort = 3

                    elif queasy.char2 == "":
                        flag_sort = 4

            elif sorttype == 1:
                if res_line.resstatus == 6:
                    if queasy.char2 != "":
                        doit = True
                        flag_sort = 1

            elif sorttype == 2:
                if res_line.resstatus == 6:
                    if queasy.char2 == "":
                        doit = True
                        flag_sort = 2

            elif sorttype == 3:
                if res_line.resstatus != 6:
                    if queasy.char2 != "":
                        doit = True
                        flag_sort = 3

            elif sorttype == 4:
                if res_line.resstatus != 6:
                    if queasy.char2 == "":
                        doit = True
                        flag_sort = 4

        if doit:
            reslin_queasy = get_cache(
                Reslin_queasy, {"key": [(eq, "actual-invoice")], "resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)], "betriebsnr": [(eq, to_int(queasy._recid))]})

            if reslin_queasy:
                doit = False

        if doit:
            periode_list_data.clear()
            calc_periode()

            for periode_list in query(periode_list_data):
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.resnr = res_line.resnr
                output_list1.reslinnr = res_line.reslinnr
                output_list1.ankunft = res_line.ankunft
                output_list1.abreise = res_line.abreise
                output_list1.roomnr = res_line.zinr
                output_list1.roomnr = res_line.zinr
                output_list1.resstatus = rstatus[res_line.resstatus - 1]
                output_list1.start_date = periode_list.periode1
                output_list1.end_date = periode_list.periode2
                output_list1.periodbilling = (
                    periode_list.periode2 - periode_list.periode1) + 1
                output_list1.type_flag = flag_sort
                output_list1.extend_rsv = queasy.logi3
                output_list1.invoiceno = queasy.char2

                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:
                    output_list1.logis = arrangement.argt_artikelnr

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    output_list1.roomtype = zimkateg.kurzbez

                guest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    # output_list1.guestname = guest.name + ", " + \
                    #     guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    output_list1.guestname = f"{guest.name}, {guest.vorname1}{guest.anredefirma} {guest.anrede1}"

    for output_list1 in query(output_list1_data, sort_by=[("resnr", False)]):
        for loop_date in date_range(output_list1.start_date, output_list1.end_date):

            reslin_queasy = get_cache(
                Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, output_list1.resnr)], "reslinnr": [(eq, output_list1.reslinnr)], "date1": [(le, loop_date)], "date2": [(ge, loop_date)]})

            if reslin_queasy:
                output_list1.rental_amount = to_decimal(
                    output_list1.rental_amount) + (- to_decimal(reslin_queasy.deci1))
                output_list1.rmrate = to_decimal(reslin_queasy.deci1)

        bill = get_cache(
            Bill, {"rechnr": [(eq, to_int(output_list1.invoiceno))], "resnr": [(eq, output_list1.resnr)], "parent_nr": [(eq, output_list1.reslinnr)], "billnr": [(eq, 1)]})

        if bill:
            if output_list1.end_date < fdate:
                for tbill_line in db_session.query(Tbill_line).filter(
                        (Tbill_line.rechnr == bill.rechnr) & (Tbill_line.bill_datum >= output_list1.start_date) & (Tbill_line.bill_datum <= output_list1.end_date) & (Tbill_line.artnr == output_list1.logis)).order_by(Tbill_line._recid).all():
                    output_list1.consumed = output_list1.consumed + 1
                    output_list1.revenue = to_decimal(
                        output_list1.revenue + tbill_line.betrag)

            elif output_list1.end_date >= fdate:
                for tbill_line in db_session.query(Tbill_line).filter(
                        (Tbill_line.rechnr == bill.rechnr) & (Tbill_line.bill_datum >= output_list1.start_date) & (Tbill_line.bill_datum <= fdate) & (Tbill_line.artnr == output_list1.logis)).order_by(Tbill_line._recid).all():
                    output_list1.consumed = output_list1.consumed + 1
                    output_list1.revenue = to_decimal(
                        output_list1.revenue) + to_decimal(tbill_line.betrag)

        output_list1.rental_amount = to_decimal(
            round(output_list1.rental_amount, 0))
        output_list1.remainbilling = output_list1.periodBilling - output_list1.consumed

        if exclude_tax:
            res_line = get_cache(
                Res_line, {"resnr": [(eq, output_list1.resnr)], "reslinnr": [(eq, output_list1.reslinnr)]})

            if res_line:
                arrangement = get_cache(
                    Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement:
                    log_artnr = arrangement.artnr_logis

                service = to_decimal("0")
                tax = to_decimal("0")
                tax2 = to_decimal("0")
                netto = to_decimal("0")

                artikel = get_cache(
                    Artikel, {"artnr": [(eq, log_artnr)]})

                if artikel:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(
                        1, artikel.artnr, artikel.departement, output_list1.ankunft))
                output_list1.rental_amount = to_decimal(
                    output_list1.rental_amount / fact)
                output_list1.revenue = to_decimal(
                    output_list1.revenue / fact)
                output_list1.rmrate = to_decimal(
                    output_list1.rmrate / fact)

        output_list1.deffrental = to_decimal(output_list1.rental_amount)
        output_list1.diff = to_decimal(
            output_list1.rental_amount + output_list1.Revenue)

        if output_list1.type_flag == 2 or output_list1.type_flag == 4:
            output_list1.deffrental = to_decimal("0")
            output_list1.revenue = to_decimal(output_list1.Revenue)
            output_list1.diff = to_decimal(
                output_list1.deffRental + output_list1.Revenue)

        if (output_list1.diff > -10 and output_list1.diff < 0) or (output_list1.diff > 0 and output_list1.diff < 500):
            output_list1.diff = to_decimal("0")

    if sorttype == 0:
        for output_list1 in query(output_list1_data, sort_by=[("type_flag", False)]):
            if curr_sort != output_list1.type_flag:
                if curr_sort != 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.roomtype = "T O T A L"
                    output_list.revenue = to_decimal(tot_revenue)
                    output_list.deffrental = to_decimal(tot_deffrental)
                    output_list.diff = to_decimal(tot_diff)
                    output_list.rental_amount = to_decimal(tot_amount)
                    output_list.rmrate = to_decimal(tot_rmrate)
                    tot_revenue = to_decimal("0")
                    tot_deffrental = to_decimal("0")
                    tot_diff = to_decimal("0")
                    tot_amount = to_decimal("0")
                    tot_rmrate = to_decimal("0")

                    output_list = Output_list()
                    output_list_data.append(output_list)

                output_list = Output_list()
                output_list_data.append(output_list)

                if curr_sort + 1 == 1:
                    output_list.roomtype = "Arrived & Invoice Already Printed"

                elif curr_sort + 1 == 2:
                    output_list.roomtype = "Arrived & Invoice not Printed Yet"

                elif curr_sort + 1 == 3:
                    output_list.roomtype = "Future Reservation & Invoice Printed"

                elif curr_sort + 1 == 4:
                    output_list.roomtype = "Future Reservation & Invoice not Printed Yet"

            output_list = Output_list()
            output_list_data.append(output_list)

            buffer_copy(output_list1, output_list)
            curr_sort = output_list1.type_flag
            tot_revenue = to_decimal(tot_revenue + output_list1.Revenue)
            tot_deffrental = to_decimal(tot_deffrental + output_list1.deffRental)
            tot_diff = to_decimal(tot_diff + output_list1.diff)
            tot_amount = to_decimal(tot_amount + output_list1.rental_amount)
            tot_rmrate = to_decimal(tot_rmrate + output_list1.rmRate)
            gtot_revenue = to_decimal(gtot_revenue + output_list1.Revenue)
            gtot_deffrental = to_decimal(gtot_deffrental + output_list1.deffRental)
            gtot_diff = to_decimal(gtot_diff + output_list1.diff)
            gtot_amount = to_decimal(gtot_amount + output_list1.rental_amount)
            gtot_rmrate = to_decimal(gtot_rmrate + output_list1.rmRate)

    else:
        for output_list1 in query(output_list1_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            buffer_copy(output_list1, output_list)

            if output_list1.diff < 10:
                output_list1.diff = to_decimal("0")

            tot_revenue = to_decimal(tot_revenue + output_list1.Revenue)
            tot_deffrental = to_decimal(tot_deffrental + output_list1.deffRental)
            tot_diff = to_decimal(tot_diff + output_list1.diff)
            tot_amount = to_decimal(tot_amount + output_list1.rental_amount)
            tot_rmrate = to_decimal(tot_rmrate + output_list1.rmRate)
            gtot_revenue = to_decimal(gtot_revenue + output_list1.Revenue)
            gtot_deffrental = to_decimal(gtot_deffrental + output_list1.deffRental)
            gtot_diff = to_decimal(gtot_diff + output_list1.diff)
            gtot_amount = to_decimal(gtot_amount + output_list1.rental_amount)
            gtot_rmrate = to_decimal(gtot_rmrate + output_list1.rmRate)

    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.roomtype = "T O T A L"
    output_list.revenue = to_decimal(tot_revenue)
    output_list.deffrental = to_decimal(tot_deffrental)
    output_list.diff = to_decimal(tot_diff)
    output_list.rental_amount = to_decimal(tot_amount)
    output_list.rmrate = to_decimal(tot_rmrate)

    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.roomtype = "Grand T O T A L"
    output_list.revenue = to_decimal(gtot_revenue)
    output_list.deffrental = to_decimal(gtot_deffrental)
    output_list.diff = to_decimal(gtot_diff)
    output_list.rental_amount = to_decimal(gtot_amount)
    output_list.rmrate = to_decimal(gtot_rmrate)

    return generate_output()
