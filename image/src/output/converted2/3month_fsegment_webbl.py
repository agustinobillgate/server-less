#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Segment, Res_line, Htparam, Zimmer, Genstat, Reservation, Arrangement, Bill_line, Queasy, Reslin_queasy, Zkstat, Zinrstat, Outorder

def 3month_fsegment_webbl(from_date:date):

    prepare_cache ([Segment, Res_line, Htparam, Genstat, Reservation, Arrangement, Queasy, Reslin_queasy, Zkstat, Zinrstat])

    output_list_list = []
    to_date:date = None
    fr_date:date = None
    last_tdate:date = None
    last_fdate:date = None
    long_digit:bool = False
    black_list:int = 0
    ci_date:date = None
    tot_rm:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    tot_arr:Decimal = to_decimal("0.0")
    tot_pax:int = 0
    tot_occpr:int = 0
    tot_doccpr:int = 0
    all_rm:int = 0
    act_rm:int = 0
    inactive:int = 0
    tot_room:int = 0
    trev1:List[Decimal] = create_empty_list(12,to_decimal("0"))
    trm1:List[Decimal] = create_empty_list(12,to_decimal("0"))
    loopi:int = 0
    monthnr:int = 0
    yearnr:int = 0
    mtd_act:int = 0
    mtd_totrm:int = 0
    do_it:bool = False
    segment = res_line = htparam = zimmer = genstat = reservation = arrangement = bill_line = queasy = reslin_queasy = zkstat = zinrstat = outorder = None

    output_list = boutput = segmtype_exist = rline = None

    output_list_list, Output_list = create_model("Output_list", {"segmentcode":int, "segment":string, "monthyear":date, "room":int, "revenue":Decimal, "avrg_rev":Decimal, "pax":int, "occpr":Decimal, "doccpr":Decimal})

    Boutput = Output_list
    boutput_list = output_list_list

    Segmtype_exist = create_buffer("Segmtype_exist",Segment)
    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, to_date, fr_date, last_tdate, last_fdate, long_digit, black_list, ci_date, tot_rm, tot_rev, tot_arr, tot_pax, tot_occpr, tot_doccpr, all_rm, act_rm, inactive, tot_room, trev1, trm1, loopi, monthnr, yearnr, mtd_act, mtd_totrm, do_it, segment, res_line, htparam, zimmer, genstat, reservation, arrangement, bill_line, queasy, reslin_queasy, zkstat, zinrstat, outorder
        nonlocal from_date
        nonlocal boutput, segmtype_exist, rline


        nonlocal output_list, boutput, segmtype_exist, rline
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, to_date, fr_date, last_tdate, last_fdate, long_digit, black_list, ci_date, tot_rm, tot_rev, tot_arr, tot_pax, tot_occpr, tot_doccpr, all_rm, act_rm, inactive, tot_room, trev1, trm1, loopi, monthnr, yearnr, mtd_act, mtd_totrm, do_it, segment, res_line, htparam, zimmer, genstat, reservation, arrangement, bill_line, queasy, reslin_queasy, zkstat, zinrstat, outorder
        nonlocal from_date
        nonlocal boutput, segmtype_exist, rline


        nonlocal output_list, boutput, segmtype_exist, rline
        nonlocal output_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        tdate:date = None
        fdate:date = None
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        pax:int = 0
        consider_it:bool = False
        dayuse_flag:bool = False

        if to_date < (ci_date - timedelta(days=1)):
            tdate = to_date
        else:
            tdate = ci_date - timedelta(days=1)

        for genstat in db_session.query(Genstat).filter(
                 (((Genstat.datum >= fr_date) & (Genstat.datum <= tdate)) | ((Genstat.datum >= date_mdy(get_month(fr_date) , get_day(fr_date) , get_year(fr_date) - 1)) & (Genstat.datum <= (date_mdy(get_month(to_date) + 1, 1, get_year(to_date) - 1) - 1)))) & (Genstat.segmentcode != 0) & (Genstat.segmentcode != black_list) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13) & (not_ (Genstat.res_date[inc_value(0)] < Genstat.datum) & (Genstat.res_date[inc_value(1)] == Genstat.datum) & (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

            output_list = query(output_list_list, filters=(lambda output_list: output_list.segmentcode == genstat.segmentcode and output_list.monthyear == date_mdy(get_month(genstat.datum) , 1, get_year(genstat.datum))), first=True)

            if not output_list:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.segmentcode = genstat.segmentcode
                    output_list.segment = segment.bezeich
                    output_list.monthyear = date_mdy(get_month(genstat.datum) , 1, get_year(genstat.datum))


            output_list.room = output_list.room + 1
            output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(genstat.logis)
            output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)
            output_list.pax = output_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                do_it = True
                dayuse_flag = False

                if do_it and res_line.resstatus == 8:
                    dayuse_flag = True

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                    do_it = None != bill_line

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if do_it and zimmer:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode),(ne, black_list)]})

                if segment and do_it:

                    if res_line.ankunft >= ci_date:
                        datum1 = res_line.ankunft
                    else:
                        datum1 = ci_date

                    if res_line.abreise <= to_date:
                        datum2 = res_line.abreise - timedelta(days=1)
                    else:
                        datum2 = to_date
                    for datum in date_range(datum1,datum2) :
                        net_lodg =  to_decimal("0")
                        curr_i = curr_i + 1

                        if datum == res_line.abreise:
                            pass
                        else:
                            net_lodg =  to_decimal("0")
                            tot_breakfast =  to_decimal("0")
                            tot_lunch =  to_decimal("0")
                            tot_dinner =  to_decimal("0")
                            tot_other =  to_decimal("0")
                            tot_rmrev =  to_decimal("0")
                            tot_vat =  to_decimal("0")
                            tot_service =  to_decimal("0")
                            pax = res_line.erwachs

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                            if reslin_queasy and reslin_queasy.number3 != 0:
                                pax = reslin_queasy.number3
                            consider_it = True

                            if res_line.zimmerfix:

                                rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                                if rline:
                                    consider_it = False
                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, fr_date))

                            if tot_rmrev == 0:
                                net_lodg =  to_decimal("0")
                                fnet_lodg =  to_decimal("0")
                                tot_breakfast =  to_decimal("0")
                                tot_lunch =  to_decimal("0")
                                tot_dinner =  to_decimal("0")
                                tot_other =  to_decimal("0")

                            output_list = query(output_list_list, filters=(lambda output_list: output_list.segmentcode == reservation.segmentcode and output_list.monthyear == date_mdy(get_month(datum) , 1, get_year(datum))), first=True)

                            if not output_list:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.segmentcode = reservation.segmentcode
                                output_list.segment = segment.bezeich
                                output_list.monthyear = date_mdy(get_month(datum) , 1, get_year(datum))

                            if datum == res_line.ankunft and consider_it:

                                if res_line.ankunft < res_line.abreise or dayuse_flag:

                                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                        output_list.room = output_list.room + res_line.zimmeranz
                                        output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)
                                        output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)

                                    if res_line.resstatus != 11 and res_line.resstatus != 13:
                                        output_list.pax = output_list.pax + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                            if res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != datum and res_line.abreise != datum):

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    output_list.room = output_list.room + res_line.zimmeranz
                                    output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)
                                    output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)

                                if res_line.resstatus != 11 and res_line.resstatus != 13:
                                    output_list.pax = output_list.pax + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz


    def count_mtd_totrm(in_date:date):

        nonlocal output_list_list, to_date, fr_date, last_tdate, last_fdate, long_digit, black_list, ci_date, tot_rm, tot_rev, tot_arr, tot_pax, tot_occpr, tot_doccpr, all_rm, act_rm, inactive, tot_room, trev1, trm1, loopi, monthnr, yearnr, mtd_act, mtd_totrm, do_it, segment, res_line, htparam, zimmer, genstat, reservation, arrangement, bill_line, queasy, reslin_queasy, zkstat, zinrstat, outorder
        nonlocal from_date
        nonlocal boutput, segmtype_exist, rline


        nonlocal output_list, boutput, segmtype_exist, rline
        nonlocal output_list_list

        datum:date = None
        ldatum:date = None
        ooo:int = 0
        mtd_totrm = 0 mtd_act == 0 all_rm == 0

        if get_month(in_date) == 12:
            datum = date_mdy(1, 1, get_year(in_date) + timedelta(days=1) - 1)
        else:
            datum = date_mdy(get_month(in_date) + timedelta(days=1, 1, get_year(in_date)) - 1)

        if (get_month(in_date) < get_month(ci_date) and get_year(in_date) == get_year(ci_date)) or (get_year(in_date) < get_year(ci_date)):

            for zkstat in db_session.query(Zkstat).filter(
                     (get_month(Zkstat.datum) == get_month(in_date)) & (get_year(Zkstat.datum) == get_year(in_date))).order_by(Zkstat._recid).all():
                all_rm = all_rm + zkstat.anz100

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("tot-rm").lower()) & (get_month(Zinrstat.datum) == get_month(in_date)) & (get_year(Zinrstat.datum) == get_year(in_date))).order_by(Zinrstat._recid).all():
                mtd_totrm = mtd_totrm + zinrstat.zimmeranz

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ooo").lower()) & (get_month(Zinrstat.datum) == get_month(in_date)) & (get_year(Zinrstat.datum) == get_year(in_date))).order_by(Zinrstat._recid).all():
                ooo = ooo + zinrstat.zimmeranz

        elif get_month(in_date) == get_month(ci_date) and get_year(in_date) == get_year(ci_date):

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= in_date) & (Zkstat.datum <= ci_date)).order_by(Zkstat._recid).all():
                all_rm = all_rm + zkstat.anz100

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("tot-rm").lower()) & (Zinrstat.datum >= in_date) & (Zinrstat.datum <= ci_date)).order_by(Zinrstat._recid).all():
                mtd_totrm = mtd_totrm + zinrstat.zimmeranz

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ooo").lower()) & (Zinrstat.datum >= in_date) & (Zinrstat.datum <= ci_date)).order_by(Zinrstat._recid).all():
                ooo = ooo + zinrstat.zimmeranz
            all_rm = all_rm + (act_rm * (datum - ci_date))
            mtd_totrm = mtd_totrm + (tot_room * (datum - ci_date))
            for ldatum in date_range(ci_date + 1,datum) :

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= ldatum) & (Outorder.gespende >= ldatum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    ooo = ooo + 1
        else:
            all_rm = act_rm * (datum - in_date + 1)
            mtd_totrm = mtd_totrm + (tot_room * (datum - in_date + 1))
            for ldatum in date_range(in_date,datum) :

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= ldatum) & (Outorder.gespende >= ldatum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    ooo = ooo + 1
        mtd_act = all_rm - ooo


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
    black_list = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        act_rm = act_rm + 1

    for zimmer in db_session.query(Zimmer).filter(
             not_ (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        inactive = inactive + 1
    tot_room = act_rm + inactive
    fr_date = date_mdy(get_month(from_date) , 1, get_year(from_date))

    if get_month(fr_date) >= 10:
        to_date = date_mdy(3 - (12 - get_month(from_date)) , 1, get_year(from_date) + timedelta(days=1) - 1)
    else:
        to_date = date_mdy(get_month(from_date) + timedelta(days=3, 1, get_year(from_date)) - 1)

    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr == 0) & (Segment.segmentcode != black_list)).order_by(Segment.segmentcode).all():
        for loopi in range(get_month(fr_date),get_month(fr_date) + 2 + 1) :

            if loopi > 12:
                monthnr = loopi - 12
                yearnr = 1


            else:
                monthnr = loopi
                yearnr = 0


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.segmentcode = segment.segmentcode
            output_list.segment = entry(0, segment.bezeich, "$$0")
            output_list.monthyear = date_mdy(monthnr, 1, get_year(from_date) + timedelta(days=yearnr))


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.segmentcode = segment.segmentcode
            output_list.segment = entry(0, segment.bezeich, "$$0")
            output_list.monthyear = date_mdy(monthnr, 1, get_year(from_date) + timedelta(days=yearnr - 1))


    create_list()
    tot_rm = 0
    tot_rev =  to_decimal("0")
    tot_arr =  to_decimal("0")
    tot_pax = 0
    tot_occpr = 0
    tot_doccpr = 0
    for loopi in range(get_month(fr_date),get_month(fr_date) + 2 + 1) :

        if loopi > 12:
            monthnr = loopi - 12
            yearnr = 1


        else:
            monthnr = loopi
            yearnr = 0


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.segmentcode = 99999
        output_list.segment = "T O T A L"
        output_list.monthyear = date_mdy(monthnr, 1, get_year(from_date) + timedelta(days=yearnr))


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.segmentcode = 99999
        output_list.segment = "T O T A L"
        output_list.monthyear = date_mdy(monthnr, 1, get_year(from_date) + timedelta(days=yearnr - 1))

    for output_list in query(output_list_list, sort_by=[("segmentcode",False)]):
        count_mtd_totrm(output_list.monthyear)

        if output_list.segmentcode != 99999:

            if output_list.room == 0:
                continue
            output_list.occpr =  to_decimal(output_list.room) / to_decimal(mtd_act) * to_decimal("100")
            output_list.doccpr = ( to_decimal(output_list.pax) - to_decimal(output_list.room)) / to_decimal(output_list.room) * to_decimal("100")

            boutput = query(boutput_list, filters=(lambda boutput: boutput.segmentcode == 99999 and boutput.monthyear == output_list.monthyear), first=True)

            if boutput:
                boutput.room = boutput.room + output_list.room
                boutput.revenue =  to_decimal(boutput.revenue) + to_decimal(output_list.revenue)
                boutput.pax = boutput.pax + output_list.pax


        else:

            if output_list.room == 0:
                continue
            output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)
            output_list.occpr =  to_decimal(output_list.room) / to_decimal(mtd_act) * to_decimal("100")
            output_list.doccpr = ( to_decimal(output_list.pax) - to_decimal(output_list.room)) / to_decimal(output_list.room) * to_decimal("100")

            if output_list.avrg_rev == None:
                output_list.avrg_rev =  to_decimal(0.00)

    return generate_output()