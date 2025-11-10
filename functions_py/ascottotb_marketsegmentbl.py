# using conversion tools version: 1.0.0.119
"""_yusufwijasena_07/11/2025

    Ticket ID: 5C46F2
        _remark_:   - update from ITA: BFC578
                    - fix python indentation
                    - add import from function_py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
# from functions.htpint import htpint
# from functions.get_room_breakdown import get_room_breakdown
from functions_py.htpint import htpint
from functions_py.get_room_breakdown import get_room_breakdown
from models import Segment, Segmentstat, Res_line, Htparam, Zimmer, Genstat, Zinrstat, Waehrung, Reservation, Reslin_queasy, Arrangement, Bill_line

otb_list_data, Otb_list = create_model(
    "Otb_list",
    {
        "hcode": string,
        "datum": date,
        "segment": string,
        "rm_sold": int,
        "rm_rev": Decimal,
        "budget_rm": int,
        "budget_rev": Decimal,
        "ttlfixedroom": int,
        "fbrev": Decimal,
        "arrivalcount": int,
        "departcount": int,
        "noshowcount": int,
        "grouprmcount": int,
        "notgroupcount": int,
        "adultcount": int,
        "childcount": int,
        "datatype": string,
        "recordcount": int,
        "total_rev": Decimal,
        "rm_transient": int
    })


def ascottotb_marketsegmentbl(hotel_code: string, fdate: date, tdate: date, otb_list_data: Otb_list):

    prepare_cache([Res_line, Htparam, Genstat, Zinrstat, Reservation, Reslin_queasy, Arrangement])

    otb_count = 0
    w_int: int = 0
    indv: int = 0
    cnt: int = 0
    rm_rev = to_decimal("0.0")
    ttl_rm_rev = to_decimal("0.0")
    ttl_rm_sold: int = 0
    cdate: date = None
    ci_date: date = None
    fnet_lodging = to_decimal("0.0")
    lnet_lodging = to_decimal("0.0")
    net_breakfast = to_decimal("0.0")
    net_lunch = to_decimal("0.0")
    net_dinner = to_decimal("0.0")
    net_others = to_decimal("0.0")
    tot_rmrev = to_decimal("0.0")
    nett_vat = to_decimal("0.0")
    nett_service = to_decimal("0.0")
    icount: int = 0
    price_decimal: int = 0
    curr_segment: int = 0
    zimm: int = 0
    pax: int = 0
    do_it: bool = False
    dayuse_flag: bool = False
    consider_it: bool = False
    segment = segmentstat = res_line = htparam = zimmer = genstat = zinrstat = waehrung = reservation = reslin_queasy = arrangement = bill_line = None
    otb_list = t_segment = t_segmentstat = bsegment = rline1 = botb = None

    t_segment_data, T_segment = create_model_like(Segment)
    t_segmentstat_data, T_segmentstat = create_model_like(Segmentstat)

    Bsegment = T_segment
    bsegment_data = t_segment_data

    Rline1 = create_buffer("Rline1", Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal otb_count, w_int, indv, cnt, rm_rev, ttl_rm_rev, ttl_rm_sold, cdate, ci_date, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, icount, price_decimal, curr_segment, zimm, pax, do_it, dayuse_flag, consider_it, segment, segmentstat, res_line, htparam, zimmer, genstat, zinrstat, waehrung, reservation, reslin_queasy, arrangement, bill_line
        nonlocal hotel_code, fdate, tdate
        nonlocal bsegment, rline1
        nonlocal otb_list, t_segment, t_segmentstat, bsegment, rline1, botb
        nonlocal t_segment_data, t_segmentstat_data

        return {
            "otb_count": otb_count,
            "otb-list": otb_list_data
        }

    def create_list():
        nonlocal otb_count, w_int, indv, cnt, rm_rev, ttl_rm_rev, ttl_rm_sold, cdate, ci_date, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, icount, price_decimal, curr_segment, zimm, pax, do_it, dayuse_flag, consider_it, segment, segmentstat, res_line, htparam, zimmer, genstat, zinrstat, waehrung, reservation, reslin_queasy, arrangement, bill_line
        nonlocal hotel_code, fdate, tdate
        nonlocal bsegment, rline1
        nonlocal otb_list, t_segment, t_segmentstat, bsegment, rline1, botb
        nonlocal t_segment_data, t_segmentstat_data

        start_date: date = None
        end_date: date = None
        datum1: date = None
        datum2: date = None
        curr_i: int = 0
        Botb = Otb_list
        botb_data = otb_list_data
        start_date = fdate

        if tdate < ci_date:
            end_date = tdate

        else:
            end_date = ci_date - timedelta(days=1)

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= start_date) & 
                (Genstat.datum <= end_date) & 
                (Genstat.resstatus != 13) & 
                (Genstat.res_logic[inc_value(1)]) & 
                (Genstat.segmentcode != 0) & 
                (Genstat.nationnr != 0) & 
                (Genstat.zinr != "")).order_by(Genstat.segmentcode).all():

            t_segment = query(t_segment_data, filters=(
                lambda t_segment: t_segment.segmentcode == genstat.segmentcode), first=True)

            if t_segment:
                otb_list = query(otb_list_data, filters=(lambda otb_list: otb_list.datum == genstat.datum and otb_list.segment == t_segment.bezeich), first=True)

                if not otb_list:
                    icount = icount + 1
                    otb_list = Otb_list()
                    otb_list_data.append(otb_list)

                    otb_list.hcode = hotel_code
                    otb_list.datatype = "actual"
                    otb_list.datum = genstat.datum
                    otb_list.segment = t_segment.bezeich
                    otb_list.ttlfixedroom = zimm
                    otb_list.noshowcount = 0
                    otb_list.recordcount = icount

                    t_segmentstat = query(t_segmentstat_data, filters=(lambda t_segmentstat: t_segmentstat.datum == genstat.datum and t_segmentstat.segmentcode == t_segment.segmentcode), first=True)

                    if t_segmentstat:
                        otb_list.budget_rev = to_decimal(
                            otb_list.budget_rev + round(t_segmentstat.budlogis, price_decimal))
                        otb_list.budget_rm = otb_list.budget_rm + t_segmentstat.budzimmeranz

                if genstat.res_date[0] == genstat.datum:
                    otb_list.arrivalcount = otb_list.arrivalcount + 1

                if genstat.res_char[2] != "":
                    otb_list.grouprmcount = otb_list.grouprmcount + 1
                else:
                    otb_list.notgroupcount = otb_list.notgroupcount + 1
                otb_list.rm_sold = otb_list.rm_sold + 1
                otb_list.rm_rev = to_decimal(
                    otb_list.rm_rev + round(genstat.logis, price_decimal))
                ttl_rm_sold = ttl_rm_sold + 1
                ttl_rm_rev = to_decimal(
                    ttl_rm_rev + round(genstat.logis, price_decimal))
                otb_list.fbrev = to_decimal(otb_list.fbrev + round(
                    genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3], price_decimal))
                otb_list.adultcount = otb_list.adultcount + genstat.erwachs + genstat.gratis
                otb_list.childcount = otb_list.childcount + \
                    genstat.kind1 + genstat.kind2 + genstat.kind3
                otb_list.total_rev = to_decimal(otb_list.total_rev + round(genstat.logis, price_decimal) + round(
                    genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3], price_decimal))

                zinrstat = get_cache(
                    Zinrstat, {"zinr": [(eq, "departure")], "datum": [(eq, genstat.datum)]})

                if zinrstat:
                    for otb_list in query(otb_list_data, filters=(lambda otb_list: otb_list.datum == zinrstat.datum)):
                        otb_list.departcount = zinrstat.zimmeranz
        start_date = end_date + timedelta(days=1)
        end_date = tdate

        if tdate >= ci_date:
            res_line_obj_list = {}
            for res_line, waehrung, reservation in db_session.query(Res_line, Waehrung, Reservation).join(Waehrung, (Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation, (Reservation.resnr == Res_line.resnr)).filter(
                    ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.resstatus != 3) & (not_(Res_line.ankunft > end_date)) & (not_(Res_line.abreise < start_date))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.segmentcode).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                t_segment = query(t_segment_data, filters=(
                    lambda t_segment: t_segment.segmentcode == reservation.segmentcode), first=True)

                if t_segment:
                    datum1 = start_date

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = tdate

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for cdate in date_range(datum1, datum2):
                        curr_i = 1
                        lnet_lodging = to_decimal("0")

                        otb_list = query(otb_list_data, filters=(
                            lambda otb_list: otb_list.datum == cdate and otb_list.segment == t_segment.bezeich), first=True)

                        if not otb_list:
                            icount = icount + 1
                            otb_list = Otb_list()
                            otb_list_data.append(otb_list)

                            otb_list.hcode = hotel_code
                            otb_list.datatype = "forecast"
                            otb_list.datum = cdate
                            otb_list.segment = t_segment.bezeich
                            otb_list.noshowcount = 0
                            otb_list.ttlfixedroom = zimm
                            otb_list.recordcount = icount

                        # if cdate == res_line.abreise:
                        #     pass
                        # else:
                        if cdate != res_line.abreise:
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                                get_room_breakdown(res_line._recid, cdate, curr_i, fdate))
                            otb_list.rm_sold = otb_list.rm_sold + res_line.zimmeranz
                            otb_list.rm_rev = to_decimal(
                                otb_list.rm_rev + round(lnet_lodging, price_decimal))
                            ttl_rm_sold = ttl_rm_sold + res_line.zimmeranz
                            ttl_rm_rev = to_decimal(
                                ttl_rm_rev + round(lnet_lodging, price_decimal))

                            if reservation.groupname != "":
                                otb_list.grouprmcount = otb_list.grouprmcount + 1
                            else:
                                otb_list.notgroupcount = otb_list.notgroupcount + 1

                            t_segmentstat = query(t_segmentstat_data, filters=(
                                lambda t_segmentstat: t_segmentstat.datum == cdate and t_segmentstat.segmentcode == bsegment.segmentcode), first=True)

                            if t_segmentstat:
                                otb_list.budget_rev = to_decimal(
                                    otb_list.budget_rev + round(t_segmentstat.budlogis, price_decimal))
                                otb_list.budget_rm = otb_list.budget_rm + t_segmentstat.budzimmeranz

                        if cdate == ci_date:
                            if res_line.active_flag == 1:
                                fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                                    get_room_breakdown(res_line._recid, cdate, 1, fdate))
                                otb_list.fbrev = to_decimal(
                                    otb_list.fbrev + round(net_breakfast + net_lunch + net_dinner, price_decimal))
                        else:
                            # if cdate == res_line.abreise:
                            #     pass
                            # else:
                            if cdate != res_line.abreise:
                                fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                                    get_room_breakdown(res_line._recid, cdate, 1, fdate))
                                otb_list.fbrev = to_decimal(
                                    otb_list.fbrev + round(net_breakfast + net_lunch + net_dinner, price_decimal))
                        otb_list.total_rev = to_decimal(otb_list.total_rev + round(
                            lnet_lodging, price_decimal) + round(net_breakfast + net_lunch + net_dinner, price_decimal))

                        pax = res_line.erwachs

                        reslin_queasy = get_cache(
                            Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                            eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, cdate)], "date2": [(ge, cdate)]})

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                        do_it = True

                        if do_it and res_line.resstatus == 8:
                            dayuse_flag = True

                            arrangement = get_cache(
                                Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                            bill_line = get_cache(
                                Bill_line, {"departement": [(eq, 0)], "artnr": [(eq, arrangement.argt_artikelnr)], "bill_datum": [(eq, ci_date)], "massnr": [(eq, res_line.resnr)], "billin_nr": [(eq, res_line.reslinnr)]})
                            # do_it = None != bill_line
                            do_it = bill_line is not None
                        consider_it = True

                        if res_line.zimmerfix:
                            rline1 = get_cache(
                                Res_line, {"resnr": [(eq, res_line.resnr)], "reslinnr": [(ne, res_line.reslinnr)], "resstatus": [(eq, 8)], "abreise": [(gt, cdate)]})

                            if rline1:
                                consider_it = False

                        if cdate == res_line.ankunft and consider_it and res_line.resstatus != 3:
                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                otb_list.arrivalcount = otb_list.arrivalcount + res_line.zimmeranz

                            if res_line.ankunft < res_line.abreise or dayuse_flag:
                                if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                    otb_list.adultcount = otb_list.adultcount + \
                                        (pax + res_line.gratis) * \
                                        res_line.zimmeranz
                                    otb_list.childcount = otb_list.childcount + \
                                        (res_line.kind1 + res_line.kind2 +
                                         res_line.l_zuordnung[3]) * res_line.zimmeranz

                        if cdate == res_line.abreise and res_line.resstatus != 3 and consider_it:
                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                otb_list.departcount = otb_list.departcount + res_line.zimmeranz

                        if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != cdate and res_line.abreise != cdate):
                            if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                otb_list.adultcount = otb_list.adultcount + \
                                    (pax + res_line.gratis) * res_line.zimmeranz
                                otb_list.childcount = otb_list.childcount + \
                                    (res_line.kind1 + res_line.kind2 +
                                     res_line.l_zuordnung[3]) * res_line.zimmeranz

        for t_segment in query(t_segment_data):
            for cdate in date_range(fdate, tdate):
                otb_list = query(otb_list_data, filters=(
                    lambda otb_list: otb_list.segment == t_segment.bezeich and otb_list.datum == cdate), first=True)

                if not otb_list:
                    icount = icount + 1
                    otb_list = Otb_list()
                    otb_list_data.append(otb_list)

                    otb_list.hcode = hotel_code
                    otb_list.datum = cdate
                    otb_list.segment = t_segment.bezeich
                    otb_list.rm_sold = 0
                    otb_list.rm_rev = to_decimal("0")
                    otb_list.noshowcount = 0
                    otb_list.ttlfixedroom = zimm
                    otb_list.recordcount = icount

                    if cdate >= ci_date:
                        otb_list.datatype = "forecast"
                    else:
                        otb_list.datatype = "actual"

                    t_segmentstat = query(t_segmentstat_data, filters=(
                        lambda t_segmentstat: t_segmentstat.segmentcode == t_segment.segmentcode and t_segmentstat.datum == cdate), first=True)

                    if t_segmentstat:
                        otb_list.budget_rev = to_decimal(
                            round(t_segmentstat.budlogis, price_decimal))
                        otb_list.budget_rm = t_segmentstat.budzimmeranz

    def create_list1():
        nonlocal otb_count, w_int, indv, cnt, rm_rev, ttl_rm_rev, ttl_rm_sold, cdate, ci_date, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, icount, price_decimal, curr_segment, zimm, pax, do_it, dayuse_flag, consider_it, segment, segmentstat, res_line, htparam, zimmer, genstat, zinrstat, waehrung, reservation, reslin_queasy, arrangement, bill_line
        nonlocal hotel_code, fdate, tdate
        nonlocal bsegment, rline1
        nonlocal otb_list, t_segment, t_segmentstat, bsegment, rline1, botb
        nonlocal t_segment_data, t_segmentstat_data

        datum1: date = None
        datum2: date = None
        curr_i: int = 0

        res_line_obj_list = {}
        for res_line, waehrung, reservation in db_session.query(Res_line, Waehrung, Reservation).join(Waehrung, (Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation, (Reservation.resnr == Res_line.resnr)).filter(
                ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.resstatus != 3) & (not_(Res_line.ankunft > tdate)) & (not_(Res_line.abreise < fdate))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.segmentcode).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            t_segment = query(t_segment_data, filters=(
                lambda t_segment: t_segment.segmentcode == reservation.segmentcode), first=True)

            if t_segment:
                datum1 = fdate

                if res_line.ankunft > datum1:
                    datum1 = res_line.ankunft
                datum2 = tdate

                if res_line.abreise < datum2:
                    datum2 = res_line.abreise
                for cdate in date_range(datum1, datum2):
                    curr_i = 1
                    lnet_lodging = to_decimal("0")

                    otb_list = query(otb_list_data, filters=(
                        lambda otb_list: otb_list.datum == cdate and otb_list.segment == t_segment.bezeich), first=True)

                    if not otb_list:
                        icount = icount + 1
                        otb_list = Otb_list()
                        otb_list_data.append(otb_list)

                        otb_list.hcode = hotel_code
                        otb_list.datatype = "forecast"
                        otb_list.datum = cdate
                        otb_list.segment = t_segment.bezeich
                        otb_list.noshowcount = 0
                        otb_list.ttlfixedroom = zimm
                        otb_list.recordcount = icount

                    # if cdate == res_line.abreise:
                    #     pass
                    # else:
                    if cdate != res_line.abreise:
                        fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                            get_room_breakdown(res_line._recid, cdate, curr_i, fdate))
                        otb_list.rm_sold = otb_list.rm_sold + res_line.zimmeranz
                        otb_list.rm_rev = to_decimal(
                            otb_list.rm_rev + round(lnet_lodging, price_decimal))
                        ttl_rm_sold = ttl_rm_sold + res_line.zimmeranz
                        ttl_rm_rev = to_decimal(
                            ttl_rm_rev + round(lnet_lodging, price_decimal))

                        if reservation.groupname != "":
                            otb_list.grouprmcount = otb_list.grouprmcount + 1
                        else:
                            otb_list.notgroupcount = otb_list.notgroupcount + 1

                        t_segmentstat = query(t_segmentstat_data, filters=(
                            lambda t_segmentstat: t_segmentstat.datum == cdate and t_segmentstat.segmentcode == bsegment.segmentcode), first=True)

                        if t_segmentstat:
                            otb_list.budget_rev = to_decimal(
                                otb_list.budget_rev + round(t_segmentstat.budlogis, price_decimal))
                            otb_list.budget_rm = otb_list.budget_rm + t_segmentstat.budzimmeranz

                    if cdate == ci_date:
                        if res_line.active_flag == 1:
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                                get_room_breakdown(res_line._recid, cdate, 1, fdate))
                            otb_list.fbrev = to_decimal(
                                otb_list.fbrev + round(net_breakfast + net_lunch + net_dinner, price_decimal))
                    else:
                        # if cdate == res_line.abreise:
                        #     pass
                        # else:
                        if cdate != res_line.abreise:
                            fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service = get_output(
                                get_room_breakdown(res_line._recid, cdate, 1, fdate))
                            otb_list.fbrev = to_decimal(
                                otb_list.fbrev + round(net_breakfast + net_lunch + net_dinner, price_decimal))
                    otb_list.total_rev = to_decimal(otb_list.total_rev + round(
                        lnet_lodging, price_decimal) + round(net_breakfast + net_lunch + net_dinner, price_decimal))

                    pax = res_line.erwachs

                    reslin_queasy = get_cache(
                        Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, cdate)], "date2": [(ge, cdate)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    do_it = True

                    if do_it and res_line.resstatus == 8:
                        dayuse_flag = True

                        arrangement = get_cache(
                            Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                        bill_line = get_cache(
                            Bill_line, {"departement": [(eq, 0)], "artnr": [(eq, arrangement.argt_artikelnr)], "bill_datum": [(eq, ci_date)], "massnr": [(eq, res_line.resnr)], "billin_nr": [(eq, res_line.reslinnr)]})
                        # do_it = None != bill_line
                        do_it = bill_line is not None
                    consider_it = True

                    if res_line.zimmerfix:
                        rline1 = get_cache(Res_line, {"resnr": [(eq, res_line.resnr)], "reslinnr": [(ne, res_line.reslinnr)], "resstatus": [(eq, 8)], "abreise": [(gt, cdate)]})

                        if rline1:
                            consider_it = False

                    if cdate == res_line.ankunft and consider_it and res_line.resstatus != 3:
                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            otb_list.arrivalcount = otb_list.arrivalcount + res_line.zimmeranz

                        if res_line.ankunft < res_line.abreise or dayuse_flag:
                            if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                otb_list.adultcount = otb_list.adultcount + \
                                    (pax + res_line.gratis) * res_line.zimmeranz
                                otb_list.childcount = otb_list.childcount + \
                                    (res_line.kind1 + res_line.kind2 +
                                     res_line.l_zuordnung[3]) * res_line.zimmeranz

                    if cdate == res_line.abreise and res_line.resstatus != 3 and consider_it:
                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            otb_list.departcount = otb_list.departcount + res_line.zimmeranz

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != cdate and res_line.abreise != cdate):
                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                            otb_list.adultcount = otb_list.adultcount + \
                                (pax + res_line.gratis) * res_line.zimmeranz
                            otb_list.childcount = otb_list.childcount + \
                                (res_line.kind1 + res_line.kind2 +
                                 res_line.l_zuordnung[3]) * res_line.zimmeranz

        for t_segment in query(t_segment_data):
            for cdate in date_range(fdate, tdate):
                otb_list = query(otb_list_data, filters=(
                    lambda otb_list: otb_list.segment == t_segment.bezeich and otb_list.datum == cdate), first=True)

                if not otb_list:
                    icount = icount + 1
                    otb_list = Otb_list()
                    otb_list_data.append(otb_list)

                    otb_list.hcode = hotel_code
                    otb_list.datum = cdate
                    otb_list.segment = t_segment.bezeich
                    otb_list.rm_sold = 0
                    otb_list.rm_rev = to_decimal("0")
                    otb_list.noshowcount = 0
                    otb_list.ttlfixedroom = zimm
                    otb_list.recordcount = icount

                    if cdate >= ci_date:
                        otb_list.datatype = "forecast"
                    else:
                        otb_list.datatype = "actual"

                    t_segmentstat = query(t_segmentstat_data, filters=(
                        lambda t_segmentstat: t_segmentstat.segmentcode == t_segment.segmentcode and t_segmentstat.datum == cdate), first=True)

                    if t_segmentstat:
                        otb_list.budget_rev = to_decimal(
                            round(t_segmentstat.budlogis, price_decimal))
                        otb_list.budget_rm = t_segmentstat.budzimmeranz

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 109)]})

    if htparam:
        w_int = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 123)]})

    if htparam:
        indv = htparam.finteger

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate
    price_decimal = get_output(htpint(491))
    otb_list_data.clear()

    for zimmer in db_session.query(Zimmer).filter(
            (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        zimm = zimm + 1

    for segment in db_session.query(Segment).filter(
            (not_(matches(Segment.bezeich, ("*$$0"))))).order_by(Segment._recid).all():
        t_segment = T_segment()
        t_segment_data.append(t_segment)

        buffer_copy(segment, t_segment)

    for segmentstat in db_session.query(Segmentstat).filter(
            (Segmentstat.datum >= fdate) & (Segmentstat.datum <= tdate)).order_by(Segmentstat._recid).all():
        t_segmentstat = T_segmentstat()
        t_segmentstat_data.append(t_segmentstat)

        buffer_copy(segmentstat, t_segmentstat)

    if fdate < ci_date:
        create_list()
    else:
        create_list1()
    otb_count = icount

    return generate_output()
