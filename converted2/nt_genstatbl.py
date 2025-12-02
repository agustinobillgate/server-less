#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from functions.ratecode_compli import ratecode_compli
from models import Guest, Segment, Res_line, Htparam, Nation, Reservation, Arrangement, Zimmer, Zimkateg, Bill_line, Genstat, Reslin_queasy, Akt_cust, Bediener, Waehrung, Artikel, Argt_line, Kontline, Bill, Guestseg, Guest_pr, Segmentstat, Nationstat, Natstat1, Sources, Landstat, Guestat1, Guestat, Zinrstat, Zkstat

def nt_genstatbl():

    prepare_cache ([Guest, Segment, Res_line, Htparam, Nation, Reservation, Arrangement, Zimmer, Zimkateg, Genstat, Reslin_queasy, Akt_cust, Bediener, Waehrung, Artikel, Argt_line, Kontline, Guestseg, Guest_pr, Segmentstat])

    bill_date:date = None
    price_decimal:int = 0
    invno:int = 0
    purno:int = 0
    lodg_betrag:Decimal = to_decimal("0.0")
    rate:Decimal = to_decimal("0.0")
    ratelocal:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
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
    revtype:List[int] = [5, 1, 2, 3, 5, 3, 4]
    guest = segment = res_line = htparam = nation = reservation = arrangement = zimmer = zimkateg = bill_line = genstat = reslin_queasy = akt_cust = bediener = waehrung = artikel = argt_line = kontline = bill = guestseg = guest_pr = segmentstat = nationstat = natstat1 = sources = landstat = guestat1 = guestat = zinrstat = zkstat = None

    t_list = rguest = compliment = rline = accline = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "rechnr":int, "billno":int, "bezeich":string, "food":Decimal, "bev":Decimal, "other":Decimal, "pay":Decimal, "rmtrans":Decimal})

    Rguest = create_buffer("Rguest",Guest)
    Compliment = create_buffer("Compliment",Segment)
    Rline = create_buffer("Rline",Res_line)
    Accline = create_buffer("Accline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, revtype, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, kontline, bill, guestseg, guest_pr, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat
        nonlocal rguest, compliment, rline, accline


        nonlocal t_list, rguest, compliment, rline, accline
        nonlocal t_list_data

        return {}

    def update_genstat_ratecode(ratecode:string):

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, revtype, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, kontline, bill, guestseg, guest_pr, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat
        nonlocal rguest, compliment, rline, accline


        nonlocal t_list, rguest, compliment, rline, accline
        nonlocal t_list_data

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

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, revtype, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, kontline, bill, guestseg, guest_pr, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat
        nonlocal rguest, compliment, rline, accline


        nonlocal t_list, rguest, compliment, rline, accline
        nonlocal t_list_data

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
            stay = to_int(substring(options, j - 1, 2))
            pay = to_int(substring(options, j + 2 - 1, 2))

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


    def reorg_stat():

        nonlocal bill_date, price_decimal, invno, purno, lodg_betrag, rate, ratelocal, service, vat, argt_betrag, ex_rate, exchg_rate, frate, netto, def_nation, do_it, rm_serv, rm_vat, serv_taxable, foreign_rate, new_contrate, bonus, tot_rmcharge, revtype, guest, segment, res_line, htparam, nation, reservation, arrangement, zimmer, zimkateg, bill_line, genstat, reslin_queasy, akt_cust, bediener, waehrung, artikel, argt_line, kontline, bill, guestseg, guest_pr, segmentstat, nationstat, natstat1, sources, landstat, guestat1, guestat, zinrstat, zkstat
        nonlocal rguest, compliment, rline, accline


        nonlocal t_list, rguest, compliment, rline, accline
        nonlocal t_list_data

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
            db_session.delete(scbuff)
            pass

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

        zinrstat_obj_list = {}
        for zinrstat, zimmer in db_session.query(Zinrstat, Zimmer).join(Zimmer,(Zimmer.zinr == Zinrstat.zinr)).filter(
                 (Zinrstat.datum == bill_date)).order_by(Zinrstat._recid).all():
            if zinrstat_obj_list.get(zinrstat._recid):
                continue
            else:
                zinrstat_obj_list[zinrstat._recid] = True

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

                if genstat.zipreis == 0 and genstat.gratis >= 1:
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


            vat = 0 service == 0

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if arrangement:

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

                if artikel:

                    if rm_serv:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                        if htparam and htparam.fdecimal != 0:
                            service =  to_decimal(htparam.fdecimal) / to_decimal("100")

                    if rm_vat:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                        if htparam and htparam.fdecimal != 0:
                            vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                        if htparam.flogical:
                            vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
                        vat =  to_decimal(round (vat , 2))

            if not issharer:
                zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                if genstat.zipreis == 0:
                    zinrstat.betriebsnr = zinrstat.betriebsnr + 1
            zinrstat.personen = zinrstat.personen + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

            if genstat.zipreis != 0:
                zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(genstat.logis)
                zinrstat.argtumsatz =  to_decimal(zinrstat.argtumsatz) + to_decimal(genstat.ratelocal) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )

            if rm_serv:
                zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(genstat.ratelocal) * to_decimal((1) + to_decimal(vat) + to_decimal(service))
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
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resstatus, Res_line.active_flag).all():

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

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

            genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnrmember": [(eq, res_line.gastnrmember)],"zinr": [(eq, res_line.zinr)]})

            if not genstat:
                genstat = Genstat()
                db_session.add(genstat)

                genstat.datum = bill_date
                genstat.gastnr = res_line.gastnr
                genstat.gastnrmember = res_line.gastnrmember
                genstat.wahrungsnr = res_line.betriebsnr
                genstat.resnr = res_line.resnr
                genstat.res_int[0] = res_line.reslinnr
                genstat.res_int[1] = res_line.reserve_int
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

                if reservation.vesrdepot != "" and not matches(res_line.zimmer_wunsch,r"*voucher*"):
                    genstat.res_char[1] = genstat.res_char[1] + "voucher" + reservation.vesrdepot + ";"

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                if reslin_queasy and reslin_queasy.char2 != "":
                    update_genstat_ratecode(reslin_queasy.char2)

                if nation:
                    genstat.nationnr = nation.nationnr
                else:
                    genstat.nationnr = def_nation

                if res_line.l_zuordnung[0] != 0:
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

                    rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

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
            service =  to_decimal("0")
            vat =  to_decimal("0")

            if rm_serv:

                htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                if htparam and htparam.fdecimal != 0:
                    service =  to_decimal(htparam.fdecimal) / to_decimal("100")

            if rm_vat:

                htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                if htparam and htparam.fdecimal != 0:
                    vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                if htparam.flogical:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
                vat =  to_decimal(round (vat , 2))
            lodg_betrag =  to_decimal(rate) * to_decimal(frate)

            if rate > 0:

                if res_line.reserve_dec != 0:
                    ratelocal =  to_decimal(rate) * to_decimal(res_line.reserve_dec)
                else:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        ratelocal =  to_decimal(rate) * to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                genstat.zipreis =  to_decimal(rate)
                genstat.ratelocal =  to_decimal(ratelocal)

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)
            lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))

            if rm_serv:
                lodg_betrag =  to_decimal(lodg_betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))
            rate =  to_decimal(res_line.zipreis)
            genstat.logis =  to_decimal(genstat.logis) + to_decimal(lodg_betrag)
            genstat.erwachs = genstat.erwachs + res_line.erwachs
            genstat.gratis = genstat.gratis + res_line.gratis
            genstat.kind1 = genstat.kind1 + res_line.kind1
            genstat.kind2 = genstat.kind2 + res_line.kind2
            genstat.kind3 = genstat.kind3 + res_line.l_zuordnung[3]

            if rate == 0 and res_line.gratis > 0 and res_line.resstatus != 13 and compliment:

                rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"resstatus": [(ne, 12)],"zipreis": [(gt, 0)],"reslinnr": [(ne, res_line.reslinnr)]})

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

    bill_line_obj_list = {}
    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == 0) & (Artikel.umsatzart == 1)).filter(
             (Bill_line.rechnr > 0) & (Bill_line.bill_datum == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
        if bill_line_obj_list.get(bill_line._recid):
            continue
        else:
            bill_line_obj_list[bill_line._recid] = True


        service =  to_decimal("0")
        vat =  to_decimal("0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

        if htparam and htparam.fdecimal != 0:
            service =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

        if htparam and htparam.fdecimal != 0:
            vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

        if htparam.flogical:
            vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
        vat = to_decimal(round(vat , 2))
        lodg_betrag =  to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))
        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))

        bill = get_cache (Bill, {"rechnr": [(eq, bill_line.rechnr)]})

        genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnr": [(eq, bill.gastnr)],"zinr": [(eq, bill_line.zinr)]})

        if not genstat:

            genstat = get_cache (Genstat, {"datum": [(eq, bill_date)],"gastnr": [(eq, bill.gastnr)]})

        if not genstat:

            rguest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

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
    reorg_stat()

    return generate_output()