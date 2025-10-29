#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 22-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betragbl import argt_betragbl
from sqlalchemy import func
from models import Guest, Segment, Res_line, Htparam, Nation, Reservation, Arrangement, Zimmer, Zimkateg, Bill_line, Genstat, Reslin_queasy, Akt_cust, Bediener, Waehrung, Artikel, Argt_line, Zwkum, Fixleist, Kontline, Bill, Guestseg, Segmentstat, Nationstat, Natstat1, Sources, Landstat, Guestat1, Guestat, Zinrstat, Zkstat, H_artikel, H_bill_line

def nt_genstat():

    prepare_cache ([Segment, Res_line, Htparam, Nation, Reservation, Arrangement, Zimmer, Zimkateg, Bill_line, Genstat, Reslin_queasy, Akt_cust, Bediener, Waehrung, Artikel, Argt_line, Fixleist, Kontline, Guestseg, Segmentstat, Nationstat, Natstat1, Sources, Guestat1, Guestat, Zinrstat, Zkstat, H_artikel, H_bill_line])

    bill_date:date = None
    price_decimal:int = 0
    invno:int = 0
    purno:int = 0
    lodg_betrag:Decimal = to_decimal("0.0")
    rate:Decimal = to_decimal("0.0")
    ratelocal:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    vat2_art:Decimal = to_decimal("0.0")
    fact_art:Decimal = to_decimal("0.0")
    argt_betrag:Decimal = to_decimal("0.0")
    ex_rate:Decimal = to_decimal("0.0")
    exchg_rate:Decimal = 1
    frate:Decimal = 1
    netto:Decimal = to_decimal("0.0")
    def_nation:int = 0
    do_it:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    serv_taxable:bool = False
    foreign_rate:bool = False
    new_contrate:bool = False
    bonus:bool = False
    tot_rmcharge:Decimal = to_decimal("0.0")
    gastmemberno:int = 0
    revtype:List[int] = [5, 1, 2, 3, 5, 3, 4]
    fb_dept:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    post_it:bool = False
    fcost:Decimal = to_decimal("0.0")
    ba_dept:int = 0
    pax:int = 0
    price:Decimal = to_decimal("0.0")
    vat_art:Decimal = to_decimal("0.0")
    service_art:Decimal = to_decimal("0.0")
    gross_argt:Decimal = to_decimal("0.0")
    net_argt:Decimal = to_decimal("0.0")
    guest = segment = res_line = htparam = nation = reservation = arrangement = zimmer = zimkateg = bill_line = genstat = reslin_queasy = akt_cust = bediener = waehrung = artikel = argt_line = zwkum = fixleist = kontline = bill = guestseg = segmentstat = nationstat = natstat1 = sources = landstat = guestat1 = guestat = zinrstat = zkstat = h_artikel = h_bill_line = None

    t_list = argt_list = rguest = compliment = rline = mguest = dummyguest = tguest = accline = bline = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "rechnr":int, "billno":int, "bezeich":string, "food":Decimal, "bev":Decimal, "other":Decimal, "pay":Decimal, "rmtrans":Decimal})
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argt_artnr":int, "departement":int, "is_charged":int, "period":int, "vt_percnt":int})

    Rguest = create_buffer("Rguest",Guest)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)
    Mguest = create_buffer("Mguest",Guest)
    Dummyguest = create_buffer("Dummyguest",Guest)
    Tguest = create_buffer("Tguest",Guest)
    Accline = create_buffer("Accline",Res_line)
    Bline = create_buffer("Bline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        return {}

    def correct_depart():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        for bline in db_session.query(Bline).filter(
                 (Bline.abreise == bill_date) & (Bline.resstatus == 8)).order_by(Bline._recid).all():

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.resnr == bline.resnr) & (Genstat.res_int[inc_value(0)] == bline.reslinnr) & (Genstat.res_date[inc_value(1)] != bline.abreise)).order_by(Genstat._recid).all():

                bgenstat = get_cache (Genstat, {"_recid": [(eq, genstat._recid)]})
                bgenstat.res_date[1] = bline.abreise


                pass
                pass


    def update_genstat_ratecode(ratecode:string):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        str:string = ""
        zwstr:string = ""
        curr_i:int = 0
        found:bool = False
        for curr_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(curr_i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                zwstr = zwstr + "$CODE$" + ratecode + ";"
                found = True
            else:
                zwstr = zwstr + str + ";"

        if not found:
            zwstr = zwstr + "$CODE$" + ratecode + ";"
        genstat.res_char[1] = zwstr


    def check_bonus():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

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
        bonus = (res_line.zipreis == 0) and ((res_line.erwachs + res_line.kind1) > 0)

        return generate_inner_output()


    def reorg_stat():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        anz:int = 0
        issharer:bool = False
        segbuff = None
        natbuff = None
        nsbuff = None
        scbuff = None
        landbuff = None
        gsbuff = None
        gubuff = None
        zibuff = None
        genbuff = None
        zimbuff = None
        zkbuff = None
        Segbuff =  create_buffer("Segbuff",Segmentstat)
        Natbuff =  create_buffer("Natbuff",Nationstat)
        Nsbuff =  create_buffer("Nsbuff",Natstat1)
        Scbuff =  create_buffer("Scbuff",Sources)
        Landbuff =  create_buffer("Landbuff",Landstat)
        Gsbuff =  create_buffer("Gsbuff",Guestat1)
        Gubuff =  create_buffer("Gubuff",Guestat)
        Zibuff =  create_buffer("Zibuff",Zinrstat)
        Genbuff =  create_buffer("Genbuff",Genstat)
        Zimbuff =  create_buffer("Zimbuff",Zimmer)
        Zkbuff =  create_buffer("Zkbuff",Zkstat)

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == bill_date)).order_by(Segmentstat._recid).all():

            segbuff = get_cache (Segmentstat, {"_recid": [(eq, segmentstat._recid)]})
            segbuff.logis =  to_decimal("0")
            segbuff.zimmeranz = 0
            segbuff.persanz = 0
            segbuff.kind1 = 0
            segbuff.kind2 = 0
            segbuff.gratis = 0
            segbuff.betriebsnr = 0


            pass

        for nationstat in db_session.query(Nationstat).filter(
                 (Nationstat.datum == bill_date)).order_by(Nationstat._recid).all():

            natbuff = get_cache (Nationstat, {"_recid": [(eq, nationstat._recid)]})
            db_session.delete(natbuff)
            pass

        for natstat1 in db_session.query(Natstat1).filter(
                 (Natstat1.datum == bill_date)).order_by(Natstat1._recid).all():

            nsbuff = get_cache (Natstat1, {"_recid": [(eq, natstat1._recid)]})
            db_session.delete(nsbuff)
            pass

        for sources in db_session.query(Sources).filter(
                 (Sources.datum == bill_date)).order_by(Sources._recid).all():

            scbuff = get_cache (Sources, {"_recid": [(eq, sources._recid)]})
            scbuff.logis =  to_decimal("0")
            scbuff.zimmeranz = 0
            scbuff.persanz = 0
            scbuff.betriebsnr = 0


            pass

        for landstat in db_session.query(Landstat).filter(
                 (Landstat.datum == bill_date)).order_by(Landstat._recid).all():

            landbuff = db_session.query(Landbuff).filter(
                     (Landbuff._recid == landstat._recid)).first()
            db_session.delete(landstat)
            pass

        for guestat1 in db_session.query(Guestat1).filter(
                 (Guestat1.datum == bill_date)).order_by(Guestat1._recid).all():

            gsbuff = get_cache (Guestat1, {"_recid": [(eq, guestat1._recid)]})
            db_session.delete(gsbuff)
            pass

        for guestat in db_session.query(Guestat).filter(
                 (Guestat.jahr == get_year(bill_date)) & (Guestat.monat == get_month(bill_date))).order_by(Guestat._recid).all():

            gubuff = get_cache (Guestat, {"_recid": [(eq, guestat._recid)]})
            db_session.delete(gubuff)
            pass

        zinrstat_obj_list = {}
        zinrstat = Zinrstat()
        zimmer = Zimmer()
        for zinrstat._recid, zinrstat.zimmeranz, zinrstat.betriebsnr, zinrstat.personen, zinrstat.logisumsatz, zinrstat.argtumsatz, zinrstat.gesamtumsatz, zinrstat.datum, zinrstat.zinr, zimmer.sleeping, zimmer._recid in db_session.query(Zinrstat._recid, Zinrstat.zimmeranz, Zinrstat.betriebsnr, Zinrstat.personen, Zinrstat.logisumsatz, Zinrstat.argtumsatz, Zinrstat.gesamtumsatz, Zinrstat.datum, Zinrstat.zinr, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Zinrstat.zinr)).filter(
                 (Zinrstat.datum == bill_date)).order_by(Zinrstat._recid).all():
            if zinrstat_obj_list.get(zinrstat._recid):
                continue
            else:
                zinrstat_obj_list[zinrstat._recid] = True

            zibuff = get_cache (Zinrstat, {"_recid": [(eq, zinrstat._recid)]})
            db_session.delete(zibuff)
            pass

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == bill_date)).order_by(Zkstat._recid).all():

            zkbuff = get_cache (Zkstat, {"_recid": [(eq, zkstat._recid)]})
            db_session.delete(zkbuff)
            pass

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            anz = 0

            for zimbuff in db_session.query(Zimbuff).filter(
                     (Zimbuff.zikatnr == zimkateg.zikatnr) & (Zimbuff.sleeping)).order_by(Zimbuff._recid).all():
                anz = anz + 1

            zkstat = get_cache (Zkstat, {"datum": [(eq, bill_date)],"zikatnr": [(eq, zimkateg.zikatnr)]})

            if not zkstat:
                zkstat = Zkstat()
                db_session.add(zkstat)

                zkstat.datum = bill_date
                zkstat.zikatnr = zimkateg.zikatnr


            zkstat.anz100 = anz
            pass

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum == bill_date) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            segmentstat = get_cache (Segmentstat, {"datum": [(eq, bill_date)],"segmentcode": [(eq, genstat.segmentcode)]})

            if not segmentstat:
                segmentstat = Segmentstat()
                db_session.add(segmentstat)

                segmentstat.datum = bill_date
                segmentstat.segmentcode = genstat.segmentcode


            issharer = genstat.resstatus == 13

            if not issharer:
                segmentstat.zimmeranz = segmentstat.zimmeranz + 1

                if genstat.zipreis == 0 and (genstat.gratis >= 1):
                    segmentstat.betriebsnr = segmentstat.betriebsnr + 1
            segmentstat.persanz = segmentstat.persanz + genstat.erwachs
            segmentstat.kind1 = segmentstat.kind1 + genstat.kind1 +\
                    genstat.kind3
            segmentstat.kind2 = segmentstat.kind2 + genstat.kind2
            segmentstat.gratis = segmentstat.gratis + genstat.gratis
            segmentstat.logis =  to_decimal(segmentstat.logis) + to_decimal(genstat.logis)


            pass

            if genstat.domestic != 0:

                nationstat = get_cache (Nationstat, {"datum": [(eq, bill_date)],"nationnr": [(eq, genstat.domestic)]})

                if not nationstat:
                    nationstat = Nationstat()
                    db_session.add(nationstat)

                    nationstat.datum = bill_date
                    nationstat.nationnr = genstat.domestic

                if not issharer:
                    nationstat.dankzimmer = nationstat.dankzimmer + 1

                    if genstat.zipreis == 0:
                        nationstat.betriebsnr = nationstat.betriebsnr + 1
                nationstat.logerwachs = nationstat.logerwachs + genstat.erwachs
                nationstat.loggratis = nationstat.loggratis + genstat.gratis
                nationstat.logkind1 = nationstat.logkind1 + genstat.kind1 + genstat.kind3
                nationstat.logkind2 = nationstat.logkind2 + genstat.kind2

                if not issharer and genstat.res_date[0] == bill_date:
                    nationstat.ankerwachs = nationstat.ankerwachs + genstat.erwachs
                    nationstat.ankkind1 = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                    nationstat.ankkind2 = nationstat.ankkind2 + genstat.kind2
                    nationstat.ankgratis = nationstat.ankgratis + genstat.gratis


                pass

            nationstat = get_cache (Nationstat, {"datum": [(eq, bill_date)],"nationnr": [(eq, genstat.nationnr)]})

            if not nationstat:
                nationstat = Nationstat()
                db_session.add(nationstat)

                nationstat.datum = bill_date
                nationstat.nationnr = genstat.nationnr

            if not issharer:
                nationstat.dankzimmer = nationstat.dankzimmer + 1

                if genstat.zipreis == 0:
                    nationstat.betriebsnr = nationstat.betriebsnr + 1
            nationstat.logerwachs = nationstat.logerwachs + genstat.erwachs
            nationstat.loggratis = nationstat.loggratis + genstat.gratis
            nationstat.logkind1 = nationstat.logkind1 + genstat.kind1 + genstat.kind3
            nationstat.logkind2 = nationstat.logkind2 + genstat.kind2

            if not issharer and genstat.res_date[0] == bill_date:
                nationstat.ankerwachs = nationstat.ankerwachs + genstat.erwachs
                nationstat.ankkind1 = nationstat.ankkind1 + genstat.kind1 + genstat.kind3
                nationstat.ankkind2 = nationstat.ankkind2 + genstat.kind2
                nationstat.ankgratis = nationstat.ankgratis + genstat.gratis

            if genstat.res_date[1] > genstat.res_date[0]:
                nationstat.dlogkind1 = nationstat.dlogkind1 + genstat.res_date[1] - genstat.res_date[0]
            else:
                nationstat.dlogkind1 = nationstat.dlogkind1 + 1
            nationstat.dlogkind2 = nationstat.dlogkind2 + 1
            pass

            natstat1 = get_cache (Natstat1, {"datum": [(eq, bill_date)],"nationnr": [(eq, genstat.nationnr)]})

            if not natstat1:
                natstat1 = Natstat1()
                db_session.add(natstat1)

                natstat1.datum = bill_date
                natstat1.nationnr = genstat.nationnr

            if not issharer:
                natstat1.zimmeranz = natstat1.zimmeranz + 1

                if genstat.zipreis == 0:
                    natstat1.betriebsnr = natstat1.betriebsnr + 1
            natstat1.persanz = natstat1.persanz + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(genstat.logis)
            pass

            if genstat.domestic != 0:

                natstat1 = get_cache (Natstat1, {"datum": [(eq, bill_date)],"nationnr": [(eq, genstat.domestic)]})

                if not natstat1:
                    natstat1 = Natstat1()
                    db_session.add(natstat1)

                    natstat1.datum = bill_date
                    natstat1.nationnr = genstat.domestic

                if not issharer:
                    natstat1.zimmeranz = natstat1.zimmeranz + 1

                    if genstat.zipreis == 0:
                        natstat1.betriebsnr = natstat1.betriebsnr + 1
                natstat1.persanz = natstat1.persanz + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

                if genstat.zipreis != 0:
                    natstat1.logis =  to_decimal(natstat1.logis) + to_decimal(genstat.logis)
                pass

            sources = get_cache (Sources, {"datum": [(eq, bill_date)],"source_code": [(eq, genstat.source)]})

            if not sources:
                sources = Sources()
                db_session.add(sources)

                sources.datum = bill_date
                sources.source_code = genstat.source

            if not issharer:
                sources.zimmeranz = sources.zimmeranz + 1

                if genstat.zipreis == 0:
                    sources.betriebsnr = sources.betriebsnr + 1
            sources.persanz = sources.persanz + genstat.erwachs +\
                    genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                sources.logis =  to_decimal(sources.logis) + to_decimal(genstat.logis)
            pass

            landstat = get_cache (Landstat, {"datum": [(eq, bill_date)],"nationnr": [(eq, genstat.resident)]})

            if not landstat:
                landstat = Landstat()
                db_session.add(landstat)

                landstat.datum = bill_date
                landstat.nationnr = genstat.resident

            if not issharer:
                landstat.zimmeranz = landstat.zimmeranz + 1

                if genstat.zipreis == 0:
                    landstat.betriebsnr = landstat.betriebsnr + 1
            landstat.persanz = landstat.persanz + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                landstat.logis =  to_decimal(landstat.logis) + to_decimal(genstat.logis)
            pass

            guestat1 = get_cache (Guestat1, {"datum": [(eq, bill_date)],"gastnr": [(eq, genstat.gastnr)]})

            if not guestat1:
                guestat1 = Guestat1()
                db_session.add(guestat1)

                guestat1.datum = bill_date
                guestat1.gastnr = genstat.gastnr

            if not issharer:
                guestat1.zimmeranz = guestat1.zimmeranz + 1

                if genstat.zipreis == 0:
                    guestat1.betriebsnr = guestat1.betriebsnr + 1
            guestat1.persanz = guestat1.persanz + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                guestat1.logis =  to_decimal(guestat1.logis) + to_decimal(genstat.logis)
            pass

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, bill_date)],"zinr": [(eq, genstat.zinr)]})

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = genstat.zinr


            vat = 0 
            service == 0

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if arrangement:

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

                if artikel:
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))

            if not issharer:
                zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                if genstat.zipreis == 0:
                    zinrstat.betriebsnr = zinrstat.betriebsnr + 1
            zinrstat.personen = zinrstat.personen + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(genstat.logis)
                zinrstat.argtumsatz =  to_decimal(zinrstat.argtumsatz) + to_decimal(genstat.ratelocal) / to_decimal(fact)

            if rm_serv:
                zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(genstat.ratelocal) * to_decimal(fact)
            else:
                zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(genstat.ratelocal)

            zkstat = get_cache (Zkstat, {"zikatnr": [(eq, genstat.zikatnr)],"datum": [(eq, bill_date)]})

            if not zkstat:
                zkstat = Zkstat()
                db_session.add(zkstat)

                zkstat.datum = bill_date
                zkstat.zikatnr = genstat.zikatnr


            anz = 0

            if not issharer:
                zkstat.zimmeranz = zkstat.zimmeranz + 1

                if genstat.zipreis == 0 and genstat.gratis >= 1:
                    zkstat.betriebsnr = zkstat.betriebsnr + 1
            zkstat.personen = zkstat.personen + genstat.erwachs + genstat.kind1 +\
                    genstat.kind2 + genstat.kind3 + genstat.gratis

            if genstat.zipreis == 0:

                if genstat.gratis == 0 and (genstat.erwachs + genstat.kind1) > 0:
                    zkstat.arrangement_art[0] = zkstat.arrangement_art[0] + 1

            if genstat.res_date[0] == bill_date and genstat.res_date[1] > bill_date:
                zkstat.anz_ankunft = zkstat.anz_ankunft + 1

            if genstat.res_date[0] == genstat.res_date[1]:
                zkstat.anz_abr = zkstat.anz_abr + 1
            pass

        for genbuff in db_session.query(Genbuff).filter(
                 (get_year(Genbuff.datum) == get_year(bill_date)) & (get_month(Genbuff.datum) == get_month(bill_date)) & (Genbuff.zinr != "")).order_by(Genbuff._recid).all():

            guestat = get_cache (Guestat, {"monat": [(eq, get_month(bill_date))],"jahr": [(eq, get_year(bill_date))],"gastnr": [(eq, genbuff.gastnr)]})

            if not guestat:
                guestat = Guestat()
                db_session.add(guestat)

                guestat.monat = get_month(bill_date)
                guestat.jahr = get_year(bill_date)
                guestat.gastnr = genbuff.gastnr

            if genbuff.resstatus == 6 or (genbuff.res_date[0] == genbuff.res_date[1] and genbuff.resstatus != 13):
                guestat.room_nights = guestat.room_nights + 1
            pass


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        post_it = False
        delta:int = 0
        start_date:date = None
        curr_date:date = None

        def generate_inner_output():
            return (post_it)

        curr_date = bill_date

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = (lfakt - res_line.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    def check_fixargt_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, start_date:date):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        post_it = False
        curr_date:date = None

        def generate_inner_output():
            return (post_it)

        curr_date = bill_date

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if curr_date <= (start_date + timedelta(days=(intervall - 1))) and curr_date >= start_date:
                post_it = True

        return generate_inner_output()


    def banq_rev():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, ba_dept, pax, price, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, zwkum, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline


        nonlocal t_list, argt_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline, bline
        nonlocal t_list_data, argt_list_data

        ba_betrag:Decimal = to_decimal("0.0")
        invoice_no:int = 0
        i:int = 0
        curr_inv_no:int = 0
        t_bill_line = None
        artlist = None
        T_bill_line =  create_buffer("T_bill_line",Bill_line)
        Artlist =  create_buffer("Artlist",Artikel)

        t_bill_line_obj_list = {}
        t_bill_line = Bill_line()
        artikel = Artikel()
        for t_bill_line.bezeich, t_bill_line.betrag, t_bill_line.rechnr, t_bill_line._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel.artart, artikel._recid in db_session.query(T_bill_line.bezeich, T_bill_line.betrag, T_bill_line.rechnr, T_bill_line._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == T_bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 0)).filter(
                 (T_bill_line.rechnr > 0) & (T_bill_line.bill_datum == bill_date) & (T_bill_line.zeit >= 0) & (T_bill_line.departement == ba_dept)).order_by(T_bill_line.bezeich).all():
            if t_bill_line_obj_list.get(t_bill_line._recid):
                continue
            else:
                t_bill_line_obj_list[t_bill_line._recid] = True


            service =  to_decimal("0")
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")
            fact =  to_decimal("0")
            ba_betrag =  to_decimal("0")

            if artikel.artart == 1:
                for i in range(1,length(t_bill_line.bezeich)  + 1) :

                    if substring(t_bill_line.bezeich, i - 1, 1) == ("*").lower() :
                        invoice_no = to_int(substring(t_bill_line.bezeich, i + 1 - 1, length(t_bill_line.bezeich)))


                        i = 999

                if curr_inv_no != invoice_no:

                    h_bill_line_obj_list = {}
                    h_bill_line = H_bill_line()
                    h_artikel = H_artikel()
                    for h_bill_line.betrag, h_bill_line._recid, h_artikel.artnrfront, h_artikel.departement, h_artikel._recid in db_session.query(H_bill_line.betrag, H_bill_line._recid, H_artikel.artnrfront, H_artikel.departement, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == ba_dept) & (H_artikel.artart == 0)).filter(
                             (H_bill_line.rechnr == invoice_no) & (H_bill_line.departement == ba_dept) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line._recid).all():
                        if h_bill_line_obj_list.get(h_bill_line._recid):
                            continue
                        else:
                            h_bill_line_obj_list[h_bill_line._recid] = True


                        service =  to_decimal("0")
                        vat =  to_decimal("0")
                        vat2 =  to_decimal("0")
                        fact =  to_decimal("0")

                        artlist = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        if artlist:
                            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artlist.artnr, artlist.departement, bill_date))
                            ba_betrag =  to_decimal(ba_betrag) + to_decimal((h_bill_line.betrag) / to_decimal(fact) )


                    curr_inv_no = invoice_no


            else:
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                ba_betrag =  to_decimal(t_bill_line.betrag) / to_decimal(fact)

            bill = get_cache (Bill, {"rechnr": [(eq, t_bill_line.rechnr)]})

            genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnr": [(eq, bill.gastnr)]})

            if not genstat:
                genstat = Genstat()
                db_session.add(genstat)

                genstat.datum = bill_date
                genstat.gastnr = bill.gastnr
                genstat.gastnrmember = bill.gastnr


            genstat.res_deci[6] = genstat.res_deci[6] + ba_betrag


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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
    fb_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
    lundin_art = htparam.finteger

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
    ba_dept = htparam.finteger

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resstatus, Res_line.active_flag).all():

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        rguest = db_session.query(Rguest).filter(
                 (Rguest.gastnr == res_line.gastnr)).first()

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
        do_it = False
        tot_rmcharge =  to_decimal("0")

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
            do_it = None != bill_line

        elif res_line.active_flag == 2 and res_line.ankunft < bill_date:

            if res_line.zimmerfix:
                do_it = False
            else:

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, bill_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line
        else:
            do_it = True

        if do_it:
            purno = 0
            rate =  to_decimal("0")
            ratelocal =  to_decimal("0")
            lodg_betrag =  to_decimal("0")
            bonus = False
            gastmemberno = res_line.gastnrmember

            genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnrmember": [(eq, res_line.gastnrmember)],"zinr": [(eq, res_line.zinr)]})

            if genstat:

                mguest = db_session.query(Mguest).order_by(Mguest._recid.desc()).first()
                gastmemberno = mguest.gastnr + 1

                tguest = db_session.query(Tguest).filter(
                         (Tguest.gastnr == res_line.gastnrmember)).first()

                if tguest:
                    dummyguest = Guest()
                    db_session.add(dummyguest)

                    buffer_copy(tguest, dummyguest,except_fields=["gastnr","karteityp"])
                    dummyguest.gastnr = gastmemberno
                    dummyguest.karteityp = tguest.karteityp


            genstat = Genstat()
            db_session.add(genstat)

            genstat.datum = bill_date
            genstat.gastnr = res_line.gastnr
            genstat.gastnrmember = gastmemberno
            genstat.wahrungsnr = res_line.betriebsnr
            genstat.resnr = res_line.resnr
            genstat.res_int[0] = res_line.reslinnr
            genstat.res_int[1] = res_line.reserve_int
            genstat.res_int[6] = guest.master_gastnr
            genstat.res_int[7] = reservation.kontakt_nr
            genstat.res_int[8] = res_line.l_zuordnung[0]
            genstat.res_logic[0] = False
            genstat.res_logic[1] = zimmer.sleeping
            genstat.res_date[0] = res_line.ankunft
            genstat.res_date[1] = res_line.abreise
            genstat.res_char[0] = res_line.reserve_char
            genstat.res_char[1] = res_line.zimmer_wunsch
            genstat.res_char[2] = reservation.groupname
            genstat.resstatus = res_line.resstatus
            genstat.ankflag = (res_line.ankunft == bill_date)
            genstat.zikatnr = res_line.zikatnr
            genstat.argt = arrangement.arrangement
            genstat.zinr = res_line.zinr
            genstat.karteityp = rguest.karteityp
            genstat.source = reservation.resart
            genstat.segmentcode = reservation.segmentcode
            genstat.res_date[2] = reservation.resdat

            if reservation.kontakt_nr != 0:
                genstat.res_char[3] = to_string(reservation.kontakt_nr)

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

            if reslin_queasy and reslin_queasy.char2 != "":
                update_genstat_ratecode(reslin_queasy.char2)

            if reservation.vesrdepot != "" and not matches(res_line.zimmer_wunsch,r"*voucher*"):
                genstat.res_char[1] = genstat.res_char[1] + "voucher" + reservation.vesrdepot + ";"

            if nation:
                genstat.nationnr = nation.nationnr
            else:
                genstat.nationnr = def_nation

            if res_line.l_zuordnung[0] != 0 and res_line.l_zuordnung[0] != res_line.zikatnr:
                genstat.res_char[1] = genstat.res_char[1] +\
                    "RmUpgrade" + to_string(res_line.l_zuordnung[0]) + ";"

            accline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"kontakt_nr": [(eq, res_line.reslinnr)],"l_zuordnung[2]": [(eq, 1)]})

            if accline:
                genstat.res_int[2] = accline.gastnrmember

            if accline:

                curr_recid = accline._recid
                accline = db_session.query(Accline).filter(
                             (Accline.resnr == res_line.resnr) & (Accline.kontakt_nr == res_line.reslinnr) & (Accline.l_zuordnung[inc_value(2)] == 1) & (Accline._recid > curr_recid)).first()

            if accline:
                genstat.res_int[3] = accline.gastnrmember

            if accline:

                curr_recid = accline._recid
                accline = db_session.query(Accline).filter(
                             (Accline.resnr == res_line.resnr) & (Accline.kontakt_nr == res_line.reslinnr) & (Accline.l_zuordnung[inc_value(2)] == 1) & (Accline._recid > curr_recid)).first()

            if accline:
                genstat.res_int[4] = accline.gastnrmember


            pass

            akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, res_line.gastnr)]})

            if akt_cust:

                bediener = get_cache (Bediener, {"userinit": [(eq, akt_cust.userinit)]})

            if not akt_cust or not bediener:

                rguest = db_session.query(Rguest).filter(
                             (Rguest.gastnr == res_line.gastnr)).first()

                if rguest.phonetik3 != "":

                    bediener = get_cache (Bediener, {"userinit": [(eq, rguest.phonetik3)]})

            if bediener:
                genstat.res_int[5] = bediener.nr


            bonus = check_bonus()
            genstat.res_logic[2] = bonus

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            rate =  to_decimal(res_line.zipreis)

            if bonus:
                rate =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})
            service, vat, vat2, fact = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))
            lodg_betrag =  to_decimal(rate) * to_decimal(frate)
            gross_argt =  to_decimal("0")
            net_argt =  to_decimal("0")
            ex_rate =  to_decimal("1")

            if lodg_betrag > 0:

                if res_line.reserve_dec != 0:
                    ratelocal =  to_decimal(rate) * to_decimal(res_line.reserve_dec)
                else:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        ratelocal =  to_decimal(rate) * to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                genstat.zipreis =  to_decimal(rate)
                genstat.ratelocal =  to_decimal(ratelocal)

                argt_line_obj_list = {}
                argt_line = Argt_line()
                artikel = Artikel()
                for argt_line._recid, argt_line.argtnr, argt_line.departement, argt_line.argt_artnr, argt_line.vt_percnt, argt_line.fakt_modus, argt_line.intervall, argt_line.betriebsnr, argt_line.betrag, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel.artart, artikel._recid in db_session.query(Argt_line._recid, Argt_line.argtnr, Argt_line.departement, Argt_line.argt_artnr, Argt_line.vt_percnt, Argt_line.fakt_modus, Argt_line.intervall, Argt_line.betriebsnr, Argt_line.betrag, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                    if argt_line_obj_list.get(argt_line._recid):
                        continue
                    else:
                        argt_line_obj_list[argt_line._recid] = True


                    argt_betrag, ex_rate = get_output(argt_betragbl(res_line._recid, argt_line._recid))
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                    argt_betrag =  to_decimal(argt_betrag) * to_decimal(ex_rate)
                    gross_argt =  to_decimal(gross_argt) + to_decimal(argt_betrag)
                    argt_betrag =  to_decimal(argt_betrag) / to_decimal(fact_art)
                    net_argt =  to_decimal(net_argt) + to_decimal(argt_betrag)

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + argt_betrag
                        else:
                            genstat.res_deci[1] = genstat.res_deci[1] + argt_betrag

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + argt_betrag
                        else:
                            genstat.res_deci[2] = genstat.res_deci[2] + argt_betrag

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + argt_betrag
                        else:
                            genstat.res_deci[3] = genstat.res_deci[3] + argt_betrag

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + argt_betrag
                        else:
                            genstat.res_deci[2] = genstat.res_deci[2] + argt_betrag
                    else:

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + argt_betrag
                        else:
                            genstat.res_deci[4] = genstat.res_deci[4] + argt_betrag

                if rm_vat:
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(gross_argt)
                    lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)


                else:
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(net_argt)

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():

                if argt_line.fakt_modus == 6:

                    argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.is_charged == 1), first=True)

                    if not argt_list:
                        argt_list = Argt_list()
                        argt_list_data.append(argt_list)

                        argt_list.argtnr = argt_line.argtnr
                        argt_list.departement = argt_line.departement
                        argt_list.argt_artnr = argt_line.argt_artnr
                        argt_list.vt_percnt = argt_line.vt_percnt
                        argt_list.is_charged = 1
                        argt_list.period = 0

                    if argt_list.period < argt_line.intervall:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                        if reslin_queasy:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:
                                post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, reslin_queasy.date1)

                                if post_it :
                                    argt_list.period = argt_list.period + 1
                            else:
                                post_it = False
                        else:
                            post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, res_line.ankunft)

                            if post_it :
                                argt_list.period = argt_list.period + 1
                    else:
                        post_it = False
                else:
                    post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, res_line.ankunft)

                if post_it:

                    artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            pax = res_line.erwachs
                        else:
                            pax = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        pax = res_line.kind1

                    elif argt_line.vt_percnt == 2:
                        pax = res_line.kind2
                    else:
                        pax = 0
                    price =  to_decimal("0")

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                    if reslin_queasy:

                        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                 (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():

                            if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                zwkum = db_session.query(Zwkum).filter(
                                         (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                if zwkum:
                                    price =  to_decimal(ratelocal) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                else:
                                    price =  to_decimal(ratelocal) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                            else:

                                if reslin_queasy.deci1 != 0:
                                    price =  to_decimal(reslin_queasy.deci1)

                                elif reslin_queasy.deci2 != 0:
                                    price =  to_decimal(reslin_queasy.deci2)

                                elif reslin_queasy.deci3 != 0:
                                    price =  to_decimal(reslin_queasy.deci3)
                            fcost = ( to_decimal(price) * to_decimal(pax)) * to_decimal(ex_rate)
                            fcost =  to_decimal(fcost) / to_decimal(fact_art)

                            if price != 0:

                                if argt_line.departement == ba_dept:
                                    genstat.res_deci[6] = genstat.res_deci[6] + fcost
                                else:
                                    genstat.res_deci[5] = genstat.res_deci[5] + fcost

                    if argt_line.betrag > 0:
                        fcost = ( to_decimal(argt_line.betrag) * to_decimal(pax)) * to_decimal(ex_rate)
                        fcost =  to_decimal(fcost) / to_decimal(fact_art)


                    else:

                        zwkum = db_session.query(Zwkum).filter(
                                 (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                        if zwkum:
                            fcost = ( to_decimal(ratelocal) * to_decimal((argt_line.betrag) / to_decimal(100))) * to_decimal(pax) * to_decimal(ex_rate)
                        else:
                            fcost = ( to_decimal(ratelocal) * to_decimal(- to_decimal(argt_line.betrag) / to_decimal(100))) * to_decimal(pax) * to_decimal(ex_rate)
                        fcost =  to_decimal(fcost) / to_decimal(fact_art)

                    if price == 0:

                        if argt_line.departement == ba_dept:
                            genstat.res_deci[6] = genstat.res_deci[6] + fcost
                        else:
                            genstat.res_deci[5] = genstat.res_deci[5] + fcost

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:

                    artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                    fcost = ( to_decimal(fixleist.betrag) * to_decimal(fixleist.number)) * to_decimal(ex_rate)
                    fcost =  to_decimal(fcost) / to_decimal(fact_art)

                    if fixleist.departement == ba_dept:
                        genstat.res_deci[6] = genstat.res_deci[6] + fcost
                    else:
                        genstat.res_deci[5] = genstat.res_deci[5] + fcost
            rate =  to_decimal(res_line.zipreis)
            genstat.logis =  to_decimal(genstat.logis) + to_decimal(lodg_betrag)
            genstat.erwachs = genstat.erwachs + res_line.erwachs
            genstat.gratis = genstat.gratis + res_line.gratis
            genstat.kind1 = genstat.kind1 + res_line.kind1
            genstat.kind2 = genstat.kind2 + res_line.kind2
            genstat.kind3 = genstat.kind3 + res_line.l_zuordnung[3]

            if rate == 0 and res_line.gratis > 0 and res_line.resstatus != 13 and compliment:

                rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"resstatus": [(ne, 12),(ne, 99)],"zipreis": [(gt, 0)],"reslinnr": [(ne, res_line.reslinnr)]})

                if rline:
                    genstat.segmentcode = compliment.segmentcode

            if res_line.kontignr > 0:

                kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)]})

                if kontline:
                    genstat.kontcode = kontline.kontcode

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

            if nation:
                genstat.resident = nation.nationnr


            else:
                genstat.resident = genstat.nationnr

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation2)]})

            if nation:
                genstat.domestic = nation.nationnr


            pass
            pass

    bill_line_obj_list = {}
    bill_line = Bill_line()
    artikel = Artikel()
    for bill_line.bezeich, bill_line.betrag, bill_line.rechnr, bill_line._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel.artart, artikel._recid in db_session.query(Bill_line.bezeich, Bill_line.betrag, Bill_line.rechnr, Bill_line._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 1)).filter(
             (Bill_line.rechnr > 0) & (Bill_line.bill_datum == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
        if bill_line_obj_list.get(bill_line._recid):
            continue
        else:
            bill_line_obj_list[bill_line._recid] = True


        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal(fact)

        bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

        genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnr": [(eq, bill.gastnr)],"zinr": [(eq, bill_line.zinr)]})

        if not genstat:

            genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnr": [(eq, bill.gastnr)]})

        if not genstat:

            rguest = db_session.query(Rguest).filter(
                     (Rguest.gastnr == bill.gastnr)).first()

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, bill.resnr)],"reihenfolge": [(eq, 1)]})

            if not guestseg:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, bill.resnr)]})
            genstat = Genstat()
            db_session.add(genstat)

            genstat.datum = bill_date
            genstat.gastnr = bill.gastnr
            genstat.gastnrmember = bill.gastnr
            genstat.res_logic[0] = False
            genstat.karteityp = rguest.karteityp

            if guestseg:
                genstat.segmentcode = guestseg.segmentcode

            if rguest.karteityp == 0:

                nation = get_cache (Nation, {"kurzbez": [(eq, rguest.land)]})

                if nation:
                    genstat.resident = nation.nationnr

                nation = get_cache (Nation, {"kurzbez": [(eq, rguest.nation2)]})

                if nation:
                    genstat.domestic = nation.nationnr


        genstat.res_deci[0] = genstat.res_deci[0] + lodg_betrag


        pass
    banq_rev()
    reorg_stat()
    correct_depart()

    return generate_output()