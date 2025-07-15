#using conversion tools version: 1.0.0.61

from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Segment, Genstat, Res_line, Reservation

def rm_fbysegment_btn_go_1bl(sum_month:bool, fr_date:date, to_date:date, to_year:int, ex_tent:bool, ex_comp:bool):
    output_list_list = []
    output_list1_list = []
    black_list:int = 0
    counter:int = 0
    ci_date:date = None
    curr_date:date = None
    tot_rm:decimal = to_decimal("0.0")
    trm:decimal = to_decimal("0.0")
    tot_rev:decimal = to_decimal("0.0")
    trev:decimal = to_decimal("0.0")
    trev1:List[decimal] = create_empty_list(12,to_decimal("0"))
    trm1:List[decimal] = create_empty_list(12,to_decimal("0"))
    loopi:int = 0
    htparam = segment = genstat = res_line = reservation = None

    output_list = output_list1 = boutput = boutput1 = None

    output_list_list, Output_list = create_model("Output_list", {"counter":int, "segmentcode":int, "datum":date, "str_datum":str, "segment":str, "room":int, "revenue":decimal, "avrg_rev":decimal, "str_room":str, "str_revenue":str, "str_avrg":str})
    output_list1_list, Output_list1 = create_model("Output_list1", {"counter":int, "segmentcode":int, "segment":str, "room":[int,12], "revenue":[decimal,12], "avrg_rev":[decimal,12]})

    Boutput = Output_list
    boutput_list = output_list_list

    Boutput1 = Output_list1
    boutput1_list = output_list1_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, output_list1_list, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, segment, genstat, res_line, reservation
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_list, output_list1_list

        return {"output-list": output_list_list, "output-list1": output_list1_list}

    def create_browse():

        nonlocal output_list_list, output_list1_list, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, segment, genstat, res_line, reservation
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_list, output_list1_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        tdate:date = None
        fdate:date = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        curr_i:int = 0
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")

        if to_date < (ci_date - timedelta(days=1)):
            tdate = to_date
        else:
            tdate = ci_date - timedelta(days=1)

        genstat_obj_list = []
        recs = (db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.segmentcode != black_list)).filter(
                 (Genstat.datum >= fr_date) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat.segmentcode).all())
        for genstat, segment in recs:
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            output_list = query(output_list_list, filters=(lambda output_list: output_list.segmentcode == genstat.segmentcode and output_list.datum == genstat.datum), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.segmentcode = genstat.segmentcode
                output_list.datum = genstat.datum
                output_list.segment = segment.bezeich


            output_list.room = output_list.room + 1
            output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(genstat.logis)


        htparam.fdate = tdate + timedelta(days=1)

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < htparam.fdate)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode) & (Segment.segmentcode != black_list)).first()

                if segment:

                    if ex_tent:

                        if res_line.resstatus == 3:
                            continue

                    if ex_comp:

                        if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                            continue

                    if (res_line.resstatus != 3 or (res_line.resstatus == 3 and not ex_tent)) and res_line.resstatus != 4 and res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        datum1 = htparam.fdate

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

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

                                output_list = query(output_list_list, filters=(lambda output_list: output_list.segmentcode == reservation.segmentcode and output_list.datum == datum), first=True)

                                if not output_list:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.segmentcode = reservation.segmentcode
                                    output_list.datum = datum
                                    output_list.segment = segment.bezeich


                                output_list.room = output_list.room + res_line.zimmeranz


                                output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)


    def create_browse1():

        nonlocal output_list_list, output_list1_list, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, segment, genstat, res_line, reservation
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_list, output_list1_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        tdate:date = None
        fdate:date = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        curr_i:int = 0
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")

        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == reservation.segmentcode) & (Segment.segmentcode != black_list)).first()

            if segment:

                if ex_tent:

                    if res_line.resstatus == 3:
                        continue

                if ex_comp:

                    if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                        continue

                if (res_line.resstatus != 3 or (res_line.resstatus == 3 and not ex_tent)) and res_line.resstatus != 4 and res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                    datum1 = fr_date

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

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

                            output_list = query(output_list_list, filters=(lambda output_list: output_list.segmentcode == reservation.segmentcode and output_list.datum == datum), first=True)

                            if not output_list:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.segmentcode = reservation.segmentcode
                                output_list.datum = datum
                                output_list.segment = segment.bezeich


                            output_list.room = output_list.room + res_line.zimmeranz


                            output_list.revenue =  to_decimal(output_list.revenue) + to_decimal(net_lodg)


    def create_browse2():

        nonlocal output_list_list, output_list1_list, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, segment, genstat, res_line, reservation
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_list, output_list1_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        tdate:date = None
        fdate:date = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        curr_i:int = 0
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
        frdate:date = None
        todate:date = None
        frdate = date_mdy(1, 1, to_year)
        todate = date_mdy(12, 31, to_year)
        tdate = ci_date - timedelta(days=1)

        genstat_obj_list = []
        for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.segmentcode != black_list)).filter(
                 (Genstat.datum >= frdate) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat.segmentcode).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            output_list1 = query(output_list1_list, filters=(lambda output_list1: output_list1.segmentcode == genstat.segmentcode), first=True)

            if not output_list1:
                output_list1 = Output_list1()
                output_list1_list.append(output_list1)

                output_list1.segmentcode = genstat.segmentcode
                output_list1.segment = segment.bezeich


            output_list1.room[get_month(genstat.datum) - 1] = output_list1.room[get_month(genstat.datum) - 1] + 1
            output_list1.revenue[get_month(genstat.datum) - 1] = output_list1.revenue[get_month(genstat.datum) - 1] + genstat.logis


        htparam.fdate = tdate + timedelta(days=1)

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > todate)) & (not_ (Res_line.abreise < htparam.fdate)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode) & (Segment.segmentcode != black_list)).first()

                if segment:

                    if ex_tent:

                        if res_line.resstatus == 3:
                            continue

                    if ex_comp:

                        if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                            continue

                    if (res_line.resstatus != 3 or (res_line.resstatus == 3 and not ex_tent)) and res_line.resstatus != 4 and res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
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

                                output_list1 = query(output_list1_list, filters=(lambda output_list1: output_list1.segmentcode == reservation.segmentcode), first=True)

                                if not output_list1:
                                    output_list1 = Output_list1()
                                    output_list1_list.append(output_list1)

                                    output_list1.segmentcode = reservation.segmentcode
                                    output_list1.segment = segment.bezeich


                                output_list1.room[get_month(datum) - 1] = output_list1.room[get_month(datum) - 1] + res_line.zimmeranz


                                output_list1.revenue[get_month(datum) - 1] = output_list1.revenue[get_month(datum) - 1] + net_lodg


    def create_browse3():

        nonlocal output_list_list, output_list1_list, black_list, counter, ci_date, curr_date, tot_rm, trm, tot_rev, trev, trev1, trm1, loopi, htparam, segment, genstat, res_line, reservation
        nonlocal sum_month, fr_date, to_date, to_year, ex_tent, ex_comp
        nonlocal boutput, boutput1


        nonlocal output_list, output_list1, boutput, boutput1
        nonlocal output_list_list, output_list1_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        tdate:date = None
        fdate:date = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        curr_i:int = 0
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
        frdate:date = None
        todate:date = None
        frdate = date_mdy(1, 1, to_year)
        todate = date_mdy(12, 31, to_year)

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > todate)) & (not_ (Res_line.abreise < frdate)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == reservation.segmentcode) & (Segment.segmentcode != black_list)).first()

            if segment:

                if ex_tent:

                    if res_line.resstatus == 3:
                        continue

                if ex_comp:

                    if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                        continue

                if (res_line.resstatus != 3 or (res_line.resstatus == 3 and not ex_tent)) and res_line.resstatus != 4 and res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
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


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, fr_date))

                            output_list1 = query(output_list1_list, filters=(lambda output_list1: output_list1.segmentcode == reservation.segmentcode), first=True)

                            if not output_list1:
                                output_list1 = Output_list1()
                                output_list1_list.append(output_list1)

                                output_list1.segmentcode = reservation.segmentcode
                                output_list1.segment = segment.bezeich


                            output_list1.room[get_month(datum) - 1] = output_list1.room[get_month(datum) - 1] + res_line.zimmeranz


                            output_list1.revenue[get_month(datum) - 1] = output_list1.revenue[get_month(datum) - 1] + net_lodg

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    if htparam:
        ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 709)).first()
    black_list = htparam.finteger

    if sum_month == False:

        if fr_date < ci_date:
            create_browse()
        else:
            create_browse1()

        for output_list in query(output_list_list, sort_by=[("datum",False)]):

            if curr_date == None:
                boutput = Boutput()
                boutput_list.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.segment = to_string(output_list.datum, "99/99/9999")

            elif curr_date != None and curr_date != output_list.datum:
                boutput = Boutput()
                boutput_list.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.datum = curr_date
                boutput.str_datum = to_string(curr_date, "99/99/9999")
                boutput.segment = "TOTAL"
                boutput.room = tot_rm
                boutput.revenue =  to_decimal(tot_rev)
                boutput.avrg_rev =  to_decimal(tot_rev) / to_decimal(tot_rm)
                tot_rm =  to_decimal("0")
                tot_rev =  to_decimal("0")
                boutput.str_room = to_string(boutput.room, ">>>,>>9")
                boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
                boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")


                boutput = Boutput()
                boutput_list.append(boutput)

                counter = counter + 1
                boutput.counter = counter


                boutput = Boutput()
                boutput_list.append(boutput)

                counter = counter + 1
                boutput.counter = counter
                boutput.segment = to_string(output_list.datum, "99/99/9999")

            if output_list.room != 0 and output_list.room != None:
                output_list.avrg_rev =  to_decimal(output_list.revenue) / to_decimal(output_list.room)
            counter = counter + 1
            output_list.counter = counter
            output_list.str_room = to_string(output_list.room, ">>>,>>9")
            output_list.str_revenue = to_string(output_list.revenue, "->>>,>>>,>>>,>>9.99")
            output_list.str_avrg = to_string(output_list.avrg_rev, "->>>,>>>,>>>,>>9.99")
            curr_date = output_list.datum
            tot_rm =  to_decimal(tot_rm) + to_decimal(output_list.room)
            tot_rev =  to_decimal(tot_rev) + to_decimal(output_list.revenue)
            trm =  to_decimal(trm) + to_decimal(output_list.room)
            trev =  to_decimal(trev) + to_decimal(output_list.revenue)


        boutput = Boutput()
        boutput_list.append(boutput)

        counter = counter + 1
        boutput.counter = counter
        boutput.datum = curr_date
        boutput.str_datum = to_string(curr_date, "99/99/9999")
        boutput.segment = "TOTAL"
        boutput.room = tot_rm
        boutput.revenue =  to_decimal(tot_rev)
        boutput.avrg_rev =  to_decimal(tot_rev) / to_decimal(tot_rm)
        tot_rm =  to_decimal("0")
        tot_rev =  to_decimal("0")
        boutput.str_room = to_string(boutput.room, ">>>,>>9")
        boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
        boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")


        boutput = Boutput()
        boutput_list.append(boutput)

        counter = counter + 1
        boutput.counter = counter
        boutput.segment = "Grand TOTAL"
        boutput.room = trm
        boutput.revenue =  to_decimal(trev)
        boutput.avrg_rev =  to_decimal(trev) / to_decimal(trm)
        boutput.str_room = to_string(boutput.room, ">>>,>>9")
        boutput.str_revenue = to_string(boutput.revenue, "->>>,>>>,>>>,>>9.99")
        boutput.str_avrg = to_string(boutput.avrg_rev, "->>>,>>>,>>>,>>9.99")

    elif sum_month :

        if to_year <= get_year(ci_date):
            create_browse2()
        else:
            create_browse3()

        for output_list1 in query(output_list1_list):
            for loopi in range(1,12 + 1) :
                counter = counter + 1
                output_list1.counter = counter
                output_list1.avrg_rev[loopi - 1] = output_list1.revenue[loopi - 1] / output_list1.room[loopi - 1]
                trm1[loopi - 1] = trm1[loopi - 1] + output_list1.room[loopi - 1]
                trev1[loopi - 1] = trev1[loopi - 1] + output_list1.revenue[loopi - 1]

                if output_list1.avrg_rev[loopi - 1] == None:
                    output_list1.avrg_rev[loopi - 1] = 0


        boutput1 = Boutput1()
        boutput1_list.append(boutput1)

        counter = counter + 1
        boutput1.counter = counter
        boutput1.segment = "TOTAL"


        for loopi in range(1,12 + 1) :
            boutput1.room[loopi - 1] = trm1[loopi - 1]
            boutput1.revenue[loopi - 1] = trev1[loopi - 1]
            boutput1.avrg_rev[loopi - 1] = trev1[loopi - 1] / trm1[loopi - 1]

            if boutput1.avrg_rev[loopi - 1] == None:
                boutput1.avrg_rev[loopi - 1] = 0

    return generate_output()