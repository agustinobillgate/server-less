from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Res_line, Kontline, Guest, Nation, Genstat, Segment, Waehrung, Reservation, Sourccod, Arrangement, Bill_line, Zimmer, Queasy, Reslin_queasy

def create_forecast_history(fr_date:date, to_date:date, excl_comp:bool):
    var = None
    t_list_list = []
    ci_date:date = None
    htparam = res_line = kontline = guest = nation = genstat = segment = waehrung = reservation = sourccod = arrangement = bill_line = zimmer = queasy = reslin_queasy = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":decimal, "bfast_guaranteed":decimal, "lunch_guaranteed":decimal, "dinner_guaranteed":decimal, "misc_guaranteed":decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":decimal, "bfast_tentative":decimal, "lunch_tentative":decimal, "dinner_tentative":decimal, "misc_tentative":decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":str, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":str, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":str, "zipreis":decimal, "flag_history":bool, "firmen_nr":int, "steuernr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal var, t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp


        nonlocal t_list
        nonlocal t_list_list

        return {"t-list": t_list_list}

    def create_umsatz():

        nonlocal var, t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp


        nonlocal t_list
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
        local_net_lodg:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        consider_it:bool = False
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
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

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == genstat.gastnr)).first()
                t_list.firmen_nr = guest.firmen_nr
                t_list.steuernr = guest.steuernr

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()
                t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                t_list.rsv_karteityp = guest.karteityp

                if nation:
                    t_list.rsv_nationnr = nation.nationnr
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
                    t_list.guest_nationnr = gnation.nationnr
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
                t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis)
                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                        genstat.kind2 + genstat.gratis + genstat.kind3
                t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis)
                t_list.flag_history = True


    def create_umsatz_excl_compliment():

        nonlocal var, t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp


        nonlocal t_list
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
        local_net_lodg:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        consider_it:bool = False
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
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

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it:
                t_list = T_list()
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == genstat.gastnr)).first()
                t_list.firmen_nr = guest.firmen_nr
                t_list.steuernr = guest.steuernr

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()
                t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                t_list.rsv_karteityp = guest.karteityp

                if nation:
                    t_list.rsv_nationnr = nation.nationnr
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
                    t_list.guest_nationnr = gnation.nationnr
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
                t_list.logis_guaranteed =  to_decimal(t_list.logis_guaranteed) + to_decimal(genstat.logis)
                t_list.bfast_guaranteed =  to_decimal(t_list.bfast_guaranteed) + to_decimal(genstat.res_deci[1])
                t_list.lunch_guaranteed =  to_decimal(t_list.lunch_guaranteed) + to_decimal(genstat.res_deci[2])
                t_list.dinner_guaranteed =  to_decimal(t_list.dinner_guaranteed) + to_decimal(genstat.res_deci[3])
                t_list.misc_guaranteed =  to_decimal(t_list.misc_guaranteed) + to_decimal(genstat.res_deci[4])
                t_list.pax_guaranteed = t_list.pax_guaranteed + genstat.erwachs + genstat.kind1 +\
                        genstat.kind2 + genstat.gratis + genstat.kind3
                t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal(genstat.zipreis)
                t_list.flag_history = True


    def create_umsatz1():

        nonlocal var, t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp


        nonlocal t_list
        nonlocal t_list_list

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        pax:int = 0
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
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
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < fr_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                     (Sourccod.source_code == reservation.resart)).first()
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
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
                         (Arrangement.arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == ci_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == res_line.zinr)).first()

            if do_it and zimmer:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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
                t_list_list.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr)).first()
                t_list.firmen_nr = guest.firmen_nr
                t_list.steuernr = guest.steuernr

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()
                t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                t_list.rsv_karteityp = guest.karteityp

                if nation:
                    t_list.rsv_nationnr = nation.nationnr
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
                    t_list.guest_nationnr = gnation.nationnr
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

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                 (Rline1.resnr == res_line.resnr) & (Rline1.reslinnr != res_line.reslinnr) & (Rline1.resstatus == 8) & (Rline1.abreise > datum)).first()

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

                        kline = db_session.query(Kline).filter(
                                 (Kline.kontignr == res_line.kontignr) & (Kline.kontstat == 1)).first()

                        kontline = db_session.query(Kontline).filter(
                                 (Kontline.kontcode == kline.kontcode) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstat == 1)).first()

                        if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                            pass
        for datum in date_range(d2,to_date) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it:
                    pass


    def create_umsatz1_excl_compliment():

        nonlocal var, t_list_list, ci_date, htparam, res_line, kontline, guest, nation, genstat, segment, waehrung, reservation, sourccod, arrangement, bill_line, zimmer, queasy, reslin_queasy
        nonlocal fr_date, to_date, excl_comp


        nonlocal t_list
        nonlocal t_list_list

        do_it:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        pax:int = 0
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
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

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                     (Sourccod.source_code == reservation.resart)).first()
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
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
                         (Arrangement.arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == ci_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == res_line.zinr)).first()

            if do_it and zimmer:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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
                t_list_list.append(t_list)


                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr)).first()
                t_list.firmen_nr = guest.firmen_nr
                t_list.steuernr = guest.steuernr

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()
                t_list.rsv_name = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                t_list.rsv_karteityp = guest.karteityp

                if nation:
                    t_list.rsv_nationnr = nation.nationnr
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
                    t_list.guest_nationnr = gnation.nationnr
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

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = db_session.query(Rline1).filter(
                                 (Rline1.resnr == res_line.resnr) & (Rline1.reslinnr != res_line.reslinnr) & (Rline1.resstatus == 8) & (Rline1.abreise > datum)).first()

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

                        kline = db_session.query(Kline).filter(
                                 (Kline.kontignr == res_line.kontignr) & (Kline.kontstat == 1)).first()

                        kontline = db_session.query(Kontline).filter(
                                 (Kontline.kontcode == kline.kontcode) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstat == 1)).first()

                        if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                            pass
        for datum in date_range(d2,to_date) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
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

    for t_list in query(t_list_list, filters=(lambda t_list:(t_list.pax_guaranteed == 0 and t_list.room_guaranteed == 0 and t_list.logis_guaranteed == 0) and (t_list.pax_tentative == 0 and t_list.room_tentative == 0 and t_list.logis_tentative == 0))):
        t_list_list.remove(t_list)

    return generate_output()