#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servvat import calc_servvat
from models import Res_line, Htparam, Genstat, Segment, Reservation, Arrangement, Bill_line, Zimmer, Queasy, Waehrung, Zkstat, Artikel, Umsatz

def nt_tauziarpt_gen_occfcastbl(lydate:date, casetype:int, currdate:date, curr_date:date):
    avrgrate = to_decimal("0.0")
    lyavrgrate = to_decimal("0.0")
    qtygroupd = 0
    lyqtygroupd = 0
    qtygroupt = 0
    qtyfit = 0
    lyqtyfit = 0
    totroom = 0
    lytotroom = 0
    avrg_leadtime = to_decimal("0.0")
    pay = 0
    lypay = 0
    lyqtygroupt:int = 0
    lyavrg_leadtime:decimal = to_decimal("0.0")
    otherrev:decimal = to_decimal("0.0")
    res_line = htparam = genstat = segment = reservation = arrangement = bill_line = zimmer = queasy = waehrung = zkstat = artikel = umsatz = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avrgrate, lyavrgrate, qtygroupd, lyqtygroupd, qtygroupt, qtyfit, lyqtyfit, totroom, lytotroom, avrg_leadtime, pay, lypay, lyqtygroupt, lyavrg_leadtime, otherrev, res_line, htparam, genstat, segment, reservation, arrangement, bill_line, zimmer, queasy, waehrung, zkstat, artikel, umsatz
        nonlocal lydate, casetype, currdate, curr_date

        return {"avrgrate": avrgrate, "lyavrgrate": lyavrgrate, "qtygroupd": qtygroupd, "lyqtygroupd": lyqtygroupd, "qtygroupt": qtygroupt, "qtyfit": qtyfit, "lyqtyfit": lyqtyfit, "totroom": totroom, "lytotroom": lytotroom, "avrg_leadtime": avrg_leadtime, "pay": pay, "lypay": lypay}

    def count_occ(casetype:int, period:date):

        nonlocal avrgrate, lyavrgrate, qtygroupd, lyqtygroupd, qtygroupt, qtyfit, lyqtyfit, totroom, lytotroom, avrg_leadtime, lypay, lyqtygroupt, lyavrg_leadtime, otherrev, res_line, htparam, genstat, segment, reservation, arrangement, bill_line, zimmer, queasy, waehrung, zkstat, artikel, umsatz
        nonlocal lydate, currdate, curr_date

        gid = 0
        git = 0
        fit = 0
        avrg_rate = to_decimal("0.0")
        pay1 = 0
        avrg_leadtime = to_decimal("0.0")
        do_it:bool = False
        rmsharer:bool = False
        dayuse_flag:bool = False
        consider_it:bool = False
        ci_date:date = None
        pay:int = 0
        pay_comp:int = 0
        lodg_betrag:decimal = to_decimal("0.0")
        argt_betrag:decimal = to_decimal("0.0")
        ex_rate:decimal = to_decimal("0.0")
        frate:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        price_dec:int = 0
        rm_serv = None
        rm_vat = None
        fnet_lodg:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
        lead_time:int = 0
        resnr_genstat:int = 0
        counter:int = 0
        rline1 = None

        def generate_inner_output():
            return (gid, git, fit, avrg_rate, pay1, avrg_leadtime)

        Rline1 =  create_buffer("Rline1",Res_line)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
        price_dec = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 127)).first()
        rm_vat = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 128)).first()
        rm_serv = htparam.flogical

        if casetype == 1:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == period) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                do_it = True

                if do_it:

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == genstat.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0
                rmsharer = (genstat.resstatus == 13)

                if do_it:

                    if not rmsharer:
                        pay1 = pay1 + 1

                        if genstat.gratis == 0 and genstat.zipreis != 0:
                            pay = pay + 1

                        if genstat.res_date[0] == genstat.datum:
                            counter = counter + 1

                            reservation = db_session.query(Reservation).filter(
                                     (Reservation.resnr == genstat.resnr)).first()

                            if reservation:
                                lead_time = lead_time + (genstat.res_date[0] - reservation.resdat)
                        avrg_rate =  to_decimal(avrg_rate) + to_decimal(genstat.logis)

                    if genstat.res_char[2] != "":
                        gid = gid + 1
                    else:
                        fit = fit + 1

            if counter != 0:
                avrg_leadtime =  to_decimal(lead_time) / to_decimal(counter)
            otherrev = calc_othrev(period)
            avrg_rate =  to_decimal(avrg_rate) + to_decimal(otherrev)
        else:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > period)) & (not_ (Res_line.abreise < period))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                do_it = True
                dayuse_flag = False

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

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
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= period) & (Queasy.date2 >= period)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False
                consider_it = True

                if res_line.zimmerfix:

                    rline1 = db_session.query(Rline1).filter(
                             (Rline1.resnr == res_line.resnr) & (Rline1.reslinnr != res_line.reslinnr) & (Rline1.resstatus == 8) & (Rline1.abreise > period)).first()

                    if rline1:
                        consider_it = False

                if do_it:

                    if res_line.resstatus != 3:
                        net_lodg =  to_decimal("0")
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, period, 1, period))

                    if (res_line.resstatus == 3 or res_line.resstatus == 4) and reservation.groupname != "":
                        git = git + res_line.zimmeranz

                    if period == res_line.ankunft and consider_it and res_line.resstatus != 3:

                        if res_line.ankunft < res_line.abreise or res_line.ankunft == res_line.abreise:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:

                                if res_line.reserve_dec != 0:
                                    frate =  to_decimal(res_line.reserve_dec)
                                else:

                                    waehrung = db_session.query(Waehrung).filter(
                                             (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                                    if waehrung:
                                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                                lead_time = lead_time + (res_line.ankunft - reservation.resdat)
                                counter = counter + res_line.zimmeranz
                                pay1 = pay1 + res_line.zimmeranz

                                if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                    pay_comp = pay_comp + res_line.zimmeranz
                                else:
                                    avrg_rate =  to_decimal(avrg_rate) + to_decimal(net_lodg)
                                pay = pay1 - pay_comp

                                if reservation.groupname != "":
                                    gid = gid + res_line.zimmeranz
                                else:
                                    fit = fit + res_line.zimmeranz

                    if res_line.resstatus != 3 and res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != period and res_line.abreise != period):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:

                            if res_line.reserve_dec != 0:
                                frate =  to_decimal(res_line.reserve_dec)
                            else:

                                waehrung = db_session.query(Waehrung).filter(
                                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                                if waehrung:
                                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            pay1 = pay1 + res_line.zimmeranz

                            if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                pay_comp = pay_comp + res_line.zimmeranz
                            else:
                                avrg_rate =  to_decimal(avrg_rate) + to_decimal(net_lodg)
                            pay = pay1 - pay_comp

                            if reservation.groupname != "":
                                gid = gid + res_line.zimmeranz
                            else:
                                fit = fit + res_line.zimmeranz

            if counter != 0:
                avrg_leadtime =  to_decimal(lead_time) / to_decimal(counter)
            otherrev = calc_othrev(period)
            avrg_rate =  to_decimal(avrg_rate) + to_decimal(otherrev)

        if avrg_rate != 0:
            avrg_rate =  to_decimal(avrg_rate) / to_decimal(pay)

        return generate_inner_output()


    def calc_room(currdate:date, lydate:date):

        nonlocal avrgrate, lyavrgrate, qtygroupd, lyqtygroupd, qtygroupt, qtyfit, lyqtyfit, totroom, lytotroom, avrg_leadtime, pay, lypay, lyqtygroupt, lyavrg_leadtime, otherrev, res_line, htparam, genstat, segment, reservation, arrangement, bill_line, zimmer, queasy, waehrung, zkstat, artikel, umsatz
        nonlocal casetype, curr_date

        room_count = 0
        lroom_count = 0

        def generate_inner_output():
            return (room_count, lroom_count)


        if currdate >= curr_date:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():
                room_count = room_count + 1

        else:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == currdate)).order_by(Zkstat._recid).all():
                room_count = room_count + zkstat.anz100


        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == lydate)).order_by(Zkstat._recid).all():
            lroom_count = lroom_count + zkstat.anz100

        return generate_inner_output()


    def calc_othrev(datum:date):

        nonlocal avrgrate, lyavrgrate, qtygroupd, lyqtygroupd, qtygroupt, qtyfit, lyqtyfit, totroom, lytotroom, avrg_leadtime, pay, lypay, lyqtygroupt, lyavrg_leadtime, otherrev, res_line, htparam, genstat, segment, reservation, arrangement, bill_line, zimmer, queasy, waehrung, zkstat, artikel, umsatz
        nonlocal lydate, casetype, currdate, curr_date

        othrev = to_decimal("0.0")
        i:int = 0
        max_i:int = 0
        art_list:List[int] = create_empty_list(99,0)
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")

        def generate_inner_output():
            return (othrev)


        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        for i in range(1,max_i + 1) :

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == art_list[i - 1]) & (Artikel.departement == 0)).first()

            if artikel:
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    othrev =  to_decimal(othrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

        return generate_inner_output()


    lyqtygroupd, lyqtygroupt, lyqtyfit, lyavrgrate, lypay, lyavrg_leadtime = count_occ(1, lydate)
    qtygroupd, qtygroupt, qtyfit, avrgrate, pay, avrg_leadtime = count_occ(casetype, currdate)
    totroom, lytotroom = calc_room(currdate, lydate)

    return generate_output()