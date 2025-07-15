#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
import re
from models import Guest, Waehrung, Htparam, Reservation, Genstat, Nation, Segment, Zimkateg, Sourccod, Res_line, Reslin_queasy, Arrangement, Guest_pr, Queasy, Katpreis

def leadtime_rsv_4bl(fromdate:date, todate:date, from_rsv:string, to_rsv:string, exclude:bool, rm_sharer:bool, check_cdate:bool):

    prepare_cache ([Guest, Waehrung, Htparam, Reservation, Genstat, Nation, Segment, Zimkateg, Sourccod, Res_line, Reslin_queasy, Arrangement, Guest_pr, Katpreis])

    output_list_data = []
    pax:int = 0
    ci_date:date = None
    local_curr:Decimal = to_decimal("0.0")
    foreign_curr:Decimal = to_decimal("0.0")
    curr_foreign:int = 0
    fixed_rate:bool = False
    new_contrate:bool = False
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    bill_date:date = None
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    contcode:string = ""
    ct:string = ""
    curr_zikatnr:int = 0
    rate_found:bool = False
    rm_rate:Decimal = to_decimal("0.0")
    early_flag:bool = False
    kback_flag:bool = False
    it_exist:bool = False
    bonus_array:List[bool] = create_empty_list(999, False)
    w_day:int = 0
    rack_rate:bool = False
    counter:int = 0
    datacount:int = 0
    totaldatacount:int = 0
    tmp_date:date = None
    curr_lead_days:int = 0
    guest = waehrung = htparam = reservation = genstat = nation = segment = zimkateg = sourccod = res_line = reslin_queasy = arrangement = guest_pr = queasy = katpreis = None

    output_list = tot_list = t_guest = bguest = waehrung1 = boutput = tguest = None

    output_list_data, Output_list = create_model("Output_list", {"gastnr":int, "rsvname":string, "guestname":string, "resno":int, "reslinnr":int, "rm_type":string, "create_date":date, "cidate":date, "codate":date, "room_night":int, "lead":Decimal, "argt":string, "currency":string, "rmrate":Decimal, "lodging":Decimal, "avg_rmrate":Decimal, "avg_lodging":Decimal, "rmrate1":Decimal, "lodging1":Decimal, "segment":string, "nation":string, "rm_night":int, "c_resno":string, "c_rmnight":string, "c_lead":string, "c_rmrate":string, "c_lodging":string, "c_avgrmrate":string, "c_avglodging":string, "c_rmrate1":string, "c_lodging1":string, "adult":int, "child":int, "infant":int, "comp":int, "compchild":int, "avrg_lead":Decimal, "avrg_los":Decimal, "pos":int, "tot_reserv":int, "contcode":string, "sourcecode":string, "check_flag":bool, "check_flag1":bool, "check_flag2":bool, "tot_rate":string, "tot_avg_rate":string, "tot_rate1":string, "tot_lodging":string, "tot_avg_lodging":string, "tot_lodging1":string})
    tot_list_data, Tot_list = create_model("Tot_list", {"gastnr":int, "t_lead":Decimal, "t_los":Decimal, "t_reserv":int})

    T_guest = create_buffer("T_guest",Guest)
    Bguest = create_buffer("Bguest",Guest)
    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Boutput = Output_list
    boutput_data = output_list_data

    Tguest = create_buffer("Tguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        return {"output-list": output_list_data}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def create_browse():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")
        t_roomrate:Decimal = to_decimal("0.0")
        t_avg_rmrate:Decimal = to_decimal("0.0")
        t_roomrate1:Decimal = to_decimal("0.0")
        tot_roomrate:Decimal = to_decimal("0.0")
        tot_avg_rmrate:Decimal = to_decimal("0.0")
        tot_roomrate1:Decimal = to_decimal("0.0")
        t_lodg:Decimal = to_decimal("0.0")
        t_avg_lodg:Decimal = to_decimal("0.0")
        t_lodg1:Decimal = to_decimal("0.0")
        tot_lodg:Decimal = to_decimal("0.0")
        tot_avg_lodg:Decimal = to_decimal("0.0")
        tot_lodg1:Decimal = to_decimal("0.0")
        datum = fromdate

        if todate < (ci_date - timedelta(days=1)):
            datum2 = todate
        else:
            datum2 = ci_date - timedelta(days=1)

        if check_cdate:

            genstat_obj_list = {}
            genstat = Genstat()
            reservation = Reservation()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid, Guest.name, Guest._recid, Guest.nation1).join(Reservation,(Reservation.resnr == Genstat.resnr) & (Reservation.resdat >= fromdate) & (Reservation.resdat <= todate)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True
                    output_list.tot_rate = to_string(output_list.room_night * output_list.rmrate, "->>>,>>>,>>>,>>9.99")

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2), sort_by=[("rsvname",False),("create_date",False)]):
                output_list.tot_avg_rate = to_string(to_decimal(output_list.tot_rate) / output_list.room_night, "->>>,>>>,>>>,>>9.99")
                output_list.tot_rate1 = to_string(to_decimal(output_list.tot_rate) / foreign_curr, "->>>,>>>,>>>,>>9.99")

                if foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.betriebsnr, res_line.arrangement, res_line.gastnrmember, res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.zimmer_wunsch, res_line.reserve_int, res_line.reserve_dec, res_line.zipreis, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid in db_session.query(Res_line.betriebsnr, Res_line.arrangement, Res_line.gastnrmember, Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.zimmer_wunsch, Res_line.reserve_int, Res_line.reserve_dec, Res_line.zipreis, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.resdat >= fromdate) & (Reservation.resdat <= todate)).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.resdat, Res_line.resnr.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        for ldatum in date_range(res_line.ankunft,res_line.abreise - 1) :

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin.deci1)


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)


                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in date_range(datum3,datum4) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)


                        output_list.tot_avg_rate = to_string(to_decimal(output_list.tot_rate) / output_list.room_night, "->>>,>>>,>>>,>>9.99")
                        output_list.tot_rate1 = to_string(to_decimal(output_list.tot_rate) / foreign_curr, "->>>,>>>,>>>,>>9.99")
                        output_list.tot_avg_lodging = to_string(to_decimal(output_list.tot_lodging) / output_list.room_night, "->>>,>>>,>>>,>>9.99")
                        output_list.tot_lodging1 = to_string(to_decimal(output_list.tot_lodging) / foreign_curr, "->>>,>>>,>>>,>>9.99")

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)
                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("rsvname",False),("create_date",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    boutput.tot_rate = to_string(t_roomrate, "->>>,>>>,>>>,>>9.99")
                    boutput.tot_rate1 = to_string(t_roomrate1, "->>>,>>>,>>>,>>9.99")
                    boutput.tot_avg_rate = to_string(t_avg_rmrate / t_rmnight, "->>>,>>>,>>>,>>9.99")
                    boutput.tot_lodging = to_string(t_lodg , "->>>,>>>,>>>,>>9.99")
                    boutput.tot_avg_lodging = to_string(t_avg_lodg / t_rmnight , "->>>,>>>,>>>,>>9.99")
                    boutput.tot_lodging1 = to_string(t_lodg1 , "->>>,>>>,>>>,>>9.99")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None and output_list.lead / tot_list.t_lead != 0:

                        if tot_list.t_reserv != None and tot_list.t_reserv != 0:
                            t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )


                        else:
                            t_avrglead =  to_decimal(t_avrglead) + to_decimal("0")


                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None and output_list.room_night / tot_list.t_reserv != 0:

                        if tot_list.t_reserv != None and tot_list.t_reserv != 0:
                            t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )


                        else:
                            t_avrglos =  to_decimal(t_avrglos) + to_decimal("0")


                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_roomrate =  to_decimal(tot_roomrate) + to_decimal(to_decimal(output_list.tot_rate) )
                tot_roomrate1 =  to_decimal(tot_roomrate1) + to_decimal(to_decimal(output_list.tot_rate1) )
                tot_avg_rmrate =  to_decimal(tot_avg_rmrate) + to_decimal(to_decimal(output_list.avg_rmrate) )
                tot_lodg =  to_decimal(tot_lodg) + to_decimal(to_decimal(output_list.tot_lodging) )
                tot_avg_lodg =  to_decimal(tot_avg_lodg) + to_decimal(to_decimal(output_list.tot_avg_lodging) )
                tot_lodg1 =  to_decimal(tot_lodg1) + to_decimal(to_decimal(output_list.tot_lodging1) )
                output_list.check_flag1 = False


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = t_gastnr
            output_list.rsvname = "T O T A L"
            output_list.lead =  to_decimal(t_lead)
            output_list.lodging =  to_decimal(t_lodging)
            output_list.lodging1 =  to_decimal(t_lodging1)
            output_list.room_night = t_los
            output_list.rm_night = t_rmnight
            output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
            output_list.adult = t_adult
            output_list.child = t_child
            output_list.infant = t_infant
            output_list.comp = t_comp
            output_list.compchild = t_compchild
            output_list.avrg_lead =  to_decimal(t_avrglead)
            output_list.avrg_los =  to_decimal(t_avrglos)
            output_list.rmrate =  to_decimal(t_rmrate)
            output_list.rmrate1 =  to_decimal(t_rmrate1)
            output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
            output_list.tot_rate = to_string(t_roomrate, "->>>,>>>,>>>,>>9.99")
            output_list.tot_rate1 = to_string(t_roomrate1, "->>>,>>>,>>>,>>9.99")
            output_list.tot_avg_rate = to_string(t_avg_rmrate / t_rmnight, "->>>,>>>,>>>,>>9.99")
            output_list.tot_lodging = to_string(t_lodg, "->>>,>>>,>>>,>>9.99")
            output_list.tot_avg_lodging = to_string(t_avg_lodg / t_rmnight, "->>>,>>>,>>>,>>9.99")
            output_list.tot_lodging1 = to_string(t_lodg1, "->>>,>>>,>>>,>>9.99")
            output_list.check_flag = True

            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

            if tot_list:
                output_list.tot_reserv = tot_list.t_reserv

            for tot_list in query(tot_list_data):
                tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = 999999999
            output_list.rsvname = "Grand T O T A L"
            output_list.lead =  to_decimal(tot_lead)
            output_list.lodging =  to_decimal(tot_lodging)
            output_list.lodging1 =  to_decimal(tot_lodging1)
            output_list.room_night = tot_los
            output_list.rm_night = tot_rmnight
            output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
            output_list.adult = tot_adult
            output_list.child = tot_child
            output_list.infant = tot_infant
            output_list.comp = tot_comp
            output_list.compchild = tot_compchild
            output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
            output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
            output_list.rmrate =  to_decimal(tot_rmrate)
            output_list.rmrate1 =  to_decimal(tot_rmrate1)
            output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
            output_list.tot_reserv = tot_rsv
            output_list.tot_rate = to_string(tot_roomrate, "->>>,>>>,>>>,>>9.99")
            output_list.tot_rate1 = to_string(tot_roomrate1, "->>>,>>>,>>>,>>9.99")
            output_list.tot_avg_rate = to_string(tot_avg_rmrate / tot_rmnight, "->>>,>>>,>>>,>>9.99")
            output_list.tot_lodging = to_string(tot_lodg, "->>>,>>>,>>>,>>9.99")
            output_list.tot_avg_lodging = to_string(tot_avg_lodg / tot_rmnight, "->>>,>>>,>>>,>>9.99")
            output_list.tot_lodging1 = to_string(tot_lodg1, "->>>,>>>,>>>,>>9.99")
            output_list.check_flag = True


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Guest.name, Guest._recid, Guest.nation1).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_date[0] >= datum) & (Genstat.res_date[0] <= datum2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2)):

                if foreign_curr != None and foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                         (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:

                        if from_rsv != "" and to_rsv != "":

                            tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                            if not tguest:
                                continue

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = (res_line.abreise - res_line.ankunft).days
                            output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                            output_list.argt = res_line.arrangement
                            output_list.rmrate =  to_decimal(res_line.zipreis)
                            output_list.create_date = reservation.resdat
                            curr_lead_days = (res_line.ankunft - reservation.resdat).days
                            output_list.lead =  to_decimal(curr_lead_days)
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]
                            output_list.check_flag = True
                            output_list.check_flag1 = True
                            output_list.check_flag2 = True

                            bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if bguest:

                                nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                                if nation:
                                    output_list.nation = nation.bezeich

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                            if segment:
                                output_list.segment = segment.bezeich

                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                            if reslin_queasy:

                                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in date_range(datum3,datum4) :
                                pax = res_line.erwachs
                                net_lodg =  to_decimal("0")
                                curr_i = curr_i + 1

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                                if not fixed_rate:

                                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                    if guest_pr:
                                        contcode = guest_pr.code
                                        ct = res_line.zimmer_wunsch

                                        if matches(ct,r"*$CODE$*"):
                                            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                            contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate =  to_decimal("0")
                                        output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate =  to_decimal(res_line.zipreis)

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate)


                            else:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                            if foreign_curr != None and foreign_curr != 0:
                                output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                            else:
                                output_list.lodging1 =  to_decimal("0")

                            if output_list.room_night != None and output_list.room_night != 0:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                                output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                            else:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                                output_list.avg_lodging =  to_decimal(output_list.lodging)


                            tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                            tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                            tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_data.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                            tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead != 0 and output_list.lead != None:

                        if output_list.lead / tot_list.t_lead != None:
                            t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                            tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = t_gastnr
            output_list.rsvname = "T O T A L"
            output_list.lead =  to_decimal(t_lead)
            output_list.lodging =  to_decimal(t_lodging)
            output_list.lodging1 =  to_decimal(t_lodging1)
            output_list.room_night = t_los
            output_list.rm_night = t_rmnight
            output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
            output_list.adult = t_adult
            output_list.child = t_child
            output_list.infant = t_infant
            output_list.comp = t_comp
            output_list.compchild = t_compchild
            output_list.avrg_lead =  to_decimal(t_avrglead)
            output_list.avrg_los =  to_decimal(t_avrglos)
            output_list.rmrate =  to_decimal(t_rmrate)
            output_list.rmrate1 =  to_decimal(t_rmrate1)
            output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
            output_list.check_flag = True

            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

            if tot_list:
                output_list.tot_reserv = tot_list.t_reserv

            for tot_list in query(tot_list_data):
                tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = 999999999
            output_list.rsvname = "Grand T O T A L"
            output_list.lead =  to_decimal(tot_lead)
            output_list.lodging =  to_decimal(tot_lodging)
            output_list.lodging1 =  to_decimal(tot_lodging1)
            output_list.room_night = tot_los
            output_list.rm_night = tot_rmnight
            output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
            output_list.adult = tot_adult
            output_list.child = tot_child
            output_list.infant = tot_infant
            output_list.comp = tot_comp
            output_list.compchild = tot_compchild
            output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
            output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
            output_list.rmrate =  to_decimal(tot_rmrate)
            output_list.rmrate1 =  to_decimal(tot_rmrate1)
            output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
            output_list.tot_reserv = tot_rsv
            output_list.check_flag = True


    def create_browse1():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")

        if check_cdate:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.betriebsnr, res_line.arrangement, res_line.gastnrmember, res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.zimmer_wunsch, res_line.reserve_int, res_line.reserve_dec, res_line.zipreis, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid in db_session.query(Res_line.betriebsnr, Res_line.arrangement, Res_line.gastnrmember, Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.zimmer_wunsch, Res_line.reserve_int, Res_line.reserve_dec, Res_line.zipreis, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.resdat >= fromdate) & (Reservation.resdat <= todate)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.resdat, Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("rsvname",False),("create_date",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        else:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.resno = datacount
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    totaldatacount = totaldatacount + datacount
                    datacount = 0
                    boutput.check_flag = True

                    if t_rmnight != None and t_rmnight != 0:

                        if t_avrlodging != None and t_avrlodging != 0:
                            boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)

                        if t_avrgrmrate != None and t_avrgrmrate != 0:
                            boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv


                datacount = datacount + 1

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.resno = datacount
        output_list.lead =  to_decimal(t_lead)
        output_list.lodging =  to_decimal(t_lodging)
        output_list.lodging1 =  to_decimal(t_lodging1)
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead =  to_decimal(t_avrglead)
        output_list.avrg_los =  to_decimal(t_avrglos)
        output_list.rmrate =  to_decimal(t_rmrate)
        output_list.rmrate1 =  to_decimal(t_rmrate1)
        output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
        totaldatacount = totaldatacount + datacount
        datacount = 0
        output_list.check_flag = True

        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_data):
            tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.resno = totaldatacount
        output_list.lead =  to_decimal(tot_lead)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.lodging1 =  to_decimal(tot_lodging1)
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
        output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
        output_list.rmrate =  to_decimal(tot_rmrate)
        output_list.rmrate1 =  to_decimal(tot_rmrate1)
        output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
        output_list.tot_reserv = tot_rsv
        totaldatacount = 0
        output_list.check_flag = True


    def create_browse_exclude():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")
        datum = fromdate

        if todate < (ci_date - timedelta(days=1)):
            datum2 = todate
        else:
            datum2 = ci_date - timedelta(days=1)

        if check_cdate:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Guest.name, Guest._recid, Guest.nation1).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                reservation = get_cache (Reservation, {"resdat": [(ge, fromdate),(le, todate)],"resnr": [(eq, genstat.resnr)]})

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2), sort_by=[("create_date",False)]):

                if foreign_curr != None and foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            for res_line in db_session.query(Res_line).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] > 1)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.rmrate =  to_decimal(res_line.zipreis)
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in date_range(datum3,datum4) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("rsvname",False),("create_date",False),("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Guest.name, Guest._recid, Guest.nation1).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_date[0] >= datum) & (Genstat.res_date[0] <= datum2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2)):

                if foreign_curr != None and foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                         (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] > 1)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:

                        if from_rsv != "" and to_rsv != "":

                            tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                            if not tguest:
                                continue

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = (res_line.abreise - res_line.ankunft).days
                            output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                            output_list.argt = res_line.arrangement
                            output_list.rmrate =  to_decimal(res_line.zipreis)
                            output_list.create_date = reservation.resdat
                            curr_lead_days = (res_line.ankunft - reservation.resdat).days
                            output_list.lead =  to_decimal(curr_lead_days)
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]
                            output_list.check_flag = True
                            output_list.check_flag1 = True
                            output_list.check_flag2 = True

                            bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if bguest:

                                nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                                if nation:
                                    output_list.nation = nation.bezeich

                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                            if segment:
                                output_list.segment = segment.bezeich

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                            if reslin_queasy:

                                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in date_range(datum3,datum4) :
                                pax = res_line.erwachs
                                net_lodg =  to_decimal("0")
                                curr_i = curr_i + 1

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                                if not fixed_rate:

                                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                    if guest_pr:
                                        contcode = guest_pr.code
                                        ct = res_line.zimmer_wunsch

                                        if matches(ct,r"*$CODE$*"):
                                            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                            contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate =  to_decimal("0")
                                        output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate =  to_decimal(res_line.zipreis)

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate)


                            else:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                            if foreign_curr != None and foreign_curr != 0:
                                output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                            else:
                                output_list.lodging1 =  to_decimal("0")

                            if output_list.room_night != None and output_list.room_night != 0:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                                output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                            else:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                                output_list.avg_lodging =  to_decimal(output_list.lodging)


                            tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                            tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                            tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_data.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                            tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead =  to_decimal(t_lead)
        output_list.lodging =  to_decimal(t_lodging)
        output_list.lodging1 =  to_decimal(t_lodging1)
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead =  to_decimal(t_avrglead)
        output_list.avrg_los =  to_decimal(t_avrglos)
        output_list.rmrate =  to_decimal(t_rmrate)
        output_list.rmrate1 =  to_decimal(t_rmrate1)
        output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
        output_list.check_flag = True

        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_data):
            tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead =  to_decimal(tot_lead)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.lodging1 =  to_decimal(tot_lodging1)
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
        output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
        output_list.rmrate =  to_decimal(tot_rmrate)
        output_list.rmrate1 =  to_decimal(tot_rmrate1)
        output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
        output_list.tot_reserv = tot_rsv
        output_list.check_flag = True


    def create_browse_exclude1():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")

        if check_cdate:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.betriebsnr, res_line.arrangement, res_line.gastnrmember, res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.zimmer_wunsch, res_line.reserve_int, res_line.reserve_dec, res_line.zipreis, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid in db_session.query(Res_line.betriebsnr, Res_line.arrangement, Res_line.gastnrmember, Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.zimmer_wunsch, Res_line.reserve_int, Res_line.reserve_dec, Res_line.zipreis, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resdat >= fromdate) & (Reservation.resdat <= todate) & (Reservation.resnr == Res_line.resnr)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] > 1)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)


                        output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)
                        output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                        output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging =  to_decimal(output_list.lodging)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("create_date",False),("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead != 0 and output_list.lead != None:

                        if output_list.lead / tot_list.t_lead != None:
                            t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                            tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        else:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] > 1)).order_by(Res_line.resnr).all():
                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead =  to_decimal(t_lead)
        output_list.lodging =  to_decimal(t_lodging)
        output_list.lodging1 =  to_decimal(t_lodging1)
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead =  to_decimal(t_avrglead)
        output_list.avrg_los =  to_decimal(t_avrglos)
        output_list.rmrate =  to_decimal(t_rmrate)
        output_list.rmrate1 =  to_decimal(t_rmrate1)
        output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
        output_list.check_flag = True

        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_data):
            tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead =  to_decimal(tot_lead)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.lodging1 =  to_decimal(tot_lodging1)
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
        output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
        output_list.rmrate =  to_decimal(tot_rmrate)
        output_list.rmrate1 =  to_decimal(tot_rmrate1)
        output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
        output_list.tot_reserv = tot_rsv
        output_list.check_flag = True


    def create_browse_rm_sharer():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")
        datum = fromdate

        if todate < (ci_date - timedelta(days=1)):
            datum2 = todate
        else:
            datum2 = ci_date - timedelta(days=1)

        if check_cdate:

            genstat_obj_list = {}
            genstat = Genstat()
            reservation = Reservation()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid, Guest.name, Guest._recid, Guest.nation1).join(Reservation,(Reservation.resdat >= fromdate) & (Reservation.resdat <= todate) & (Reservation.gastnr == Genstat.gastnr)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_date[0] >= datum) & (Genstat.res_date[0] <= datum2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ") & (Genstat.resstatus != 13)).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2), sort_by=[("create_date",False)]):

                if foreign_curr != None and foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.betriebsnr, res_line.arrangement, res_line.gastnrmember, res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.zimmer_wunsch, res_line.reserve_int, res_line.reserve_dec, res_line.zipreis, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid in db_session.query(Res_line.betriebsnr, Res_line.arrangement, Res_line.gastnrmember, Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.zimmer_wunsch, Res_line.reserve_int, Res_line.reserve_dec, Res_line.zipreis, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resdat >= fromdate) & (Reservation.resdat <= todate) & (Reservation.resnr == Res_line.resnr)).filter(
                     (((Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.active_flag <= 1))) | ((Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.rmrate =  to_decimal(res_line.zipreis)
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in date_range(datum3,datum4) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("create_date",False),("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.argt, genstat.zipreis, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.gastnrmember, genstat.segmentcode, genstat.zikatnr, genstat._recid, guest.name, guest._recid, guest.nation1 in db_session.query(Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.argt, Genstat.zipreis, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.gastnrmember, Genstat.segmentcode, Genstat.zikatnr, Genstat._recid, Guest.name, Guest._recid, Guest.nation1).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.res_date[0] >= datum) & (Genstat.res_date[0] <= datum2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ") & (Genstat.resstatus != 13)).order_by(Genstat.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if from_rsv != "" and to_rsv != "":

                    tguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                    if not tguest:
                        continue

                reservation = get_cache (Reservation, {"gastnr": [(eq, genstat.gastnr)]})

                output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.rm_night = (genstat.res_date[1] - genstat.res_date[0]).days
                    output_list.argt = genstat.argt
                    output_list.rmrate =  to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(genstat.logis)
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3
                    output_list.check_flag = True
                    output_list.check_flag1 = True
                    output_list.check_flag2 = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    if bguest:

                        nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                        if nation:
                            output_list.nation = nation.bezeich

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if segment:
                        output_list.segment = segment.bezeich

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead =  to_decimal(genstat.res_date[0]) - to_decimal(reservation.resdat)

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(genstat.zipreis)

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(genstat.zipreis)
                    output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag2)):

                if foreign_curr != None and foreign_curr != 0:
                    output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)
                    output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                else:
                    output_list.rmrate1 =  to_decimal("0")
                    output_list.lodging1 =  to_decimal("0")

                if output_list.room_night != None and output_list.room_night != 0:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                    output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                else:
                    output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                    output_list.avg_lodging =  to_decimal(output_list.lodging)


                tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_data.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                tot_list.t_reserv = tot_list.t_reserv + 1
                output_list.check_flag2 = False


            datum2 = datum2 + timedelta(days=1)

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                         (((Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.active_flag <= 1) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate))) | ((Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:

                        if from_rsv != "" and to_rsv != "":

                            tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                            if not tguest:
                                continue

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = (res_line.abreise - res_line.ankunft).days
                            output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                            output_list.argt = res_line.arrangement
                            output_list.rmrate =  to_decimal(res_line.zipreis)
                            output_list.create_date = reservation.resdat
                            curr_lead_days = (res_line.ankunft - reservation.resdat).days
                            output_list.lead =  to_decimal(curr_lead_days)
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]
                            output_list.check_flag = True
                            output_list.check_flag1 = True
                            output_list.check_flag2 = True

                            bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if bguest:

                                nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                                if nation:
                                    output_list.nation = nation.bezeich

                            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                            if segment:
                                output_list.segment = segment.bezeich

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                            if reslin_queasy:

                                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in date_range(datum3,datum4) :
                                pax = res_line.erwachs
                                net_lodg =  to_decimal("0")
                                curr_i = curr_i + 1

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                                if not fixed_rate:

                                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                    if guest_pr:
                                        contcode = guest_pr.code
                                        ct = res_line.zimmer_wunsch

                                        if matches(ct,r"*$CODE$*"):
                                            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                            contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate =  to_decimal("0")
                                        output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate =  to_decimal(res_line.zipreis)

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                        if not katpreis:

                                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate)


                            else:
                                output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                            if foreign_curr != None and foreign_curr != 0:
                                output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                            else:
                                output_list.lodging1 =  to_decimal("0")

                            if output_list.room_night != None and output_list.room_night != 0:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                                output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                            else:
                                output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                                output_list.avg_lodging =  to_decimal(output_list.lodging)


                            tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                            tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                            tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_data.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                            tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead =  to_decimal(t_lead)
        output_list.lodging =  to_decimal(t_lodging)
        output_list.lodging1 =  to_decimal(t_lodging1)
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead =  to_decimal(t_avrglead)
        output_list.avrg_los =  to_decimal(t_avrglos)
        output_list.rmrate =  to_decimal(t_rmrate)
        output_list.rmrate1 =  to_decimal(t_rmrate1)
        output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
        output_list.check_flag = True

        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_data):
            tot_rsv =  to_decimal(tot_rsv) + to_decimal(tot_list.t_reserv)


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead =  to_decimal(tot_lead)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.lodging1 =  to_decimal(tot_lodging1)
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging =  to_decimal(tot_avrlodging) / to_decimal(tot_rmnight)
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead =  to_decimal(tot_avrglead) / to_decimal(tot_rsv)
        output_list.avrg_los =  to_decimal(tot_avrglos) / to_decimal(tot_rsv)
        output_list.rmrate =  to_decimal(tot_rmrate)
        output_list.rmrate1 =  to_decimal(tot_rmrate1)
        output_list.avg_rmrate =  to_decimal(tot_avrgrmrate) / to_decimal(tot_rmnight)
        output_list.tot_reserv = tot_rsv
        output_list.check_flag = True


    def create_browse_rm_sharer1():

        nonlocal output_list_data, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, datacount, totaldatacount, tmp_date, curr_lead_days, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, arrangement, guest_pr, queasy, katpreis
        nonlocal fromdate, todate, from_rsv, to_rsv, exclude, rm_sharer, check_cdate
        nonlocal t_guest, bguest, waehrung1, boutput, tguest


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput, tguest
        nonlocal output_list_data, tot_list_data

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
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
        tot_lead:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_lodging1:Decimal = to_decimal("0.0")
        tot_avrlodging:Decimal = to_decimal("0.0")
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:Decimal = to_decimal("0.0")
        t_lodging:Decimal = to_decimal("0.0")
        t_lodging1:Decimal = to_decimal("0.0")
        t_avrlodging:Decimal = to_decimal("0.0")
        t_avrglead:Decimal = to_decimal("0.0")
        t_avrglos:Decimal = to_decimal("0.0")
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:Decimal = to_decimal("0.0")
        tot_avrglos:Decimal = to_decimal("0.0")
        t_rmrate:Decimal = to_decimal("0.0")
        t_rmrate1:Decimal = to_decimal("0.0")
        t_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rmrate:Decimal = to_decimal("0.0")
        tot_rmrate1:Decimal = to_decimal("0.0")
        tot_avrgrmrate:Decimal = to_decimal("0.0")
        tot_rsv:Decimal = to_decimal("0.0")

        if check_cdate:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.betriebsnr, res_line.arrangement, res_line.gastnrmember, res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.zimmer_wunsch, res_line.reserve_int, res_line.reserve_dec, res_line.zipreis, reservation.name, reservation.resart, reservation.resdat, reservation.segmentcode, reservation._recid in db_session.query(Res_line.betriebsnr, Res_line.arrangement, Res_line.gastnrmember, Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.zimmer_wunsch, Res_line.reserve_int, Res_line.reserve_dec, Res_line.zipreis, Reservation.name, Reservation.resart, Reservation.resdat, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resdat >= fromdate) & (Reservation.resdat <= todate) & (Reservation.resnr == Res_line.resnr)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13)) | ((Res_line.active_flag == 2) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("create_date",False),("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        else:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft >= fromdate) & (Res_line.ankunft <= todate)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 11) & (Res_line.resstatus != 13) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                curr_i = 0
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")
                ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
                kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:

                    if from_rsv != "" and to_rsv != "":

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)],"name": [(ge, from_rsv),(le, to_rsv)]})

                        if not tguest:
                            continue

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    output_list = query(output_list_data, filters=(lambda output_list: output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = (res_line.abreise - res_line.ankunft).days
                        output_list.rm_night = (res_line.abreise - res_line.ankunft).days
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        curr_lead_days = (res_line.ankunft - reservation.resdat).days
                        output_list.lead =  to_decimal(curr_lead_days)
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]
                        output_list.check_flag = True
                        output_list.check_flag1 = True
                        output_list.check_flag2 = True

                        bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if bguest:

                            nation = get_cache (Nation, {"kurzbez": [(eq, bguest.nation1)]})

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment:
                            output_list.segment = segment.bezeich

                        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                        if reslin_queasy:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        tmp_date = res_line.abreise - timedelta(days=1)
                        for ldatum in date_range(res_line.ankunft,tmp_date) :
                            pax = res_line.erwachs
                            net_lodg =  to_decimal("0")
                            curr_i = curr_i + 1

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, ldatum)],"date2": [(ge, ldatum)]})

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(reslin_queasy.deci1)

                            if not fixed_rate:

                                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                                if guest_pr:
                                    contcode = guest_pr.code
                                    ct = res_line.zimmer_wunsch

                                    if matches(ct,r"*$CODE$*"):
                                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                        contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate =  to_decimal("0")
                                    output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate =  to_decimal(res_line.zipreis)

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                                    if not katpreis:

                                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
                                output_list.rmrate =  to_decimal(output_list.rmrate) + to_decimal(rm_rate)


                            else:
                                ct = res_line.zimmer_wunsch

                                if matches(ct,r"*$CODE$*"):
                                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                                    contcode = substring(ct, 0, get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(net_lodg)

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate)


                        else:
                            output_list.rmrate1 =  to_decimal(output_list.rmrate) / to_decimal(foreign_curr)

                        if foreign_curr != None and foreign_curr != 0:
                            output_list.lodging1 =  to_decimal(output_list.lodging) / to_decimal(foreign_curr)


                        else:
                            output_list.lodging1 =  to_decimal("0")

                        if output_list.room_night != None and output_list.room_night != 0:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate) / to_decimal(output_list.room_night)
                            output_list.avg_lodging =  to_decimal(output_list.lodging) / to_decimal(output_list.room_night)


                        else:
                            output_list.avg_rmrate =  to_decimal(output_list.rmrate)
                            output_list.avg_lodging =  to_decimal(output_list.lodging)


                        tot_lead =  to_decimal(tot_lead) + to_decimal(output_list.lead)
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                        tot_lodging1 =  to_decimal(tot_lodging1) + to_decimal(output_list.lodging1)
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging =  to_decimal(tot_avrlodging) + to_decimal(output_list.lodging)
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_data.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead =  to_decimal(tot_list.t_lead) + to_decimal(output_list.lead)
                        tot_list.t_los =  to_decimal(tot_list.t_los) + to_decimal(output_list.room_night)
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag1), sort_by=[("gastnr",False)]):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_data.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead =  to_decimal(t_lead)
                    boutput.lodging =  to_decimal(t_lodging)
                    boutput.lodging1 =  to_decimal(t_lodging1)
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead =  to_decimal(t_avrglead)
                    boutput.avrg_los =  to_decimal(t_avrglos)
                    boutput.pos = counter
                    boutput.rmrate =  to_decimal(t_rmrate)
                    boutput.rmrate1 =  to_decimal(t_rmrate1)
                    boutput.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
                    t_rmrate =  to_decimal("0")
                    t_rmrate1 =  to_decimal("0")
                    t_avrgrmrate =  to_decimal("0")
                    t_lead =  to_decimal("0")
                    t_lodging =  to_decimal("0")
                    t_lodging1 =  to_decimal("0")
                    t_avrlodging =  to_decimal("0")
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead =  to_decimal("0")
                    t_avrglos =  to_decimal("0")
                    counter = counter + 1
                    boutput.check_flag = True

                    tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead =  to_decimal(output_list.lead)
                    output_list.avrg_los =  to_decimal(output_list.room_night)

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead =  to_decimal(t_avrglead) + to_decimal((output_list.lead) / to_decimal(tot_list.t_reserv) )
                        tot_avrglead =  to_decimal(tot_avrglead) + to_decimal(output_list.lead)

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos =  to_decimal(t_avrglos) + to_decimal((output_list.room_night) / to_decimal(tot_list.t_reserv) )
                        tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.room_night)


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead =  to_decimal(t_lead) + to_decimal(output_list.lead)
                t_lodging =  to_decimal(t_lodging) + to_decimal(output_list.lodging)
                t_lodging1 =  to_decimal(t_lodging1) + to_decimal(output_list.lodging1)
                t_avrlodging =  to_decimal(t_avrlodging) + to_decimal(output_list.lodging)
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos =  to_decimal(t_avrglos) + to_decimal(output_list.avrg_los)
                tot_avrglos =  to_decimal(tot_avrglos) + to_decimal(output_list.avrg_los)
                t_rmrate =  to_decimal(t_rmrate) + to_decimal(output_list.rmrate)
                t_rmrate1 =  to_decimal(t_rmrate1) + to_decimal(output_list.rmrate1)
                t_avrgrmrate =  to_decimal(t_avrgrmrate) + to_decimal(output_list.rmrate)
                tot_rmrate =  to_decimal(tot_rmrate) + to_decimal(output_list.rmrate)
                tot_rmrate1 =  to_decimal(tot_rmrate1) + to_decimal(output_list.rmrate1)
                tot_avrgrmrate =  to_decimal(tot_avrgrmrate) + to_decimal(output_list.rmrate)
                output_list.check_flag1 = False


        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead =  to_decimal(t_lead)
        output_list.lodging =  to_decimal(t_lodging)
        output_list.lodging1 =  to_decimal(t_lodging1)
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging =  to_decimal(t_avrlodging) / to_decimal(t_rmnight)
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead =  to_decimal(t_avrglead)
        output_list.avrg_los =  to_decimal(t_avrglos)
        output_list.rmrate =  to_decimal(t_rmrate)
        output_list.rmrate1 =  to_decimal(t_rmrate1)
        output_list.avg_rmrate =  to_decimal(t_avrgrmrate) / to_decimal(t_rmnight)
        output_list.check_flag = True

        tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung1:
        local_curr =  to_decimal(waehrung1.ankauf)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung1:
        foreign_curr =  to_decimal(waehrung1.ankauf)
        curr_foreign = waehrung1.waehrungsnr

    if fromdate < ci_date:
        create_browse()

    elif fromdate < ci_date and exclude :
        create_browse_exclude()

    elif fromdate >= ci_date and exclude :
        create_browse_exclude1()

    elif fromdate < ci_date and rm_sharer :
        create_browse_rm_sharer()

    elif fromdate >= ci_date and rm_sharer :
        create_browse_rm_sharer1()
    else:
        create_browse1()

    for output_list in query(output_list_data, filters=(lambda output_list: output_list.check_flag)):

        if output_list.resno == 0:
            output_list.c_resno = " "
        else:
            output_list.c_resno = to_string(output_list.resno, ">>>>>>>>9")

        if output_list.room_night == 0:
            output_list.c_rmnight = " "
        else:
            output_list.c_rmnight = to_string(output_list.room_night, ">>>9")

        if output_list.lead == 0:
            output_list.c_lead = " "
        else:
            output_list.c_lead = to_string(output_list.lead, "->,>>>9.99")

        if output_list.rmrate == 0:
            output_list.c_rmrate = " "
        else:
            output_list.c_rmrate = to_string(output_list.rmrate, "->>>,>>>,>>>,>>9.99")

        if output_list.lodging == 0:
            output_list.c_lodging = " "
        else:
            output_list.c_lodging = to_string(output_list.lodging, "->>>,>>>,>>>,>>9.99")

        if output_list.rmrate1 == 0:
            output_list.c_rmrate1 = " "
        else:
            output_list.c_rmrate1 = to_string(output_list.rmrate1, "->>>,>>>,>>>,>>9.99")

        if output_list.lodging1 == 0:
            output_list.c_lodging1 = " "
        else:
            output_list.c_lodging1 = to_string(output_list.lodging1, "->>>,>>>,>>>,>>9.99")

        if output_list.avg_rmrate == 0:
            output_list.c_avgrmrate = " "
        else:
            output_list.c_avgrmrate = to_string(output_list.avg_rmrate, "->>>,>>>,>>>,>>9.99")

        if output_list.avrg_lead == None:
            output_list.avrg_lead =  to_decimal("0")

        if output_list.avrg_los == None:
            output_list.avrg_los =  to_decimal("0")

        if output_list.rmrate == 0:
            output_list.tot_rate = " "
        else:
            output_list.tot_rate = to_string(output_list.rmrate, "->>>,>>>,>>>,>>9.99")

        if output_list.lodging == 0:
            output_list.tot_lodging = " "
        else:
            output_list.tot_lodging = to_string(output_list.lodging, "->>>,>>>,>>>,>>9.99")

        if output_list.avg_rmrate == 0:
            output_list.tot_avg_rate = " "
        else:
            output_list.tot_avg_rate = to_string(output_list.avg_rmrate, "->>>,>>>,>>>,>>9.99")

        if output_list.avg_lodging == 0:
            output_list.tot_avg_lodging = " "
        else:
            output_list.tot_avg_lodging = to_string(output_list.avg_lodging, "->>>,>>>,>>>,>>9.99")

        if output_list.rmrate1 == 0:
            output_list.tot_rate1 = " "
        else:
            output_list.tot_rate1 = to_string(output_list.rmrate1, "->>>,>>>,>>>,>>9.99")

        if output_list.lodging1 == 0:
            output_list.tot_lodging1 = " "
        else:
            output_list.tot_lodging1 = to_string(output_list.lodging1, "->>>,>>>,>>>,>>9.99")
        output_list.check_flag = False

    return generate_output()