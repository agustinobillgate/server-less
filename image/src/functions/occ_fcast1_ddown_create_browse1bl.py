from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Kontline, Htparam, Zimmer, Reservation, Zimkateg, Guest, Waehrung, Segment, Guestseg, Queasy, Reslin_queasy, Outorder, Zinrstat

def occ_fcast1_ddown_create_browse1bl(case_type:int, datum:date, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, incl_tent:bool, exclooo:bool, argt_list:[Argt_list], segm_list:[Segm_list], zikat_list:[Zikat_list]):
    room_list_list = []
    tot_room:int = 0
    vhp_limited:bool = False
    pax:int = 0
    res_line = kontline = htparam = zimmer = reservation = zimkateg = guest = waehrung = segment = guestseg = queasy = reslin_queasy = outorder = zinrstat = None

    room_list = segm_list = argt_list = zikat_list = rmcat_list = rline1 = s_list = a_list = z_list = kline = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":str, "room":decimal, "coom":[str, 17], "k_pax":int, "t_pax":int, "lodg":[decimal, 4], "avrglodg":decimal, "resnr":str, "rmno":str, "rmcat":str, "name":str, "argt":str, "company":str, "segment":str, "currency":str, "adult":int, "ch1":int, "ch2":int, "compli":int, "depart":date, "arrival":date, "nights":int, "arrtime":str, "deptime":str, "qty":int, "pax":int, "pocc":decimal, "sleeping":bool, "t_avail":int, "t_ooo":int, "t_alot":int, "t_occ":int, "zikatnr":int, "kurzbez":str})
    segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":str, "bezeich":str, "zinr":str}, {"sleeping": True})

    Rline1 = Res_line
    S_list = Segm_list
    s_list_list = segm_list_list

    A_list = Argt_list
    a_list_list = argt_list_list

    Z_list = Zikat_list
    z_list_list = zikat_list_list

    Kline = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal rline1, s_list, a_list, z_list, kline


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list, kline
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, rmcat_list_list
        return {"room-list": room_list_list}

    def create_browse1():

        nonlocal room_list_list, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal rline1, s_list, a_list, z_list, kline


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list, kline
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, rmcat_list_list

        p_room:int = 0
        p_lodg:decimal = 0
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:decimal = 0
        do_it:bool = False
        consider_it:bool = False
        n:int = 0
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:decimal = 0
        net_lodg:decimal = 0
        curr_i:int = 0
        rsvstat:str = ""
        avrg_lodging:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        sum_breakfast:decimal = 0
        sum_lunch:decimal = 0
        sum_dinner:decimal = 0
        sum_other:decimal = 0
        tot_pax:int = 0
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_compli:int = 0
        tot_nights:int = 0
        tot_qty:int = 0
        tot_pocc:decimal = 0
        ci_date:date = None
        tot_actroom:int = 0
        tot_occrm:int = 0
        tot_ooo:int = 0
        tot_alot:int = 0
        tot_avail:int = 0
        tot_avail2:int = 0
        S_list = Segm_list
        A_list = Argt_list
        Z_list = Zikat_list
        Kline = Kontline

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()

        if htparam:
            ci_date = htparam.fdate


        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                (sleeping)).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

                if z_list:
                    tot_room = tot_room + 1
        tot_pax = 0
        tot_adult = 0
        tot_ch1 = 0
        tot_ch2 = 0
        tot_compli = 0
        tot_qty = 0
        tot_pocc = 0

        if case_type == 1:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 2) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == reservation.gastnr)).first()

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

                if not vhp_limited:
                    do_it = True
                else:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == reservation.gastnr)).first()

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        kont_doit = None != s_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= (datum - 1)) &  (Queasy.date2 >= (datum - 1))).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if (datum - 1) == res_line.ankunft and consider_it and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and res_line.active_flag <= 1:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.abreise > res_line.ankunft:
                                room_list = Room_list()
                                room_list_list.append(room_list)


                                if zimkateg:
                                    room_list.rmcat = zimkateg.kurzbez
                                room_list.resnr = to_string(res_line.resnr)
                                room_list.name = res_line.name
                                room_list.rmno = res_line.zinr
                                room_list.depart = res_line.abreise
                                room_list.arrival = res_line.ankunft
                                room_list.argt = res_line.arrangement
                                room_list.Adult = pax
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

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > (datum - 1) and res_line.ankunft < (datum - 1) and res_line.ankunft != (datum - 1) and res_line.abreise != (datum - 1)) and res_line.active_flag <= 1:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list = Room_list()
                        room_list_list.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.Adult = pax
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

                    if res_line.resstatus == 8 and consider_it and res_line.active_flag == 2 and res_line.abreise == (datum - 1) and res_line.ankunft == (datum - 1):

                        if not res_line.zimmerfix:
                            room_list = Room_list()
                        room_list_list.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.Adult = pax
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

            res_line_obj_list = []
            for res_line, reservation, guest, waehrung, zimkateg, segment in db_session.query(Res_line, Reservation, Guest, Waehrung, Zimkateg, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Waehrung,(Waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < datum))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if datum == res_line.ankunft and res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                        room_list = Room_list()
                        room_list_list.append(room_list)


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
                        room_list.Adult = pax
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.ArrTime = to_string(res_line.ankzeit, "HH:MM:SS")
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

            res_line_obj_list = []
            for res_line, reservation, guest, waehrung, zimkateg in db_session.query(Res_line, Reservation, Guest, Waehrung, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Waehrung,(Waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < datum))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if datum == res_line.abreise and res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)):
                        room_list = Room_list()
                        room_list_list.append(room_list)


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
                        room_list.Adult = res_line.erwachs * res_line.zimmeranz
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.DepTime = to_string(res_line.abreisezeit, "HH:MM:SS")
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
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == reservation.gastnr)).first()

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

                if not vhp_limited:
                    do_it = True
                else:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == reservation.gastnr)).first()

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        kont_doit = None != s_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if datum == res_line.ankunft and consider_it and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.abreise >= res_line.ankunft:
                                room_list = Room_list()
                                room_list_list.append(room_list)


                                if zimkateg:
                                    room_list.rmcat = zimkateg.kurzbez
                                room_list.resnr = to_string(res_line.resnr)
                                room_list.name = res_line.name
                                room_list.rmno = res_line.zinr
                                room_list.depart = res_line.abreise
                                room_list.arrival = res_line.ankunft
                                room_list.argt = res_line.arrangement
                                room_list.Adult = res_line.erwachs
                                room_list.compli = res_line.gratis * res_line.zimmeranz
                                room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                                room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                                room_list.currency = waehrung.wabkurz
                                room_list.segment = segment.bezeich
                                room_list.qty = res_line.zimmeranz
                                room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                room_list.pocc = (room_list.qty / tot_room) * 100

                                if guest.karteityp != 0:
                                    room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                                tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                                tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                                tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                                tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                                tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                                tot_nights = tot_nights + res_line.anztage
                                tot_qty = tot_qty + res_line.zimmeranz
                                tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > datum and res_line.ankunft < datum and res_line.ankunft != datum and res_line.abreise != datum):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list = Room_list()
                        room_list_list.append(room_list)


                        if zimkateg:
                            room_list.rmcat = zimkateg.kurzbez
                        room_list.resnr = to_string(res_line.resnr)
                        room_list.name = res_line.name
                        room_list.rmno = res_line.zinr
                        room_list.depart = res_line.abreise
                        room_list.arrival = res_line.ankunft
                        room_list.argt = res_line.arrangement
                        room_list.Adult = res_line.erwachs
                        room_list.compli = res_line.gratis * res_line.zimmeranz
                        room_list.ch1 = res_line.kind1 * res_line.zimmeranz
                        room_list.ch2 = res_line.kind2 * res_line.zimmeranz
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.qty = res_line.zimmeranz
                        room_list.pax = (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        room_list.pocc = (room_list.qty / tot_room) * 100

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz)
                        tot_adult = tot_adult + (res_line.erwachs * res_line.zimmeranz)
                        tot_ch1 = tot_ch1 + (res_line.kind1 * res_line.zimmeranz)
                        tot_ch2 = tot_ch2 + (res_line.kind2 * res_line.zimmeranz)
                        tot_compli = tot_compli + (res_line.gratis * res_line.zimmeranz)
                        tot_qty = tot_qty + res_line.zimmeranz
                        tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100

        elif case_type == 11:
            room_list_list.clear()
            count_rmcateg()

            for zimkateg in db_session.query(Zimkateg).filter(
                    (Zimkateg.verfuegbarkeit)).all():

                rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.zikatnr == zimkateg.zikatnr and rmcat_list.sleeping), first=True)

                if rmcat_list:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.sleeping = True
                    room_list.pax = rmcat_list.anzahl
                    room_list.t_avail = rmcat_list.anzahl
                    room_list.qty = rmcat_list.anzahl
                    room_list.zikatnr = zimkateg.zikatnr
                    room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
                    room_list.datum = datum

            for rmcat_list in query(rmcat_list_list, filters=(lambda rmcat_list :not rmcat_list.sleeping)):
                zimkateg = db_session.query(Zimkateg).filter((Zimkateg.zikatnr == rmcat_list.zikatnr)).first()
                if not zimkateg:
                    continue

                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.sleeping = False
                room_list.pax = rmcat_list.anzahl
                room_list.t_avail = rmcat_list.anzahl
                room_list.qty = rmcat_list.anzahl
                room_list.zikatnr = zimkateg.zikatnr
                room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
                room_list.datum = datum

            res_line_obj_list = []
            for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) &  (not Zimmer.sleeping)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == datum) &  (Res_line.abreise == datum))) &  (Res_line.zikatnr == room_list.zikatnr) &  (Res_line.zinr != "") &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if not vhp_limited:
                    do_it = True
                else:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    room_list.t_avail = room_list.t_avail - 1

            outorder_obj_list = []
            for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).filter(
                    (Outorder.betriebsnr <= 1)).all():
                if outorder._recid in outorder_obj_list:
                    continue
                else:
                    outorder_obj_list.append(outorder._recid)

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == zimmer.zikatnr and room_list.sleeping), first=True)

                if room_list:

                    if datum >= outorder.gespstart and datum <= outorder.gespende:
                        room_list.t_ooo = room_list.t_ooo + 1
                        room_list.t_avail = room_list.t_avail - 1

            for room_list in query(room_list_list, filters=(lambda room_list :room_list.sleeping)):

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 4) &  (Res_line.zikatnr == room_list.zikatnr) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == datum) &  (Res_line.abreise == datum))) &  (Res_line.kontignr >= 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zinr == res_line.zinr)).first()
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tent:
                        do_it = False

                    if do_it and vhp_limited:

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_list.t_occ = room_list.t_occ + res_line.zimmeranz
                        room_list.t_avail = room_list.t_avail - res_line.zimmeranz

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.betriebsnr == 0) &  (Kontline.datum >= Kontline.ankunft) &  (Kontline.datum < Kontline.abreise) &  (Kontline.zikatnr == room_list.zikatnr) &  (Kontline.kontstat == 1)).all():
                room_list.t_alot = room_list.t_alot + kontline.zimmeranz
                room_list.t_avail = room_list.t_avail - kontline.zimmeranz

            if tot_actroom != 0:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.bezeich = "TOTAL"
                room_list.pax = tot_avail2
                room_list.t_avail = tot_avail
                room_list.qty = tot_actroom
                room_list.t_ooo = tot_ooo
                room_list.t_occ = tot_occrm

        elif case_type == 13:

            res_line_obj_list = []
            for res_line, reservation, guest, waehrung, zimkateg in db_session.query(Res_line, Reservation, Guest, Waehrung, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Waehrung,(Waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise <= datum)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if res_line.resstatus == 3 and datum >= res_line.ankunft:
                        room_list = Room_list()
                        room_list_list.append(room_list)


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
                        room_list.Adult = res_line.erwachs * res_line.zimmeranz
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
                    (Res_line.kontignr > 0) &  (Res_line.active_flag < 2) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < datum)) &  (Res_line.resstatus < 11) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                kontline = db_session.query(Kontline).filter(
                        (Kontline.kontignr == res_line.kontignr) &  (Kontline.kontstat == 1)).first()

                if kontline:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == kontline.gastnr)).first()

                    if datum >= res_line.ankunft and datum < res_line.abreise:

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == kontline.zikatnr) &  (Zimmer.sleeping)).first()
                        room_list = Room_list()
                        room_list_list.append(room_list)

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

            zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ooo") &  (Zinrstat.datum == room_list.datum)).first()

            if zinrstat:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.qty = zinrstat.zimmeranz


            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).filter(
                        (Outorder.gespstart <= datum) &  (Outorder.gespende >= datum) &  (Outorder.betriebsnr <= 1)).all():
                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)


                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.qty = room_list.qty + 1
                    room_list.rmno = outorder.zinr
                    room_list.name = outorder.gespgrund
                    room_list.depart = outorder.gespende
                    room_list.arrival = outorder.gespstart
                    room_list.bezeich = zimmer.bezeich

        elif case_type == 16:

            res_line_obj_list = []
            for res_line, reservation, guest, waehrung, zimkateg in db_session.query(Res_line, Reservation, Guest, Waehrung, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Waehrung,(Waehrungsnr == Res_line.betriebsnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 4) &  (Res_line.ankunft <= datum) &  (Res_line.abreise > datum) &  (Res_line.kontignr < 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

                if not vhp_limited:
                    do_it = True
                else:
                    do_it = None != segment and segment.vip_level == 0

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            1
                        else:
                            do_it = False

                if do_it:
                    pax = res_line.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False
                    room_list = Room_list()
                    room_list_list.append(room_list)


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
                    room_list.Adult = res_line.erwachs * res_line.zimmeranz
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
            room_list_list.append(room_list)

            room_list.name = "T O T A L"
            room_list.adult = tot_adult
            room_list.compli = tot_compli
            room_list.ch1 = tot_ch1
            room_list.ch2 = tot_ch2
            room_list.qty = tot_qty
            room_list.pax = tot_pax
            room_list.pocc = tot_pocc

    def count_rmcateg():

        nonlocal room_list_list, tot_room, vhp_limited, pax, res_line, kontline, htparam, zimmer, reservation, zimkateg, guest, waehrung, segment, guestseg, queasy, reslin_queasy, outorder, zinrstat
        nonlocal rline1, s_list, a_list, z_list, kline


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, rline1, s_list, a_list, z_list, kline
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, rmcat_list_list

        zikatnr:int = 0
        rmcat_list_list.clear()
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg and zimkateg.verfuegbarkeit:
                tot_room = tot_room + 1

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_list.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    zikatnr = zimkateg.zikatnr
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1

    pass

    create_browse1()

    return generate_output()