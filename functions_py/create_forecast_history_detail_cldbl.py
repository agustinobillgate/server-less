#using conversion tools version: 1.0.0.117

#-----------------------------------------
# Rd, 31/7/2025
# gitlab: 130
# check datum None
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Res_line, Kontline, Guest, Nation, Genstat, Segment, Sourccod, Arrangement, Waehrung, Reservation, Bill_line, Zimmer, Queasy, Reslin_queasy

def create_forecast_history_detail_cldbl(fr_date:date, to_date:date, excl_comp:bool, vhp_limited:bool, scin:bool):

    prepare_cache ([Htparam, Res_line, Kontline, Guest, Nation, Genstat, Sourccod, Arrangement, Waehrung, Reservation, Queasy, Reslin_queasy])

    t_list_data = []
    ci_date:date = None
    htparam = res_line = kontline = guest = nation = genstat = segment = sourccod = arrangement = waehrung = reservation = bill_line = zimmer = queasy = reslin_queasy = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":Decimal, "bfast_guaranteed":Decimal, "lunch_guaranteed":Decimal, "dinner_guaranteed":Decimal, "misc_guaranteed":Decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":Decimal, "bfast_tentative":Decimal, "lunch_tentative":Decimal, "dinner_tentative":Decimal, "misc_tentative":Decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":string, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":string, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":string, "zipreis":Decimal, "flag_history":bool, "firmen_nr":int, "steuernr":string, "segmentcode":int, "segmentbez":string, "fcost":Decimal, "argtcode":string, "argtbez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, sourccod, arrangement, waehrung, reservation, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal t_list
        nonlocal t_list_data

        return {"t-list": t_list_data}

    def create_umsatz():

        nonlocal t_list_data, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, sourccod, arrangement, waehrung, reservation, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal t_list
        nonlocal t_list_data

        do_it:bool = False
        cur_date:date = None
        mm:int = 0
        yy:int = 0
        d2:date = None
        datum:date = None
        datum1:date = None
        datum2:date = None
        rmsharer:bool = False
        dayuse_flag:bool = False
        pax:int = 0
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        consider_it:bool = False
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        rline1 = None
        kline = None
        gmember = None
        gnation = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Kline =  create_buffer("Kline",Kontline)
        Gmember =  create_buffer("Gmember",Guest)
        Gnation =  create_buffer("Gnation",Nation)
        datum1 = fr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= d2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != "")).order_by(Genstat._recid).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                sourccod = get_cache (Sourccod, {"source_code": [(eq, genstat.source)]})

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.resnr = genstat.resnr
                t_list.reslinnr = genstat.res_int[0]

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nation.nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                gnation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnation.nationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

                if waehrung:
                    t_list.currency = waehrung.wabkurz

                if not rmsharer:
                    t_list.room_guaranteed = t_list.room_guaranteed + 1

                if scin:

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)]})

                    if res_line:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum1, 0, d2))
                        t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis) + to_decimal(tot_service)
                        t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                        t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                        t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                        t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                        t_list.fcost =  to_decimal(t_list.fcost) + to_decimal(genstat.res_deci[5])
                        t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.gratis + genstat.kind3
                        t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis) + to_decimal(tot_service)
                        t_list.flag_history = True
                        t_list.segmentcode = genstat.segmentcode
                        t_list.argtcode = res_line.arrangement


                else:
                    t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis)
                    t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                    t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                    t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                    t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                    t_list.fcost =  to_decimal(t_list.fcost) + to_decimal(genstat.res_deci[5])
                    t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis + genstat.kind3
                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis)
                    t_list.flag_history = True
                    t_list.segmentcode = genstat.segmentcode
                    # Rd 19/8/2025
                    # t_list.argtcode = genstat.Argt
                    t_list.argtcode = genstat.argt


    def create_umsatz_excl_compliment():

        nonlocal t_list_data, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, sourccod, arrangement, waehrung, reservation, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal t_list
        nonlocal t_list_data

        do_it:bool = False
        cur_date:date = None
        mm:int = 0
        yy:int = 0
        d2:date = None
        datum:date = None
        datum1:date = None
        datum2:date = None
        rmsharer:bool = False
        dayuse_flag:bool = False
        pax:int = 0
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        consider_it:bool = False
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        rline1 = None
        kline = None
        gmember = None
        gnation = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Kline =  create_buffer("Kline",Kontline)
        Gmember =  create_buffer("Gmember",Guest)
        Gnation =  create_buffer("Gnation",Nation)
        datum1 = fr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= d2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != "") & (Genstat.gratis == 0)).order_by(Genstat._recid).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                sourccod = get_cache (Sourccod, {"source_code": [(eq, genstat.source)]})

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.resnr = genstat.resnr
                t_list.reslinnr = genstat.res_int[0]

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nation.nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                gnation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnation.nationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

                if waehrung:
                    t_list.currency = waehrung.wabkurz

                if not rmsharer:
                    t_list.room_guaranteed = t_list.room_guaranteed + 1

                if scin:

                    res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)]})

                    if res_line:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum1, 0, d2))
                        t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis) + to_decimal(tot_service)
                        t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                        t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                        t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                        t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                        t_list.fcost =  to_decimal(t_list.fcost) + to_decimal(genstat.res_deci[5])
                        t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.gratis + genstat.kind3
                        t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis) + to_decimal(tot_service)
                        t_list.flag_history = True
                        t_list.segmentcode = genstat.segmentcode
                        t_list.argtcode = res_line.arrangement


                else:
                    t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis)
                    t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                    t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                    t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                    t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                    t_list.fcost =  to_decimal(t_list.fcost) + to_decimal(genstat.res_deci[5])
                    t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis + genstat.kind3
                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis)
                    t_list.flag_history = True
                    t_list.segmentcode = genstat.segmentcode
                    t_list.argtcode = genstat.argt


    def create_umsatz1():

        nonlocal t_list_data, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, sourccod, arrangement, waehrung, reservation, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal t_list
        nonlocal t_list_data

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        pax:int = 0
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        a:int = 0
        fnet_lodg:Decimal = to_decimal("0.0")
        rline1 = None
        kline = None
        gmember = None
        gnation = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Kline =  create_buffer("Kline",Kontline)
        Gmember =  create_buffer("Gmember",Guest)
        Gnation =  create_buffer("Gnation",Nation)

        if fr_date != ci_date and fr_date < ci_date:
            fr_date = ci_date
        datum1 = fr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)
        d2 = d2 + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:
                dayuse_flag = True

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                # Rd, 31/7/2025
                # queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})
                if datum is not None:
                    queasy = db_session.query(Queasy).filter(
                        Queasy.key == 14,
                        Queasy.char1 == res_line.zinr,
                        Queasy.date1 <= datum,
                        Queasy.date2 >= datum
                    ).first()
                else:
                    queasy = None

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nation.nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                gnation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnation.nationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    t_list.currency = waehrung.wabkurz
                t_list.resstatus = res_line.resstatus
                t_list.segmentcode = reservation.segmentcode
                t_list.argtcode = res_line.arrangement

                if res_line.ankunft >= fr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fr_date

                if res_line.abreise <= to_date:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = to_date
                for datum in date_range(datum1,datum2) :
                    a = a + 1
                    pax = res_line.erwachs
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")
                    tot_breakfast =  to_decimal("0")
                    tot_lunch =  to_decimal("0")
                    tot_dinner =  to_decimal("0")
                    tot_other =  to_decimal("0")


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, fr_date))

                    if tot_rmrev == 0:
                        local_net_lodg =  to_decimal("0")
                        net_lodg =  to_decimal("0")
                        tot_breakfast =  to_decimal("0")
                        tot_lunch =  to_decimal("0")
                        tot_dinner =  to_decimal("0")
                        tot_other =  to_decimal("0")


                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal((tot_rmrev) * to_decimal(res_line.zimmeranz))

                    if datum == ci_date:

                        if res_line.active_flag == 0 or (res_line.active_flag == 1 and res_line.resstatus != 8) or (res_line.active_flag == 1 and res_line.resstatus != 99):

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative =  to_decimal(t_list.bfast_tentative) + to_decimal(tot_breakfast)
                                t_list.lunch_tentative =  to_decimal(t_list.lunch_tentative) + to_decimal(tot_lunch)
                                t_list.dinner_tentative =  to_decimal(t_list.dinner_tentative) + to_decimal(tot_dinner)
                                t_list.misc_tentative =  to_decimal(t_list.misc_tentative) + to_decimal(tot_other)


                            else:
                                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(tot_breakfast)
                                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(tot_lunch)
                                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(tot_dinner)
                                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(tot_other)


                    else:

                        if datum < res_line.abreise:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative =  to_decimal(t_list.bfast_tentative) + to_decimal(tot_breakfast)
                                t_list.lunch_tentative =  to_decimal(t_list.lunch_tentative) + to_decimal(tot_lunch)
                                t_list.dinner_tentative =  to_decimal(t_list.dinner_tentative) + to_decimal(tot_dinner)
                                t_list.misc_tentative =  to_decimal(t_list.misc_tentative) + to_decimal(tot_other)


                            else:
                                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(tot_breakfast)
                                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(tot_lunch)
                                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(tot_dinner)
                                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(tot_other)

                    if datum == res_line.ankunft and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if res_line.ankunft < res_line.abreise or dayuse_flag:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                                if res_line.resstatus == 3:
                                    t_list.logis_tentative =  to_decimal(t_list.logis_tentative) + to_decimal(local_net_lodg)
                                    t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                                else:
                                    t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(local_net_lodg)
                                    t_list.room_guaranteed = t_list.room_guaranteed + res_line.zimmeranz

                            if res_line.resstatus != 11 and res_line.resstatus != 13:

                                if res_line.resstatus == 3:
                                    t_list.pax_tentative = t_list.pax_tentative + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                                else:
                                    t_list.pax_guaranteed = t_list.pax_guaranteed + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                    if datum == res_line.abreise and res_line.resstatus != 3 and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if datum != fr_date:
                            pass

                    if res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != datum and res_line.abreise != datum):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.resstatus == 3:
                                t_list.logis_tentative =  to_decimal(t_list.logis_tentative) + to_decimal(local_net_lodg)
                                t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                            else:
                                t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(local_net_lodg)
                                t_list.room_guaranteed = t_list.room_guaranteed + res_line.zimmeranz

                        if datum != fr_date:
                            pass

                        if res_line.resstatus != 11 and res_line.resstatus != 13:

                            if res_line.resstatus == 3:
                                t_list.pax_tentative = t_list.pax_tentative + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                            else:
                                t_list.pax_guaranteed = t_list.pax_guaranteed + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                    if res_line.resstatus == 3 and datum < res_line.abreise:
                        pass

                    if res_line.kontignr > 0 and res_line.active_flag <= 1 and res_line.resstatus <= 6 and res_line.resstatus != 3 and res_line.resstatus != 4 and res_line.abreise > datum:

                        kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"ankunft": [(le, datum)],"abreise": [(ge, datum)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

                        if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                            pass
        for datum in date_range(d2,to_date) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it:
                    pass


    def create_umsatz1_excl_compliment():

        nonlocal t_list_data, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, sourccod, arrangement, waehrung, reservation, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp, vhp_limited, scin


        nonlocal t_list
        nonlocal t_list_data

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        pax:int = 0
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        a:int = 0
        rline1 = None
        kline = None
        gmember = None
        gnation = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Kline =  create_buffer("Kline",Kontline)
        Gmember =  create_buffer("Gmember",Guest)
        Gnation =  create_buffer("Gnation",Nation)

        if fr_date != ci_date and fr_date < ci_date:
            fr_date = ci_date
        datum1 = fr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)
        d2 = d2 + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gratis == 0) & (Res_line.erwachs >= 1) & (Res_line.zipreis != 0) & ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

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

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nation.nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                gnation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnation.nationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    t_list.currency = waehrung.wabkurz
                t_list.resstatus = res_line.resstatus
                t_list.segmentcode = reservation.segmentcode
                t_list.argtcode = res_line.arrangement

                if res_line.ankunft >= fr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fr_date

                if res_line.abreise <= to_date:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = to_date
                for datum in date_range(datum1,datum2) :
                    a = a + 1
                    pax = res_line.erwachs
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")
                    tot_breakfast =  to_decimal("0")
                    tot_lunch =  to_decimal("0")
                    tot_dinner =  to_decimal("0")
                    tot_other =  to_decimal("0")


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, fr_date))

                    if tot_rmrev == 0:
                        local_net_lodg =  to_decimal("0")
                        net_lodg =  to_decimal("0")
                        tot_breakfast =  to_decimal("0")
                        tot_lunch =  to_decimal("0")
                        tot_dinner =  to_decimal("0")
                        tot_other =  to_decimal("0")


                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal((tot_rmrev) * to_decimal(res_line.zimmeranz))

                    if datum == ci_date:

                        if res_line.active_flag == 1 or dayuse_flag:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative =  to_decimal(t_list.bfast_tentative) + to_decimal(tot_breakfast)
                                t_list.lunch_tentative =  to_decimal(t_list.lunch_tentative) + to_decimal(tot_lunch)
                                t_list.dinner_tentative =  to_decimal(t_list.dinner_tentative) + to_decimal(tot_dinner)
                                t_list.misc_tentative =  to_decimal(t_list.misc_tentative) + to_decimal(tot_other)


                            else:
                                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(tot_breakfast)
                                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(tot_lunch)
                                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(tot_dinner)
                                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(tot_other)


                    else:

                        if datum < res_line.abreise:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative =  to_decimal(t_list.bfast_tentative) + to_decimal(tot_breakfast)
                                t_list.lunch_tentative =  to_decimal(t_list.lunch_tentative) + to_decimal(tot_lunch)
                                t_list.dinner_tentative =  to_decimal(t_list.dinner_tentative) + to_decimal(tot_dinner)
                                t_list.misc_tentative =  to_decimal(t_list.misc_tentative) + to_decimal(tot_other)


                            else:
                                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(tot_breakfast)
                                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(tot_lunch)
                                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(tot_dinner)
                                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(tot_other)

                    if datum == res_line.ankunft and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if res_line.ankunft < res_line.abreise or dayuse_flag:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                                if res_line.resstatus == 3:
                                    t_list.logis_tentative =  to_decimal(t_list.logis_tentative) + to_decimal(local_net_lodg)
                                    t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                                else:
                                    t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(local_net_lodg)
                                    t_list.room_guaranteed = t_list.room_guaranteed + res_line.zimmeranz

                            if res_line.resstatus != 11 and res_line.resstatus != 13:

                                if res_line.resstatus == 3:
                                    t_list.pax_tentative = t_list.pax_tentative + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                                else:
                                    t_list.pax_guaranteed = t_list.pax_guaranteed + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                    if datum == res_line.abreise and res_line.resstatus != 3 and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if datum != fr_date:
                            pass

                    if res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != datum and res_line.abreise != datum):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                            if res_line.resstatus == 3:
                                t_list.logis_tentative =  to_decimal(t_list.logis_tentative) + to_decimal(local_net_lodg)
                                t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                            else:
                                t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(local_net_lodg)
                                t_list.room_guaranteed = t_list.room_guaranteed + res_line.zimmeranz

                        if datum != fr_date:
                            pass

                        if res_line.resstatus != 11 and res_line.resstatus != 13:

                            if res_line.resstatus == 3:
                                t_list.pax_tentative = t_list.pax_tentative + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                            else:
                                t_list.pax_guaranteed = t_list.pax_guaranteed + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                    if res_line.resstatus == 3 and datum < res_line.abreise:
                        pass

                    if res_line.kontignr > 0 and res_line.active_flag <= 1 and res_line.resstatus <= 6 and res_line.resstatus != 3 and res_line.resstatus != 4 and res_line.abreise > datum:

                        kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"ankunft": [(le, datum)],"abreise": [(ge, datum)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

                        if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                            pass
        for datum in date_range(d2,to_date) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it:
                    pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    t_list_data.clear()

    if fr_date < ci_date:

        if not excl_comp:
            create_umsatz()
        else:
            create_umsatz_excl_compliment()

        if to_date >= ci_date:

            if not excl_comp:
                create_umsatz1()
            else:
                create_umsatz1_excl_compliment()
    else:

        if not excl_comp:
            create_umsatz1()
        else:
            create_umsatz1_excl_compliment()

    for t_list in query(t_list_data, filters=(lambda t_list:(t_list.pax_guaranteed == 0 and t_list.room_guaranteed == 0 and t_list.logis_guaranteed == 0) and (t_list.pax_tentative == 0 and t_list.room_tentative == 0 and t_list.logis_tentative == 0))):
        t_list_data.remove(t_list)

    return generate_output()