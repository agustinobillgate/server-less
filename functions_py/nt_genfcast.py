#using conversion tools version: 1.0.0.117

# ======================================================================
# Rulita, 22-10-2025
# Issue : 
# - guest_pr.code table never accessed using FIND FIRST or FOR EACH
# - guest_pr.code hardcoded as '?'
# ======================================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from models import Guest, Segment, Res_line, Htparam, Nation, Arrangement, Bill_line, Genfcast, Reservation, Zimkateg, Akt_cust, Bediener, Kontline, Waehrung, Artikel, Reslin_queasy, Argt_line

def nt_genfcast():

    prepare_cache ([Guest, Segment, Res_line, Htparam, Nation, Arrangement, Genfcast, Reservation, Akt_cust, Bediener, Kontline, Waehrung, Artikel, Argt_line])

    bill_date:date = None
    created:date = None
    price_decimal:int = 0
    rate:Decimal = to_decimal("0.0")
    ratelocal:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    argt_betrag:Decimal = to_decimal("0.0")
    ex_rate:Decimal = to_decimal("0.0")
    exchg_rate:Decimal = 1
    frate:Decimal = 1
    def_nation:int = 0
    ratecode:string = ""
    do_it:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    serv_taxable:bool = False
    foreign_rate:bool = False
    new_contrate:bool = False
    dayuse:bool = False
    dd:int = 0
    mm:int = 0
    yy:int = 0
    guest = segment = res_line = htparam = nation = arrangement = bill_line = genfcast = reservation = zimkateg = akt_cust = bediener = kontline = waehrung = artikel = reslin_queasy = argt_line = None

    rguest = compliment = rline = None

    Rguest = create_buffer("Rguest",Guest)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, created, price_decimal, rate, ratelocal, lodging, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, def_nation, ratecode, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, dayuse, dd, mm, yy, guest, segment, res_line, htparam, nation, arrangement, bill_line, genfcast, reservation, zimkateg, akt_cust, bediener, kontline, waehrung, artikel, reslin_queasy, argt_line
        nonlocal rguest, compliment, rline


        nonlocal rguest, compliment, rline

        return {}

    def genfcast_spaetabreise():

        nonlocal bill_date, created, price_decimal, rate, ratelocal, lodging, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, def_nation, ratecode, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, dayuse, dd, mm, yy, guest, segment, res_line, htparam, nation, arrangement, bill_line, genfcast, reservation, zimkateg, akt_cust, bediener, kontline, waehrung, artikel, reslin_queasy, argt_line
        nonlocal rguest, compliment, rline


        nonlocal rguest, compliment, rline

        do_it:bool = False
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Genfcast)

        for genfcast in db_session.query(Genfcast).filter(
                 (Genfcast.abreise == bill_date) & (Genfcast.cancelled == None) & not_ (Genfcast.noshow)).order_by(Genfcast._recid).all():
            do_it = True

            if do_it:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genfcast.argt)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, genfcast.resnr)],"billin_nr": [(eq, genfcast.reslinnr)]})

                if bill_line:

                    gbuff = get_cache (Genfcast, {"_recid": [(eq, genfcast._recid)]})
                    gbuff.spaetabreise = True


                    pass


    def create_genfcast():

        nonlocal bill_date, created, price_decimal, rate, ratelocal, lodging, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, def_nation, ratecode, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, dayuse, dd, mm, yy, guest, segment, res_line, htparam, nation, arrangement, bill_line, genfcast, reservation, zimkateg, akt_cust, bediener, kontline, waehrung, artikel, reslin_queasy, argt_line
        nonlocal rguest, compliment, rline


        nonlocal rguest, compliment, rline

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
        created = None
        yy = to_int(substring(res_line.reserve_char, 0, 2)) + 2000
        mm = to_int(substring(res_line.reserve_char, 3, 2))
        dd = to_int(substring(res_line.reserve_char, 6, 2))
        created = date_mdy(mm, dd, yy)

        if (created == None) or (created > res_line.ankunft):
            created = res_line.ankunft
        genfcast_ratecode()

        genfcast = get_cache (Genfcast, {"datum": [(eq, created)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if not genfcast:
            genfcast = Genfcast()
            db_session.add(genfcast)

        genfcast.datum = created
        genfcast.ratecode = ratecode
        genfcast.gastnr = res_line.gastnr
        genfcast.gastnrmember = res_line.gastnrmember
        genfcast.wahrungsnr = res_line.betriebsnr
        genfcast.resnr = res_line.resnr
        genfcast.reslinnr = res_line.reslinnr
        genfcast.markno = res_line.reserve_int
        genfcast.ankunft = res_line.ankunft
        genfcast.abreise = res_line.abreise
        genfcast.cancelled = res_line.cancelled
        genfcast.noshow = (res_line.resstatus == 10)
        genfcast.resstatus = res_line.resstatus
        genfcast.zikatnr = res_line.zikatnr
        genfcast.erwachs = res_line.erwachs
        genfcast.gratis = res_line.gratis
        genfcast.kind1 = res_line.kind1
        genfcast.kind2 = res_line.kind2
        genfcast.kind3 = res_line.l_zuordnung[3]
        genfcast.zimmeranz = res_line.zimmeranz
        genfcast.argt = arrangement.arrangement
        genfcast.karteityp = rguest.karteityp
        genfcast.groupname = reservation.groupname
        genfcast.source = reservation.resart
        genfcast.segmentcode = reservation.segmentcode

        if genfcast.cancelled > genfcast.ankunft:
            genfcast.cancelled = genfcast.ankunft

        if res_line.resstatus != 9:
            genfcast.cancelled = None

        if res_line.resstatus == 6:
            genfcast.resstatus = 1

        elif res_line.resstatus == 13:
            genfcast.resstatus = 11

        elif res_line.resstatus == 8 or res_line.resstatus == 10:

            if res_line.zimmerfix:
                genfcast.resstatus = 11
            else:
                genfcast.resstatus = 1

        elif res_line.resstatus == 9:
            genfcast.resstatus = res_line.betrieb_gastpay

        if dayuse:
            genfcast.abreise = genfcast.abreise + timedelta(days=1)

        if genfcast.resstatus == 11:
            genfcast.zimmeranz = 0

        if nation:
            genfcast.nationnr = nation.nationnr
        else:
            genfcast.nationnr = def_nation
        pass

        akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, res_line.gastnr)]})

        if akt_cust:

            bediener = get_cache (Bediener, {"userinit": [(eq, akt_cust.userinit)]})

        if not akt_cust or not bediener:

            rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if rguest.phonetik3 != "":

                bediener = get_cache (Bediener, {"userinit": [(eq, rguest.phonetik3)]})

        if bediener:
            genfcast.sales_init = bediener.userinit

        if res_line.zipreis == 0 and res_line.gratis > 0 and res_line.resstatus != 13 and compliment:

            rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"resstatus": [(ne, 12)],"zipreis": [(gt, 0)],"reslinnr": [(ne, res_line.reslinnr)]})

            if rline:
                genfcast.segmentcode = compliment.segmentcode

        if res_line.kontignr > 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)]})

            if kontline:
                genfcast.kontcode = kontline.kontcode

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation:
            genfcast.resident = nation.nationnr


        else:
            genfcast.resident = genfcast.nationnr

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation2)]})

        if nation:
            genfcast.domestic = nation.nationnr


    def genfcast_ratecode():

        nonlocal bill_date, created, price_decimal, rate, ratelocal, lodging, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, def_nation, ratecode, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, dayuse, dd, mm, yy, guest, segment, res_line, htparam, nation, arrangement, bill_line, genfcast, reservation, zimkateg, akt_cust, bediener, kontline, waehrung, artikel, reslin_queasy, argt_line
        nonlocal rguest, compliment, rline


        nonlocal rguest, compliment, rline

        str:string = ""
        curr_i:int = 0
        ratecode = ""


        for curr_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(curr_i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                ratecode = substring(str, 6)

                return


    def genfcast_average_rmrate():

        nonlocal bill_date, created, price_decimal, rate, ratelocal, lodging, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, def_nation, ratecode, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, dayuse, dd, mm, yy, guest, segment, res_line, htparam, nation, arrangement, bill_line, genfcast, reservation, zimkateg, akt_cust, bediener, kontline, waehrung, artikel, reslin_queasy, argt_line
        nonlocal rguest, compliment, rline


        nonlocal rguest, compliment, rline

        frdate:date = None
        todate:date = None
        currdate:date = None
        anzstay:int = 0
        curr_zikatnr:int = 0
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        it_exist:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        fixed_rate:bool = False
        rm_rate:Decimal = to_decimal("0.0")
        lodg_betrag:Decimal = to_decimal("0.0")

        if res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})
        rate =  to_decimal("0")
        ratelocal =  to_decimal("0")
        lodging =  to_decimal("0")
        anzstay = 0
        frdate = res_line.ankunft
        todate = res_line.abreise - timedelta(days=1)

        if res_line.ankunft == res_line.abreise:
            todate = frdate
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr
        for currdate in date_range(frdate,todate) :
            anzstay = anzstay + 1

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, currdate)],"date2": [(ge, currdate)]})
            fixed_rate = None != reslin_queasy

            if reslin_queasy:
                rm_rate =  to_decimal(reslin_queasy.deci1)

            if not fixed_rate:

                if new_contrate:
                    rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, ratecode, None, currdate, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                else:
                    # Rulita, 
                    # Issue : 
                    # - guest_pr.code table is never accessed using FIND FIRST or FOR EACH
                    # - guest_pr.code is hardcoded as '?'
                    rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, "?", currdate, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
            service, vat, vat2, fact = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))
            lodg_betrag =  to_decimal(rm_rate) * to_decimal(frate)

            if rm_rate > 0:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

            lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))

            if rm_serv:
                lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)
            lodging =  to_decimal(lodging) + to_decimal(lodg_betrag)
            rate =  to_decimal(rate) + to_decimal(rm_rate)

            if res_line.reserve_dec != 0:
                ratelocal =  to_decimal(ratelocal) + to_decimal(rm_rate) * to_decimal(res_line.reserve_dec)
            else:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    ratelocal =  to_decimal(ratelocal) + to_decimal(rm_rate) * to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        genfcast.zipreis =  to_decimal(rate) / to_decimal(anzstay)
        genfcast.ratelocal = to_decimal(round(ratelocal / anzstay , price_decimal))
        genfcast.logis = to_decimal(round(lodging / anzstay , price_decimal))

        if frate == 1:
            genfcast.zipreis = to_decimal(round(genfcast.zipreis , price_decimal))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    rm_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

    if nation:
        def_nation = nation.nationnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 377)]})

    if htparam.finteger != 0:

        compliment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})

    for res_line in db_session.query(Res_line).filter(
             (Res_line.ankunft == bill_date) & (Res_line.active_flag >= 1) & (Res_line.active_flag <= 2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.active_flag).all():

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        dayuse = False
        do_it = True

        if res_line.active_flag == 2 and res_line.resstatus == 8 and res_line.abreise == bill_date:

            bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
            do_it = None != bill_line
            dayuse = None != bill_line

        if do_it:
            create_genfcast()
            genfcast_average_rmrate()

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == 2) & (Res_line.resstatus == 9) & (Res_line.cancelled == bill_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.betrieb_gastpay != 3) & (Res_line.betrieb_gastpay != 4)).order_by(Res_line._recid).all():

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        create_genfcast()
        genfcast_average_rmrate()
        pass
    genfcast_spaetabreise()

    return generate_output()