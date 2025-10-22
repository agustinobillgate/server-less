#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 21-10-2025
# Issue :
# - Missing table name arrangement
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from functions.ratecode_compli import ratecode_compli
from models import Zimmer, Guest, Segmentstat, Segment, Res_line, Bill, Zinrstat, Htparam, Zimkateg, Zkstat, Reservation, Arrangement, Bill_line, Queasy, Waehrung, Artikel, Argt_line, Sources, Nation, Nationstat, Natstat1, Landstat, Guestat1, Guestat, Guestseg, Sourccod, Outorder, Prmarket, Kontline, Reslin_queasy, Guest_pr, Kontplan, Umsatz

def nt_rmstat():

    prepare_cache ([Zimmer, Guest, Segmentstat, Segment, Res_line, Zinrstat, Htparam, Zimkateg, Zkstat, Reservation, Arrangement, Queasy, Waehrung, Artikel, Argt_line, Sources, Nation, Nationstat, Natstat1, Landstat, Guestat1, Guestat, Guestseg, Sourccod, Prmarket, Kontline, Guest_pr, Kontplan, Umsatz])

    bill_date:date = None
    resnr:int = 0
    price_decimal:int = 0
    anz:int = 0
    comp_segm:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    fb_dept:int = 0
    prcode:int = 0
    i:int = 0
    n:int = 0
    occ_rm:int = 0
    wi_segm:int = 0
    curr_segm:int = 0
    lodg_betrag:Decimal = to_decimal("0.0")
    rate:Decimal = to_decimal("0.0")
    grate:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    argt_betrag:Decimal = to_decimal("0.0")
    ex_rate:Decimal = to_decimal("0.0")
    exchg_rate:Decimal = 1
    frate:Decimal = 1
    t_lodging:Decimal = to_decimal("0.0")
    t_rate:Decimal = to_decimal("0.0")
    tl_lodging:Decimal = to_decimal("0.0")
    tl_rate:Decimal = to_decimal("0.0")
    do_it:bool = False
    post_it:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    dayuse:bool = False
    foreign_rate:bool = False
    new_contrate:bool = False
    cb_flag:bool = False
    bonus:bool = False
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    curr_billdate:date = None
    zimmer = guest = segmentstat = segment = res_line = bill = zinrstat = htparam = zimkateg = zkstat = reservation = arrangement = bill_line = queasy = waehrung = artikel = argt_line = sources = nation = nationstat = natstat1 = landstat = guestat1 = guestat = guestseg = sourccod = outorder = prmarket = kontline = reslin_queasy = guest_pr = kontplan = umsatz = None

    zim1 = rguest = segmstat = compliment = rline = mbill = znbuff = None

    Zim1 = create_buffer("Zim1",Zimmer)
    Rguest = create_buffer("Rguest",Guest)
    Segmstat = create_buffer("Segmstat",Segmentstat)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)
    Mbill = create_buffer("Mbill",Bill)
    Znbuff = create_buffer("Znbuff",Zinrstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, zinrstat, htparam, zimkateg, zkstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, outorder, prmarket, kontline, reslin_queasy, guest_pr, kontplan, umsatz
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff

        return {}

    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int):

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, zinrstat, htparam, zimkateg, zkstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, outorder, prmarket, kontline, reslin_queasy, guest_pr, kontplan, umsatz
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff

        post_it = False

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == bill_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == bill_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(bill_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(bill_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if bill_date <= (res_line.ankunft + (intervall - 1)):
                post_it = True

        return generate_inner_output()


    def check_advpchase():

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, zinrstat, htparam, zimkateg, zkstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, outorder, prmarket, kontline, reslin_queasy, guest_pr, kontplan, umsatz
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff

        prmarket = get_cache (Prmarket, {"nr": [(eq, res_line.reserve_int)]})

        if not prmarket:

            return

        kontline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(le, res_line.ankunft)],"kontstatus": [(eq, 6)],"code": [(eq, prmarket.bezeich)]})

        if not kontline:

            return

        kontline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(le, res_line.ankunft)],"abreise": [(ge, res_line.ankunft)],"kontstatus": [(eq, 6)],"zikatnr": [(eq, res_line.zikatnr)],"arrangement": [(eq, res_line.arrangement)],"code": [(eq, prmarket.bezeich)]})

        if not kontline:

            kontline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(le, res_line.ankunft)],"abreise": [(ge, res_line.ankunft)],"kontstatus": [(eq, 6)],"zikatnr": [(eq, res_line.zikatnr)],"code": [(eq, prmarket.bezeich)]})

        if not kontline:

            kontline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(le, res_line.ankunft)],"abreise": [(ge, res_line.ankunft)],"kontstatus": [(eq, 6)],"code": [(eq, prmarket.bezeich)]})

        if kontline:
            pass
            kontline.overbooking = kontline.overbooking + 1


            pass


    def check_bonus():

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, vat2, fact, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, zinrstat, htparam, zimkateg, zkstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, outorder, prmarket, kontline, reslin_queasy, guest_pr, kontplan, umsatz
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff

        bonus = False
        bonus_array:List[bool] = create_empty_list(999, False)
        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        curr_zikatnr:int = 0
        rmcat = None

        def generate_inner_output():
            return (bonus)

        Rmcat =  create_buffer("Rmcat",Zimkateg)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:

            return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        if res_line.l_zuordnung[0] != 0:

            rmcat = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate and guest_pr:
            bonus = get_output(ratecode_compli(res_line.resnr, res_line.reslinnr, guest_pr.code, curr_zikatnr, bill_date))

            return generate_inner_output()

        if length(arrangement.OPTIONS) != 16:

            return generate_inner_output()
        j = 1
        for i in range(1,4 + 1) :
            stay = 0
            pay = 0
            
            # Rulita,
            # - Missing table name arrangement
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = (bill_date - res_line.ankunft + 1).days
        bonus = False

        if n <= 999:
            bonus = bonus_array[n - 1]

        return generate_inner_output()


    def create_umsatz_servtax():

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, fact, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, zinrstat, htparam, zimkateg, zkstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, outorder, prmarket, kontline, reslin_queasy, guest_pr, kontplan, umsatz
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill, znbuff

        serv_vat:bool = False
        tax_vat:bool = False
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        fvat:bool = False
        fvat2:bool = False
        fserv:bool = False
        kontbuff = None
        Kontbuff =  create_buffer("Kontbuff",Kontplan)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 483)]})
        tax_vat = htparam.flogical

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum == bill_date)).order_by(Umsatz._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:

                kontplan = get_cache (Kontplan, {"betriebsnr": [(eq, umsatz.departement)],"kontignr": [(eq, umsatz.artnr)],"datum": [(eq, umsatz.datum)]})

                if not kontplan:
                    service =  to_decimal("0")
                    vat =  to_decimal("0")
                    vat2 =  to_decimal("0")
                    fserv = False
                    fvat = False
                    fvat2 = False

                    if artikel.service_code != 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                        if htparam:

                            if num_entries(htparam.fchar, chr_unicode(2)) < 2:
                                service =  to_decimal(htparam.fdecimal)
                            else:
                                service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")
                                fserv = True

                    if artikel.prov_code != 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.prov_code)]})

                        if htparam:

                            if num_entries(htparam.fchar, chr_unicode(2)) < 2:
                                vat2 =  to_decimal(htparam.fdecimal)
                            else:
                                vat2 =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")
                                fvat2 = True

                        if vat2 == 100:
                            vat =  to_decimal("0")
                            service =  to_decimal("0")

                        elif serv_vat:
                            vat2 =  to_decimal(vat2) + to_decimal(vat2) * to_decimal(service) / to_decimal("100")

                    if vat2 != 0:

                        kontbuff = get_cache (Kontplan, {"betriebsnr": [(eq, umsatz.departement + 100)],"kontignr": [(eq, umsatz.artnr)],"datum": [(eq, umsatz.datum)]})

                        if not kontbuff:
                            kontbuff = Kontplan()
                            db_session.add(kontbuff)

                            kontbuff.betriebsnr = umsatz.departement + 100
                            kontbuff.kontignr = umsatz.artnr
                            kontbuff.datum = umsatz.datum
                            kontbuff.anzconf = vat2 * 100000


                            pass

                    if artikel.mwst_code != 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                        if htparam:

                            if num_entries(htparam.fchar, chr_unicode(2)) < 2:
                                vat =  to_decimal(htparam.fdecimal)
                            else:
                                vat =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")
                                fvat = True

                        if vat == 1:
                            service =  to_decimal("0")
                            vat2 =  to_decimal("0")


                        else:

                            if serv_vat and not tax_vat:
                                vat =  to_decimal(vat) * to_decimal((1) + to_decimal(service) / to_decimal(100))

                            elif serv_vat and tax_vat:
                                vat =  to_decimal(vat) * to_decimal((1) + to_decimal((service) + to_decimal(vat2)) / to_decimal(100))

                            elif not serv_vat and tax_vat:
                                vat =  to_decimal(vat) * to_decimal((1) + to_decimal(vat2) / to_decimal(100))

                    if fserv  and fvat :
                        kontplan = Kontplan()
                        db_session.add(kontplan)

                        kontplan.betriebsnr = umsatz.departement
                        kontplan.kontignr = umsatz.artnr
                        kontplan.datum = umsatz.datum
                        kontplan.anzkont = service * 100000
                        kontplan.anzconf = vat * 100000


                        pass
                    else:
                        service =  to_decimal(service) / to_decimal("100")
                        vat =  to_decimal(vat) / to_decimal("100")


                        kontplan = Kontplan()
                        db_session.add(kontplan)

                        kontplan.betriebsnr = umsatz.departement
                        kontplan.kontignr = umsatz.artnr
                        kontplan.datum = umsatz.datum
                        kontplan.anzkont = service * 10000
                        kontplan.anzconf = vat * 10000


                        pass

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
    rm_vat = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 377)]})

    if htparam.finteger != 0:

        compliment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 48)]})

    if htparam.finteger != 0:

        segment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})

        if segment:
            wi_segm = segment.segmentcode
    create_umsatz_servtax()

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

        zkstat = get_cache (Zkstat, {"datum": [(eq, bill_date)],"zikatnr": [(eq, zimkateg.zikatnr)]})

        if not zkstat:
            zkstat = Zkstat()
            db_session.add(zkstat)

            zkstat.datum = bill_date
            zkstat.zikatnr = zimkateg.zikatnr


        anz = 0

        for zim1 in db_session.query(Zim1).filter(
                 (Zim1.zikatnr == zimkateg.zikatnr) & (Zim1.sleeping)).order_by(Zim1._recid).all():
            anz = anz + 1
        zkstat.anz100 = anz

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 11)) & ((Res_line.ankunft == (bill_date + timedelta(days=1))))).order_by(Res_line._recid).all():

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "arrtmrw")],"datum": [(eq, bill_date)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "ArrTmrw"

        if res_line.resstatus != 11:
            zinrstat.zimmeranz = zinrstat.zimmeranz + 1
        zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                res_line.gratis


        zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 + res_line.kind2

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8))).order_by(Res_line.zinr, Res_line.active_flag).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        dayuse = False
        do_it = False

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})

            if bill_line:
                do_it = True
                dayuse = True

                if not res_line.zimmerfix:

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "dayuse")],"datum": [(eq, bill_date)]})

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = "dayuse"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1

        elif res_line.active_flag == 2 and res_line.ankunft < bill_date and not res_line.zimmerfix:

            bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
            do_it = None != bill_line
        else:
            do_it = True

        queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if not queasy and not zimmer.sleeping:
            do_it = False

        if queasy and queasy.number3 == res_line.gastnr:
            do_it = False

        if res_line.resstatus == 8 and res_line.abreise == bill_date and ((res_line.abreise > res_line.ankunft) or dayuse):

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "departure")],"datum": [(eq, bill_date)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = "Departure"

            if not res_line.zimmerfix:
                zinrstat.zimmeranz = zinrstat.zimmeranz + 1


            zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                    res_line.gratis
            zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 +\
                    res_line.kind2

        if do_it and ((res_line.abreise > res_line.ankunft) or dayuse):

            if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)) and (res_line.reserve_int != 0):
                check_advpchase()

            if (res_line.erwachs + res_line.kind1 + res_line.gratis) > 0 and (res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9):

                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "vip")],"datum": [(eq, bill_date)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = bill_date
                    zinrstat.zinr = "VIP"

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                    zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                        res_line.gratis

            if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)) and res_line.erwachs > 0:

                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "avrgstay")],"datum": [(eq, bill_date)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = bill_date
                    zinrstat.zinr = "AvrgStay"

                if res_line.abreise > res_line.ankunft:
                    zinrstat.personen = zinrstat.personen + res_line.abreise - res_line.ankunft
                else:
                    zinrstat.personen = zinrstat.personen + 1
                zinrstat.zimmeranz = zinrstat.zimmeranz + 1

            if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)) and (res_line.ankunft == bill_date):

                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "arrival")],"datum": [(eq, bill_date)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = bill_date
                    zinrstat.zinr = "Arrival"


                zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                        res_line.gratis
                zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 +\
                        res_line.kind2

                if reservation.segmentcode != 0 and reservation.segmentcode == wi_segm:

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "arrival-wig")],"datum": [(eq, bill_date)]})

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = "Arrival-WIG"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                    zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                            res_line.gratis
                    zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 +\
                            res_line.kind2


                else:

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "arrival-rsv")],"datum": [(eq, bill_date)]})

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = "Arrival-RSV"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                    zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                            res_line.gratis
                    zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 +\
                            res_line.kind2

            if res_line.resstatus == 6 and res_line.abreise == (bill_date + timedelta(days=1)):

                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "deptmrw")],"datum": [(eq, bill_date)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = bill_date
                    zinrstat.zinr = "DepTmrw"


                zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                zinrstat.personen = zinrstat.personen + res_line.erwachs +\
                        res_line.gratis
                zinrstat.betriebsnr = zinrstat.betriebsnr + res_line.kind1 +\
                        res_line.kind2

        if do_it:

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:
                guest.logiernachte = guest.logiernachte + 1
                pass

            if res_line.gastnr != res_line.gastnrmember:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:
                    guest.logiernachte = guest.logiernachte + 1
                    pass
            rate =  to_decimal("0")
            lodg_betrag =  to_decimal("0")
            bonus = check_bonus()

            if (res_line.zipreis > 0 or bonus):

                if not res_line.zimmerfix:
                    occ_rm = occ_rm + 1

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                rate =  to_decimal(res_line.zipreis)

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                lodg_betrag =  to_decimal(rate) * to_decimal(frate)

                if rate > 0:

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                        lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

            lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))
            rate = to_decimal(round(rate * frate , price_decimal))

            if foreign_rate and price_decimal == 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    rate = to_decimal(round(rate / n , 0) * n)

            if rm_serv:
                grate =  to_decimal(rate) * to_decimal(fact)
            else:
                grate =  to_decimal(rate)
                rate =  to_decimal(rate) / to_decimal(fact)
                lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)

            if lodg_betrag == None:
                lodg_betrag =  to_decimal("0")

            if rate == None:
                rate =  to_decimal("0")


            t_rate =  to_decimal(t_rate) + to_decimal(rate) / to_decimal(frate)
            t_lodging =  to_decimal(t_lodging) + to_decimal(lodg_betrag) / to_decimal(frate)
            tl_rate =  to_decimal(tl_rate) + to_decimal(rate)
            tl_lodging =  to_decimal(tl_lodging) + to_decimal(lodg_betrag)


            pass

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if segment and segment.betriebsnr > 0:
                pass

            elif rate == 0 and res_line.gratis > 0 and res_line.resstatus != 13:

                rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"resstatus": [(ne, 12)],"zipreis": [(gt, 0)],"reslinnr": [(ne, res_line.reslinnr)]})

            segmentstat = get_cache (Segmentstat, {"segmentcode": [(eq, reservation.segmentcode)],"datum": [(eq, bill_date)]})

            if not segmentstat:
                segmentstat = Segmentstat()
                db_session.add(segmentstat)

                segmentstat.datum = bill_date
                segmentstat.segmentcode = reservation.segmentcode

            if not res_line.zimmerfix:

                if (rate != 0) or bonus:

                    if res_line.resstatus != 13:
                        segmentstat.zimmeranz = segmentstat.zimmeranz + 1
                else:

                    if res_line.gratis > 0:

                        if compliment and rline:

                            segmstat = get_cache (Segmentstat, {"segmentcode": [(eq, compliment.segmentcode)],"datum": [(eq, bill_date)]})

                            if not segmstat:
                                segmstat = Segmentstat()
                                db_session.add(segmstat)

                                segmstat.datum = bill_date
                                segmstat.segmentcode = compliment.segmentcode

                            if res_line.resstatus != 13:
                                segmstat.zimmeranz = segmstat.zimmeranz + 1
                            segmstat.betriebsnr = segmstat.betriebsnr + 1
                        else:

                            if res_line.resstatus != 13:
                                segmentstat.zimmeranz = segmentstat.zimmeranz + 1
                            segmentstat.betriebsnr = segmentstat.betriebsnr + 1
                    else:

                        if res_line.resstatus != 13:
                            segmentstat.zimmeranz = segmentstat.zimmeranz + 1

            if rate != 0:
                segmentstat.persanz = segmentstat.persanz + res_line.erwachs
                segmentstat.kind1 = segmentstat.kind1 + res_line.kind1 +\
                        res_line.l_zuordnung[3]
                segmentstat.kind2 = segmentstat.kind2 + res_line.kind2
                segmentstat.gratis = segmentstat.gratis + res_line.gratis
                segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(lodg_betrag)


            else:

                if compliment and rline and segmstat:
                    segmstat.persanz = segmstat.persanz + res_line.erwachs
                    segmstat.kind1 = segmstat.kind1 + res_line.kind1 +\
                            res_line.l_zuordnung[3]
                    segmstat.kind2 = segmstat.kind2 + res_line.kind2
                    segmstat.gratis = segmstat.gratis + res_line.gratis


                else:
                    segmentstat.persanz = segmentstat.persanz + res_line.erwachs
                    segmentstat.kind1 = segmentstat.kind1 + res_line.kind1 +\
                            res_line.l_zuordnung[3]
                    segmentstat.kind2 = segmentstat.kind2 + res_line.kind2
                    segmentstat.gratis = segmentstat.gratis + res_line.gratis

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, res_line.zinr)],"datum": [(eq, bill_date)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = res_line.zinr

            if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                if rate == 0:
                    zinrstat.betriebsnr = zinrstat.betriebsnr + 1
            zinrstat.personen = zinrstat.personen + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

            if rate != 0:
                zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(lodg_betrag)
                zinrstat.argtumsatz =  to_decimal(zinrstat.argtumsatz) + to_decimal(rate)
                zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(grate)

            zkstat = get_cache (Zkstat, {"zikatnr": [(eq, res_line.zikatnr)],"datum": [(eq, bill_date)]})

            if not zkstat:
                zkstat = Zkstat()
                db_session.add(zkstat)

                zkstat.datum = bill_date
                zkstat.zikatnr = res_line.zikatnr
                anz = 0

                for zim1 in db_session.query(Zim1).filter(
                         (Zim1.zikatnr == res_line.zikatnr) & (Zim1.sleeping)).order_by(Zim1._recid).all():
                    anz = anz + 1
                zkstat.anz100 = anz

            if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                zkstat.zimmeranz = zkstat.zimmeranz + 1

                if rate == 0:
                    zkstat.betriebsnr = zkstat.betriebsnr + 1

                    if res_line.gratis == 0 and (res_line.erwachs + res_line.kind1) > 0:
                        zkstat.arrangement_art[0] = zkstat.arrangement_art[0] + 1

                if res_line.ankunft == bill_date and res_line.abreise > bill_date:
                    zkstat.anz_ankunft = zkstat.anz_ankunft + 1

                if dayuse:
                    zkstat.anz_abr = zkstat.anz_abr + 1
            zkstat.personen = zkstat.personen + res_line.erwachs

            if reservation.resart == 0:
                pass
            else:

                sources = get_cache (Sources, {"source_code": [(eq, reservation.resart)],"datum": [(eq, bill_date)]})

                if not sources:
                    sources = Sources()
                    db_session.add(sources)

                    sources.datum = bill_date
                    sources.source_code = reservation.resart

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    sources.zimmeranz = sources.zimmeranz + 1

                    if rate == 0:
                        sources.betriebsnr = sources.betriebsnr + 1
                sources.persanz = sources.persanz + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                if rate != 0:
                    sources.logis =  to_decimal(sources.logis) + to_decimal(lodg_betrag)

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

            if nation:

                nationstat = get_cache (Nationstat, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

                if not nationstat:
                    nationstat = Nationstat()
                    db_session.add(nationstat)

                    nationstat.datum = bill_date
                    nationstat.nationnr = nation.nationnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    nationstat.dankzimmer = nationstat.dankzimmer + 1

                    if rate == 0:
                        nationstat.betriebsnr = nationstat.betriebsnr + 1
                nationstat.logerwachs = nationstat.logerwachs + res_line.erwachs
                nationstat.loggratis = nationstat.loggratis + res_line.gratis
                nationstat.logkind1 = nationstat.logkind1 + res_line.kind1
                nationstat.logkind2 = nationstat.logkind2 + res_line.kind2

                if res_line.zipreis == 0 and res_line.resstatus != 13 and res_line.erwachs > 0:
                    nationstat.loggratis = nationstat.loggratis + res_line.erwachs

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)) and res_line.ankunft == bill_date:
                    nationstat.ankerwachs = nationstat.ankerwachs + res_line.erwachs
                    nationstat.ankkind1 = nationstat.ankkind1 + res_line.kind1
                    nationstat.ankkind2 = nationstat.ankkind2 + res_line.kind2
                    nationstat.ankgratis = nationstat.ankgratis + res_line.gratis

                natstat1 = get_cache (Natstat1, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

                if not natstat1:
                    natstat1 = Natstat1()
                    db_session.add(natstat1)

                    natstat1.datum = bill_date
                    natstat1.nationnr = nation.nationnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    natstat1.zimmeranz = natstat1.zimmeranz + 1

                    if rate == 0:
                        natstat1.betriebsnr = natstat1.betriebsnr + 1
                    natstat1.persanz = natstat1.persanz + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                    if rate != 0:
                        natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation2)]})

            if nation and guest.nation2 != "":

                nationstat = get_cache (Nationstat, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

                if not nationstat:
                    nationstat = Nationstat()
                    db_session.add(nationstat)

                    nationstat.datum = bill_date
                    nationstat.nationnr = nation.nationnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    nationstat.dankzimmer = nationstat.dankzimmer + 1

                    if rate == 0:
                        nationstat.betriebsnr = nationstat.betriebsnr + 1
                    nationstat.logerwachs = nationstat.logerwachs + res_line.erwachs
                    nationstat.loggratis = nationstat.loggratis + res_line.gratis
                    nationstat.logkind1 = nationstat.logkind1 + res_line.kind1
                    nationstat.logkind2 = nationstat.logkind2 + res_line.kind2

                    if res_line.zipreis == 0 and res_line.erwachs > 0:
                        nationstat.loggratis = nationstat.loggratis + res_line.erwachs

                    if res_line.ankunft == bill_date:
                        nationstat.ankerwachs = nationstat.ankerwachs + res_line.erwachs
                        nationstat.ankkind1 = nationstat.ankkind1 + res_line.kind1
                        nationstat.ankkind2 = nationstat.ankkind2 + res_line.kind2
                        nationstat.ankgratis = nationstat.ankgratis + res_line.gratis

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):

                    if res_line.abreise > res_line.ankunft:
                        nationstat.dlogkind1 = nationstat.dlogkind1 + res_line.abreise - res_line.ankunft
                    else:
                        nationstat.dlogkind1 = nationstat.dlogkind1 + 1
                    nationstat.dlogkind2 = nationstat.dlogkind2 + 1

                natstat1 = get_cache (Natstat1, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

                if not natstat1:
                    natstat1 = Natstat1()
                    db_session.add(natstat1)

                    natstat1.datum = bill_date
                    natstat1.nationnr = nation.nationnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    natstat1.zimmeranz = natstat1.zimmeranz + 1

                    if rate == 0:
                        natstat1.betriebsnr = natstat1.betriebsnr + 1
                    natstat1.persanz = natstat1.persanz + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                    if rate != 0:
                        natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

            if nation:

                landstat = get_cache (Landstat, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

                if not landstat:
                    landstat = Landstat()
                    db_session.add(landstat)

                    landstat.datum = bill_date
                    landstat.nationnr = nation.nationnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    landstat.zimmeranz = landstat.zimmeranz + 1

                    if rate == 0:
                        landstat.betriebsnr = landstat.betriebsnr + 1
                    landstat.persanz = landstat.persanz + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                    if rate != 0:
                        landstat.logis =  to_decimal(landstat.logis) + to_decimal(lodg_betrag)

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            if guest.karteityp >= 0:

                guestat1 = get_cache (Guestat1, {"gastnr": [(eq, guest.gastnr)],"datum": [(eq, bill_date)]})

                if not guestat1:
                    guestat1 = Guestat1()
                    db_session.add(guestat1)

                    guestat1.datum = bill_date
                    guestat1.gastnr = guest.gastnr

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):
                    guestat1.zimmeranz = guestat1.zimmeranz + 1

                    if rate == 0:
                        guestat1.betriebsnr = guestat1.betriebsnr + 1
                    guestat1.persanz = guestat1.persanz + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                    if rate != 0:
                        guestat1.logis =  to_decimal(guestat1.logis) + to_decimal(lodg_betrag)

                if ((res_line.resstatus == 6) or (dayuse and not res_line.zimmerfix)):

                    guestat = get_cache (Guestat, {"gastnr": [(eq, res_line.gastnr)],"monat": [(eq, get_month(bill_date))],"jahr": [(eq, get_year(bill_date))],"betriebsnr": [(eq, 0)]})

                    if not guestat:
                        guestat = Guestat()
                        db_session.add(guestat)

                        guestat.gastnr = res_line.gastnr
                        guestat.monat = get_month(bill_date)
                        guestat.jahr = get_year(bill_date)


                    guestat.room_nights = guestat.room_nights + 1


                    pass

                    if nation and guest.karteityp == 2:

                        guestat = get_cache (Guestat, {"gastnr": [(eq, res_line.gastnr)],"monat": [(eq, get_month(bill_date))],"jahr": [(eq, get_year(bill_date))],"betriebsnr": [(eq, nation.nationnr)]})

                        if not guestat:
                            guestat = Guestat()
                            db_session.add(guestat)

                            guestat.gastnr = res_line.gastnr
                            guestat.betriebsnr = nation.nationnr
                            guestat.monat = get_month(bill_date)
                            guestat.jahr = get_year(bill_date)


                        guestat.room_nights = guestat.room_nights + 1
                        guestat.argtumsatz =  to_decimal(guestat.argtumsatz) + to_decimal(rate)
                        guestat.logisumsatz =  to_decimal(guestat.logisumsatz) + to_decimal(lodg_betrag)


                        pass

            if resnr != res_line.resnr:
                resnr = res_line.resnr

    for reservation in db_session.query(Reservation).filter(
             (Reservation.activeflag <= 1) & (Reservation.resnr > 0) & (Reservation.resdat == bill_date)).order_by(Reservation._recid).all():

        for rline in db_session.query(Rline).filter(
                 ((Rline.resnr == reservation.resnr)) & ((Rline.resstatus != 12))).order_by(Rline._recid).all():

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "newres")],"datum": [(eq, bill_date)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = "NewRes"

            if not rline.zimmerfix:
                zinrstat.zimmeranz = zinrstat.zimmeranz + rline.zimmeranz
                zinrstat.personen = zinrstat.personen +\
                        (rline.erwachs + rline.gratis) * rline.zimmeranz

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 14) & (Queasy.deci1 != 0) & (Queasy.date1 <= bill_date) & (Queasy.date2 >= bill_date)).order_by(Queasy.number3).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, queasy.char2)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number2)]})
        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        guest = get_cache (Guest, {"gastnr": [(eq, queasy.number3)]})

        if zimmer.sleeping:
            occ_rm = occ_rm + 1
        rate =  to_decimal(queasy.deci1)
        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        lodg_betrag =  to_decimal(rate) * to_decimal(frate)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
            lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_line.betrag) * to_decimal(frate) * to_decimal(queasy.number1)
        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))
        rate = to_decimal(round(rate * frate , price_decimal))

        if foreign_rate and price_decimal == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

            if htparam.finteger != 0:
                n = 1
                for i in range(1,htparam.finteger + 1) :
                    n = n * 10
                rate = to_decimal(round(rate / n , 0) * n)

        if rm_serv:
            grate =  to_decimal(rate) * to_decimal(fact)
        else:
            grate =  to_decimal(rate)
            rate =  to_decimal(rate) / to_decimal(fact)
            lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)


        t_rate =  to_decimal(t_rate) + to_decimal(rate) / to_decimal(frate)
        t_lodging =  to_decimal(t_lodging) + to_decimal(lodg_betrag) / to_decimal(frate)
        tl_rate =  to_decimal(tl_rate) + to_decimal(rate)
        tl_lodging =  to_decimal(tl_lodging) + to_decimal(lodg_betrag)

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

        if not guestseg:

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

        segmentstat = get_cache (Segmentstat, {"segmentcode": [(eq, guestseg.segmentcode)],"datum": [(eq, bill_date)]})

        if not segmentstat:
            segmentstat = Segmentstat()
            db_session.add(segmentstat)

            segmentstat.datum = bill_date
            segmentstat.segmentcode = guestseg.segmentcode

        if zimmer.sleeping:
            segmentstat.zimmeranz = segmentstat.zimmeranz + 1
        segmentstat.persanz = segmentstat.persanz + queasy.number1
        segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(lodg_betrag)

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, bill_date)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = zimmer.zinr

        if zimmer.sleeping:
            zinrstat.zimmeranz = zinrstat.zimmeranz + 1
        zinrstat.personen = zinrstat.personen + queasy.number1
        zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(lodg_betrag)
        zinrstat.argtumsatz =  to_decimal(zinrstat.argtumsatz) + to_decimal(rate)
        zinrstat.gesamtumsatz + zinrstat.gesamtumsatz + grate

        zkstat = get_cache (Zkstat, {"zikatnr": [(eq, zimmer.zikatnr)],"datum": [(eq, bill_date)]})

        if not zkstat:
            zkstat = Zkstat()
            db_session.add(zkstat)

            zkstat.datum = bill_date
            zkstat.zikatnr = zimmer.zikatnr
            anz = 0

            for zim1 in db_session.query(Zim1).filter(
                         (Zim1.zikatnr == zimmer.zikatnr) & (Zim1.sleeping)).order_by(Zim1._recid).all():
                anz = anz + 1
            zkstat.anz100 = anz

        if zimmer.sleeping:
            zkstat.zimmeranz = zkstat.zimmeranz + 1
        zkstat.personen = zkstat.personen + queasy.number1

        reservation = get_cache (Reservation, {"gastnr": [(eq, guest.gastnr)]})

        if reservation:

            sources = get_cache (Sources, {"source_code": [(eq, reservation.resart)],"datum": [(eq, bill_date)]})

            if not sources:
                sources = Sources()
                db_session.add(sources)

                sources.datum = bill_date
                sources.source_code = reservation.resart


        else:

            sourccod = db_session.query(Sourccod).first()

            sources = get_cache (Sources, {"source_code": [(eq, sourccod.source_code)],"datum": [(eq, bill_date)]})

            if not sources:
                sources = Sources()
                db_session.add(sources)

                sources.datum = bill_date
                sources.source_code = sourccod.source_code

        if zimmer.sleeping:
            sources.zimmeranz = sources.zimmeranz + 1
        sources.persanz = sources.persanz + queasy.number1
        sources.logis =  to_decimal(sources.logis) + to_decimal(lodg_betrag)

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        if not nation:

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation:

            nationstat = get_cache (Nationstat, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

            if not nationstat:
                nationstat = Nationstat()
                db_session.add(nationstat)

                nationstat.datum = bill_date
                nationstat.nationnr = nation.nationnr

            if zimmer.sleeping:
                nationstat.dankzimmer = nationstat.dankzimmer + 1
            nationstat.logerwachs = nationstat.logerwachs + queasy.number1

            natstat1 = get_cache (Natstat1, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

            if not natstat1:
                natstat1 = Natstat1()
                db_session.add(natstat1)

                natstat1.datum = bill_date
                natstat1.nationnr = nation.nationnr

            if zimmer.sleeping:
                natstat1.zimmeranz = natstat1.zimmeranz + 1
            natstat1.persanz = natstat1.persanz + queasy.number1
            natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation:

            landstat = get_cache (Landstat, {"nationnr": [(eq, nation.nationnr)],"datum": [(eq, bill_date)]})

            if not landstat:
                landstat = Landstat()
                db_session.add(landstat)

                landstat.datum = bill_date
                landstat.nationnr = nation.nationnr

            if zimmer.sleeping:
                landstat.zimmeranz = landstat.zimmeranz + 1
            landstat.persanz = landstat.persanz + queasy.number1
            landstat.logis =  to_decimal(landstat.logis) + to_decimal(lodg_betrag)

        guestat1 = get_cache (Guestat1, {"gastnr": [(eq, guest.gastnr)],"datum": [(eq, bill_date)]})

        if not guestat1:
            guestat1 = Guestat1()
            db_session.add(guestat1)

            guestat1.datum = bill_date
            guestat1.gastnr = guest.gastnr

        if zimmer.sleeping:
            guestat1.zimmeranz = guestat1.zimmeranz + 1
        guestat1.persanz = guestat1.persanz + queasy.number1
        guestat1.logis =  to_decimal(guestat1.logis) + to_decimal(lodg_betrag)

    zinrstat = get_cache (Zinrstat, {"datum": [(eq, bill_date)],"zinr": [(eq, "avrgrate")]})

    if not zinrstat:
        zinrstat = Zinrstat()
        db_session.add(zinrstat)

        zinrstat.datum = bill_date
        zinrstat.zinr = "AvrgRate"


    zinrstat.zimmeranz = occ_rm
    zinrstat.logisumsatz =  to_decimal(t_lodging)
    zinrstat.argtumsatz =  to_decimal(t_rate)

    if foreign_rate:

        zinrstat = get_cache (Zinrstat, {"datum": [(eq, bill_date)],"zinr": [(eq, "avrglrate")]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "AvrgLRate"


        zinrstat.zimmeranz = occ_rm
        zinrstat.logisumsatz =  to_decimal(tl_lodging)
        zinrstat.argtumsatz =  to_decimal(tl_rate)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, bill_date)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "tot-rm"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

        if zimmer.sleeping:

            znbuff = get_cache (Zinrstat, {"zinr": [(eq, "act-rm")],"datum": [(eq, bill_date)]})

            if not znbuff:
                znbuff = Zinrstat()
                db_session.add(znbuff)

                znbuff.datum = bill_date
                znbuff.zinr = "act-rm"


            znbuff.zimmeranz = znbuff.zimmeranz + 1

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zistatus == 6) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():

        outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, bill_date)],"gespende": [(ge, bill_date)]})

        if outorder:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "ooo")],"datum": [(eq, bill_date)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = "ooo"


            zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zistatus <= 2) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "vacant")],"datum": [(eq, bill_date)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "vacant"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    bill_line_obj_list = {}
    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 1)).filter(
             (Bill_line.rechnr > 0) & (Bill_line.sysdate == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
        if bill_line_obj_list.get(bill_line._recid):
            continue
        else:
            bill_line_obj_list[bill_line._recid] = True


        curr_billdate = bill_line.bill_datum


        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal(fact)
        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))

        bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

        if bill.resnr > 0:

            reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
            curr_segm = reservation.segmentcode
        else:

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, bill.gastnr)],"reihenfolge": [(eq, 1)]})

            if not guestseg:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, bill.gastnr)]})

            if guestseg:
                curr_segm = guestseg.segmentcode
            else:

                segment = get_cache (Segment, {"betriebsnr": [(eq, 0)]})
                curr_segm = segment.segmentcode

        zinrstat = get_cache (Zinrstat, {"datum": [(eq, curr_billdate)],"zinr": [(eq, "segm")],"betriebsnr": [(eq, curr_segm)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = curr_billdate
            zinrstat.zinr = "SEGM"
            zinrstat.betriebsnr = curr_segm


        zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(lodg_betrag)

    return generate_output()