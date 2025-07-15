from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from models import Guest, Segment, Res_line, Htparam, Nation, Reservation, Arrangement, Zimmer, Zimkateg, Bill_line, Genstat, Reslin_queasy, Akt_cust, Bediener, Waehrung, Artikel, Argt_line, Fixleist, Kontline, Bill, Guestseg, Segmentstat, Nationstat, Natstat1, Sources, Landstat, Guestat1, Guestat, Zinrstat, Zkstat, H_artikel, H_bill_line

def nt_genstat():
    bill_date:date = None
    price_decimal:int = 0
    invno:int = 0
    purno:int = 0
    lodg_betrag:decimal = to_decimal("0.0")
    rate:decimal = to_decimal("0.0")
    ratelocal:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    vat2_art:decimal = to_decimal("0.0")
    fact_art:decimal = to_decimal("0.0")
    argt_betrag:decimal = to_decimal("0.0")
    ex_rate:decimal = to_decimal("0.0")
    exchg_rate:decimal = 1
    frate:decimal = 1
    netto:decimal = to_decimal("0.0")
    def_nation:int = 0
    do_it:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    serv_taxable:bool = False
    foreign_rate:bool = False
    new_contrate:bool = False
    bonus:bool = False
    tot_rmcharge:decimal = to_decimal("0.0")
    gastmemberno:int = 0
    revtype:List[int] = [5, 1, 2, 3, 5, 3, 4]
    fb_dept:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    post_it:bool = False
    fcost:decimal = to_decimal("0.0")
    vat_art:decimal = to_decimal("0.0")
    service_art:decimal = to_decimal("0.0")
    gross_argt:decimal = to_decimal("0.0")
    net_argt:decimal = to_decimal("0.0")
    guest = segment = res_line = htparam = nation = reservation = arrangement = zimmer = zimkateg = bill_line = genstat = reslin_queasy = akt_cust = bediener = waehrung = artikel = argt_line = fixleist = kontline = bill = guestseg = segmentstat = nationstat = natstat1 = sources = landstat = guestat1 = guestat = zinrstat = zkstat = h_artikel = h_bill_line = None

    t_list = rguest = compliment = rline = mguest = dummyguest = tguest = accline = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "rechnr":int, "billno":int, "bezeich":str, "food":decimal, "bev":decimal, "other":decimal, "pay":decimal, "rmtrans":decimal})

    Rguest = create_buffer("Rguest",Guest)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)
    Mguest = create_buffer("Mguest",Guest)
    Dummyguest = create_buffer("Dummyguest",Guest)
    Tguest = create_buffer("Tguest",Guest)
    Accline = create_buffer("Accline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

        return {}

    def update_genstat_ratecode(ratecode:str):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

        str:str = ""
        zwstr:str = ""
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

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

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

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

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

            segbuff = db_session.query(Segbuff).filter(
                     (Segbuff._recid == segmentstat._recid)).first()
            segbuff.logis =  to_decimal("0")
            segbuff.zimmeranz = 0
            segbuff.persanz = 0
            segbuff.kind1 = 0
            segbuff.kind2 = 0
            segbuff.gratis = 0
            segbuff.betriebsnr = 0

        for nationstat in db_session.query(Nationstat).filter(
                 (Nationstat.datum == bill_date)).order_by(Nationstat._recid).all():

            natbuff = db_session.query(Natbuff).filter(
                     (Natbuff._recid == nationstat._recid)).first()
            db_session.delete(natbuff)
            pass

        for natstat1 in db_session.query(Natstat1).filter(
                 (Natstat1.datum == bill_date)).order_by(Natstat1._recid).all():

            nsbuff = db_session.query(Nsbuff).filter(
                     (Nsbuff._recid == natstat1._recid)).first()
            db_session.delete(nsbuff)
            pass

        for sources in db_session.query(Sources).filter(
                 (Sources.datum == bill_date)).order_by(Sources._recid).all():

            scbuff = db_session.query(Scbuff).filter(
                     (Scbuff._recid == sources._recid)).first()
            scbuff.logis =  to_decimal("0")
            scbuff.zimmeranz = 0
            scbuff.persanz = 0
            scbuff.betriebsnr = 0

        for landstat in db_session.query(Landstat).filter(
                 (Landstat.datum == bill_date)).order_by(Landstat._recid).all():

            landbuff = db_session.query(Landbuff).filter(
                     (Landbuff._recid == landstat._recid)).first()
            db_session.delete(landstat)
            pass

        for guestat1 in db_session.query(Guestat1).filter(
                 (Guestat1.datum == bill_date)).order_by(Guestat1._recid).all():

            gsbuff = db_session.query(Gsbuff).filter(
                     (Gsbuff._recid == guestat1._recid)).first()
            db_session.delete(gsbuff)
            pass

        for guestat in db_session.query(Guestat).filter(
                 (Guestat.jahr == get_year(bill_date)) & (Guestat.monat == get_month(bill_date))).order_by(Guestat._recid).all():

            gubuff = db_session.query(Gubuff).filter(
                     (Gubuff._recid == guestat._recid)).first()
            db_session.delete(gubuff)
            pass

        zinrstat_obj_list = []
        for zinrstat, zimmer in db_session.query(Zinrstat, Zimmer).join(Zimmer,(Zimmer.zinr == Zinrstat.zinr)).filter(
                 (Zinrstat.datum == bill_date)).order_by(Zinrstat._recid).all():
            if zinrstat._recid in zinrstat_obj_list:
                continue
            else:
                zinrstat_obj_list.append(zinrstat._recid)

            zibuff = db_session.query(Zibuff).filter(
                     (Zibuff._recid == zinrstat._recid)).first()
            db_session.delete(zibuff)
            pass

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == bill_date)).order_by(Zkstat._recid).all():

            zkbuff = db_session.query(Zkbuff).filter(
                     (Zkbuff._recid == zkstat._recid)).first()
            db_session.delete(zkbuff)
            pass

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            anz = 0

            for zimbuff in db_session.query(Zimbuff).filter(
                     (Zimbuff.zikatnr == zimkateg.zikatnr) & (Zimbuff.sleeping)).order_by(Zimbuff._recid).all():
                anz = anz + 1

            zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.datum == bill_date) & (Zkstat.zikatnr == zimkateg.zikatnr)).first()

            if not zkstat:
                zkstat = Zkstat()
                db_session.add(zkstat)

                zkstat.datum = bill_date
                zkstat.zikatnr = zimkateg.zikatnr


            zkstat.anz100 = anz

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum == bill_date) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            segmentstat = db_session.query(Segmentstat).filter(
                     (Segmentstat.datum == bill_date) & (Segmentstat.segmentcode == genstat.segmentcode)).first()

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

            if genstat.domestic != 0:

                nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.datum == bill_date) & (Nationstat.nationnr == genstat.domestic)).first()

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

            nationstat = db_session.query(Nationstat).filter(
                     (Nationstat.datum == bill_date) & (Nationstat.nationnr == genstat.nationnr)).first()

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

            natstat1 = db_session.query(Natstat1).filter(
                     (Natstat1.datum == bill_date) & (Natstat1.nationnr == genstat.nationnr)).first()

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

            if genstat.domestic != 0:

                natstat1 = db_session.query(Natstat1).filter(
                         (Natstat1.datum == bill_date) & (Natstat1.nationnr == genstat.domestic)).first()

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

            sources = db_session.query(Sources).filter(
                     (Sources.datum == bill_date) & (Sources.source_code == genstat.source)).first()

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

            landstat = db_session.query(Landstat).filter(
                     (Landstat.datum == bill_date) & (Landstat.nationnr == genstat.resident)).first()

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

            guestat1 = db_session.query(Guestat1).filter(
                     (Guestat1.datum == bill_date) & (Guestat1.gastnr == genstat.gastnr)).first()

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

            zinrstat = db_session.query(Zinrstat).filter(
                     (Zinrstat.datum == bill_date) & (Zinrstat.zinr == genstat.zinr)).first()

            if not zinrstat:
                zinrstat = Zinrstat()
                db_session.add(zinrstat)

                zinrstat.datum = bill_date
                zinrstat.zinr = genstat.zinr


            vat = 0 service == 0

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == genstat.argt)).first()

            if arrangement:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()

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

            zkstat = db_session.query(Zkstat).filter(
                     (Zkstat.zikatnr == genstat.zikatnr) & (Zkstat.datum == bill_date)).first()

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

        for genbuff in db_session.query(Genbuff).filter(
                 (get_year(Genbuff.datum) == get_year(bill_date)) & (get_month(Genbuff.datum) == get_month(bill_date)) & (Genbuff.zinr != "")).order_by(Genbuff._recid).all():

            guestat = db_session.query(Guestat).filter(
                     (Guestat.monat == get_month(bill_date)) & (Guestat.jahr == get_year(bill_date)) & (Guestat.gastnr == genbuff.gastnr)).first()

            if not guestat:
                guestat = Guestat()
                db_session.add(guestat)

                guestat.monat = get_month(bill_date)
                guestat.jahr = get_year(bill_date)
                guestat.gastnr = genbuff.gastnr

            if genbuff.resstatus == 6 or (genbuff.res_date[0] == genbuff.res_date[1] and genbuff.resstatus != 13):
                guestat.room_nights = guestat.room_nights + 1


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

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
                delta = lfakt - res_line.ankunft

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


    def banq_rev():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, vat2, fact, vat2_art, fact_art, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, gastmemberno, revtype, fb_dept, bfast_art, lunch_art, dinner_art, lundin_art, post_it, fcost, vat_art, service_art, gross_argt, net_argt, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, fixleist, kontline, bill, guestseg, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat, h_artikel, h_bill_line
        nonlocal rguest, compliment, rline, mguest, dummyguest, tguest, accline


        nonlocal t_list, rguest, compliment, rline, mguest, dummyguest, tguest, accline
        nonlocal t_list_list

        ba_dept:int = 0
        ba_betrag:decimal = to_decimal("0.0")
        invoice_no:int = 0
        i:int = 0
        t_bill_line = None
        artlist = None
        T_bill_line =  create_buffer("T_bill_line",Bill_line)
        Artlist =  create_buffer("Artlist",Artikel)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 900)).first()
        ba_dept = htparam.finteger

        t_bill_line_obj_list = []
        for t_bill_line, artikel in db_session.query(T_bill_line, Artikel).join(Artikel,(Artikel.artnr == T_bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 0)).filter(
                 (T_bill_line.rechnr > 0) & (T_bill_line.bill_datum == bill_date) & (T_bill_line.zeit >= 0) & (T_bill_line.departement == ba_dept)).order_by(T_bill_line._recid).all():
            if t_bill_line._recid in t_bill_line_obj_list:
                continue
            else:
                t_bill_line_obj_list.append(t_bill_line._recid)


            service =  to_decimal("0")
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")
            fact =  to_decimal("0")
            ba_betrag =  to_decimal("0")

            if artikel.artart == 1:
                for i in range(1,len(t_bill_line.bezeich)  + 1) :

                    if substring(t_bill_line.bezeich, i - 1, 1) == ("*").lower() :
                        invoice_no = to_int(substring(t_bill_line.bezeich, i + 1 - 1, len(t_bill_line.bezeich)))


                        i = 999

                h_bill_line_obj_list = []
                for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == ba_dept) & (H_artikel.artart == 0)).filter(
                         (H_bill_line.rechnr == invoice_no) & (H_bill_line.departement == ba_dept) & (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line._recid).all():
                    if h_bill_line._recid in h_bill_line_obj_list:
                        continue
                    else:
                        h_bill_line_obj_list.append(h_bill_line._recid)


                    service =  to_decimal("0")
                    vat =  to_decimal("0")
                    vat2 =  to_decimal("0")
                    fact =  to_decimal("0")

                    artlist = db_session.query(Artlist).filter(
                             (Artlist.artnr == h_artikel.artnrfront) & (Artlist.departement == h_artikel.departement)).first()

                    if artlist:
                        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artlist.artnr, artlist.departement, bill_date))
                        ba_betrag =  to_decimal(ba_betrag) + to_decimal((h_bill_line.betrag) / to_decimal(fact) )


            else:
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                ba_betrag =  to_decimal(t_bill_line.betrag) / to_decimal(fact)

            bill = db_session.query(Bill).filter(
                     (Bill.rechnr == t_bill_line.rechnr)).first()

            genstat = db_session.query(Genstat).filter(
                     (Genstat.datum == bill_date) & (Genstat.gastnr == bill.gastnr)).first()

            if not genstat:
                genstat = Genstat()
                db_session.add(genstat)

                genstat.datum = bill_date
                genstat.gastnr = bill.gastnr
                genstat.gastnrmember = bill.gastnr


            genstat.res_deci[6] = genstat.res_deci[6] + ba_betrag


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
             (Htparam.paramnr == 126)).first()
    fb_dept = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 125)).first()
    bfast_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 227)).first()
    lunch_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 228)).first()
    dinner_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 229)).first()
    lundin_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    rm_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 153)).first()

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == htparam.fchar)).first()

    if nation:
        def_nation = nation.nationnr

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 377)).first()

    if htparam.finteger != 0:

        compliment = db_session.query(Compliment).filter(
                 (Compliment.segmentcode == htparam.finteger)).first()

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resstatus, Res_line.active_flag).all():

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == res_line.zinr)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        rguest = db_session.query(Rguest).filter(
                 (Rguest.gastnr == res_line.gastnr)).first()

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == guest.nation1)).first()

        segment = db_session.query(Segment).filter(
                 (Segment.segmentcode == reservation.segmentcode)).first()
        do_it = False
        tot_rmcharge =  to_decimal("0")

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == bill_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
            do_it = None != bill_line

        elif res_line.active_flag == 2 and res_line.ankunft < bill_date:

            if res_line.zimmerfix:
                do_it = False
            else:

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == bill_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
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

            genstat = db_session.query(Genstat).filter(
                     (Genstat.datum == bill_date) & (Genstat.gastnrmember == res_line.gastnrmember) & (Genstat.zinr == res_line.zinr)).first()

            if genstat:

                mguest = db_session.query(Mguest).order_by(Mguest._recid.desc()).first()
                gastmemberno = mguest.gastnr + 1

                tguest = db_session.query(Tguest).filter(
                         (Tguest.gastnr == res_line.gastnrmember)).first()

                if tguest:
                    dummyguest = Dummyguest()
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

            if reservation.kontakt_nr != 0:
                genstat.res_char[3] = to_string(reservation.kontakt_nr)

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= bill_date) & (Reslin_queasy.date2 >= bill_date)).first()

            if reslin_queasy and reslin_queasy.char2 != "":
                update_genstat_ratecode(reslin_queasy.char2)

            if reservation.vesrdepot != "" and not re.match(r".*voucher.*",res_line.zimmer_wunsch, re.IGNORECASE):
                genstat.res_char[1] = genstat.res_char[1] + "voucher" + reservation.vesrdepot + ";"

            if nation:
                genstat.nationnr = nation.nationnr
            else:
                genstat.nationnr = def_nation

            if res_line.l_zuordnung[0] != 0 and res_line.l_zuordnung[0] != res_line.zikatnr:
                genstat.res_char[1] = genstat.res_char[1] +\
                    "RmUpgrade" + to_string(res_line.l_zuordnung[0]) + ";"

            accline = db_session.query(Accline).filter(
                         (Accline.resnr == res_line.resnr) & (Accline.kontakt_nr == res_line.reslinnr) & (Accline.l_zuordnung[inc_value(2)] == 1)).first()

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

            akt_cust = db_session.query(Akt_cust).filter(
                         (Akt_cust.gastnr == res_line.gastnr)).first()

            if akt_cust:

                bediener = db_session.query(Bediener).filter(
                             (Bediener.userinit == akt_cust.userinit)).first()

            if not akt_cust or not bediener:

                rguest = db_session.query(Rguest).filter(
                             (Rguest.gastnr == res_line.gastnr)).first()

                if rguest.phonetik3 != "":

                    bediener = db_session.query(Bediener).filter(
                                 (Bediener.userinit == rguest.phonetik3)).first()

            if bediener:
                genstat.res_int[5] = bediener.nr


            bonus = check_bonus()
            genstat.res_logic[2] = bonus

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            rate =  to_decimal(res_line.zipreis)

            if bonus:
                rate =  to_decimal("0")

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()
            service, vat, vat2, fact = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))
            lodg_betrag =  to_decimal(rate) * to_decimal(frate)
            gross_argt =  to_decimal("0")
            net_argt =  to_decimal("0")
            ex_rate =  to_decimal("1")

            if lodg_betrag > 0:

                if res_line.reserve_dec != 0:
                    ratelocal =  to_decimal(rate) * to_decimal(res_line.reserve_dec)
                else:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                    if waehrung:
                        ratelocal =  to_decimal(rate) * to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                genstat.zipreis =  to_decimal(rate)
                genstat.ratelocal =  to_decimal(ratelocal)

                argt_line_obj_list = []
                for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                    if argt_line._recid in argt_line_obj_list:
                        continue
                    else:
                        argt_line_obj_list.append(argt_line._recid)


                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                    argt_betrag =  to_decimal(argt_betrag) * to_decimal(ex_rate)
                    gross_argt =  to_decimal(gross_argt) + to_decimal(argt_betrag)
                    argt_betrag =  to_decimal(argt_betrag) / to_decimal(fact_art)
                    net_argt =  to_decimal(net_argt) + to_decimal(argt_betrag)

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        genstat.res_deci[1] = genstat.res_deci[1] + argt_betrag

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        genstat.res_deci[2] = genstat.res_deci[2] + argt_betrag

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        genstat.res_deci[3] = genstat.res_deci[3] + argt_betrag

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        genstat.res_deci[2] = genstat.res_deci[2] + argt_betrag
                    else:
                        genstat.res_deci[4] = genstat.res_deci[4] + argt_betrag

                if rm_vat:
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(gross_argt)
                    lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)


                else:
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(net_argt)

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == fixleist.artnr) & (Artikel.departement == fixleist.departement)).first()
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                    fcost = ( to_decimal(fixleist.betrag) * to_decimal(fixleist.number)) * to_decimal(ex_rate)
                    fcost =  to_decimal(fcost) / to_decimal(fact_art)


                    genstat.res_deci[5] = genstat.res_deci[5] + fcost
            rate =  to_decimal(res_line.zipreis)
            genstat.logis =  to_decimal(genstat.logis) + to_decimal(lodg_betrag)
            genstat.erwachs = genstat.erwachs + res_line.erwachs
            genstat.gratis = genstat.gratis + res_line.gratis
            genstat.kind1 = genstat.kind1 + res_line.kind1
            genstat.kind2 = genstat.kind2 + res_line.kind2
            genstat.kind3 = genstat.kind3 + res_line.l_zuordnung[3]

            if rate == 0 and res_line.gratis > 0 and res_line.resstatus != 13 and compliment:

                rline = db_session.query(Rline).filter(
                         (Rline.resnr == res_line.resnr) & (Rline.resstatus != 12) & (Rline.resstatus != 99) & (Rline.zipreis > 0) & (Rline.reslinnr != res_line.reslinnr)).first()

                if rline:
                    genstat.segmentcode = compliment.segmentcode

            if res_line.kontignr > 0:

                kontline = db_session.query(Kontline).filter(
                         (Kontline.kontignr == res_line.kontignr)).first()

                if kontline:
                    genstat.kontcode = kontline.kontcode

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.land)).first()

            if nation:
                genstat.resident = nation.nationnr


            else:
                genstat.resident = genstat.nationnr

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guest.nation2)).first()

            if nation:
                genstat.domestic = nation.nationnr


            pass

    bill_line_obj_list = []
    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 1)).filter(
             (Bill_line.rechnr > 0) & (Bill_line.bill_datum == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
        if bill_line._recid in bill_line_obj_list:
            continue
        else:
            bill_line_obj_list.append(bill_line._recid)


        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal(fact)

        bill = db_session.query(Bill).filter(
                 (Bill.rechnr == bill_line.rechnr)).first()

        genstat = db_session.query(Genstat).filter(
                 (Genstat.datum == bill_date) & (Genstat.gastnr == bill.gastnr) & (Genstat.zinr == bill_line.zinr)).first()

        if not genstat:

            genstat = db_session.query(Genstat).filter(
                     (Genstat.datum == bill_date) & (Genstat.gastnr == bill.gastnr)).first()

        if not genstat:

            rguest = db_session.query(Rguest).filter(
                     (Rguest.gastnr == bill.gastnr)).first()

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == bill.resnr) & (Guestseg.reihenfolge == 1)).first()

            if not guestseg:

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == bill.resnr)).first()
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

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == rguest.land)).first()

                if nation:
                    genstat.resident = nation.nationnr

                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == rguest.nation2)).first()

                if nation:
                    genstat.domestic = nation.nationnr


        genstat.res_deci[0] = genstat.res_deci[0] + lodg_betrag


    banq_rev()
    reorg_stat()

    return generate_output()