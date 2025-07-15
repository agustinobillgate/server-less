from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.argt_betrag import argt_betrag
from functions.ratecode_compli import ratecode_compli
from models import Zimmer, Guest, Segmentstat, Segment, Res_line, Bill, Htparam, Zimkateg, Zkstat, Zinrstat, Reservation, Arrangement, Bill_line, Queasy, Waehrung, Artikel, Argt_line, Sources, Nation, Nationstat, Natstat1, Landstat, Guestat1, Guestat, Guestseg, Sourccod, Prmarket, Kontline, Reslin_queasy, Guest_pr, Umsatz, Kontplan

def nt_rmstat():
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
    lodg_betrag:decimal = to_decimal("0.0")
    rate:decimal = to_decimal("0.0")
    grate:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    argt_betrag:decimal = to_decimal("0.0")
    ex_rate:decimal = to_decimal("0.0")
    exchg_rate:decimal = 1
    frate:decimal = 1
    t_lodging:decimal = to_decimal("0.0")
    t_rate:decimal = to_decimal("0.0")
    tl_lodging:decimal = to_decimal("0.0")
    tl_rate:decimal = to_decimal("0.0")
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
    zimmer = guest = segmentstat = segment = res_line = bill = htparam = zimkateg = zkstat = zinrstat = reservation = arrangement = bill_line = queasy = waehrung = artikel = argt_line = sources = nation = nationstat = natstat1 = landstat = guestat1 = guestat = guestseg = sourccod = prmarket = kontline = reslin_queasy = guest_pr = umsatz = kontplan = None

    zim1 = rguest = segmstat = compliment = rline = mbill = None

    Zim1 = create_buffer("Zim1",Zimmer)
    Rguest = create_buffer("Rguest",Guest)
    Segmstat = create_buffer("Segmstat",Segmentstat)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)
    Mbill = create_buffer("Mbill",Bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, htparam, zimkateg, zkstat, zinrstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, prmarket, kontline, reslin_queasy, guest_pr, umsatz, kontplan
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill

        return {}

    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int):

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, htparam, zimkateg, zkstat, zinrstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, prmarket, kontline, reslin_queasy, guest_pr, umsatz, kontplan
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill

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

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, htparam, zimkateg, zkstat, zinrstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, prmarket, kontline, reslin_queasy, guest_pr, umsatz, kontplan
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill

        prmarket = db_session.query(Prmarket).filter(
                 (Prmarket.nr == res_line.reserve_int)).first()

        if not prmarket:

            return

        kontline = db_session.query(Kontline).filter(
                 (Kontline.gastnr == res_line.gastnr) & (Kontline.ankunft <= res_line.ankunft) & (Kontline.kontstatus == 6) & (Kontline.code == prmarket.bezeich)).first()

        if not kontline:

            return

        kontline = db_session.query(Kontline).filter(
                 (Kontline.gastnr == res_line.gastnr) & (Kontline.ankunft <= res_line.ankunft) & (Kontline.abreise >= res_line.ankunft) & (Kontline.kontstatus == 6) & (Kontline.zikatnr == res_line.zikatnr) & (Kontline.arrangement == res_line.arrangement) & (Kontline.code == prmarket.bezeich)).first()

        if not kontline:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.gastnr == res_line.gastnr) & (Kontline.ankunft <= res_line.ankunft) & (Kontline.abreise >= res_line.ankunft) & (Kontline.kontstatus == 6) & (Kontline.zikatnr == res_line.zikatnr) & (Kontline.code == prmarket.bezeich)).first()

        if not kontline:

            kontline = db_session.query(Kontline).filter(
                     (Kontline.gastnr == res_line.gastnr) & (Kontline.ankunft <= res_line.ankunft) & (Kontline.abreise >= res_line.ankunft) & (Kontline.kontstatus == 6) & (Kontline.code == prmarket.bezeich)).first()

        if kontline:
            kontline.overbooking = kontline.overbooking + 1


    def check_bonus():

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, service, vat, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, htparam, zimkateg, zkstat, zinrstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, prmarket, kontline, reslin_queasy, guest_pr, umsatz, kontplan
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill

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

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

        if reslin_queasy:

            return generate_inner_output()

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == res_line.gastnr)).first()

        if res_line.l_zuordnung[0] != 0:

            rmcat = db_session.query(Rmcat).filter(
                     (Rmcat.zikatnr == res_line.l_zuordnung[0])).first()
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate and guest_pr:
            bonus = get_output(ratecode_compli(res_line.resnr, res_line.reslinnr, guest_pr.code, curr_zikatnr, bill_date))

            return generate_inner_output()

        if len(arrangement.OPTIONS) != 16:

            return generate_inner_output()
        j = 1
        for i in range(1,4 + 1) :
            stay = 0
            pay = 0
            stay = to_int(substring(options, j - 1, 2))
            pay = to_int(substring(options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = bill_date - res_line.ankunft + 1
        bonus = False

        if n <= 999:
            bonus = bonus_array[n - 1]

        return generate_inner_output()


    def create_umsatz_servtax():

        nonlocal bill_date, resnr, price_decimal, anz, comp_segm, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, prcode, i, n, occ_rm, wi_segm, curr_segm, lodg_betrag, rate, grate, argt_betrag, ex_rate, exchg_rate, frate, t_lodging, t_rate, tl_lodging, tl_rate, do_it, post_it, rm_serv, rm_vat, dayuse, foreign_rate, new_contrate, cb_flag, bonus, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, curr_billdate, zimmer, guest, segmentstat, segment, res_line, bill, htparam, zimkateg, zkstat, zinrstat, reservation, arrangement, bill_line, queasy, waehrung, artikel, argt_line, sources, nation, nationstat, natstat1, landstat, guestat1, guestat, guestseg, sourccod, prmarket, kontline, reslin_queasy, guest_pr, umsatz, kontplan
        nonlocal zim1, rguest, segmstat, compliment, rline, mbill


        nonlocal zim1, rguest, segmstat, compliment, rline, mbill

        serv_vat:bool = False
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum == bill_date)).order_by(Umsatz._recid).all():

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == umsatz.artnr) & (Artikel.departement == umsatz.departement)).first()

            if artikel:

                kontplan = db_session.query(Kontplan).filter(
                         (Kontplan.betriebsnr == umsatz.departement) & (Kontplan.kontignr == umsatz.artnr) & (Kontplan.datum == umsatz.datum)).first()

                if not kontplan:
                    service =  to_decimal("0")
                    vat =  to_decimal("0")

                    if artikel.service_code != 0:

                        htparam = db_session.query(Htparam).filter(
                                 (Htparam.paramnr == artikel.service_code)).first()

                        if htparam:
                            service =  to_decimal(htparam.fdecimal) / to_decimal("100")

                    if artikel.mwst_code != 0:

                        htparam = db_session.query(Htparam).filter(
                                 (Htparam.paramnr == artikel.mwst_code)).first()

                        if htparam:
                            vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                        if vat == 1:
                            service =  to_decimal("0")

                        elif serv_vat:
                            vat =  to_decimal(vat) * to_decimal((1) + to_decimal(service))
                    kontplan = Kontplan()
                    db_session.add(kontplan)

                    kontplan.betriebsnr = umsatz.departement
                    kontplan.kontignr = umsatz.artnr
                    kontplan.datum = umsatz.datum
                    kontplan.anzkont = service * 10000
                    kontplan.anzconf = vat * 10000

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    rm_vat = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 377)).first()

    if htparam.finteger != 0:

        compliment = db_session.query(Compliment).filter(
                 (Compliment.segmentcode == htparam.finteger)).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 48)).first()

    if htparam.finteger != 0:

        segment = db_session.query(Segment).filter(
                 (Segment.segmentcode == htparam.finteger)).first()

        if segment:
            wi_segm = segment.segmentcode
    create_umsatz_servtax()

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

        zkstat = db_session.query(Zkstat).filter(
                 (Zkstat.datum == bill_date) & (Zkstat.zikatnr == zimkateg.zikatnr)).first()

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

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("ArrTmrw").lower()) & (Zinrstat.datum == bill_date)).first()

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

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == res_line.zinr)).first()

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()
        dayuse = False
        do_it = False

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == bill_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()

            if bill_line:
                do_it = True
                dayuse = True

                if not res_line.zimmerfix:

                    zinrstat = db_session.query(Zinrstat).filter(
                             (func.lower(Zinrstat.zinr) == ("dayuse").lower()) & (Zinrstat.datum == bill_date)).first()

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = "dayuse"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1

        elif res_line.active_flag == 2 and res_line.ankunft < bill_date and not res_line.zimmerfix:

            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == bill_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
            do_it = None != bill_line
        else:
            do_it = True

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= bill_date) & (Queasy.date2 >= bill_date)).first()

        if not queasy and not zimmer.sleeping:
            do_it = False

        if queasy and queasy.number3 == res_line.gastnr:
            do_it = False

        if res_line.resstatus == 8 and res_line.abreise == bill_date and ((res_line.abreise > res_line.ankunft) or dayuse):

            zinrstat = db_session.query(Zinrstat).filter(
                     (func.lower(Zinrstat.zinr) == ("Departure").lower()) & (Zinrstat.datum == bill_date)).first()

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

                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("VIP").lower()) & (Zinrstat.datum == bill_date)).first()

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

                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("AvrgStay").lower()) & (Zinrstat.datum == bill_date)).first()

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

                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("Arrival").lower()) & (Zinrstat.datum == bill_date)).first()

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

                    zinrstat = db_session.query(Zinrstat).filter(
                             (func.lower(Zinrstat.zinr) == ("Arrival-WIG").lower()) & (Zinrstat.datum == bill_date)).first()

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

                    zinrstat = db_session.query(Zinrstat).filter(
                             (func.lower(Zinrstat.zinr) == ("Arrival-RSV").lower()) & (Zinrstat.datum == bill_date)).first()

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

                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("DepTmrw").lower()) & (Zinrstat.datum == bill_date)).first()

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

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement)).first()

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:
                guest.logiernachte = guest.logiernachte + 1

            if res_line.gastnr != res_line.gastnrmember:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr)).first()

                if guest:
                    guest.logiernachte = guest.logiernachte + 1
            rate =  to_decimal("0")
            lodg_betrag =  to_decimal("0")
            bonus = check_bonus()

            if (res_line.zipreis > 0 or bonus):

                if not res_line.zimmerfix:
                    occ_rm = occ_rm + 1

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                    if waehrung:
                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                rate =  to_decimal(res_line.zipreis)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()
                service =  to_decimal("0")
                vat =  to_decimal("0")

                htparam = db_session.query(Htparam).filter(
                             (Htparam.paramnr == artikel.service_code)).first()

                if htparam and htparam.fdecimal != 0:
                    service =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = db_session.query(Htparam).filter(
                             (Htparam.paramnr == artikel.mwst_code)).first()

                if htparam and htparam.fdecimal != 0:
                    vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = db_session.query(Htparam).filter(
                             (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
                vat = to_decimal(round(vat , 2))
                lodg_betrag =  to_decimal(rate) * to_decimal(frate)

                if rate > 0:

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
                        argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                        lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

            lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))
            rate = to_decimal(round(rate * frate , price_decimal))

            if foreign_rate and price_decimal == 0:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 145)).first()

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.htparam.finteger + 1) :
                        n = n * 10
                    rate = to_decimal(round(rate / n , 0) * n)

            if rm_serv:
                grate =  to_decimal(rate) * to_decimal((1) + to_decimal(service) + to_decimal(vat))
            else:
                grate =  to_decimal(rate)
                rate =  to_decimal(rate) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                lodg_betrag =  to_decimal(lodg_betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )


            t_rate =  to_decimal(t_rate) + to_decimal(rate) / to_decimal(frate)
            t_lodging =  to_decimal(t_lodging) + to_decimal(lodg_betrag) / to_decimal(frate)
            tl_rate =  to_decimal(tl_rate) + to_decimal(rate)
            tl_lodging =  to_decimal(tl_lodging) + to_decimal(lodg_betrag)


            pass

            segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()

            if segment and segment.betriebsnr > 0:
                pass

            elif rate == 0 and res_line.gratis > 0 and res_line.resstatus != 13:

                rline = db_session.query(Rline).filter(
                             (Rline.resnr == res_line.resnr) & (Rline.resstatus != 12) & (Rline.zipreis > 0) & (Rline.reslinnr != res_line.reslinnr)).first()

            segmentstat = db_session.query(Segmentstat).filter(
                         (Segmentstat.segmentcode == reservation.segmentcode) & (Segmentstat.datum == bill_date)).first()

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

                            segmstat = db_session.query(Segmstat).filter(
                                         (Segmstat.segmentcode == compliment.segmentcode) & (Segmstat.datum == bill_date)).first()

                            if not segmstat:
                                segmstat = Segmstat()
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

            zinrstat = db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == res_line.zinr) & (Zinrstat.datum == bill_date)).first()

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

            zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.zikatnr == res_line.zikatnr) & (Zkstat.datum == bill_date)).first()

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

                sources = db_session.query(Sources).filter(
                         (Sources.source_code == reservation.resart) & (Sources.datum == bill_date)).first()

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

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.nation1)).first()

            if nation:

                nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.nationnr == nation.nationnr) & (Nationstat.datum == bill_date)).first()

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

                natstat1 = db_session.query(Natstat1).filter(
                         (Natstat1.nationnr == nation.nationnr) & (Natstat1.datum == bill_date)).first()

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

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.nation2)).first()

            if nation and guest.nation2 != "":

                nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.nationnr == nation.nationnr) & (Nationstat.datum == bill_date)).first()

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

                natstat1 = db_session.query(Natstat1).filter(
                         (Natstat1.nationnr == nation.nationnr) & (Natstat1.datum == bill_date)).first()

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

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.land)).first()

            if nation:

                landstat = db_session.query(Landstat).filter(
                         (Landstat.nationnr == nation.nationnr) & (Landstat.datum == bill_date)).first()

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

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()

            if guest.karteityp >= 0:

                guestat1 = db_session.query(Guestat1).filter(
                         (Guestat1.gastnr == guest.gastnr) & (Guestat1.datum == bill_date)).first()

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

                    guestat = db_session.query(Guestat).filter(
                             (Guestat.gastnr == res_line.gastnr) & (Guestat.monat == get_month(bill_date)) & (Guestat.jahr == get_year(bill_date)) & (Guestat.betriebsnr == 0)).first()

                    if not guestat:
                        guestat = Guestat()
                        db_session.add(guestat)

                        guestat.gastnr = res_line.gastnr
                        guestat.monat = get_month(bill_date)
                        guestat.jahr = get_year(bill_date)


                    guestat.room_nights = guestat.room_nights + 1

                    if nation and guest.karteityp == 2:

                        guestat = db_session.query(Guestat).filter(
                                 (Guestat.gastnr == res_line.gastnr) & (Guestat.monat == get_month(bill_date)) & (Guestat.jahr == get_year(bill_date)) & (Guestat.betriebsnr == nation.nationnr)).first()

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

            if resnr != res_line.resnr:
                resnr = res_line.resnr

    for reservation in db_session.query(Reservation).filter(
             (Reservation.activeflag <= 1) & (Reservation.resnr > 0) & (Reservation.resdat == bill_date)).order_by(Reservation._recid).all():

        for rline in db_session.query(Rline).filter(
                 ((Rline.resnr == reservation.resnr)) & ((Rline.resstatus != 12))).order_by(Rline._recid).all():

            zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("NewRes").lower()) & (Zinrstat.datum == bill_date)).first()

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

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == queasy.char1)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == queasy.char2)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr == queasy.number2)).first()
        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == queasy.number3)).first()

        if zimmer.sleeping:
            occ_rm = occ_rm + 1
        rate =  to_decimal(queasy.deci1)
        service =  to_decimal("0")
        vat =  to_decimal("0")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == artikel.service_code)).first()

        if htparam and htparam.fdecimal != 0:
            service =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == artikel.mwst_code)).first()

        if htparam and htparam.fdecimal != 0:
            vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()

        if htparam.flogical:
            vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
        vat = to_decimal(round(vat , 2))
        lodg_betrag =  to_decimal(rate) * to_decimal(frate)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
            lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_line.betrag) * to_decimal(frate) * to_decimal(queasy.number1)
        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))
        rate = to_decimal(round(rate * frate , price_decimal))

        if foreign_rate and price_decimal == 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 145)).first()

            if htparam.finteger != 0:
                n = 1
                for i in range(1,htparam.htparam.finteger + 1) :
                    n = n * 10
                rate = to_decimal(round(rate / n , 0) * n)

        if rm_serv:
            grate =  to_decimal(rate) * to_decimal((1) + to_decimal(service) + to_decimal(vat))
        else:
            grate =  to_decimal(rate)
            rate =  to_decimal(rate) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
            lodg_betrag =  to_decimal(lodg_betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )


        t_rate =  to_decimal(t_rate) + to_decimal(rate) / to_decimal(frate)
        t_lodging =  to_decimal(t_lodging) + to_decimal(lodg_betrag) / to_decimal(frate)
        tl_rate =  to_decimal(tl_rate) + to_decimal(rate)
        tl_lodging =  to_decimal(tl_lodging) + to_decimal(lodg_betrag)

        guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

        if not guestseg:

            guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == guest.gastnr)).first()

        segmentstat = db_session.query(Segmentstat).filter(
                     (Segmentstat.segmentcode == guestseg.segmentcode) & (Segmentstat.datum == bill_date)).first()

        if not segmentstat:
            segmentstat = Segmentstat()
            db_session.add(segmentstat)

            segmentstat.datum = bill_date
            segmentstat.segmentcode = guestseg.segmentcode

        if zimmer.sleeping:
            segmentstat.zimmeranz = segmentstat.zimmeranz + 1
        segmentstat.persanz = segmentstat.persanz + queasy.number1
        segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(lodg_betrag)

        zinrstat = db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == zimmer.zinr) & (Zinrstat.datum == bill_date)).first()

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

        zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.zikatnr == zimmer.zikatnr) & (Zkstat.datum == bill_date)).first()

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

        reservation = db_session.query(Reservation).filter(
                     (Reservation.gastnr == guest.gastnr)).first()

        if reservation:

            sources = db_session.query(Sources).filter(
                         (Sources.source_code == reservation.resart) & (Sources.datum == bill_date)).first()

            if not sources:
                sources = Sources()
                db_session.add(sources)

                sources.datum = bill_date
                sources.source_code = reservation.resart


        else:

            sourccod = db_session.query(Sourccod).first()

            sources = db_session.query(Sources).filter(
                         (Sources.source_code == sourccod.source_code) & (Sources.datum == bill_date)).first()

            if not sources:
                sources = Sources()
                db_session.add(sources)

                sources.datum = bill_date
                sources.source_code = sourccod.source_code

        if zimmer.sleeping:
            sources.zimmeranz = sources.zimmeranz + 1
        sources.persanz = sources.persanz + queasy.number1
        sources.logis =  to_decimal(sources.logis) + to_decimal(lodg_betrag)

        nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.nation1)).first()

        if not nation:

            nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.land)).first()

        if nation:

            nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.nationnr == nation.nationnr) & (Nationstat.datum == bill_date)).first()

            if not nationstat:
                nationstat = Nationstat()
                db_session.add(nationstat)

                nationstat.datum = bill_date
                nationstat.nationnr = nation.nationnr

            if zimmer.sleeping:
                nationstat.dankzimmer = nationstat.dankzimmer + 1
            nationstat.logerwachs = nationstat.logerwachs + queasy.number1

            natstat1 = db_session.query(Natstat1).filter(
                         (Natstat1.nationnr == nation.nationnr) & (Natstat1.datum == bill_date)).first()

            if not natstat1:
                natstat1 = Natstat1()
                db_session.add(natstat1)

                natstat1.datum = bill_date
                natstat1.nationnr = nation.nationnr

            if zimmer.sleeping:
                natstat1.zimmeranz = natstat1.zimmeranz + 1
            natstat1.persanz = natstat1.persanz + queasy.number1
            natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(lodg_betrag)

        nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.land)).first()

        if nation:

            landstat = db_session.query(Landstat).filter(
                         (Landstat.nationnr == nation.nationnr) & (Landstat.datum == bill_date)).first()

            if not landstat:
                landstat = Landstat()
                db_session.add(landstat)

                landstat.datum = bill_date
                landstat.nationnr = nation.nationnr

            if zimmer.sleeping:
                landstat.zimmeranz = landstat.zimmeranz + 1
            landstat.persanz = landstat.persanz + queasy.number1
            landstat.logis =  to_decimal(landstat.logis) + to_decimal(lodg_betrag)

        guestat1 = db_session.query(Guestat1).filter(
                     (Guestat1.gastnr == guest.gastnr) & (Guestat1.datum == bill_date)).first()

        if not guestat1:
            guestat1 = Guestat1()
            db_session.add(guestat1)

            guestat1.datum = bill_date
            guestat1.gastnr = guest.gastnr

        if zimmer.sleeping:
            guestat1.zimmeranz = guestat1.zimmeranz + 1
        guestat1.persanz = guestat1.persanz + queasy.number1
        guestat1.logis =  to_decimal(guestat1.logis) + to_decimal(lodg_betrag)

    zinrstat = db_session.query(Zinrstat).filter(
             (Zinrstat.datum == bill_date) & (func.lower(Zinrstat.zinr) == ("AvrgRate").lower())).first()

    if not zinrstat:
        zinrstat = Zinrstat()
        db_session.add(zinrstat)

        zinrstat.datum = bill_date
        zinrstat.zinr = "AvrgRate"


    zinrstat.zimmeranz = occ_rm
    zinrstat.logisumsatz =  to_decimal(t_lodging)
    zinrstat.argtumsatz =  to_decimal(t_rate)

    if foreign_rate:

        zinrstat = db_session.query(Zinrstat).filter(
                 (Zinrstat.datum == bill_date) & (func.lower(Zinrstat.zinr) == ("AvrgLRate").lower())).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "AvrgLRate"


        zinrstat.zimmeranz = occ_rm
        zinrstat.logisumsatz =  to_decimal(tl_lodging)
        zinrstat.argtumsatz =  to_decimal(tl_rate)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("tot-rm").lower()) & (Zinrstat.datum == bill_date)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "tot-rm"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zistatus == 6) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("ooo").lower()) & (Zinrstat.datum == bill_date)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "ooo"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.zistatus <= 2) & (Zimmer.sleeping)).order_by(Zimmer._recid).all():

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("vacant").lower()) & (Zinrstat.datum == bill_date)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = bill_date
            zinrstat.zinr = "vacant"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

    bill_line_obj_list = []
    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 1)).filter(
             (Bill_line.rechnr > 0) & (Bill_line.sysdate == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
        if bill_line._recid in bill_line_obj_list:
            continue
        else:
            bill_line_obj_list.append(bill_line._recid)


        curr_billdate = bill_line.bill_datum
        service =  to_decimal("0")
        vat =  to_decimal("0")

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.service_code)).first()

        if htparam and htparam.fdecimal != 0:
            service =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.mwst_code)).first()

        if htparam and htparam.fdecimal != 0:
            vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 479)).first()

        if htparam.flogical:
            vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
        vat = to_decimal(round(vat , 2))
        lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))
        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))

        bill = db_session.query(Bill).filter(
                 (Bill.rechnr == bill_line.rechnr)).first()

        if bill.resnr > 0:

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == bill.resnr)).first()
            curr_segm = reservation.segmentcode
        else:

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == bill.gastnr) & (Guestseg.reihenfolge == 1)).first()

            if not guestseg:

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == bill.gastnr)).first()

            if guestseg:
                curr_segm = guestseg.segmentcode
            else:

                segment = db_session.query(Segment).filter(
                         (Segment.betriebsnr == 0)).first()
                curr_segm = segment.segmentcode

        zinrstat = db_session.query(Zinrstat).filter(
                 (Zinrstat.datum == curr_billdate) & (func.lower(Zinrstat.zinr) == ("SEGM").lower()) & (Zinrstat.betriebsnr == curr_segm)).first()

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = curr_billdate
            zinrstat.zinr = "SEGM"
            zinrstat.betriebsnr = curr_segm


        zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(lodg_betrag)

    return generate_output()