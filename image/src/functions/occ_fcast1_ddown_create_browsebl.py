from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline, Zimmer, Guest, Zimkateg, Waehrung, Res_line, Segment, Genstat, Zinrstat, Outorder

def occ_fcast1_ddown_create_browsebl(case_type:int, datum:date, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, argt_list:[Argt_list], segm_list:[Segm_list], zikat_list:[Zikat_list]):
    room_list_list = []
    kontline = zimmer = guest = zimkateg = waehrung = res_line = segment = genstat = zinrstat = outorder = None

    room_list = segm_list = argt_list = zikat_list = rmcat_list = s_list = a_list = z_list = kline = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":str, "room":decimal, "coom":[str, 17], "k_pax":int, "t_pax":int, "lodg":[decimal, 4], "avrglodg":decimal, "resnr":str, "rmno":str, "rmcat":str, "name":str, "argt":str, "company":str, "segment":str, "currency":str, "adult":int, "ch1":int, "ch2":int, "compli":int, "depart":date, "arrival":date, "nights":int, "arrtime":str, "deptime":str, "qty":int, "pax":int, "pocc":decimal, "sleeping":bool, "t_avail":int, "t_ooo":int, "t_alot":int, "t_occ":int, "zikatnr":int, "kurzbez":str})
    segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
    argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":str, "bezeich":str, "zinr":str}, {"sleeping": True})

    S_list = Segm_list
    s_list_list = segm_list_list

    A_list = Argt_list
    a_list_list = argt_list_list

    Z_list = Zikat_list
    z_list_list = zikat_list_list

    Kline = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, kontline, zimmer, guest, zimkateg, waehrung, res_line, segment, genstat, zinrstat, outorder
        nonlocal s_list, a_list, z_list, kline


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, s_list, a_list, z_list, kline
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, rmcat_list_list
        return {"room-list": room_list_list}

    def create_browse():

        nonlocal room_list_list, kontline, zimmer, guest, zimkateg, waehrung, res_line, segment, genstat, zinrstat, outorder
        nonlocal s_list, a_list, z_list, kline


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, s_list, a_list, z_list, kline
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, rmcat_list_list

        curr_i:int = 0
        net_lodg:decimal = 0
        datum1:date = None
        datum2:date = None
        d2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:decimal = 0
        do_it:bool = False
        consider_it:bool = False
        rm_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:decimal = 0
        rmsharer:bool = False
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
        tot_room:int = 0
        mtd_tot_room:int = 0
        accum_tot_room:int = 0
        actual_tot_room:int = 0
        S_list = Segm_list
        A_list = Argt_list
        Z_list = Zikat_list
        Kline = Kontline
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                (sleeping)).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                zikat_list = query(zikat_list_list, filters=(lambda zikat_list :zikat_list.zikatnr == zimmer.zikatnr and zikat_list.selected), first=True)

                if zikat_list:
                    tot_room = tot_room + 1

        if case_type == 1:

            genstat_obj_list = []
            for genstat, guest, zimkateg, waehrung, res_line, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Res_line, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrungsnr == Genstat.wahrungsnr)).join(Res_line,(Res_line.resnr == Genstat.resnr) &  (Res_line.reslinnr == Genstat.res_int[0])).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                    (Genstat.datum >= (datum - 1)) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.datum == (datum - 1):
                    do_it = True

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        do_it = False

                    if do_it and not all_segm:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it :
                        room_list = Room_list()
                        room_list_list.append(room_list)

                        room_list.qty = room_list.qty + 1
                        room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        room_list.resnr = to_string(genstat.resnr)
                        room_list.rmcat = zimkateg.kurzbez
                        room_list.rmno = genstat.zinr
                        room_list.pocc = (room_list.qty / tot_room) * 100
                        room_list.depart = genstat.res_date[1]
                        room_list.arrival = genstat.res_date[0]
                        room_list.argt = genstat.argt
                        room_list.nights = res_line.anztage
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        room_list.Adult = genstat.erwachs
                        room_list.compli = genstat.gratis
                        room_list.ch1 = genstat.kind1
                        room_list.ch2 = genstat.kind2

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_adult = tot_adult + genstat.erwachs
                        tot_ch1 = tot_ch1 + genstat.kind1
                        tot_compli = tot_compli + genstat.gratis
                        tot_ch2 = tot_ch2 + genstat.kind2 + genstat.kind3
                        tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100
                        tot_nights = tot_nights + res_line.anztage
                        tot_qty = tot_qty + 1
                        tot_pax = tot_adult + tot_ch1 + tot_ch2 + tot_compli

        elif case_type == 3:

            genstat_obj_list = []
            for genstat, guest, zimkateg, waehrung, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                    (Genstat.res_date[0] >= datum) &  (Genstat.res_date[0] <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.datum == datum:
                    do_it = True

                    if do_it and not all_segm:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:
                        room_list = Room_list()
                        room_list_list.append(room_list)

                        room_list.qty = room_list.qty + 1
                        room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        room_list.resnr = to_string(genstat.resnr)
                        room_list.rmcat = zimkateg.kurzbez
                        room_list.rmno = genstat.zinr
                        room_list.kurzbez = zimkateg.kurzbez
                        room_list.depart = genstat.res_date[1]
                        room_list.arrival = genstat.res_date[0]
                        room_list.argt = genstat.argt
                        room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        room_list.Adult = genstat.erwachs
                        room_list.compli = genstat.gratis
                        room_list.ch1 = genstat.kind1
                        room_list.ch2 = genstat.kind2
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis)
                        tot_adult = tot_adult + genstat.erwachs
                        tot_ch1 = tot_ch1 + genstat.kind1
                        tot_compli = tot_compli + genstat.gratis
                        tot_ch2 = tot_ch2 + genstat.kind2
                        tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100
                        tot_qty = tot_qty + 1

        elif case_type == 5:

            genstat_obj_list = []
            for genstat, guest, zimkateg, waehrung, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                    (Genstat.res_date[1] >= datum) &  (Genstat.res_date[1] <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1]) &  (Genstat.zinr != " ")).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.res_date[1] == datum:
                    do_it = True

                    if do_it and not all_segm:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:

                        room_list = query(room_list_list, filters=(lambda room_list :room_list.resnr == to_string(genstat.resnr) and room_list.rmno == genstat.zinr), first=True)

                        if not room_list:
                            room_list = Room_list()
                            room_list_list.append(room_list)

                            room_list.qty = room_list.qty + 1
                            room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            room_list.resnr = to_string(genstat.resnr)
                            room_list.rmcat = zimkateg.kurzbez
                            room_list.rmno = genstat.zinr
                            room_list.pocc = (room_list.qty / tot_room) * 100
                            room_list.kurzbez = zimkateg.kurzbez
                            room_list.depart = genstat.res_date[1]
                            room_list.arrival = genstat.res_date[0]
                            room_list.argt = genstat.argt
                            room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            room_list.Adult = genstat.erwachs
                            room_list.compli = genstat.gratis
                            room_list.ch1 = genstat.kind1
                            room_list.ch2 = genstat.kind2
                            room_list.currency = waehrung.wabkurz
                            room_list.segment = segment.bezeich

                            if guest.karteityp != 0:
                                room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                            tot_pax = tot_pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis)
                            tot_adult = tot_adult + genstat.erwachs
                            tot_ch1 = tot_ch1 + genstat.kind1
                            tot_compli = tot_compli + genstat.gratis
                            tot_ch2 = tot_ch2 + genstat.kind2
                            tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100
                            tot_qty = tot_qty + 1

        elif case_type == 7:

            genstat_obj_list = []
            for genstat, guest, zimkateg, waehrung, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                    (Genstat.datum >= datum) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    1

                elif genstat.datum == datum:
                    do_it = True

                    if do_it and not all_segm:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_list, filters=(lambda a_list :a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list :z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:
                        room_list = Room_list()
                        room_list_list.append(room_list)

                        room_list.qty = room_list.qty + 1
                        room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        room_list.resnr = to_string(genstat.resnr)
                        room_list.rmcat = zimkateg.kurzbez
                        room_list.rmno = genstat.zinr
                        room_list.pocc = (room_list.qty / tot_room) * 100

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis)
                        tot_adult = tot_adult + genstat.erwachs
                        tot_ch1 = tot_ch1 + genstat.kind1
                        tot_compli = tot_compli + genstat.gratis
                        tot_ch2 = tot_ch2 + genstat.kind2
                        tot_pocc = tot_pocc + (room_list.qty / tot_room) * 100
                        tot_qty = tot_qty + 1

        elif case_type == 15:

            zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ooo") &  (Zinrstat.datum == datum)).first()

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

        if tot_pax != 0:
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.name = "T O T A L"
            room_list.adult = tot_adult
            room_list.compli = tot_compli
            room_list.ch1 = tot_ch1
            room_list.ch2 = tot_ch2
            room_list.nights = tot_nights
            room_list.qty = tot_qty
            room_list.pax = tot_pax
            room_list.pocc = tot_pocc

    pass

    create_browse()

    return generate_output()