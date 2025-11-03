#using conversion tools version: 1.0.0.119

# ==============================
# Rulita, 03-11-2025 
# - New compile program
# ==============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Res_line, Kontline, Htparam, Zimmer, Reservation, Zimkateg, Guest, Waehrung, Segment, Guestseg, Queasy, Reslin_queasy, Outorder, Zinrstat

argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
segm_list_data, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})

def occ_fcast1_ddown_create_browse1bl(case_type:int, datum:date, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, incl_tent:bool, exclooo:bool, argt_list_data:[Argt_list], segm_list_data:[Segm_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Res_line, Kontline, Htparam, Zimmer, Reservation, Zimkateg, Guest, Waehrung, Guestseg, Queasy, Reslin_queasy, Outorder, Zinrstat])

    room_list_data = []
    tot_room:int = 0
    vhp_limited:bool = False
    pax:int = 0
    res_line = kontline = htparam = zimmer = reservation = zimkateg = guest = waehrung = segment = guestseg = queasy = reslin_queasy = outorder = zinrstat = None

    room_list = segm_list = argt_list = zikat_list = rmcat_list = rline1 = s_list = a_list = z_list = None

    room_list_data, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":string, "room":[Decimal,17], "coom":[string,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,4], "avrglodg":Decimal, "resnr":string, "rmno":string, "rmcat":string, "name":string, "argt":string, "company":string, "segment":string, "currency":string, "adult":int, "ch1":int, "ch2":int, "compli":int, "depart":date, "arrival":date, "nights":int, "arrtime":string, "deptime":string, "qty":int, "pax":int, "pocc":Decimal, "sleeping":bool, "t_avail":int, "t_ooo":int, "t_alot":int, "t_occ":int, "zikatnr":int, "kurzbez":string})
    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":string, "bezeich":string, "zinr":string}, {"sleeping": True})

    Rline1 = create_buffer("Rline1",Res_line)

    set_cache(Reslin_queasy, (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum),[["key", "resnr", "reslinnr"]], True,["date1", "date2"],[])
    set_cache(Zimmer, None,[["zinr"]], True,[],[])
    set_cache(Queasy, (Queasy.key == 14) & (((Queasy.date1 <= datum) & (Queasy.date2 >= datum)) | (Queasy.date1 <= datum - timedelta(days=1)) & (Queasy.date2 >= datum - timedelta(days=1))),[["key", "char1"]], True,["date1", "date2"],[])
    set_cache(Res_line, (Res_line.abreise > datum) & (Res_line.resstatus == 8),[["resnr", "resstatus"]], True,["reslinnr", "abreise"],[])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal case_type, datum, curr_date, to_date, all_segm, all_argt, all_zikat, incl_tent, exclooo
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list
        nonlocal room_list_data, rmcat_list_data

        return {"room-list": room_list_data}

    def create_browse1():

        nonlocal room_list_data, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal case_type, datum, curr_date, to_date, all_segm, all_argt, all_zikat, incl_tent, exclooo
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list
        nonlocal room_list_data, rmcat_list_data

        p_room:int = 0
        p_lodg:Decimal = to_decimal("0.0")
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:Decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        n:int = 0
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        curr_i:int = 0
        fnet_lodg:Decimal = to_decimal("0.0")
        rsvstat:string = ""
        avrg_lodging:Decimal = to_decimal("0.0")
        kline = None
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        sum_breakfast:Decimal = to_decimal("0.0")
        sum_lunch:Decimal = to_decimal("0.0")
        sum_dinner:Decimal = to_decimal("0.0")
        sum_other:Decimal = to_decimal("0.0")
        tot_pax:int = 0
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_compli:int = 0
        tot_nights:int = 0
        tot_qty:int = 0
        tot_pocc:Decimal = to_decimal("0.0")
        tot_lodg:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        tmp_date:date = None
        ci_date:date = None
        tot_actroom:int = 0
        tot_occrm:int = 0
        tot_ooo:int = 0
        tot_alot:int = 0
        tot_avail:int = 0
        tot_avail2:int = 0
        S_list = Segm_list
        s_list_data = segm_list_data
        A_list = Argt_list
        a_list_data = argt_list_data
        Z_list = Zikat_list
        z_list_data = zikat_list_data
        Kline =  create_buffer("Kline",Kontline)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

        if htparam:
            ci_date = htparam.fdate


        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

                if z_list:
                    tot_room = tot_room + 1
        tot_pax = 0
        tot_adult = 0
        tot_ch1 = 0
        tot_ch2 = 0
        tot_compli = 0
        tot_qty = 0
        tot_pocc =  to_decimal("0")

        if case_type == 1:

            res_line_obj_list = {}
            for res_line, reservation, zimkateg, guest, waehrung, segment in db_session.query(Res_line, Reservation, Zimkateg, Guest, Waehrung, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                     (Res_line.active_flag <= 2) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

                    if guestseg:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        kont_doit = None != s_list

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if do_it and zimmer:
                    tmp_date = datum - timedelta(days=1)

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, tmp_date)],"date2": [(ge, tmp_date)]})

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    tmp_date = datum - timedelta(days=1)

                    if tmp_date == res_line.ankunft and consider_it and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and res_line.active_flag <= 1:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.abreise > res_line.ankunft:
                                room_list = Room_list()
                                room_list_data.append(room_list)


                                if zimkateg:
                                    room_list.rmcat = zimkateg.kurzbez
                                room_list.resnr = to_string(res_line.resnr)
                                room_list.name = res_line.name
                                room_list.rmno = res_line.zinr
                                room_list.depart = res_line.abreise
                                room_list.arrival = res_line.ankunft
                                room_list.argt = res_line.arrangement
                                room_list.adult = pax
                                room_list.compli = res_line.gratis * res_line.zimmeranz
                                room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                                room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                                room_list.currency = waehrung.wabkurz
                                room_list.segment = segment.bezeich
                                room_list.qty = res_line.zimmeranz
                                room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz

                                if guest.karteityp != 0:
                                    room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                                tot_pax = tot_pax + ((pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                                tot_adult = tot_adult + (pax)
                                tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                                tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                                tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                                tot_nights = tot_nights + res_line.anztage
                                tot_qty = tot_qty + res_line.zimmeranz
                    tmp_date = datum - timedelta(days=1)

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > tmp_date and res_line.ankunft < tmp_date and res_line.ankunft != tmp_date and res_line.abreise != tmp_date) and res_line.active_flag <= 1:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list = Room_list()
                            room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.adult = pax
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (pax)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz

                    if res_line.resstatus == 8 and consider_it and res_line.active_flag == 2 and res_line.abreise == (datum - timedelta(days=1)) and res_line.ankunft == (datum - timedelta(days=1)):

                        if not res_line.zimmerfix:
                            room_list = Room_list()
                            room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.adult = pax
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (pax)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz

        elif case_type == 3:

            res_line_obj_list = {}
            for res_line, reservation, guest, waehrung, zimkateg, segment in db_session.query(Res_line, Reservation, Guest, Waehrung, Zimkateg, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < datum))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

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

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False

                    if datum == res_line.ankunft and res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                        room_list = Room_list()
                        room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 +\
                                res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                        room_list.adult = pax
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (pax)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_nights = tot_nights + res_line.anztage
                        tot_qty = tot_qty + res_line.zimmeranz

        elif case_type == 5:

            res_line_obj_list = {}
            for res_line, reservation, guest, waehrung, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Waehrung, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < datum))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

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

                if do_it:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False

                    if datum == res_line.abreise and res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)):
                        room_list = Room_list()
                        room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.pax = (res_line.erwachs + res_line.kind1 + res_line.kind2 +\
                                res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                        room_list.adult = res_line.erwachs * res_line.zimmeranz
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.deptime = to_string(res_line.abreisezeit, "HH:MM:SS")
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz

        elif case_type == 7:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))

                if not vhp_limited:
                    do_it = True
                else:

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

                    if guestseg:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        kont_doit = None != s_list

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

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False

                    if datum == res_line.ankunft and consider_it and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.abreise >= res_line.ankunft:
                                room_list = Room_list()
                                room_list_data.append(room_list)


                                if zimkateg:
                                    room_list.rmcat = zimkateg.kurzbez
                                room_list.resnr = to_string(res_line.resnr)
                                room_list.name = res_line.name
                                room_list.rmno = res_line.zinr
                                room_list.depart = res_line.abreise
                                room_list.arrival = res_line.ankunft
                                room_list.argt = res_line.arrangement
                                room_list.adult = res_line.erwachs
                                room_list.compli = res_line.gratis * res_line.zimmeranz
                                room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                                room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                                room_list.currency = waehrung.wabkurz
                                room_list.segment = segment.bezeich
                                room_list.qty = res_line.zimmeranz
                                room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                                room_list.lodg[3] = net_lodg

                                if guest.karteityp != 0:
                                    room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                                tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                                tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                                tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                                tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                                tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                                tot_nights = tot_nights + res_line.anztage
                                tot_qty = tot_qty + res_line.zimmeranz
                                tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                                tot_lodg =  to_decimal(tot_lodg) + to_decimal(net_lodg)

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > datum and res_line.ankunft < datum and res_line.ankunft != datum and res_line.abreise != datum):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list = Room_list()
                            room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.adult = res_line.erwachs
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        room_list.lodg[3] = net_lodg

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz
                        tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        tot_lodg =  to_decimal(tot_lodg) + to_decimal(net_lodg)

        elif case_type == 11:
            room_list_data.clear()
            count_rmcateg()

            for zimkateg in db_session.query(Zimkateg).filter(
                     (Zimkateg.verfuegbarkeit)).order_by(Zimkateg.zikatnr).all():

                rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimkateg.zikatnr and rmcat_list.sleeping), first=True)

                if rmcat_list:
                    room_list = Room_list()
                    room_list_data.append(room_list)

                    room_list.sleeping = True
                    room_list.pax = rmcat_list.anzahl
                    room_list.t_avail = rmcat_list.anzahl
                    room_list.qty = rmcat_list.anzahl
                    room_list.zikatnr = zimkateg.zikatnr
                    room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
                    room_list.datum = datum
                    room_list.rmcat = zimkateg.kurzbez

            zimkateg_obj_list = {}
            for zimkateg in db_session.query(Zimkateg).filter(
                     ((Zimkateg.zikatnr.in_(list(set([rmcat_list.zikatnr for rmcat_list in rmcat_list_data if ~rmcat_list.sleeping])))))).order_by(Zimkateg.zikatnr).all():
                if zimkateg_obj_list.get(zimkateg._recid):
                    continue
                else:
                    zimkateg_obj_list[zimkateg._recid] = True

                rmcat_list = query(rmcat_list_data, (lambda rmcat_list: (zimkateg.zikatnr == rmcat_list.zikatnr)), first=True)
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.sleeping = False
                room_list.pax = rmcat_list.anzahl
                room_list.t_avail = rmcat_list.anzahl
                room_list.qty = rmcat_list.anzahl
                room_list.zikatnr = zimkateg.zikatnr
                room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
                room_list.datum = datum

            res_line_obj_list = {}
            res_line = Res_line()
            zimmer = Zimmer()
            for res_line.arrangement, res_line.zikatnr, res_line.zinr, res_line.gastnr, res_line.erwachs, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.resstatus, res_line.active_flag, res_line.zimmerfix, res_line.name, res_line.abreise, res_line.gratis, res_line.zimmeranz, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.anztage, res_line.ankzeit, res_line.abreisezeit, res_line.betriebsnr, res_line._recid, res_line.kontignr, zimmer.zikatnr, zimmer.sleeping, zimmer.zinr, zimmer.bezeich, zimmer._recid in db_session.query(Res_line.arrangement, Res_line.zikatnr, Res_line.zinr, Res_line.gastnr, Res_line.erwachs, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.resstatus, Res_line.active_flag, Res_line.zimmerfix, Res_line.name, Res_line.abreise, Res_line.gratis, Res_line.zimmeranz, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.anztage, Res_line.ankzeit, Res_line.abreisezeit, Res_line.betriebsnr, Res_line._recid, Res_line.kontignr, Zimmer.zikatnr, Zimmer.sleeping, Zimmer.zinr, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & not_ (Zimmer.sleeping)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.zikatnr == room_list.zikatnr) & (Res_line.zinr != "") & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if not vhp_limited:
                    do_it = True
                else:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    room_list.t_avail = room_list.t_avail - 1

            outorder_obj_list = {}
            outorder = Outorder()
            zimmer = Zimmer()
            for outorder.gespstart, outorder.gespende, outorder.zinr, outorder.gespgrund, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer.zinr, zimmer.bezeich, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder.zinr, Outorder.gespgrund, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer.zinr, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                     (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.sleeping), first=True)

                if room_list:

                    if datum >= outorder.gespstart and datum <= outorder.gespende:
                        room_list.t_ooo = room_list.t_ooo + 1
                        room_list.t_avail = room_list.t_avail - 1

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.sleeping)):

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.zikatnr == room_list.zikatnr) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tent:
                        do_it = False

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_list.t_occ = room_list.t_occ + res_line.zimmeranz
                        room_list.t_avail = room_list.t_avail - res_line.zimmeranz

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 0) & (datum >= Kontline.ankunft) & (datum < Kontline.abreise) & (Kontline.zikatnr == room_list.zikatnr) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                room_list.t_alot = room_list.t_alot + kontline.zimmeranz
                room_list.t_avail = room_list.t_avail - kontline.zimmeranz

            if tot_actroom != 0:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.bezeich = "TOTAL"
                room_list.pax = tot_avail2
                room_list.t_avail = tot_avail
                room_list.qty = tot_actroom
                room_list.t_ooo = tot_ooo
                room_list.t_occ = tot_occrm

        elif case_type == 13:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            waehrung = Waehrung()
            zimkateg = Zimkateg()
            for res_line.arrangement, res_line.zikatnr, res_line.zinr, res_line.gastnr, res_line.erwachs, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.resstatus, res_line.active_flag, res_line.zimmerfix, res_line.name, res_line.abreise, res_line.gratis, res_line.zimmeranz, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.anztage, res_line.ankzeit, res_line.abreisezeit, res_line.betriebsnr, res_line._recid, res_line.kontignr, reservation.segmentcode, reservation.gastnr, reservation._recid, guest.gastnr, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, waehrung.wabkurz, waehrung._recid, zimkateg.kurzbez, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.arrangement, Res_line.zikatnr, Res_line.zinr, Res_line.gastnr, Res_line.erwachs, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.resstatus, Res_line.active_flag, Res_line.zimmerfix, Res_line.name, Res_line.abreise, Res_line.gratis, Res_line.zimmeranz, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.anztage, Res_line.ankzeit, Res_line.abreisezeit, Res_line.betriebsnr, Res_line._recid, Res_line.kontignr, Reservation.segmentcode, Reservation.gastnr, Reservation._recid, Guest.gastnr, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Waehrung.wabkurz, Waehrung._recid, Zimkateg.kurzbez, Zimkateg.zikatnr, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise <= datum)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

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

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False

                    if res_line.resstatus == 3 and datum >= res_line.ankunft:
                        room_list = Room_list()
                        room_list_data.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.qty = res_line.zimmeranz
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.arrival = res_line.ankunft
                        room_list.depart = res_line.abreise
                        room_list.argt = res_line.arrangement
                        room_list.segment = segment.bezeich
                        room_list.adult = res_line.erwachs * res_line.zimmeranz
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.currency = waehrung.wabkurz
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz

        elif case_type == 14:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.kontignr > 0) & (Res_line.active_flag < 2) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < datum)) & (Res_line.resstatus < 11) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kontline:

                    guest = get_cache (Guest, {"gastnr": [(eq, kontline.gastnr)]})

                    if datum >= res_line.ankunft and datum < res_line.abreise:

                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zikatnr == kontline.zikatnr) & (Zimmer.sleeping)).first()
                        room_list = Room_list()
                        room_list_data.append(room_list)

                        room_list.resnr = to_string(res_line.resnr)
                        room_list.qty = kontline.zimmeranz
                        room_list.rmno = zimmer.zinr
                        room_list.name = kontline.kontcode
                        room_list.depart = kontline.abreise
                        room_list.arrival = kontline.ankunft
                        room_list.t_alot = res_line.zimmeranz

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 +\
                                " " + guest.anrede1 + guest.anredefirma

        elif case_type == 15:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, datum)]})

            if zinrstat:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.qty = zinrstat.zimmeranz


            else:

                outorder_obj_list = {}
                outorder = Outorder()
                zimmer = Zimmer()
                for outorder.gespstart, outorder.gespende, outorder.zinr, outorder.gespgrund, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer.zinr, zimmer.bezeich, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder.zinr, Outorder.gespgrund, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer.zinr, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= datum) & (Outorder.gespende >= datum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    room_list = Room_list()
                    room_list_data.append(room_list)

                    room_list.qty = room_list.qty + 1
                    room_list.rmno = outorder.zinr
                    room_list.name = outorder.gespgrund
                    room_list.depart = outorder.gespende
                    room_list.arrival = outorder.gespstart
                    room_list.bezeich = zimmer.bezeich

        elif case_type == 16:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            waehrung = Waehrung()
            zimkateg = Zimkateg()
            for res_line.arrangement, res_line.zikatnr, res_line.zinr, res_line.gastnr, res_line.erwachs, res_line.resnr, res_line.reslinnr, res_line.ankunft, res_line.resstatus, res_line.active_flag, res_line.zimmerfix, res_line.name, res_line.abreise, res_line.gratis, res_line.zimmeranz, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.anztage, res_line.ankzeit, res_line.abreisezeit, res_line.betriebsnr, res_line._recid, res_line.kontignr, reservation.segmentcode, reservation.gastnr, reservation._recid, guest.gastnr, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, waehrung.wabkurz, waehrung._recid, zimkateg.kurzbez, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.arrangement, Res_line.zikatnr, Res_line.zinr, Res_line.gastnr, Res_line.erwachs, Res_line.resnr, Res_line.reslinnr, Res_line.ankunft, Res_line.resstatus, Res_line.active_flag, Res_line.zimmerfix, Res_line.name, Res_line.abreise, Res_line.gratis, Res_line.zimmeranz, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.anztage, Res_line.ankzeit, Res_line.abreisezeit, Res_line.betriebsnr, Res_line._recid, Res_line.kontignr, Reservation.segmentcode, Reservation.gastnr, Reservation._recid, Guest.gastnr, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Waehrung.wabkurz, Waehrung._recid, Zimkateg.kurzbez, Zimkateg.zikatnr, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

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

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    room_list = Room_list()
                    room_list_data.append(room_list)


                    if zimkateg:
                        room_list.rmcat = zimkateg.kurzbez
                    room_list.qty = res_line.zimmeranz
                    room_list.resnr = to_string(res_line.resnr)
                    room_list.name = res_line.name
                    room_list.rmno = res_line.zinr
                    room_list.arrival = res_line.ankunft
                    room_list.depart = res_line.abreise
                    room_list.argt = res_line.arrangement
                    room_list.segment = segment.bezeich
                    room_list.adult = res_line.erwachs * res_line.zimmeranz
                    room_list.compli = res_line.gratis * res_line.zimmeranz
                    room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                    room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                    room_list.currency = waehrung.wabkurz
                    room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                            res_line.gratis) * res_line.zimmeranz

                    if guest.karteityp != 0:
                        room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                    tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                    tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                    tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                    tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                    tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                    tot_qty = tot_qty + res_line.zimmeranz

        if tot_pax != 0:
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = "T O T A L"
            room_list.adult = tot_adult
            room_list.compli = tot_compli
            room_list.ch1 = tot_ch1
            room_list.ch2 = tot_ch2
            room_list.qty = tot_qty
            room_list.pax = tot_pax
            room_list.pocc =  to_decimal(tot_pocc)

            if case_type == 7:
                room_list.lodg[3] = tot_lodg


    def count_rmcateg():

        nonlocal room_list_data, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal case_type, datum, curr_date, to_date, all_segm, all_argt, all_zikat, incl_tent, exclooo
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list
        nonlocal room_list_data, rmcat_list_data

        zikatnr:int = 0
        rmcat_list_data.clear()
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg and zimkateg.verfuegbarkeit:
                tot_room = tot_room + 1

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    zikatnr = zimkateg.zikatnr
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1


    create_browse1()

    return generate_output()