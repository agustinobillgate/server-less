#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Genstat, Segment, Res_line, Reservation, Zinrstat, Zimmer, Outorder, Zkstat

def _3monthly_forecastbl(fmonth:string, tmonth:string):

    prepare_cache ([Htparam, Genstat, Segment, Res_line, Reservation, Zinrstat, Zkstat])

    output_list1_data = []
    bill_date:date = None
    fdate:date = None
    tdate:date = None
    fmm:int = 0
    fyy:int = 0
    tmm:int = 0
    tyy:int = 0
    datum:date = None
    datum1:date = None
    datum2:date = None
    datum3:date = None
    curr_i:int = 0
    net_lodg:Decimal = to_decimal("0.0")
    fnet_lodg:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_other:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
    actual_tot_room:int = 0
    curr_month:int = 0
    tot_rmsold:Decimal = to_decimal("0.0")
    tot_ooo:Decimal = to_decimal("0.0")
    tot_comp:Decimal = to_decimal("0.0")
    tot_houseuse:Decimal = to_decimal("0.0")
    tot_rmrevenue:Decimal = to_decimal("0.0")
    tot_avrgrevenue:Decimal = to_decimal("0.0")
    tot_room:int = 0
    tot_zinr:int = 0
    htparam = genstat = segment = res_line = reservation = zinrstat = zimmer = outorder = zkstat = None

    output_list = output_list1 = active_rm_list = boutput = None

    output_list_data, Output_list = create_model("Output_list", {"datum":date, "smonth":int, "rmsold":int, "ooo":int, "comp":int, "houseuse":int, "rmrevenue":Decimal, "percent_occ":Decimal})
    output_list1_data, Output_list1 = create_model_like(Output_list, {"counter":int, "sdate":string, "avrgrevenue":Decimal})
    active_rm_list_data, Active_rm_list = create_model("Active_rm_list", {"datum":date, "zimmeranz":int})

    Boutput = Output_list
    boutput_data = output_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list1_data, bill_date, fdate, tdate, fmm, fyy, tmm, tyy, datum, datum1, datum2, datum3, curr_i, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, actual_tot_room, curr_month, tot_rmsold, tot_ooo, tot_comp, tot_houseuse, tot_rmrevenue, tot_avrgrevenue, tot_room, tot_zinr, htparam, genstat, segment, res_line, reservation, zinrstat, zimmer, outorder, zkstat
        nonlocal fmonth, tmonth
        nonlocal boutput


        nonlocal output_list, output_list1, active_rm_list, boutput
        nonlocal output_list_data, output_list1_data, active_rm_list_data

        return {"output-list1": output_list1_data}

    def get_active_room(curr_datum:date):

        nonlocal output_list1_data, bill_date, fdate, tdate, fmm, fyy, tmm, tyy, datum, datum1, datum2, datum3, curr_i, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, actual_tot_room, curr_month, tot_rmsold, tot_ooo, tot_comp, tot_houseuse, tot_rmrevenue, tot_avrgrevenue, tot_room, tot_zinr, htparam, genstat, segment, res_line, reservation, zinrstat, zimmer, outorder, zkstat
        nonlocal fmonth, tmonth
        nonlocal boutput


        nonlocal output_list, output_list1, active_rm_list, boutput
        nonlocal output_list_data, output_list1_data, active_rm_list_data

        active_room = 0

        def generate_inner_output():
            return (active_room)


        if curr_datum >= bill_date:
            active_room = actual_tot_room

            return generate_inner_output()

        active_rm_list = query(active_rm_list_data, filters=(lambda active_rm_list: active_rm_list.datum == curr_datum), first=True)

        if active_rm_list:
            active_room = active_rm_list.zimmeranz

        return generate_inner_output()


    def create_active_room_list():

        nonlocal output_list1_data, bill_date, fdate, tdate, fmm, fyy, tmm, tyy, datum, datum1, datum2, datum3, curr_i, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, actual_tot_room, curr_month, tot_rmsold, tot_ooo, tot_comp, tot_houseuse, tot_rmrevenue, tot_avrgrevenue, tot_room, tot_zinr, htparam, genstat, segment, res_line, reservation, zinrstat, zimmer, outorder, zkstat
        nonlocal fmonth, tmonth
        nonlocal boutput


        nonlocal output_list, output_list1, active_rm_list, boutput
        nonlocal output_list_data, output_list1_data, active_rm_list_data

        end_date:date = None
        actual_date:date = None

        if tdate < bill_date:
            end_date = tdate
        else:
            end_date = bill_date - timedelta(days=1)

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum >= fdate) & (Zkstat.datum <= end_date)).order_by(Zkstat.datum).all():

            if actual_date != zkstat.datum:
                active_rm_list = Active_rm_list()
                active_rm_list_data.append(active_rm_list)

                active_rm_list.datum = zkstat.datum
                actual_date = zkstat.datum


            active_rm_list.zimmeranz = active_rm_list.zimmeranz + zkstat.anz100


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate


    fmm = to_int(entry(0, fmonth, "/"))
    fyy = to_int(entry(1, fmonth, "/"))
    tmm = to_int(entry(0, tmonth, "/"))
    tyy = to_int(entry(1, tmonth, "/"))
    fdate = date_mdy(fmm, 1, fyy)


    if tmm + 1 > 12:
        tdate = date_mdy(1, 1, tyy + timedelta(days=1)) - timedelta(days=1)


    else:
        tdate = date_mdy(tmm + 1, 1, tyy) - timedelta(days=1)

    if fdate < bill_date:
        datum1 = fdate

        if datum1 < bill_date:

            if tdate < (bill_date - timedelta(days=1)):
                datum2 = tdate
            else:
                datum2 = bill_date - timedelta(days=1)
        else:
            datum2 = tdate

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= datum2) & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != "")).order_by(Genstat._recid).all():

            output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == genstat.datum), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.datum = genstat.datum
                output_list.smonth = get_month(genstat.datum)


            output_list.rmsold = output_list.rmsold + 1
            output_list.rmrevenue =  to_decimal(output_list.rmrevenue) + to_decimal(genstat.logis)

            segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

            if segment and (segment.betriebsnr == 1 or segment.betriebsnr == 2):

                if segment.betriebsnr == 1:
                    output_list.comp = output_list.comp + 1

                elif segment.betriebsnr == 2:
                    output_list.houseuse = output_list.houseuse + 1


            else:

                if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1]:
                    output_list.comp = output_list.comp + 1

        if tdate >= bill_date:

            for res_line in db_session.query(Res_line).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 3) & (Res_line.resstatus != 13) & (Res_line.resstatus != 11) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > tdate)) & (not_ (Res_line.abreise < bill_date)))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == bill_date) & (Res_line.abreise == bill_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == bill_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                datum1 = bill_date

                if res_line.ankunft > datum1:
                    datum1 = res_line.ankunft
                datum2 = tdate

                if res_line.abreise < datum2:
                    datum2 = res_line.abreise
                for datum3 in date_range(datum1,datum2) :

                    if datum3 == res_line.abreise:
                        pass
                    else:

                        output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == datum3), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.datum = datum3
                            output_list.smonth = get_month(datum3)


                        net_lodg =  to_decimal("0")
                        fnet_lodg =  to_decimal("0")
                        tot_breakfast =  to_decimal("0")
                        tot_lunch =  to_decimal("0")
                        tot_dinner =  to_decimal("0")
                        tot_other =  to_decimal("0")

                        if res_line.zipreis > 0:
                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum3, curr_i, bill_date))

                        if net_lodg == None:
                            net_lodg =  to_decimal("0")

                        if tot_rmrev == None:
                            tot_rmrev =  to_decimal("0")

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            output_list.rmsold = output_list.rmsold + res_line.zimmeranz
                            output_list.rmrevenue =  to_decimal(output_list.rmrevenue) + to_decimal(net_lodg)

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment and (segment.betriebsnr == 1 or segment.betriebsnr == 2):

                            if segment.betriebsnr == 1:
                                output_list.comp = output_list.comp + 1

                            elif segment.betriebsnr == 2:
                                output_list.houseuse = output_list.houseuse + res_line.zimmeranz


                        else:

                            if res_line.zipreis == 0 and res_line.gratis != 0:
                                output_list.comp = output_list.comp + res_line.zimmeranz


    else:

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 3) & (Res_line.resstatus != 13) & (Res_line.resstatus != 11) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > tdate)) & (not_ (Res_line.abreise < fdate)))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == bill_date) & (Res_line.abreise == bill_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == bill_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            datum1 = fdate

            if res_line.ankunft > datum1:
                datum1 = res_line.ankunft
            datum2 = tdate

            if res_line.abreise < datum2:
                datum2 = res_line.abreise
            for datum3 in date_range(datum1,datum2) :

                if datum3 == res_line.abreise:
                    pass
                else:

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == datum3), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.datum = datum3
                        output_list.smonth = get_month(datum3)


                    net_lodg =  to_decimal("0")
                    fnet_lodg =  to_decimal("0")
                    tot_breakfast =  to_decimal("0")
                    tot_lunch =  to_decimal("0")
                    tot_dinner =  to_decimal("0")
                    tot_other =  to_decimal("0")
                    curr_i = curr_i + 1

                    if res_line.zipreis > 0:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum3, curr_i, fdate))

                    if net_lodg == None:
                        net_lodg =  to_decimal("0")

                    if tot_rmrev == None:
                        tot_rmrev =  to_decimal("0")

                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        output_list.rmsold = output_list.rmsold + res_line.zimmeranz
                        output_list.rmrevenue =  to_decimal(output_list.rmrevenue) + to_decimal(net_lodg)

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment and (segment.betriebsnr == 1 or segment.betriebsnr == 2):

                        if segment.betriebsnr == 1:
                            output_list.comp = output_list.comp + 1

                        elif segment.betriebsnr == 2:
                            output_list.houseuse = output_list.houseuse + res_line.zimmeranz


                    else:

                        if res_line.zipreis == 0 and res_line.gratis != 0:
                            output_list.comp = output_list.comp + res_line.zimmeranz


    for datum in date_range(fdate,tdate) :

        if datum < bill_date:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, datum)]})

            if zinrstat:

                output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == datum), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.datum = datum
                    output_list.smonth = get_month(datum)


                output_list.ooo = output_list.ooo + zinrstat.zimmeranz


        else:

            outorder_obj_list = {}
            for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                     (Outorder.betriebsnr <= 1) & (datum >= Outorder.gespstart) & (datum <= Outorder.gespende)).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True

                output_list = query(output_list_data, filters=(lambda output_list: output_list.datum == datum), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.datum = datum
                    output_list.smonth = get_month(datum)


                output_list.ooo = output_list.ooo + 1

        boutput = query(boutput_data, filters=(lambda boutput: boutput.datum == datum), first=True)

        if not boutput:
            boutput = Boutput()
            boutput_data.append(boutput)

            boutput.datum = datum
            boutput.smonth = get_month(datum)
            boutput.rmsold = 0
            boutput.ooo = 0
            boutput.comp = 0
            boutput.houseuse = 0
            boutput.rmrevenue =  to_decimal("0")


    actual_tot_room = 0

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        actual_tot_room = actual_tot_room + 1


    create_active_room_list()

    for output_list in query(output_list_data, sort_by=[("datum",False)]):

        if curr_month != 0 and curr_month != get_month(output_list.datum):
            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

            counter = counter + 1
            output_list1.counter = counter
            output_list1.sdate = "T O T A L"
            output_list1.smonth = curr_month
            output_list1.rmsold = tot_rmsold
            output_list1.ooo = tot_ooo
            output_list1.comp = tot_comp
            output_list1.houseuse = tot_houseuse
            output_list1.rmrevenue =  to_decimal(tot_rmrevenue)
            output_list1.avrgrevenue =  to_decimal(output_list1.rmRevenue) / to_decimal(output_list1.rmSold)
            output_list1.percent_occ =  to_decimal(output_list1.rmSold) / to_decimal(tot_zinr) * to_decimal("100")
            tot_rmsold =  to_decimal("0")
            tot_ooo =  to_decimal("0")
            tot_comp =  to_decimal("0")
            tot_houseuse =  to_decimal("0")
            tot_rmrevenue =  to_decimal("0")
            tot_avrgrevenue =  to_decimal("0")
            tot_zinr = 0


        tot_room = get_active_room(datum)
        output_list1 = Output_list1()
        output_list1_data.append(output_list1)

        buffer_copy(output_list, output_list1)
        counter = counter + 1
        output_list1.counter = counter
        output_list1.sdate = to_string(output_list.datum)
        output_list1.avrgrevenue =  to_decimal(output_list.rmRevenue) / to_decimal(output_list.rmSold)
        output_list1.percent_occ =  to_decimal(output_list.rmSold) / to_decimal(tot_room) * to_decimal("100")
        curr_month = get_month(output_list.datum)
        tot_rmsold =  to_decimal(tot_rmsold) + to_decimal(output_list1.rmSold)
        tot_ooo =  to_decimal(tot_ooo) + to_decimal(output_list1.ooo)
        tot_comp =  to_decimal(tot_comp) + to_decimal(output_list1.comp)
        tot_houseuse =  to_decimal(tot_houseuse) + to_decimal(output_list1.houseUse)
        tot_rmrevenue =  to_decimal(tot_rmrevenue) + to_decimal(output_list1.rmRevenue)
        tot_avrgrevenue =  to_decimal(tot_avrgrevenue) + to_decimal(output_list1.avrgRevenue)
        tot_zinr = tot_zinr + tot_room


    output_list1 = Output_list1()
    output_list1_data.append(output_list1)

    counter = counter + 1
    output_list1.counter = counter
    output_list1.sdate = "T O T A L"
    output_list1.smonth = curr_month
    output_list1.rmsold = tot_rmsold
    output_list1.ooo = tot_ooo
    output_list1.comp = tot_comp
    output_list1.houseuse = tot_houseuse
    output_list1.rmrevenue =  to_decimal(tot_rmrevenue)
    output_list1.avrgrevenue =  to_decimal(output_list1.rmRevenue) / to_decimal(output_list1.rmSold)
    output_list1.percent_occ =  to_decimal(output_list1.rmSold) / to_decimal(tot_zinr) * to_decimal("100")

    return generate_output()