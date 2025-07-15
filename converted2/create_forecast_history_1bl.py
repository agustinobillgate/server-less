from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from sqlalchemy import func
from models import Htparam, Res_line, Kontline, Guest, Nation, Genstat, Segment, Waehrung, Reservation, Sourccod, Arrangement, Bill_line, Zimmer, Queasy, Reslin_queasy

def create_forecast_history_1bl(fr_date:date, to_date:date, excl_comp:bool, vhp_limited:bool, scin:bool):
    t_list_list = []
    ci_date:date = None
    htparam = res_line = kontline = guest = nation = genstat = segment = waehrung = reservation = sourccod = arrangement = bill_line = zimmer = queasy = reslin_queasy = None

    t_list = rline1 = kline = gmember = gnation = None

    t_list_list, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":decimal, "bfast_guaranteed":decimal, "lunch_guaranteed":decimal, "dinner_guaranteed":decimal, "misc_guaranteed":decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":decimal, "bfast_tentative":decimal, "lunch_tentative":decimal, "dinner_tentative":decimal, "misc_tentative":decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":str, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":str, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":str, "zipreis":decimal, "flag_history":bool, "firmen_nr":int, "steuernr":str, "segmentcode":int, "segmentbez":str, "fcost":decimal})

    Rline1 = Res_line
    Kline = Kontline
    Gmember = Guest
    Gnation = Nation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal rline1, kline, gmember, gnation


        nonlocal t_list, rline1, kline, gmember, gnation
        nonlocal t_list_list
        return {"t-list": t_list_list}

    def create_umsatz():

        nonlocal t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal rline1, kline, gmember, gnation


        nonlocal t_list, rline1, kline, gmember, gnation
        nonlocal t_list_list

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
        local_net_lodg:decimal = 0
        net_lodg:decimal = 0
        consider_it:bool = False
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        fnet_lodg:decimal = 0
        Rline1 = Res_line
        Kline = Kontline
        Gmember = Guest
        Gnation = Nation
        datum1 = fr_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= datum1) &  (Genstat.datum <= d2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != "")).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnr)).first()

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.nation1)).first()
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = db_session.query(Gmember).filter(
                        (Gmember.gastnr == genstat.gastnrmember)).first()

                gnation = db_session.query(Gnation).filter(
                        (Gnation.kurzbez == gmember.nation1)).first()

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.waehrungsnr == genstat.wahrungsnr)).first()

                if waehrung:
                    t_list.currency = waehrung.wabkurz

                if not rmsharer:
                    t_list.room_guaranteed = t_list.room_guaranteed + 1

                if scin:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr)).first()

                    if res_line:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum1, 0, d2))
                        t_list.logis_guaranteed = t_list.logis_guaranteed + genstat.logis + tot_service
                        t_list.bfast_guaranteed = t_list.bfast_guaranteed + genstat.res_deci[1]
                        t_list.lunch_guaranteed = t_list.lunch_guaranteed + genstat.res_deci[2]
                        t_list.dinner_guaranteed = t_list.dinner_guaranteed + genstat.res_deci[3]
                        t_list.misc_guaranteed = t_list.misc_guaranteed + genstat.res_deci[4] + genstat.res_deci[5]
                        t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.gratis + genstat.kind3
                        t_list.zipreis = t_list.zipreis + genstat.zipreis + tot_service
                        t_list.flag_history = True
                        t_list.segmentcode = genstat.segmentcode


                    else:

                        return
                else:
                    t_list.logis_guaranteed = t_list.logis_guaranteed + genstat.logis
                    t_list.bfast_guaranteed = t_list.bfast_guaranteed + genstat.res_deci[1]
                    t_list.lunch_guaranteed = t_list.lunch_guaranteed + genstat.res_deci[2]
                    t_list.dinner_guaranteed = t_list.dinner_guaranteed + genstat.res_deci[3]
                    t_list.misc_guaranteed = t_list.misc_guaranteed + genstat.res_deci[4] + genstat.res_deci[5]
                    t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis + genstat.kind3
                    t_list.zipreis = t_list.zipreis + genstat.zipreis
                    t_list.flag_history = True
                    t_list.segmentcode = genstat.segmentcode

    def create_umsatz_excl_compliment():

        nonlocal t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal rline1, kline, gmember, gnation


        nonlocal t_list, rline1, kline, gmember, gnation
        nonlocal t_list_list

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
        local_net_lodg:decimal = 0
        net_lodg:decimal = 0
        consider_it:bool = False
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        fnet_lodg:decimal = 0
        Rline1 = Res_line
        Kline = Kontline
        Gmember = Guest
        Gnation = Nation
        datum1 = fr_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= datum1) &  (Genstat.datum <= d2) &  (Genstat.res_logic[1]) &  (Genstat.zinr != "") &  (Genstat.gratis == 0)).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnr)).first()

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.nation1)).first()
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = db_session.query(Gmember).filter(
                        (Gmember.gastnr == genstat.gastnrmember)).first()

                gnation = db_session.query(Gnation).filter(
                        (Gnation.kurzbez == gmember.nation1)).first()

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.waehrungsnr == genstat.wahrungsnr)).first()

                if waehrung:
                    t_list.currency = waehrung.wabkurz

                if not rmsharer:
                    t_list.room_guaranteed = t_list.room_guaranteed + 1

                if scin:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr)).first()

                    if res_line:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum1, 0, d2))
                        t_list.logis_guaranteed = t_list.logis_guaranteed + genstat.logis + tot_service
                        t_list.bfast_guaranteed = t_list.bfast_guaranteed + genstat.res_deci[1]
                        t_list.lunch_guaranteed = t_list.lunch_guaranteed + genstat.res_deci[2]
                        t_list.dinner_guaranteed = t_list.dinner_guaranteed + genstat.res_deci[3]
                        t_list.misc_guaranteed = t_list.misc_guaranteed + genstat.res_deci[4] + genstat.res_deci[5]
                        t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.gratis + genstat.kind3
                        t_list.zipreis = t_list.zipreis + genstat.zipreis + tot_service
                        t_list.flag_history = True
                        t_list.segmentcode = genstat.segmentcode


                    else:

                        return
                else:
                    t_list.logis_guaranteed = t_list.logis_guaranteed + genstat.logis
                    t_list.bfast_guaranteed = t_list.bfast_guaranteed + genstat.res_deci[1]
                    t_list.lunch_guaranteed = t_list.lunch_guaranteed + genstat.res_deci[2]
                    t_list.dinner_guaranteed = t_list.dinner_guaranteed + genstat.res_deci[3]
                    t_list.misc_guaranteed = t_list.misc_guaranteed + genstat.res_deci[4] + genstat.res_deci[5]
                    t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis + genstat.kind3
                    t_list.zipreis = t_list.zipreis + genstat.zipreis
                    t_list.flag_history = True
                    t_list.segmentcode = genstat.segmentcode

    def create_umsatz1():

        nonlocal t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal rline1, kline, gmember, gnation


        nonlocal t_list, rline1, kline, gmember, gnation
        nonlocal t_list_list

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:decimal = 0
        net_lodg:decimal = 0
        pax:int = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        a:int = 0
        fnet_lodg:decimal = 0
        Rline1 = Res_line
        Kline = Kontline
        Gmember = Guest
        Gnation = Nation

        if fr_date != ci_date and fr_date < ci_date:
            fr_date = ci_date
        datum1 = fr_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1
        d2 = d2 + 1

        for res_line in db_session.query(Res_line).filter(
                ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < fr_date))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                    (Sourccod.source_code == reservation.resart)).first()
            tot_breakfast = 0
            tot_lunch = 0
            tot_dinner = 0
            tot_other = 0
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:
                dayuse_flag = True

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

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
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnr)).first()

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.nation1)).first()
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = db_session.query(Gmember).filter(
                        (Gmember.gastnr == res_line.gastnrmember)).first()

                gnation = db_session.query(Gnation).filter(
                        (Gnation.kurzbez == gmember.nation1)).first()

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = Gnation.nationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    t_list.currency = waehrung.wabkurz
                t_list.resstatus = res_line.resstatus
                t_list.segmentcode = reservation.segmentcode

                if res_line.ankunft >= fr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fr_date

                if res_line.abreise <= to_date:
                    datum2 = res_line.abreise - 1
                else:
                    datum2 = to_date
                for datum in range(datum1,datum2 + 1) :
                    a = a + 1
                    pax = res_line.erwachs
                    local_net_lodg = 0
                    net_lodg = 0

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
                    local_net_lodg = 0
                    net_lodg = 0
                    tot_breakfast = 0
                    tot_lunch = 0
                    tot_dinner = 0
                    tot_other = 0


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, fr_date))

                    if tot_rmrev == 0:
                        local_net_lodg = 0
                        net_lodg = 0
                        tot_breakfast = 0
                        tot_lunch = 0
                        tot_dinner = 0
                        tot_other = 0


                    t_list.zipreis = t_list.zipreis + (tot_rmrev * res_line.zimmeranz)

                    if datum == ci_date:

                        if res_line.active_flag == 0 or (res_line.active_flag == 1 and res_line.resstatus != 8) or (res_line.active_flag == 1 and res_line.resstatus != 99):

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative = t_list.bfast_tentative + tot_breakfast
                                t_list.lunch_tentative = t_list.lunch_tentative + tot_lunch
                                t_list.dinner_tentative = t_list.dinner_tentative + tot_dinner
                                t_list.misc_tentative = t_list.misc_tentative + tot_other


                            else:
                                t_list.bfast_guaranteed = t_list.bfast_guaranteed + tot_breakfast
                                t_list.lunch_guaranteed = t_list.lunch_guaranteed + tot_lunch
                                t_list.dinner_guaranteed = t_list.dinner_guaranteed + tot_dinner
                                t_list.misc_guaranteed = t_list.misc_guaranteed + tot_other


                    else:

                        if datum < res_line.abreise:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative = t_list.bfast_tentative + tot_breakfast
                                t_list.lunch_tentative = t_list.lunch_tentative + tot_lunch
                                t_list.dinner_tentative = t_list.dinner_tentative + tot_dinner
                                t_list.misc_tentative = t_list.misc_tentative + tot_other


                            else:
                                t_list.bfast_guaranteed = t_list.bfast_guaranteed + tot_breakfast
                                t_list.lunch_guaranteed = t_list.lunch_guaranteed + tot_lunch
                                t_list.dinner_guaranteed = t_list.dinner_guaranteed + tot_dinner
                                t_list.misc_guaranteed = t_list.misc_guaranteed + tot_other

                    if datum == res_line.ankunft and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if res_line.ankunft < res_line.abreise or dayuse_flag:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                                if res_line.resstatus == 3:
                                    t_list.logis_tentative = t_list.logis_tentative + local_net_lodg
                                    t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                                else:
                                    t_list.logis_guaranteed = t_list.logis_guaranteed + local_net_lodg
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
                                t_list.logis_tentative = t_list.logis_tentative + local_net_lodg
                                t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                            else:
                                t_list.logis_guaranteed = t_list.logis_guaranteed + local_net_lodg
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

                        kline = db_session.query(Kline).filter(
                                (Kline.kontignr == res_line.kontignr) &   1)).first()

                        kontline = db_session.query(Kontline).filter(
                                (Kontline.kontcode == kline.kontcode) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstatus  == 1)).first()

                        if kontline and datum >= (ci_date + kontline.ruecktage):
                            pass
        for datum in range(d2,to_date + 1) :

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstatus  == 1)).all():
                do_it = True

                if do_it:
                    pass

    def create_umsatz1_excl_compliment():

        nonlocal t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal rline1, kline, gmember, gnation


        nonlocal t_list, rline1, kline, gmember, gnation
        nonlocal t_list_list

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:decimal = 0
        net_lodg:decimal = 0
        pax:int = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        a:int = 0
        Rline1 = Res_line
        Kline = Kontline
        Gmember = Guest
        Gnation = Nation

        if fr_date != ci_date and fr_date < ci_date:
            fr_date = ci_date
        datum1 = fr_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1
        d2 = d2 + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.gratis == 0) &  (Res_line.erwachs >= 1) &  (Res_line.zipreis != 0) &  ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < fr_date))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                    (Sourccod.source_code == reservation.resart)).first()
            tot_breakfast = 0
            tot_lunch = 0
            tot_dinner = 0
            tot_other = 0
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:
                dayuse_flag = True

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

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
                t_list = T_list()
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnr)).first()

                if guest:
                    t_list.firmen_nr = guest.firmen_nr
                    t_list.steuernr = guest.steuernr

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.nation1)).first()
                    t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.rsv_karteityp = guest.karteityp

                    if nation:
                        t_list.rsv_nationnr = nationnr
                else:
                    t_list.rsv_nationnr = 999

                gmember = db_session.query(Gmember).filter(
                        (Gmember.gastnr == res_line.gastnrmember)).first()

                gnation = db_session.query(Gnation).filter(
                        (Gnation.kurzbez == gmember.nation1)).first()

                if gmember:
                    t_list.guest_name = gmember.name + ", " + gmember.vorname1 + " " +\
                            gmember.anrede1 + gmember.anredefirma
                    t_list.guest_karteityp = gmember.karteityp

                if gnation:
                    t_list.guest_nationnr = gnationnr
                else:
                    t_list.guest_nationnr = 999

                if sourccod:
                    t_list.sob = sourccod.source_code
                else:
                    t_list.sob = 999

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    t_list.currency = waehrung.wabkurz
                t_list.resstatus = res_line.resstatus
                t_list.segmentcode = reservation.segmentcode

                if res_line.ankunft >= fr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fr_date

                if res_line.abreise <= to_date:
                    datum2 = res_line.abreise - 1
                else:
                    datum2 = to_date
                for datum in range(datum1,datum2 + 1) :
                    a = a + 1
                    pax = res_line.erwachs
                    local_net_lodg = 0
                    net_lodg = 0

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
                    local_net_lodg = 0
                    net_lodg = 0
                    tot_breakfast = 0
                    tot_lunch = 0
                    tot_dinner = 0
                    tot_other = 0


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, fr_date))

                    if tot_rmrev == 0:
                        local_net_lodg = 0
                        net_lodg = 0
                        tot_breakfast = 0
                        tot_lunch = 0
                        tot_dinner = 0
                        tot_other = 0


                    t_list.zipreis = t_list.zipreis + (tot_rmrev * res_line.zimmeranz)

                    if datum == ci_date:

                        if res_line.active_flag == 1 or dayuse_flag:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative = t_list.bfast_tentative + tot_breakfast
                                t_list.lunch_tentative = t_list.lunch_tentative + tot_lunch
                                t_list.dinner_tentative = t_list.dinner_tentative + tot_dinner
                                t_list.misc_tentative = t_list.misc_tentative + tot_other


                            else:
                                t_list.bfast_guaranteed = t_list.bfast_guaranteed + tot_breakfast
                                t_list.lunch_guaranteed = t_list.lunch_guaranteed + tot_lunch
                                t_list.dinner_guaranteed = t_list.dinner_guaranteed + tot_dinner
                                t_list.misc_guaranteed = t_list.misc_guaranteed + tot_other


                    else:

                        if datum < res_line.abreise:

                            if res_line.resstatus == 3:
                                t_list.bfast_tentative = t_list.bfast_tentative + tot_breakfast
                                t_list.lunch_tentative = t_list.lunch_tentative + tot_lunch
                                t_list.dinner_tentative = t_list.dinner_tentative + tot_dinner
                                t_list.misc_tentative = t_list.misc_tentative + tot_other


                            else:
                                t_list.bfast_guaranteed = t_list.bfast_guaranteed + tot_breakfast
                                t_list.lunch_guaranteed = t_list.lunch_guaranteed + tot_lunch
                                t_list.dinner_guaranteed = t_list.dinner_guaranteed + tot_dinner
                                t_list.misc_guaranteed = t_list.misc_guaranteed + tot_other

                    if datum == res_line.ankunft and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            pass

                        if res_line.ankunft < res_line.abreise or dayuse_flag:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:

                                if res_line.resstatus == 3:
                                    t_list.logis_tentative = t_list.logis_tentative + local_net_lodg
                                    t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                                else:
                                    t_list.logis_guaranteed = t_list.logis_guaranteed + local_net_lodg
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
                                t_list.logis_tentative = t_list.logis_tentative + local_net_lodg
                                t_list.room_tentative = t_list.room_tentative + res_line.zimmeranz


                            else:
                                t_list.logis_guaranteed = t_list.logis_guaranteed + local_net_lodg
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

                        kline = db_session.query(Kline).filter(
                                (Kline.kontignr == res_line.kontignr) &   1)).first()

                        kontline = db_session.query(Kontline).filter(
                                (Kontline.kontcode == kline.kontcode) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstatus  == 1)).first()

                        if kontline and datum >= (ci_date + kontline.ruecktage):
                            pass
        for datum in range(d2,to_date + 1) :

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstatus  == 1)).all():
                do_it = True

                if do_it:
                    pass

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    t_list_list.clear()

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

    for t_list in query(t_list_list, filters=(lambda t_list :(t_list.pax_guaranteed == 0 and t_list.room_guaranteed == 0 and t_list.logis_guaranteed == 0) and (t_list.pax_tentative == 0 and t_list.room_tentative == 0 and t_list.logis_tentative == 0))):
        t_list_list.remove(t_list)

    return generate_output()