#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 18/7/25
# gitlab #977
# bad gateway/lama
#-----------------------------------------


from functions.additional_functions import *
from decimal import Decimal, InvalidOperation
from datetime import date
from sqlalchemy import or_, and_, not_
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Zimkateg, Genstat, Res_line, Reservation, Arrangement, Bill_line, Zimmer, Queasy

def safe_divide(numerator, denominator):
    numerator, denominator = to_decimal(numerator), to_decimal(denominator)
    return (numerator / denominator * to_decimal("100")) if denominator != 0 else to_decimal("0")


def rm_fbyroomtype_btn_go_1bl(sum_month:bool, fr_date:date, to_date:date, to_year:int, ex_tent:bool, ex_comp:bool):

    prepare_cache ([Htparam, Zimkateg, Genstat, Res_line, Arrangement, Queasy])

    output_list_data = []
    output_list1_data = []
    black_list:int = 0
    counter:int = 0
    ci_date:date = None
    curr_date:date = None
    tot_rm:Decimal = to_decimal("0.0")
    trm:Decimal = to_decimal("0.0")
    tot_rev:Decimal = to_decimal("0.0")
    trev:Decimal = to_decimal("0.0")
    trev1:List[Decimal] = create_empty_list(12,to_decimal("0"))
    trm1:List[Decimal] = create_empty_list(12,to_decimal("0"))
    loopi:int = 0
    htparam = zimkateg = genstat = res_line = reservation = arrangement = bill_line = zimmer = queasy = None

    output_list = output_list1 = boutput = boutput1 = None

    output_list_data, Output_list = create_model("Output_list", {"counter":int, "datum":date, "str_datum":string, "room":int, "revenue":Decimal, "avrg_rev":Decimal, "str_room":string, "str_revenue":string, "str_avrg":string, "zikatnr":int, "roomtype":string})
    output_list1_data, Output_list1 = create_model("Output_list1", {"counter":int, "zikatnr":int, "roomtype":string, "room":[int,12], "revenue":[Decimal,12], "avrg_rev":[Decimal,12]})

    Boutput = Output_list
    boutput_data = output_list_data

    Boutput1 = Output_list1
    boutput1_data = output_list1_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, output_list1_data, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, zimkateg, genstat, res_line, reservation, arrangement, bill_line, zimmer, queasy
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_data, output_list1_data

        return {"output-list": output_list_data, "output-list1": output_list1_data}

    def create_browse():

        nonlocal output_list_data, output_list1_data, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, zimkateg, genstat, res_line, reservation, arrangement, bill_line, zimmer, queasy
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_data, output_list1_data

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
        do_it:bool = False

        if to_date < (ci_date - timedelta(days=1)):
            tdate = to_date
        else:
            tdate = ci_date - timedelta(days=1)

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        for genstat.resstatus, genstat.zikatnr, genstat.datum, genstat.logis, genstat._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Genstat.resstatus, Genstat.zikatnr, Genstat.datum, Genstat.logis, Genstat._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                 (Genstat.datum >= fr_date) & (Genstat.datum <= tdate) & (Genstat.zikatnr != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat.zikatnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.resstatus != 11 and genstat.resstatus != 13:

                output_list = query(output_list_data, filters=(lambda output_list: output_list.zikatnr == genstat.zikatnr and output_list.datum == genstat.datum), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.zikatnr = genstat.zikatnr
                    output_list.datum = genstat.datum
                    output_list.roomtype = zimkateg.kurzbez


                output_list.room = output_list.room + 1
                output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(genstat.logis)


        htparam.fdate = tdate + timedelta(days=1)

        if to_date >= ci_date:

            recs = db_session.query(Res_line).filter(
                    (
                        (
                            (Res_line.resstatus <= 13)
                            & ~(Res_line.resstatus.in_([4, 8, 9, 10, 12]))
                            & (Res_line.active_flag <= 1)
                            & (Res_line.ankunft <= to_date)
                            & (Res_line.abreise >= fr_date)
                        )
                        |
                        (
                            (Res_line.resstatus == 8)
                            & (Res_line.active_flag == 2)
                            & (Res_line.ankunft == ci_date)
                            & (Res_line.abreise == ci_date)
                        )
                    )
                    & (Res_line.gastnr > 0)
                    & (Res_line.l_zuordnung[inc_value(2)] == 0)
                ).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all()
            print("CreateBrowse, nRecs:", len(recs))
            for res_line in recs:
                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    do_it = True

                    if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:

                        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                        bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                        do_it = None != bill_line

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if do_it and zimmer:

                        queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, fr_date - timedelta(days=1))],"date2": [(ge, fr_date - timedelta(days=1))]})

                        if zimmer.sleeping:

                            if queasy and queasy.number3 == res_line.gastnr:
                                do_it = False
                        else:

                            if queasy and queasy.number3 != res_line.gastnr:
                                pass
                            else:
                                do_it = False

                    if ex_tent:

                        if res_line.resstatus == 3:
                            continue

                    if ex_comp:

                        if res_line.gratis != 0:
                            continue

                    if do_it:
                        datum1 = htparam.fdate

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise

                    # Rd, 21/7/2025    
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

                            if res_line.zipreis > 0:
                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, fr_date))

                            if net_lodg == None:
                                net_lodg =  to_decimal("0")

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                                output_list = query(output_list_data, filters=(lambda output_list: output_list.zikatnr == res_line.zikatnr and output_list.datum == datum), first=True)

                                if not output_list:
                                    output_list = Output_list()
                                    output_list_data.append(output_list)

                                    output_list.zikatnr = res_line.zikatnr
                                    output_list.datum = datum
                                    output_list.roomtype = zimkateg.kurzbez


                                output_list.room = output_list.room + res_line.zimmeranz


                                output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)
    
    def create_browse1():
        nonlocal output_list_data, Output_list, db_session
        nonlocal fr_date, to_date, ci_date, ex_tent, ex_comp
        curr_i:int = 0
        # Use dictionary for fast lookup of (zikatnr, datum)
        output_index = {}

        # Step 1: Query filtered Res_line rows
        recs = db_session.query(Res_line).filter(
            and_(
                or_(
                    and_(
                        Res_line.resstatus <= 13,
                        Res_line.resstatus.notin_([4, 8, 9, 10, 12]),
                        Res_line.active_flag <= 1,
                        Res_line.ankunft <= to_date,
                        Res_line.abreise >= fr_date,
                    ),
                    and_(
                        Res_line.resstatus == 8,
                        Res_line.active_flag == 2,
                        Res_line.ankunft == ci_date,
                        Res_line.abreise == ci_date,
                    )
                ),
                Res_line.gastnr > 0,
                Res_line.l_zuordnung[inc_value(2)] == 0
            )
        ).order_by(
            Res_line.resnr,
            Res_line.reslinnr.desc()
        ).all()

        print("Createbrowse1:", len(recs))

        for res_line in recs:
            do_it = False

            zimkateg = get_cache(Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
            if not zimkateg:
                continue

            do_it = True

            if res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:
                arrangement = get_cache(Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
                if arrangement:
                    bill_line = get_cache(Bill_line, {
                        "departement": [(eq, 0)],
                        "artnr": [(eq, arrangement.argt_artikelnr)],
                        "bill_datum": [(eq, ci_date)],
                        "massnr": [(eq, res_line.resnr)],
                        "billin_nr": [(eq, res_line.reslinnr)]
                    })
                    do_it = bill_line is not None
                else:
                    do_it = False

            zimmer = get_cache(Zimmer, {"zinr": [(eq, res_line.zinr)]})
            if do_it and zimmer:
                queasy = get_cache(Queasy, {
                    "key": [(eq, 14)],
                    "char1": [(eq, res_line.zinr)],
                    "date1": [(le, fr_date - timedelta(days=1))],
                    "date2": [(ge, fr_date - timedelta(days=1))]
                })

                if zimmer.sleeping:
                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:
                    if not queasy or queasy.number3 == res_line.gastnr:
                        do_it = False

            if ex_tent and res_line.resstatus == 3:
                continue

            if ex_comp and res_line.gratis != 0:
                continue

            if not do_it:
                continue

            datum1 = max(fr_date, res_line.ankunft)
            datum2 = min(to_date, res_line.abreise)

            print("Datum1-2:", datum1, datum2)

            datum = datum1
            while datum <= datum2:
                if datum != res_line.abreise:
                    curr_i += 1
                    net_lodg = to_decimal("0")

                    # room breakdown logic is skipped
                    # if res_line.zipreis > 0:
                    #     fnet_lodg, net_lodg, ..., = get_output(...)

                    if net_lodg is None:
                        net_lodg = to_decimal("0")

                    if res_line.resstatus not in (11, 13) and not res_line.zimmerfix:
                        key = (res_line.zikatnr, datum)

                        if key not in output_index:
                            output_list = Output_list()
                            output_list.zikatnr = res_line.zikatnr
                            output_list.datum = datum
                            output_list.roomtype = zimkateg.kurzbez
                            output_list_data.append(output_list)
                            output_index[key] = output_list
                        else:
                            output_list = output_index[key]

                        output_list.room += res_line.zimmeranz
                        output_list.revenue = to_decimal(output_list.revenue) + net_lodg

                datum += timedelta(days=1)


    # def create_browse1():

    #     nonlocal output_list_data, output_list1_data, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, zimkateg, genstat, res_line, reservation, arrangement, bill_line, zimmer, queasy
    #     nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
    #     nonlocal boutput, boutput1


    #     nonlocal output_list, output_list1, boutput, boutput1
    #     nonlocal output_list_data, output_list1_data

    #     datum:date = None
    #     datum1:date = None
    #     datum2:date = None
    #     tdate:date = None
    #     fdate:date = None
    #     tot_breakfast:Decimal = to_decimal("0.0")
    #     tot_lunch:Decimal = to_decimal("0.0")
    #     tot_dinner:Decimal = to_decimal("0.0")
    #     tot_other:Decimal = to_decimal("0.0")
    #     curr_i:int = 0
    #     net_lodg:Decimal = to_decimal("0.0")
    #     fnet_lodg:Decimal = to_decimal("0.0")
    #     tot_rmrev:Decimal = to_decimal("0.0")
    #     tot_vat:Decimal = to_decimal("0.0")
    #     tot_service:Decimal = to_decimal("0.0")
    #     do_it:bool = False

    #     # for res_line in db_session.query(Res_line).filter(
    #     #          (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

    #     recs = db_session.query(Res_line).filter(
    #                 and_(
    #                     or_(
    #                         and_(
    #                             Res_line.resstatus <= 13,
    #                             Res_line.resstatus.notin_([4, 8, 9, 10, 12]),
    #                             Res_line.active_flag <= 1,
    #                             Res_line.ankunft <= to_date,
    #                             Res_line.abreise >= fr_date,
    #                         ),
    #                         and_(
    #                             Res_line.resstatus == 8,
    #                             Res_line.active_flag == 2,
    #                             Res_line.ankunft == ci_date,
    #                             Res_line.abreise == ci_date,
    #                         )
    #                     ),
    #                     Res_line.gastnr > 0,
    #                     Res_line.l_zuordnung[inc_value(2)] == 0
    #                 )
    #             ).order_by(
    #                 Res_line.resnr,
    #                 Res_line.reslinnr.desc()
    #             ).all()
    #     print("Createbrowse1:", len(recs))
    #     for res_line in recs:
    #         reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

    #         zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})


    #         if zimkateg:
    #             do_it = True

    #             if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:

    #                 arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    #                 bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
    #                 do_it = None != bill_line

    #             zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

    #             if do_it and zimmer:

    #                 queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, fr_date - timedelta(days=1))],"date2": [(ge, fr_date - timedelta(days=1))]})

    #                 if zimmer.sleeping:

    #                     if queasy and queasy.number3 == res_line.gastnr:
    #                         do_it = False
    #                 else:

    #                     if queasy and queasy.number3 != res_line.gastnr:
    #                         pass
    #                     else:
    #                         do_it = False

    #             if ex_tent:

    #                 if res_line.resstatus == 3:
    #                     continue

    #             if ex_comp:

    #                 if res_line.gratis != 0:
    #                     continue

    #             if do_it:
    #                 datum1 = fr_date

    #                 if res_line.ankunft > datum1:
    #                     datum1 = res_line.ankunft
    #                 datum2 = to_date

    #                 if res_line.abreise < datum2:
    #                     datum2 = res_line.abreise

    #                 print("Datum1-2:", datum1, datum2)
    #                 for datum in date_range(datum1,datum2) :
    #                     net_lodg =  to_decimal("0")
    #                     curr_i = curr_i + 1

    #                     if datum == res_line.abreise:
    #                         pass
    #                     else:
    #                         net_lodg =  to_decimal("0")
    #                         tot_breakfast =  to_decimal("0")
    #                         tot_lunch =  to_decimal("0")
    #                         tot_dinner =  to_decimal("0")
    #                         tot_other =  to_decimal("0")
    #                         tot_rmrev =  to_decimal("0")
    #                         tot_vat =  to_decimal("0")
    #                         tot_service =  to_decimal("0")

    #                         # if res_line.zipreis > 0:
    #                         #     fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, fr_date))

    #                         if net_lodg == None:
    #                             net_lodg =  to_decimal("0")

    #                         if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

    #                             output_list = query(output_list_data, filters=(lambda output_list: output_list.zikatnr == res_line.zikatnr and output_list.datum == datum), first=True)

    #                             if not output_list:
    #                                 output_list = Output_list()
    #                                 output_list_data.append(output_list)

    #                                 output_list.zikatnr = res_line.zikatnr
    #                                 output_list.datum = datum
    #                                 output_list.roomtype = zimkateg.kurzbez


    #                             output_list.room = output_list.room + res_line.zimmeranz
    #                             output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)

    

    def create_browse2():

        nonlocal output_list_data, output_list1_data, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, zimkateg, genstat, res_line, reservation, arrangement, bill_line, zimmer, queasy
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_data, output_list1_data

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
        frdate:date = None
        todate:date = None
        frdate = date_mdy(1, 1, to_year)
        todate = date_mdy(12, 31, to_year)
        tdate = ci_date - timedelta(days=1)

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        for genstat.resstatus, genstat.zikatnr, genstat.datum, genstat.logis, genstat._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Genstat.resstatus, Genstat.zikatnr, Genstat.datum, Genstat.logis, Genstat._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                 (Genstat.datum >= frdate) & (Genstat.datum <= tdate) & (Genstat.zikatnr != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat.zikatnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            output_list1 = query(output_list1_data, filters=(lambda output_list1: output_list1.zikatnr == genstat.zikatnr), first=True)

            if not output_list1:
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.zikatnr = genstat.zikatnr
                output_list1.roomtype = zimkateg.kurzbez


            output_list1.room[get_month(genstat.datum) - 1] = output_list1.room[get_month(genstat.datum) - 1] + 1
            output_list1.revenue[get_month(genstat.datum) - 1] = output_list1.revenue[get_month(genstat.datum) - 1] + genstat.logis


        htparam.fdate = tdate + timedelta(days=1)

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > todate)) & (not_ (Res_line.abreise < htparam.fdate)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:

                    if ex_tent:

                        if res_line.resstatus == 3:
                            continue

                    if ex_comp:

                        if res_line.gratis != 0:
                            continue
                    datum1 = htparam.fdate

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = todate

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
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


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, fr_date))

                            output_list1 = query(output_list1_data, filters=(lambda output_list1: output_list1.zikatnr == res_line.zikatnr), first=True)

                            if not output_list1:
                                output_list1 = Output_list1()
                                output_list1_data.append(output_list1)

                                output_list1.zikatnr = res_line.zikatnr
                                output_list1.roomtype = zimkateg.kurzbez


                            output_list1.room[get_month(datum) - 1] = output_list1.room[get_month(datum) - 1] + res_line.zimmeranz


                            output_list1.revenue[get_month(datum) - 1] = output_list1.revenue[get_month(datum) - 1] + net_lodg


    def create_browse3():

        nonlocal output_list_data, output_list1_data, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, zimkateg, genstat, res_line, reservation, arrangement, bill_line, zimmer, queasy
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_data, output_list1_data

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
        frdate:date = None
        todate:date = None
        frdate = date_mdy(1, 1, to_year)
        todate = date_mdy(12, 31, to_year)

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > todate)) & (not_ (Res_line.abreise < frdate)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            if zimkateg:

                if ex_tent:

                    if res_line.resstatus == 3:
                        continue

                if ex_comp:

                    if res_line.gratis != 0:
                        continue
                datum1 = frdate

                if res_line.ankunft > datum1:
                    datum1 = res_line.ankunft
                datum2 = todate

                if res_line.abreise < datum2:
                    datum2 = res_line.abreise
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

                        if res_line.zipreis != 0:
                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, fr_date))

                        output_list1 = query(output_list1_data, filters=(lambda output_list1: output_list1.zikatnr == res_line.zikatnr), first=True)

                        if not output_list1:
                            output_list1 = Output_list1()
                            output_list1_data.append(output_list1)

                            output_list1.zikatnr = res_line.zikatnr
                            output_list1.roomtype = zimkateg.kurzbez


                        output_list1.room[get_month(datum) - 1] = output_list1.room[get_month(datum) - 1] + res_line.zimmeranz


                        output_list1.revenue[get_month(datum) - 1] = output_list1.revenue[get_month(datum) - 1] + net_lodg

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
    black_list = htparam.finteger

    if sum_month == False:

        if fr_date < ci_date:
            print("create_browse")
            create_browse()
        else:
            print("create_browse111")
            create_browse1()

        for output_list in query(output_list_data, sort_by=[("datum",False),("zikatnr",False)]):

            if curr_date == None:
                boutput = Boutput()
                boutput_data.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.roomtype = to_string(output_list.datum, "99/99/9999")

            elif curr_date != None and curr_date != output_list.datum:
                boutput = Boutput()
                boutput_data.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.datum = curr_date
                boutput.str_datum = to_string(curr_date, "99/99/9999")
                boutput.roomtype = "TOTAL"
                boutput.room = tot_rm
                boutput.revenue =  to_decimal(tot_rev)
                # Rd, 21/7/25, divide none/zero
                # boutput.avrg_rev =  to_decimal(tot_rev) / to_decimal(tot_rm)
                boutput.avrg_rev =  safe_divide(tot_rev , tot_rm)
                tot_rm =  to_decimal("0")
                tot_rev =  to_decimal("0")
                boutput.str_room = to_string(boutput.room, ">>>,>>9")
                boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
                boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")


                boutput = Boutput()
                boutput_data.append(boutput)

                counter = counter + 1
                boutput.counter = counter


                boutput = Boutput()
                boutput_data.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.roomtype = to_string(output_list.datum, "99/99/9999")


            counter = counter + 1
            output_list.counter = counter
            # output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)
            output_list.avrg_rev = (
                to_decimal(output_list.revenue) / to_decimal(output_list.room)
                if to_decimal(output_list.room) not in (0, None)
                else Decimal("0")
            )
            output_list.str_room = to_string(output_list.room, ">>>,>>9")
            output_list.str_revenue = to_string(output_list.revenue, "->>>,>>>,>>>,>>9.99")
            output_list.str_avrg = to_string(output_list.avrg_rev, "->>>,>>>,>>>,>>9.99")
            curr_date = output_list.datum
            tot_rm =  to_decimal(tot_rm) + to_decimal(output_list.room)
            tot_rev =  to_decimal(tot_rev) + to_decimal(output_list.revenue)
            trm =  to_decimal(trm) + to_decimal(output_list.room)
            trev =  to_decimal(trev) + to_decimal(output_list.revenue)


        boutput = Boutput()
        boutput_data.append(boutput)

        counter = counter + 1
        boutput.counter = counter
        boutput.datum = curr_date
        boutput.str_datum = to_string(curr_date, "99/99/9999")
        boutput.roomtype = "TOTAL"
        boutput.room = tot_rm
        boutput.revenue =  to_decimal(tot_rev)

        # boutput.avrg_rev =  to_decimal(tot_rev) / to_decimal(tot_rm)
        boutput.avrg_rev =  safe_divide(tot_rev , tot_rm)
        tot_rm =  to_decimal("0")
        tot_rev =  to_decimal("0")
        boutput.str_room = to_string(boutput.room, ">>>,>>9")
        boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
        boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")


        boutput = Boutput()
        boutput_data.append(boutput)

        counter = counter + 1
        boutput.counter = counter
        boutput.roomtype = "Grand TOTAL"
        boutput.room = trm
        boutput.revenue =  to_decimal(trev)
        # boutput.avrg_rev =  to_decimal(trev) / to_decimal(trm)
        boutput.avrg_rev =  safe_divide(tot_rev , tot_rm)
        
        boutput.str_room = to_string(boutput.room, ">>>,>>9")
        boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
        boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")

    elif sum_month :
        if to_year <= get_year(ci_date):
            create_browse2()
        else:
            create_browse3()

        for output_list1 in query(output_list1_data, sort_by=[("zikatnr",False)]):
            for loopi in range(1,12 + 1) :
                counter = counter + 1
                output_list1.counter = counter
                output_list1.avrg_rev[loopi - 1] = output_list1.revenue[loopi - 1] / output_list1.room[loopi - 1]
                trm1[loopi - 1] = trm1[loopi - 1] + output_list1.room[loopi - 1]
                trev1[loopi - 1] = trev1[loopi - 1] + output_list1.revenue[loopi - 1]

                if output_list1.avrg_rev[loopi - 1] == None:
                    output_list1.avrg_rev[loopi - 1] = 0


        boutput1 = Boutput1()
        boutput1_data.append(boutput1)

        counter = counter + 1
        boutput1.counter = counter
        boutput1.roomtype = "TOTAL"


        for loopi in range(1,12 + 1) :
            boutput1.room[loopi - 1] = trm1[loopi - 1]
            boutput1.revenue[loopi - 1] = trev1[loopi - 1]
            boutput1.avrg_rev[loopi - 1] = trev1[loopi - 1] / trm1[loopi - 1]

            if boutput1.avrg_rev[loopi - 1] == None:
                boutput1.avrg_rev[loopi - 1] = 0

    return generate_output()