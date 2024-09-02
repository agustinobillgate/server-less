from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Waehrung, Htparam, Reservation, Genstat, Nation, Segment, Zimkateg, Sourccod, Res_line, Reslin_queasy, Guest_pr, Queasy, Katpreis

def leadtime_rsv_4bl(fromdate:date, todate:date, from_rsv:str, to_rsv:str, exclude:bool, rm_sharer:bool, check_cdate:bool):
    output_list_list = []
    pax:int = 0
    ci_date:date = None
    local_curr:decimal = 0
    foreign_curr:decimal = 0
    curr_foreign:int = 0
    fixed_rate:bool = False
    new_contrate:bool = False
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    bill_date:date = None
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    contcode:str = ""
    ct:str = ""
    curr_zikatnr:int = 0
    rate_found:bool = False
    rm_rate:decimal = 0
    early_flag:bool = False
    kback_flag:bool = False
    it_exist:bool = False
    bonus_array:[bool] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    w_day:int = 0
    rack_rate:bool = False
    counter:int = 0
    guest = waehrung = htparam = reservation = genstat = nation = segment = zimkateg = sourccod = res_line = reslin_queasy = guest_pr = queasy = katpreis = None

    output_list = tot_list = t_guest = bguest = waehrung1 = boutput = None

    output_list_list, Output_list = create_model("Output_list", {"gastnr":int, "rsvname":str, "guestname":str, "resno":int, "reslinnr":int, "rm_type":str, "create_date":date, "cidate":date, "codate":date, "room_night":int, "lead":decimal, "argt":str, "currency":str, "rmrate":decimal, "lodging":decimal, "avg_rmrate":decimal, "avg_lodging":decimal, "rmrate1":decimal, "lodging1":decimal, "segment":str, "nation":str, "rm_night":int, "c_resno":str, "c_rmnight":str, "c_lead":str, "c_rmrate":str, "c_lodging":str, "c_avgrmrate":str, "c_avglodging":str, "c_rmrate1":str, "c_lodging1":str, "adult":int, "child":int, "infant":int, "comp":int, "compchild":int, "avrg_lead":decimal, "avrg_los":decimal, "pos":int, "tot_reserv":int, "contcode":str, "sourcecode":str})
    tot_list_list, Tot_list = create_model("Tot_list", {"gastnr":int, "t_lead":decimal, "t_los":decimal, "t_reserv":int})

    T_guest = Guest
    Bguest = Guest
    Waehrung1 = Waehrung
    Boutput = Output_list
    boutput_list = output_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list
        return {"output-list": output_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def create_browse():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0
        datum = fromdate

        if todate < (ci_date - 1):
            datum2 = todate
        else:
            datum2 = ci_date - 1

        if check_cdate:

            genstat_obj_list = []
            for genstat, reservation, guest in db_session.query(Genstat, Reservation, Guest).join(Reservation,(Reservation.resnr == Genstat.resnr) &  (Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate)).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_logic[1]) &  (Genstat.zinr != " ")).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.rmrate = res_line.zipreis
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(datum3,datum4 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


            output_list = Output_list()
            output_list_list.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = t_gastnr
            output_list.rsvname = "T O T A L"
            output_list.lead = t_lead
            output_list.lodging = t_lodging
            output_list.lodging1 = t_lodging1
            output_list.room_night = t_los
            output_list.rm_night = t_rmnight
            output_list.avg_lodging = t_avrlodging / t_rmnight
            output_list.adult = t_adult
            output_list.child = t_child
            output_list.infant = t_infant
            output_list.comp = t_comp
            output_list.compchild = t_compchild
            output_list.avrg_lead = t_avrglead
            output_list.avrg_los = t_avrglos
            output_list.rmrate = t_rmrate
            output_list.rmrate1 = t_rmrate1
            output_list.avg_rmrate = t_avrgrmrate / t_rmnight

            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

            if tot_list:
                output_list.tot_reserv = tot_list.t_reserv

            for tot_list in query(tot_list_list):
                tot_rsv = tot_rsv + tot_list.t_reserv


            output_list = Output_list()
            output_list_list.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = 999999999
            output_list.rsvname = "Grand T O T A L"
            output_list.lead = tot_lead
            output_list.lodging = tot_lodging
            output_list.lodging1 = tot_lodging1
            output_list.room_night = tot_los
            output_list.rm_night = tot_rmnight
            output_list.avg_lodging = tot_avrlodging / tot_rmnight
            output_list.adult = tot_adult
            output_list.child = tot_child
            output_list.infant = tot_infant
            output_list.comp = tot_comp
            output_list.compchild = tot_compchild
            output_list.avrg_lead = tot_avrglead / tot_rsv
            output_list.avrg_los = tot_avrglos / tot_rsv
            output_list.rmrate = tot_rmrate
            output_list.rmrate1 = tot_rmrate1
            output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
            output_list.tot_reserv = tot_rsv


        else:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_date[0] >= datum) &  (Genstat.res_date[0] <= datum2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != " ")).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == genstat.resnr)).first()

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                        (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                    if guest:

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = res_line.abreise - res_line.ankunft
                            output_list.rm_night = res_line.abreise - res_line.ankunft
                            output_list.argt = res_line.arrangement
                            output_list.rmrate = res_line.zipreis
                            output_list.create_date = reservation.resdat
                            output_list.lead = res_line.ankunft - reservation.resdat
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]

                            bguest = db_session.query(Bguest).filter(
                                    (Bguest.gastnr == res_line.gastnrmember)).first()

                            if bguest:

                                nation = db_session.query(Nation).filter(
                                        (Nation.kurzbez == bguest.nation1)).first()

                                if nation:
                                    output_list.nation = nation.bezeich

                            segment = db_session.query(Segment).filter(
                                    (Segment.segmentcode == reservation.segmentcode)).first()

                            if segment:
                                output_list.segment = segment.bezeich

                            sourccod = db_session.query(Sourccod).filter(
                                    (Sourccod.source_code == reservation.resart)).first()

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            zimkateg = db_session.query(Zimkateg).filter(
                                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                            if reslin_queasy:

                                waehrung = db_session.query(Waehrung).filter(
                                        (Waehrungsnr == res_line.betriebsnr)).first()

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in range(datum3,datum4 + 1) :
                                pax = res_line.erwachs
                                net_lodg = 0
                                curr_i = curr_i + 1

                                reslin_queasy = db_session.query(Reslin_queasy).filter(
                                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                                if not fixed_rate:

                                    guest_pr = db_session.query(Guest_pr).filter(
                                            (Guest_pr.gastnr == res_line.gastnr)).first()

                                    if guest_pr:
                                        contcode = guest_pr.CODE
                                        ct = res_line.zimmer_wunsch

                                        if re.match(".*\$CODE\$.*",ct):
                                            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                            contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = db_session.query(Queasy).filter(
                                                (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                            rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate = 0
                                        output_list.rmrate = output_list.rmrate + rm_rate


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate = res_line.zipreis

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging = output_list.lodging + net_lodg

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 = output_list.rmrate


                            else:
                                output_list.rmrate1 = output_list.rmrate / foreign_curr


                            output_list.lodging1 = output_list.lodging / foreign_curr
                            output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                            output_list.avg_lodging = output_list.lodging / output_list.room_night

                            if output_list.avg_rmrate == None:
                                output_list.avg_rmrate = output_list.rmrate

                            if output_list.avg_lodging == None:
                                output_list.avg_lodging = output_list.lodging


                            tot_lead = tot_lead + output_list.lead
                            tot_lodging = tot_lodging + output_list.lodging
                            tot_lodging1 = tot_lodging1 + output_list.lodging1
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging = tot_avrlodging + output_list.lodging
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_list.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead = tot_list.t_lead + output_list.lead
                            tot_list.t_los = tot_list.t_los + output_list.room_night
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


            output_list = Output_list()
            output_list_list.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = t_gastnr
            output_list.rsvname = "T O T A L"
            output_list.lead = t_lead
            output_list.lodging = t_lodging
            output_list.lodging1 = t_lodging1
            output_list.room_night = t_los
            output_list.rm_night = t_rmnight
            output_list.avg_lodging = t_avrlodging / t_rmnight
            output_list.adult = t_adult
            output_list.child = t_child
            output_list.infant = t_infant
            output_list.comp = t_comp
            output_list.compchild = t_compchild
            output_list.avrg_lead = t_avrglead
            output_list.avrg_los = t_avrglos
            output_list.rmrate = t_rmrate
            output_list.rmrate1 = t_rmrate1
            output_list.avg_rmrate = t_avrgrmrate / t_rmnight

            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

            if tot_list:
                output_list.tot_reserv = tot_list.t_reserv

            for tot_list in query(tot_list_list):
                tot_rsv = tot_rsv + tot_list.t_reserv


            output_list = Output_list()
            output_list_list.append(output_list)

            counter = counter + 1
            output_list.pos = counter
            output_list.gastnr = 999999999
            output_list.rsvname = "Grand T O T A L"
            output_list.lead = tot_lead
            output_list.lodging = tot_lodging
            output_list.lodging1 = tot_lodging1
            output_list.room_night = tot_los
            output_list.rm_night = tot_rmnight
            output_list.avg_lodging = tot_avrlodging / tot_rmnight
            output_list.adult = tot_adult
            output_list.child = tot_child
            output_list.infant = tot_infant
            output_list.comp = tot_comp
            output_list.compchild = tot_compchild
            output_list.avrg_lead = tot_avrglead / tot_rsv
            output_list.avrg_los = tot_avrglos / tot_rsv
            output_list.rmrate = tot_rmrate
            output_list.rmrate1 = tot_rmrate1
            output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
            output_list.tot_reserv = tot_rsv

    def create_browse1():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0

        if check_cdate:

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate)).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        else:

            for res_line in db_session.query(Res_line).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead = t_lead
        output_list.lodging = t_lodging
        output_list.lodging1 = t_lodging1
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging = t_avrlodging / t_rmnight
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead = t_avrglead
        output_list.avrg_los = t_avrglos
        output_list.rmrate = t_rmrate
        output_list.rmrate1 = t_rmrate1
        output_list.avg_rmrate = t_avrgrmrate / t_rmnight

        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_list):
            tot_rsv = tot_rsv + tot_list.t_reserv


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead = tot_lead
        output_list.lodging = tot_lodging
        output_list.lodging1 = tot_lodging1
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging = tot_avrlodging / tot_rmnight
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead = tot_avrglead / tot_rsv
        output_list.avrg_los = tot_avrglos / tot_rsv
        output_list.rmrate = tot_rmrate
        output_list.rmrate1 = tot_rmrate1
        output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
        output_list.tot_reserv = tot_rsv

    def create_browse_exclude():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0
        datum = fromdate

        if todate < (ci_date - 1):
            datum2 = todate
        else:
            datum2 = ci_date - 1

        if check_cdate:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_logic[1]) &  (Genstat.zinr != " ")).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate) &  (Reservation.resnr == genstat.resnr)).first()

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            for res_line in db_session.query(Res_line).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] > 1)).all():

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.rmrate = res_line.zipreis
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(datum3,datum4 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        else:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_date[0] >= datum) &  (Genstat.res_date[0] <= datum2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != " ")).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == genstat.resnr)).first()

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                        (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] > 1)).all():

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                    if guest:

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = res_line.abreise - res_line.ankunft
                            output_list.rm_night = res_line.abreise - res_line.ankunft
                            output_list.argt = res_line.arrangement
                            output_list.rmrate = res_line.zipreis
                            output_list.create_date = reservation.resdat
                            output_list.lead = res_line.ankunft - reservation.resdat
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]

                            bguest = db_session.query(Bguest).filter(
                                    (Bguest.gastnr == res_line.gastnrmember)).first()

                            if bguest:

                                nation = db_session.query(Nation).filter(
                                        (Nation.kurzbez == bguest.nation1)).first()

                                if nation:
                                    output_list.nation = nation.bezeich

                            sourccod = db_session.query(Sourccod).filter(
                                    (Sourccod.source_code == reservation.resart)).first()

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            segment = db_session.query(Segment).filter(
                                    (Segment.segmentcode == reservation.segmentcode)).first()

                            if segment:
                                output_list.segment = segment.bezeich

                            zimkateg = db_session.query(Zimkateg).filter(
                                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                            if reslin_queasy:

                                waehrung = db_session.query(Waehrung).filter(
                                        (Waehrungsnr == res_line.betriebsnr)).first()

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in range(datum3,datum4 + 1) :
                                pax = res_line.erwachs
                                net_lodg = 0
                                curr_i = curr_i + 1

                                reslin_queasy = db_session.query(Reslin_queasy).filter(
                                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                                if not fixed_rate:

                                    guest_pr = db_session.query(Guest_pr).filter(
                                            (Guest_pr.gastnr == res_line.gastnr)).first()

                                    if guest_pr:
                                        contcode = guest_pr.CODE
                                        ct = res_line.zimmer_wunsch

                                        if re.match(".*\$CODE\$.*",ct):
                                            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                            contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = db_session.query(Queasy).filter(
                                                (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                            rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate = 0
                                        output_list.rmrate = output_list.rmrate + rm_rate


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate = res_line.zipreis

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging = output_list.lodging + net_lodg

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 = output_list.rmrate


                            else:
                                output_list.rmrate1 = output_list.rmrate / foreign_curr


                            output_list.lodging1 = output_list.lodging / foreign_curr
                            output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                            output_list.avg_lodging = output_list.lodging / output_list.room_night

                            if output_list.avg_rmrate == None:
                                output_list.avg_rmrate = output_list.rmrate

                            if output_list.avg_lodging == None:
                                output_list.avg_lodging = output_list.lodging


                            tot_lead = tot_lead + output_list.lead
                            tot_lodging = tot_lodging + output_list.lodging
                            tot_lodging1 = tot_lodging1 + output_list.lodging1
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging = tot_avrlodging + output_list.lodging
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_list.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead = tot_list.t_lead + output_list.lead
                            tot_list.t_los = tot_list.t_los + output_list.room_night
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead = t_lead
        output_list.lodging = t_lodging
        output_list.lodging1 = t_lodging1
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging = t_avrlodging / t_rmnight
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead = t_avrglead
        output_list.avrg_los = t_avrglos
        output_list.rmrate = t_rmrate
        output_list.rmrate1 = t_rmrate1
        output_list.avg_rmrate = t_avrgrmrate / t_rmnight

        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_list):
            tot_rsv = tot_rsv + tot_list.t_reserv


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead = tot_lead
        output_list.lodging = tot_lodging
        output_list.lodging1 = tot_lodging1
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging = tot_avrlodging / tot_rmnight
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead = tot_avrglead / tot_rsv
        output_list.avrg_los = tot_avrglos / tot_rsv
        output_list.rmrate = tot_rmrate
        output_list.rmrate1 = tot_rmrate1
        output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
        output_list.tot_reserv = tot_rsv

    def create_browse_exclude1():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0

        if check_cdate:

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate) &  (Reservation.resnr == Res_line.resnr)).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] > 1)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        else:

            for res_line in db_session.query(Res_line).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] > 1)).all():
                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead = t_lead
        output_list.lodging = t_lodging
        output_list.lodging1 = t_lodging1
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging = t_avrlodging / t_rmnight
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead = t_avrglead
        output_list.avrg_los = t_avrglos
        output_list.rmrate = t_rmrate
        output_list.rmrate1 = t_rmrate1
        output_list.avg_rmrate = t_avrgrmrate / t_rmnight

        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_list):
            tot_rsv = tot_rsv + tot_list.t_reserv


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead = tot_lead
        output_list.lodging = tot_lodging
        output_list.lodging1 = tot_lodging1
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging = tot_avrlodging / tot_rmnight
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead = tot_avrglead / tot_rsv
        output_list.avrg_los = tot_avrglos / tot_rsv
        output_list.rmrate = tot_rmrate
        output_list.rmrate1 = tot_rmrate1
        output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
        output_list.tot_reserv = tot_rsv

    def create_browse_rm_sharer():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0
        datum = fromdate

        if todate < (ci_date - 1):
            datum2 = todate
        else:
            datum2 = ci_date - 1

        if check_cdate:

            genstat_obj_list = []
            for genstat, reservation, guest in db_session.query(Genstat, Reservation, Guest).join(Reservation,(Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate) &  (Reservation.gastnr == Genstat.gastnr)).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_date[0] >= datum) &  (Genstat.res_date[0] <= datum2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != " ") &  (Genstat.resstatus == 11)).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate) &  (Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus == 11) &  (Res_line.active_flag <= 1))) |  ((Res_line.resstatus == 11) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.rmrate = res_line.zipreis
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = datum2

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(datum3,datum4 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        else:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).filter(
                    (Genstat.res_date[0] >= datum) &  (Genstat.res_date[0] <= datum2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != " ") &  (Genstat.resstatus == 11)).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.gastnr == genstat.gastnr)).first()

                output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == genstat.gastnr and output_list.resno == genstat.resnr and output_list.reslinnr == genstat.res_int[0]), first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gastnr = genstat.gastnr
                    output_list.rsvname = reservation.name
                    output_list.guestname = guest.name
                    output_list.resno = genstat.resnr
                    output_list.reslinnr = genstat.res_int[0]
                    output_list.cidate = genstat.res_date[0]
                    output_list.codate = genstat.res_date[1]
                    output_list.room_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.rm_night = genstat.res_date[1] - genstat.res_date[0]
                    output_list.argt = genstat.argt
                    output_list.rmrate = genstat.zipreis
                    output_list.lodging = genstat.logis
                    output_list.adult = genstat.erwachs
                    output_list.child = genstat.kind1
                    output_list.infant = genstat.kind2
                    output_list.comp = genstat.gratis
                    output_list.compchild = genstat.kind3

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    if bguest:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == bguest.nation1)).first()

                        if nation:
                            output_list.nation = nation.bezeich

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == reservation.resart)).first()

                    if sourccod:
                        output_list.sourcecode = sourccod.bezeich

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == genstat.segmentcode)).first()

                    if segment:
                        output_list.segment = segment.bezeich

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == genstat.zikatnr)).first()

                    if zimkateg:
                        output_list.rm_type = zimkateg.kurzbez

                    if reservation:
                        output_list.create_date = reservation.resdat
                        output_list.lead = genstat.res_date[0] - reservation.resdat

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == genstat.resnr) &  (Reslin_queasy.reslinnr == genstat.res_int[0])).first()

                    if reslin_queasy:

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = genstat.zipreis

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            output_list.currency = waehrung.wabkurz
                else:
                    output_list.rmrate = output_list.rmrate + genstat.zipreis
                    output_list.lodging = output_list.lodging + genstat.logis

            for output_list in query(output_list_list):
                output_list.rmrate1 = output_list.rmrate / foreign_curr
                output_list.lodging1 = output_list.lodging / foreign_curr
                output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                output_list.avg_lodging = output_list.lodging / output_list.room_night

                if output_list.avg_rmrate == None:
                    output_list.avg_rmrate = output_list.rmrate

                if output_list.avg_lodging == None:
                    output_list.avg_lodging = output_list.lodging


                tot_lead = tot_lead + output_list.lead
                tot_lodging = tot_lodging + output_list.lodging
                tot_lodging1 = tot_lodging1 + output_list.lodging1
                tot_los = tot_los + output_list.room_night
                tot_rmnight = tot_rmnight + output_list.rm_night
                tot_avrlodging = tot_avrlodging + output_list.lodging
                tot_adult = tot_adult + output_list.adult
                tot_child = tot_child + output_list.child
                tot_infant = tot_infant + output_list.infant
                tot_comp = tot_comp + output_list.comp
                tot_compchild = tot_compchild + output_list.compchild

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if not tot_list:
                    tot_list = Tot_list()
                    tot_list_list.append(tot_list)

                    tot_list.gastnr = output_list.gastnr


                tot_list.t_lead = tot_list.t_lead + output_list.lead
                tot_list.t_los = tot_list.t_los + output_list.room_night
                tot_list.t_reserv = tot_list.t_reserv + 1


            datum2 = datum2 + 1

            if todate >= ci_date:

                for res_line in db_session.query(Res_line).filter(
                        (((Res_line.resstatus == 11) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate))) |  ((Res_line.resstatus == 11) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                    if guest:

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.gastnr = res_line.gastnr
                            output_list.rsvname = reservation.name
                            output_list.guestname = guest.name
                            output_list.resno = res_line.resnr
                            output_list.reslinnr = res_line.reslinnr
                            output_list.cidate = res_line.ankunft
                            output_list.codate = res_line.abreise
                            output_list.room_night = res_line.abreise - res_line.ankunft
                            output_list.rm_night = res_line.abreise - res_line.ankunft
                            output_list.argt = res_line.arrangement
                            output_list.rmrate = res_line.zipreis
                            output_list.create_date = reservation.resdat
                            output_list.lead = res_line.ankunft - reservation.resdat
                            output_list.adult = res_line.erwachs
                            output_list.child = res_line.kind1
                            output_list.infant = res_line.kind2
                            output_list.comp = res_line.gratis
                            output_list.compchild = res_line.l_zuordnung[3]

                            bguest = db_session.query(Bguest).filter(
                                    (Bguest.gastnr == res_line.gastnrmember)).first()

                            if bguest:

                                nation = db_session.query(Nation).filter(
                                        (Nation.kurzbez == bguest.nation1)).first()

                                if nation:
                                    output_list.nation = nation.bezeich

                            sourccod = db_session.query(Sourccod).filter(
                                    (Sourccod.source_code == reservation.resart)).first()

                            if sourccod:
                                output_list.sourcecode = sourccod.bezeich

                            segment = db_session.query(Segment).filter(
                                    (Segment.segmentcode == reservation.segmentcode)).first()

                            if segment:
                                output_list.segment = segment.bezeich

                            zimkateg = db_session.query(Zimkateg).filter(
                                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

                            if zimkateg:
                                output_list.rm_type = zimkateg.kurzbez

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                            if reslin_queasy:

                                waehrung = db_session.query(Waehrung).filter(
                                        (Waehrungsnr == res_line.betriebsnr)).first()

                                if waehrung:
                                    output_list.currency = waehrung.wabkurz
                            datum3 = datum2

                            if res_line.ankunft > datum3:
                                datum3 = res_line.ankunft
                            datum4 = todate

                            if res_line.abreise < datum4:
                                datum4 = res_line.abreise
                            for ldatum in range(datum3,datum4 + 1) :
                                pax = res_line.erwachs
                                net_lodg = 0
                                curr_i = curr_i + 1

                                reslin_queasy = db_session.query(Reslin_queasy).filter(
                                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                                if reslin_queasy:
                                    fixed_rate = True

                                    if reslin_queasy.number3 != 0:
                                        pax = reslin_queasy.number3
                                    output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                                if not fixed_rate:

                                    guest_pr = db_session.query(Guest_pr).filter(
                                            (Guest_pr.gastnr == res_line.gastnr)).first()

                                    if guest_pr:
                                        contcode = guest_pr.CODE
                                        ct = res_line.zimmer_wunsch

                                        if re.match(".*\$CODE\$.*",ct):
                                            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                            contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                            output_list.contcode = contcode

                                        if res_line.l_zuordnung[0] != 0:
                                            curr_zikatnr = res_line.l_zuordnung[0]
                                        else:
                                            curr_zikatnr = res_line.zikatnr

                                        queasy = db_session.query(Queasy).filter(
                                                (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                        if queasy and queasy.logi3:
                                            bill_date = res_line.ankunft

                                        if new_contrate:
                                            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        else:
                                            rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                            rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                            if it_exist:
                                                rate_found = True

                                            if not it_exist and bonus_array[curr_i - 1] :
                                                rm_rate = 0
                                        output_list.rmrate = output_list.rmrate + rm_rate


                                    w_day = wd_array[get_weekday(bill_date) - 1]

                                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                        rm_rate = res_line.zipreis

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                            rack_rate = True

                                    elif rack_rate:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                        if not katpreis:

                                            katpreis = db_session.query(Katpreis).filter(
                                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                            rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                else:
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                                output_list.lodging = output_list.lodging + net_lodg

                            if res_line.betriebsnr == curr_foreign:
                                output_list.rmrate1 = output_list.rmrate


                            else:
                                output_list.rmrate1 = output_list.rmrate / foreign_curr


                            output_list.lodging1 = output_list.lodging / foreign_curr
                            output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                            output_list.avg_lodging = output_list.lodging / output_list.room_night

                            if output_list.avg_rmrate == None:
                                output_list.avg_rmrate = output_list.rmrate

                            if output_list.avg_lodging == None:
                                output_list.avg_lodging = output_list.lodging


                            tot_lead = tot_lead + output_list.lead
                            tot_lodging = tot_lodging + output_list.lodging
                            tot_lodging1 = tot_lodging1 + output_list.lodging1
                            tot_los = tot_los + output_list.room_night
                            tot_rmnight = tot_rmnight + output_list.rm_night
                            tot_avrlodging = tot_avrlodging + output_list.lodging
                            tot_adult = tot_adult + output_list.adult
                            tot_child = tot_child + output_list.child
                            tot_infant = tot_infant + output_list.infant
                            tot_comp = tot_comp + output_list.comp
                            tot_compchild = tot_compchild + output_list.compchild

                            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                            if not tot_list:
                                tot_list = Tot_list()
                                tot_list_list.append(tot_list)

                                tot_list.gastnr = output_list.gastnr


                            tot_list.t_lead = tot_list.t_lead + output_list.lead
                            tot_list.t_los = tot_list.t_los + output_list.room_night
                            tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead = t_lead
        output_list.lodging = t_lodging
        output_list.lodging1 = t_lodging1
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging = t_avrlodging / t_rmnight
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead = t_avrglead
        output_list.avrg_los = t_avrglos
        output_list.rmrate = t_rmrate
        output_list.rmrate1 = t_rmrate1
        output_list.avg_rmrate = t_avrgrmrate / t_rmnight

        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv

        for tot_list in query(tot_list_list):
            tot_rsv = tot_rsv + tot_list.t_reserv


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = 999999999
        output_list.rsvname = "Grand T O T A L"
        output_list.lead = tot_lead
        output_list.lodging = tot_lodging
        output_list.lodging1 = tot_lodging1
        output_list.room_night = tot_los
        output_list.rm_night = tot_rmnight
        output_list.avg_lodging = tot_avrlodging / tot_rmnight
        output_list.adult = tot_adult
        output_list.child = tot_child
        output_list.infant = tot_infant
        output_list.comp = tot_comp
        output_list.compchild = tot_compchild
        output_list.avrg_lead = tot_avrglead / tot_rsv
        output_list.avrg_los = tot_avrglos / tot_rsv
        output_list.rmrate = tot_rmrate
        output_list.rmrate1 = tot_rmrate1
        output_list.avg_rmrate = tot_avrgrmrate / tot_rmnight
        output_list.tot_reserv = tot_rsv

    def create_browse_rm_sharer1():

        nonlocal output_list_list, pax, ci_date, local_curr, foreign_curr, curr_foreign, fixed_rate, new_contrate, wd_array, bill_date, ebdisc_flag, kbdisc_flag, contcode, ct, curr_zikatnr, rate_found, rm_rate, early_flag, kback_flag, it_exist, bonus_array, w_day, rack_rate, counter, guest, waehrung, htparam, reservation, genstat, nation, segment, zimkateg, sourccod, res_line, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal t_guest, bguest, waehrung1, boutput


        nonlocal output_list, tot_list, t_guest, bguest, waehrung1, boutput
        nonlocal output_list_list, tot_list_list

        datum:date = None
        datum2:date = None
        datum3:date = None
        datum4:date = None
        ldatum:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lead:decimal = 0
        tot_lodging:decimal = 0
        tot_lodging1:decimal = 0
        tot_avrlodging:decimal = 0
        tot_los:int = 0
        tot_rmnight:int = 0
        tot_adult:int = 0
        tot_child:int = 0
        tot_infant:int = 0
        tot_comp:int = 0
        tot_compchild:int = 0
        t_gastnr:int = 0
        t_lead:decimal = 0
        t_lodging:decimal = 0
        t_lodging1:decimal = 0
        t_avrlodging:decimal = 0
        t_avrglead:decimal = 0
        t_avrglos:decimal = 0
        t_los:int = 0
        t_rmnight:int = 0
        t_adult:int = 0
        t_child:int = 0
        t_infant:int = 0
        t_comp:int = 0
        t_compchild:int = 0
        tot_avrglead:decimal = 0
        tot_avrglos:decimal = 0
        t_rmrate:decimal = 0
        t_rmrate1:decimal = 0
        t_avrgrmrate:decimal = 0
        tot_rmrate:decimal = 0
        tot_rmrate1:decimal = 0
        tot_avrgrmrate:decimal = 0
        tot_rsv:decimal = 0

        if check_cdate:

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resdat >= fromdate) &  (Reservation.resdat <= todate) &  (Reservation.resnr == Res_line.resnr)).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus == 11)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 11) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        else:

            for res_line in db_session.query(Res_line).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus == 11) &  (Res_line.ankunft >= fromdate) &  (Res_line.ankunft <= todate)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 11) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                curr_i = 0
                tot_breakfast = 0
                tot_lunch = 0
                tot_dinner = 0
                tot_other = 0
                ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
                kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember) &  (func.lower(Guest.name) >= (from_rsv).lower()) &  (func.lower(Guest.name) <= (to_rsv).lower())).first()

                if guest:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.gastnr == res_line.gastnr and output_list.resno == res_line.resnr and output_list.reslinnr == res_line.reslinnr), first=True)

                    if not output_list:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.gastnr = res_line.gastnr
                        output_list.rsvname = reservation.name
                        output_list.guestname = guest.name
                        output_list.resno = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.cidate = res_line.ankunft
                        output_list.codate = res_line.abreise
                        output_list.room_night = res_line.abreise - res_line.ankunft
                        output_list.rm_night = res_line.abreise - res_line.ankunft
                        output_list.argt = res_line.arrangement
                        output_list.create_date = reservation.resdat
                        output_list.lead = res_line.ankunft - reservation.resdat
                        output_list.adult = res_line.erwachs
                        output_list.child = res_line.kind1
                        output_list.infant = res_line.kind2
                        output_list.comp = res_line.gratis
                        output_list.compchild = res_line.l_zuordnung[3]

                        bguest = db_session.query(Bguest).filter(
                                (Bguest.gastnr == res_line.gastnrmember)).first()

                        if bguest:

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == bguest.nation1)).first()

                            if nation:
                                output_list.nation = nation.bezeich

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment:
                            output_list.segment = segment.bezeich

                        sourccod = db_session.query(Sourccod).filter(
                                (Sourccod.source_code == reservation.resart)).first()

                        if sourccod:
                            output_list.sourcecode = sourccod.bezeich

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()

                        if zimkateg:
                            output_list.rm_type = zimkateg.kurzbez

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                output_list.currency = waehrung.wabkurz
                        datum3 = fromdate

                        if res_line.ankunft > datum3:
                            datum3 = res_line.ankunft
                        datum4 = todate

                        if res_line.abreise < datum4:
                            datum4 = res_line.abreise
                        for ldatum in range(res_line.ankunft,res_line.abreise - 1 + 1) :
                            pax = res_line.erwachs
                            net_lodg = 0
                            curr_i = curr_i + 1

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= ldatum) &  (Reslin_queasy.date2 >= ldatum)).first()

                            if reslin_queasy:
                                fixed_rate = True

                                if reslin_queasy.number3 != 0:
                                    pax = reslin_queasy.number3
                                output_list.rmrate = output_list.rmrate + reslin_queasy.deci1

                            if not fixed_rate:

                                guest_pr = db_session.query(Guest_pr).filter(
                                        (Guest_pr.gastnr == res_line.gastnr)).first()

                                if guest_pr:
                                    contcode = guest_pr.CODE
                                    ct = res_line.zimmer_wunsch

                                    if re.match(".*\$CODE\$.*",ct):
                                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                        output_list.contcode = contcode

                                    if res_line.l_zuordnung[0] != 0:
                                        curr_zikatnr = res_line.l_zuordnung[0]
                                    else:
                                        curr_zikatnr = res_line.zikatnr

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                                    if queasy and queasy.logi3:
                                        bill_date = res_line.ankunft

                                    if new_contrate:
                                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                    else:
                                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                        rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                        if it_exist:
                                            rate_found = True

                                        if not it_exist and bonus_array[curr_i - 1] :
                                            rm_rate = 0
                                    output_list.rmrate = output_list.rmrate + rm_rate


                                w_day = wd_array[get_weekday(bill_date) - 1]

                                if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                    rm_rate = res_line.zipreis

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                        rack_rate = True

                                elif rack_rate:

                                    katpreis = db_session.query(Katpreis).filter(
                                            (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                                    if not katpreis:

                                        katpreis = db_session.query(Katpreis).filter(
                                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                                    if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                        rm_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
                                output_list.rmrate = output_list.rmrate + rm_rate


                            else:
                                ct = res_line.zimmer_wunsch

                                if re.match(".*\$CODE\$.*",ct):
                                    ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                                    contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
                                    output_list.contcode = contcode


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, ldatum, curr_i, fromdate))
                            output_list.lodging = output_list.lodging + net_lodg

                        if res_line.betriebsnr == curr_foreign:
                            output_list.rmrate1 = output_list.rmrate


                        else:
                            output_list.rmrate1 = output_list.rmrate / foreign_curr


                        output_list.lodging1 = output_list.lodging / foreign_curr
                        output_list.avg_rmrate = output_list.rmrate / output_list.room_night
                        output_list.avg_lodging = output_list.lodging / output_list.room_night

                        if output_list.avg_rmrate == None:
                            output_list.avg_rmrate = output_list.rmrate

                        if output_list.avg_lodging == None:
                            output_list.avg_lodging = output_list.lodging


                        tot_lead = tot_lead + output_list.lead
                        tot_lodging = tot_lodging + output_list.lodging
                        tot_lodging1 = tot_lodging1 + output_list.lodging1
                        tot_los = tot_los + output_list.room_night
                        tot_rmnight = tot_rmnight + output_list.rm_night
                        tot_avrlodging = tot_avrlodging + output_list.lodging
                        tot_adult = tot_adult + output_list.adult
                        tot_child = tot_child + output_list.child
                        tot_infant = tot_infant + output_list.infant
                        tot_comp = tot_comp + output_list.comp
                        tot_compchild = tot_compchild + output_list.compchild

                        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                        if not tot_list:
                            tot_list = Tot_list()
                            tot_list_list.append(tot_list)

                            tot_list.gastnr = output_list.gastnr


                        tot_list.t_lead = tot_list.t_lead + output_list.lead
                        tot_list.t_los = tot_list.t_los + output_list.room_night
                        tot_list.t_reserv = tot_list.t_reserv + 1

            for output_list in query(output_list_list):
                counter = counter + 1

                if t_gastnr != 0 and t_gastnr != output_list.gastnr:
                    boutput = Boutput()
                    boutput_list.append(boutput)

                    boutput.gastnr = t_gastnr
                    boutput.rsvname = "T O T A L"
                    boutput.lead = t_lead
                    boutput.lodging = t_lodging
                    boutput.lodging1 = t_lodging1
                    boutput.room_night = t_los
                    boutput.rm_night = t_rmnight
                    boutput.avg_lodging = t_avrlodging / t_rmnight
                    boutput.adult = t_adult
                    boutput.child = t_child
                    boutput.infant = t_infant
                    boutput.comp = t_comp
                    boutput.compchild = t_compchild
                    boutput.avrg_lead = t_avrglead
                    boutput.avrg_los = t_avrglos
                    boutput.pos = counter
                    boutput.rmrate = t_rmrate
                    boutput.rmrate1 = t_rmrate1
                    boutput.avg_rmrate = t_avrgrmrate / t_rmnight
                    t_rmrate = 0
                    t_rmrate1 = 0
                    t_avrgrmrate = 0
                    t_lead = 0
                    t_lodging = 0
                    t_lodging1 = 0
                    t_avrlodging = 0
                    t_los = 0
                    t_rmnight = 0
                    t_adult = 0
                    t_child = 0
                    t_infant = 0
                    t_comp = 0
                    t_compchild = 0
                    t_avrglead = 0
                    t_avrglos = 0
                    counter = counter + 1

                    tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

                    if tot_list:
                        boutput.tot_reserv = tot_list.t_reserv

                tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == output_list.gastnr), first=True)

                if tot_list:
                    output_list.avrg_lead = output_list.lead
                    output_list.avrg_los = output_list.room_night

                    if output_list.lead / tot_list.t_lead != None:
                        t_avrglead = t_avrglead + (output_list.lead / tot_list.t_reserv)
                        tot_avrglead = tot_avrglead + output_list.lead

                    if output_list.room_night / tot_list.t_reserv != None:
                        t_avrglos = t_avrglos + (output_list.room_night / tot_list.t_reserv)
                        tot_avrglos = tot_avrglos + output_list.room_night


                output_list.pos = counter
                t_gastnr = output_list.gastnr
                t_lead = t_lead + output_list.lead
                t_lodging = t_lodging + output_list.lodging
                t_lodging1 = t_lodging1 + output_list.lodging1
                t_avrlodging = t_avrlodging + output_list.lodging
                t_los = t_los + output_list.room_night
                t_rmnight = t_rmnight + output_list.rm_night
                t_adult = t_adult + output_list.adult
                t_child = t_child + output_list.child
                t_infant = t_infant + output_list.infant
                t_comp = t_comp + output_list.comp
                t_compchild = t_compchild + output_list.compchild
                t_avrglos = t_avrglos + output_list.avrg_los
                tot_avrglos = tot_avrglos + output_list.avrg_los
                t_rmrate = t_rmrate + output_list.rmrate
                t_rmrate1 = t_rmrate1 + output_list.rmrate1
                t_avrgrmrate = t_avrgrmrate + output_list.rmrate
                tot_rmrate = tot_rmrate + output_list.rmrate
                tot_rmrate1 = tot_rmrate1 + output_list.rmrate1
                tot_avrgrmrate = tot_avrgrmrate + output_list.rmrate


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.pos = counter
        output_list.gastnr = t_gastnr
        output_list.rsvname = "T O T A L"
        output_list.lead = t_lead
        output_list.lodging = t_lodging
        output_list.lodging1 = t_lodging1
        output_list.room_night = t_los
        output_list.rm_night = t_rmnight
        output_list.avg_lodging = t_avrlodging / t_rmnight
        output_list.adult = t_adult
        output_list.child = t_child
        output_list.infant = t_infant
        output_list.comp = t_comp
        output_list.compchild = t_compchild
        output_list.avrg_lead = t_avrglead
        output_list.avrg_los = t_avrglos
        output_list.rmrate = t_rmrate
        output_list.rmrate1 = t_rmrate1
        output_list.avg_rmrate = t_avrgrmrate / t_rmnight

        tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.gastnr == t_gastnr), first=True)

        if tot_list:
            output_list.tot_reserv = tot_list.t_reserv


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung1 = db_session.query(Waehrung1).filter(
            (Waehrung1.wabkurz == htparam.fchar)).first()

    if waehrung1:
        local_curr = waehrung1.ankauf

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung1 = db_session.query(Waehrung1).filter(
            (Waehrung1.wabkurz == htparam.fchar)).first()

    if waehrung1:
        foreign_curr = waehrung1.ankauf
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

    for output_list in query(output_list_list):

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
            output_list.avrg_lead = 0

        if output_list.avrg_los == None:
            output_list.avrg_los = 0

    return generate_output()