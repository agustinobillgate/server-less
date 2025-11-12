#using conversion tools version: 1.0.0.119

# ==============================
# Rulita, 03-11-2025 | 17B500
# - New compile program
# ==============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Zimmer, Guest, Zimkateg, Waehrung, Res_line, Segment, Genstat, History, Zinrstat, Outorder

argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
segm_list_data, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":string})

def occ_fcast1_ddown_create_browsebl(case_type:int, datum:date, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, argt_list_data:[Argt_list], segm_list_data:[Segm_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Zimmer, Guest, Zimkateg, Waehrung, Res_line, Segment, Genstat, Outorder])

    room_list_data = []
    kontline = zimmer = guest = zimkateg = waehrung = res_line = segment = genstat = history = zinrstat = outorder = None

    room_list = segm_list = argt_list = zikat_list = rmcat_list = s_list = a_list = z_list = None

    room_list_data, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":string, "room":[Decimal,17], "coom":[string,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,4], "avrglodg":Decimal, "resnr":string, "rmno":string, "rmcat":string, "name":string, "argt":string, "company":string, "segment":string, "currency":string, "adult":int, "ch1":int, "ch2":int, "compli":int, "depart":date, "arrival":date, "nights":int, "arrtime":string, "deptime":string, "qty":int, "pax":int, "pocc":Decimal, "sleeping":bool, "t_avail":int, "t_ooo":int, "t_alot":int, "t_occ":int, "zikatnr":int, "kurzbez":string})
    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":string, "bezeich":string, "zinr":string}, {"sleeping": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, kontline, zimmer, guest, zimkateg, waehrung, res_line, segment, genstat, history, zinrstat, outorder
        nonlocal case_type, datum, curr_date, to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, s_list, a_list, z_list
        nonlocal room_list_data, rmcat_list_data

        return {"room-list": room_list_data}

    def create_browse():

        nonlocal room_list_data, kontline, zimmer, guest, zimkateg, waehrung, res_line, segment, genstat, history, zinrstat, outorder
        nonlocal case_type, datum, curr_date, to_date, all_segm, all_argt, all_zikat


        nonlocal room_list, segm_list, argt_list, zikat_list, rmcat_list, s_list, a_list, z_list
        nonlocal room_list_data, rmcat_list_data

        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        datum1:date = None
        datum2:date = None
        d2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:Decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        rm_array:List[int] = create_empty_list(18,0)
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:Decimal = to_decimal("0.0")
        rmsharer:bool = False
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
        tot_room:int = 0
        mtd_tot_room:int = 0
        accum_tot_room:int = 0
        actual_tot_room:int = 0
        S_list = Segm_list
        s_list_data = segm_list_data
        A_list = Argt_list
        a_list_data = argt_list_data
        Z_list = Zikat_list
        z_list_data = zikat_list_data
        Kline =  create_buffer("Kline",Kontline)
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == zimmer.zikatnr and zikat_list.selected), first=True)

                if zikat_list:
                    tot_room = tot_room + 1

        if case_type == 1:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            zimkateg = Zimkateg()
            waehrung = Waehrung()
            res_line = Res_line()
            segment = Segment()
            for genstat.datum, genstat.resstatus, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.resnr, genstat.zinr, genstat.res_date, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.res_int, genstat.logis, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, zimkateg.kurzbez, zimkateg._recid, waehrung.wabkurz, waehrung._recid, res_line.anztage, res_line._recid, segment.bezeich, segment._recid in db_session.query(Genstat.datum, Genstat.resstatus, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.resnr, Genstat.zinr, Genstat.res_date, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.res_int, Genstat.logis, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Waehrung.wabkurz, Waehrung._recid, Res_line.anztage, Res_line._recid, Segment.bezeich, Segment._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.datum >= (datum - timedelta(days=1))) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.datum == (datum - timedelta(days=1)):
                    do_it = True

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        do_it = False

                    if do_it and not all_segm:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it :
                        room_list = Room_list()
                        room_list_data.append(room_list)

                        room_list.qty = room_list.qty + 1
                        room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        room_list.resnr = to_string(genstat.resnr)
                        room_list.rmcat = zimkateg.kurzbez
                        room_list.rmno = genstat.zinr
                        room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        room_list.depart = genstat.res_date[1]
                        room_list.arrival = genstat.res_date[0]
                        room_list.argt = genstat.argt
                        room_list.nights = res_line.anztage
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        room_list.adult = genstat.erwachs
                        room_list.compli = genstat.gratis
                        room_list.ch1 = genstat.kind1
                        room_list.ch2 = genstat.kind2

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_adult = tot_adult + genstat.erwachs
                        tot_ch1 = tot_ch1 + genstat.kind1
                        tot_compli = tot_compli + genstat.gratis
                        tot_ch2 = tot_ch2 + genstat.kind2 + genstat.kind3
                        tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        tot_nights = tot_nights + res_line.anztage
                        tot_qty = tot_qty + 1
                        tot_pax = tot_adult + tot_ch1 + tot_ch2 + tot_compli

        elif case_type == 3:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            zimkateg = Zimkateg()
            waehrung = Waehrung()
            segment = Segment()
            for genstat.datum, genstat.resstatus, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.resnr, genstat.zinr, genstat.res_date, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.res_int, genstat.logis, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, zimkateg.kurzbez, zimkateg._recid, waehrung.wabkurz, waehrung._recid, segment.bezeich, segment._recid in db_session.query(Genstat.datum, Genstat.resstatus, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.resnr, Genstat.zinr, Genstat.res_date, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.res_int, Genstat.logis, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Waehrung.wabkurz, Waehrung._recid, Segment.bezeich, Segment._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.res_date[0] >= datum) & (Genstat.res_date[0] <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.datum == datum:
                    do_it = True

                    if do_it and not all_segm:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:
                        room_list = Room_list()
                        room_list_data.append(room_list)

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
                        room_list.adult = genstat.erwachs
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
                        tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        tot_qty = tot_qty + 1

        elif case_type == 5:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            zimkateg = Zimkateg()
            waehrung = Waehrung()
            segment = Segment()
            for genstat.datum, genstat.resstatus, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.resnr, genstat.zinr, genstat.res_date, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.res_int, genstat.logis, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, zimkateg.kurzbez, zimkateg._recid, waehrung.wabkurz, waehrung._recid, segment.bezeich, segment._recid in db_session.query(Genstat.datum, Genstat.resstatus, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.resnr, Genstat.zinr, Genstat.res_date, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.res_int, Genstat.logis, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Waehrung.wabkurz, Waehrung._recid, Segment.bezeich, Segment._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.res_date[inc_value(1)] >= datum) & (Genstat.res_date[inc_value(1)] <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.res_date[1] == datum:

                    history = get_cache (History, {"zinr": [(eq, genstat.zinr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"zi_wechsel": [(eq, True)]})
                    do_it = not None != history

                    if do_it and not all_segm:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.resnr == to_string(genstat.resnr) and room_list.rmno == genstat.zinr), first=True)

                        if not room_list:
                            room_list = Room_list()
                            room_list_data.append(room_list)

                            room_list.qty = room_list.qty + 1
                            room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            room_list.resnr = to_string(genstat.resnr)
                            room_list.rmcat = zimkateg.kurzbez
                            room_list.rmno = genstat.zinr
                            room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                            room_list.kurzbez = zimkateg.kurzbez
                            room_list.depart = genstat.res_date[1]
                            room_list.arrival = genstat.res_date[0]
                            room_list.argt = genstat.argt
                            room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            room_list.adult = genstat.erwachs
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
                            tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                            tot_qty = tot_qty + 1

        elif case_type == 7:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            zimkateg = Zimkateg()
            waehrung = Waehrung()
            segment = Segment()
            for genstat.datum, genstat.resstatus, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.resnr, genstat.zinr, genstat.res_date, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.res_int, genstat.logis, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, zimkateg.kurzbez, zimkateg._recid, waehrung.wabkurz, waehrung._recid, segment.bezeich, segment._recid in db_session.query(Genstat.datum, Genstat.resstatus, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.resnr, Genstat.zinr, Genstat.res_date, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.res_int, Genstat.logis, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid, Waehrung.wabkurz, Waehrung._recid, Segment.bezeich, Segment._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                     (Genstat.datum >= datum) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                    pass

                elif genstat.datum == datum:
                    do_it = True

                    if do_it and not all_segm:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                    if do_it and not all_argt:

                        a_list = query(a_list_data, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                        do_it = None != a_list

                    if do_it and not all_zikat:

                        z_list = query(z_list_data, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                        do_it = None != z_list

                    if do_it:
                        room_list = Room_list()
                        room_list_data.append(room_list)

                        room_list.qty = room_list.qty + 1
                        room_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        room_list.resnr = to_string(genstat.resnr)
                        room_list.rmcat = zimkateg.kurzbez
                        room_list.rmno = genstat.zinr
                        room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        room_list.kurzbez = zimkateg.kurzbez
                        room_list.depart = genstat.res_date[1]
                        room_list.arrival = genstat.res_date[0]
                        room_list.argt = genstat.argt
                        room_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        room_list.adult = genstat.erwachs
                        room_list.compli = genstat.gratis
                        room_list.ch1 = genstat.kind1
                        room_list.ch2 = genstat.kind2
                        room_list.currency = waehrung.wabkurz
                        room_list.segment = segment.bezeich
                        room_list.pocc = ( to_decimal(room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        room_list.lodg[3] = genstat.logis

                        if guest.karteityp != 0:
                            room_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        tot_pax = tot_pax + (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis)
                        tot_adult = tot_adult + genstat.erwachs
                        tot_ch1 = tot_ch1 + genstat.kind1
                        tot_compli = tot_compli + genstat.gratis
                        tot_ch2 = tot_ch2 + genstat.kind2
                        tot_pocc =  to_decimal(tot_pocc) + to_decimal((room_list.qty) / to_decimal(tot_room)) * to_decimal("100")
                        tot_qty = tot_qty + 1
                        tot_lodg =  to_decimal(tot_lodg) + to_decimal(genstat.logis)

        elif case_type == 15:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, datum)]})

            if zinrstat:
                pass
            else:

                outorder_obj_list = {}
                outorder = Outorder()
                zimmer = Zimmer()
                for outorder.zinr, outorder.gespgrund, outorder.gespende, outorder.gespstart, outorder._recid, zimmer.zikatnr, zimmer.bezeich, zimmer._recid in db_session.query(Outorder.zinr, Outorder.gespgrund, Outorder.gespende, Outorder.gespstart, Outorder._recid, Zimmer.zikatnr, Zimmer.bezeich, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
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

        if tot_pax != 0:
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = "T O T A L"
            room_list.adult = tot_adult
            room_list.compli = tot_compli
            room_list.ch1 = tot_ch1
            room_list.ch2 = tot_ch2
            room_list.nights = tot_nights
            room_list.qty = tot_qty
            room_list.pax = tot_pax
            room_list.pocc =  to_decimal(tot_pocc)

            if case_type == 7:
                room_list.lodg[3] = tot_lodg


    create_browse()

    return generate_output()