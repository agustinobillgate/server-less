#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Segmentstat, Sources, Htparam, Nationstat, Natstat1, Landstat, Guestat1, Guestat, Zinrstat, Genstat, Zimmer, Zkstat, Arrangement, Artikel

def correct_statistic_btn_okbl(fdate:date, tdate:date, rm_serv:bool, rm_vat:bool):

    prepare_cache ([Htparam, Arrangement, Artikel])

    bill_date:date = None
    curr_i:int = 0
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    fact_scvat:Decimal = to_decimal("0.0")
    segmentstat = sources = htparam = nationstat = natstat1 = landstat = guestat1 = guestat = zinrstat = genstat = zimmer = zkstat = arrangement = artikel = None

    t_segmentstat = t_sources = None

    t_segmentstat_data, T_segmentstat = create_model_like(Segmentstat)
    t_sources_data, T_sources = create_model_like(Sources)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal fdate, tdate, rm_serv, rm_vat


        nonlocal t_segmentstat, t_sources
        nonlocal t_segmentstat_data, t_sources_data

        return {}

    def reorg_stat():

        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal fdate, tdate, rm_serv, rm_vat


        nonlocal t_segmentstat, t_sources
        nonlocal t_segmentstat_data, t_sources_data

        anz:int = 0
        issharer:bool = False
        do_it:bool = True
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
        num_date:int = 0
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
        for bill_date in date_range(fdate,tdate) :

            segmentstat = get_cache (Segmentstat, {"datum": [(eq, bill_date)]})
            while None != segmentstat:

                segbuff = db_session.query(Segbuff).filter(
                             (Segbuff._recid == segmentstat._recid)).first()
                t_segmentstat = T_segmentstat()
                t_segmentstat_data.append(t_segmentstat)

                t_segmentstat.datum = bill_date
                t_segmentstat.segmentcode = segbuff.segmentcode
                t_segmentstat.budlogis =  to_decimal(segbuff.budlogis)
                t_segmentstat.budzimmeranz = segbuff.budzimmeranz
                t_segmentstat.budpersanz = segbuff.budpersanz


                db_session.delete(segbuff)
                pass

                curr_recid = segmentstat._recid
                segmentstat = db_session.query(Segmentstat).filter(
                         (Segmentstat.datum == bill_date) & (Segmentstat._recid > curr_recid)).first()

            nationstat = get_cache (Nationstat, {"datum": [(eq, bill_date)]})
            while None != nationstat:

                natbuff = db_session.query(Natbuff).filter(
                             (Natbuff._recid == nationstat._recid)).first()
                db_session.delete(natbuff)
                pass

                curr_recid = nationstat._recid
                nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.datum == bill_date) & (Nationstat._recid > curr_recid)).first()

            natstat1 = get_cache (Natstat1, {"datum": [(eq, bill_date)]})
            while None != natstat1:

                nsbuff = db_session.query(Nsbuff).filter(
                             (Nsbuff._recid == natstat1._recid)).first()
                db_session.delete(nsbuff)
                pass

                curr_recid = natstat1._recid
                natstat1 = db_session.query(Natstat1).filter(
                         (Natstat1.datum == bill_date) & (Natstat1._recid > curr_recid)).first()

            sources = get_cache (Sources, {"datum": [(eq, bill_date)]})
            while None != sources:

                scbuff = db_session.query(Scbuff).filter(
                             (Scbuff._recid == sources._recid)).first()
                t_sources = T_sources()
                t_sources_data.append(t_sources)

                t_sources.datum = bill_date
                t_sources.source_code = scbuff.source_code
                t_sources.budlogis =  to_decimal(scbuff.budlogis)
                t_sources.budzimmeranz = scbuff.budzimmeranz
                t_sources.budpersanz = scbuff.budpersanz


                db_session.delete(scbuff)
                pass

                curr_recid = sources._recid
                sources = db_session.query(Sources).filter(
                         (Sources.datum == bill_date) & (Sources._recid > curr_recid)).first()

            landstat = get_cache (Landstat, {"datum": [(eq, bill_date)]})
            while None != landstat:

                landbuff = db_session.query(Landbuff).filter(
                             (Landbuff._recid == landstat._recid)).first()
                db_session.delete(landstat)
                pass

                curr_recid = landstat._recid
                landstat = db_session.query(Landstat).filter(
                         (Landstat.datum == bill_date) & (Landstat._recid > curr_recid)).first()

            guestat1 = get_cache (Guestat1, {"datum": [(eq, bill_date)]})
            while None != guestat1:

                gsbuff = db_session.query(Gsbuff).filter(
                             (Gsbuff._recid == guestat1._recid)).first()
                db_session.delete(gsbuff)
                pass

                curr_recid = guestat1._recid
                guestat1 = db_session.query(Guestat1).filter(
                         (Guestat1.datum == bill_date) & (Guestat1._recid > curr_recid)).first()

            guestat = get_cache (Guestat, {"jahr": [(eq, get_year(bill_date))],"monat": [(eq, get_month(bill_date))]})
            while None != guestat:

                gubuff = db_session.query(Gubuff).filter(
                             (Gubuff._recid == guestat._recid)).first()
                db_session.delete(gubuff)
                pass

                curr_recid = guestat._recid
                guestat = db_session.query(Guestat).filter(
                         (Guestat.jahr == get_year(bill_date)) & (Guestat.monat == get_month(bill_date)) & (Guestat._recid > curr_recid)).first()

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, bill_date)]})
            while None != zinrstat:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, zinrstat.zinr)]})

                if zimmer:

                    zibuff = db_session.query(Zibuff).filter(
                             (Zibuff._recid == zinrstat._recid)).first()
                    db_session.delete(zibuff)
                    pass

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                         (Zinrstat.datum == bill_date) & (Zinrstat._recid > curr_recid)).first()

            zkstat = get_cache (Zkstat, {"datum": [(eq, bill_date)]})
            while None != zkstat:

                zkbuff = db_session.query(Zkbuff).filter(
                             (Zkbuff._recid == zkstat._recid)).first()
                zkbuff.personen = 0
                zkbuff.anz_ankunft = 0
                zkbuff.anz_abr = 0
                zkbuff.betriebsnr = 0


                for curr_i in range(1,9 + 1) :
                    zkbuff.arrangement_art[curr_i - 1] = 0
                    zkbuff.anz100argtart[curr_i - 1] = 0


                pass
                pass

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum == bill_date) & (Zkstat._recid > curr_recid)).first()

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == bill_date) & (Genstat.resstatus == 13) & (Genstat.zipreis > 0)).order_by(Genstat._recid).all():

                genbuff = db_session.query(Genbuff).filter(
                         (Genbuff.datum == bill_date) & (Genbuff.zinr == genstat.zinr) & (Genbuff.resstatus == 6)).first()

                if not genbuff:

                    genbuff = db_session.query(Genbuff).filter(
                             (Genbuff._recid == genstat._recid)).first()
                    genbuff.resstatus = 6


                    pass

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == bill_date) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                do_it = True

                if genstat.res_date[1] == bill_date and genstat.resstatus == 8 and genstat.zipreis == 0:

                    genbuff = db_session.query(Genbuff).filter(
                             (Genbuff._recid == genstat._recid)).first()
                    db_session.delete(genbuff)
                    pass
                    do_it = False

                if do_it:

                    segmentstat = get_cache (Segmentstat, {"datum": [(eq, bill_date)],"segmentcode": [(eq, genstat.segmentcode)]})

                    if not segmentstat:
                        segmentstat = Segmentstat()
                        db_session.add(segmentstat)

                        segmentstat.datum = bill_date
                        segmentstat.segmentcode = genstat.segmentcode


                    issharer = genstat.resstatus == 13

                    if not issharer:
                        segmentstat.zimmeranz = segmentstat.zimmeranz + 1

                        if genstat.zipreis == 0 and (genstat.gratis > 0):
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
                        num_date = (genstat.res_date[1] - genstat.res_date[0]).days
                        nationstat.dlogkind1 = nationstat.dlogkind1 + num_date
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

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                    if arrangement:

                        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

                        if artikel:
                            service, vat, vat2, fact_scvat = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))

                    if not issharer:
                        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                        if genstat.zipreis == 0:
                            zinrstat.betriebsnr = zinrstat.betriebsnr + 1
                    zinrstat.personen = zinrstat.personen + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

                    if genstat.ratelocal != 0:
                        zinrstat.logisumsatz =  to_decimal(zinrstat.logisumsatz) + to_decimal(genstat.logis)
                        zinrstat.argtumsatz =  to_decimal(zinrstat.argtumsatz) + to_decimal(genstat.ratelocal) / to_decimal(fact_scvat)

                    if rm_serv:
                        zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(genstat.ratelocal) * to_decimal(fact_scvat)
                    else:
                        zinrstat.gesamtumsatz =  to_decimal(zinrstat.gesamtumsatz) + to_decimal(genstat.ratelocal)

                    zkstat = get_cache (Zkstat, {"zikatnr": [(eq, genstat.zikatnr)],"datum": [(eq, bill_date)]})

                    if not zkstat:
                        zkstat = Zkstat()
                        db_session.add(zkstat)

                        zkstat.datum = bill_date
                        zkstat.zikatnr = genstat.zikatnr


                    anz = 0

                    for zimbuff in db_session.query(Zimbuff).filter(
                             (Zimbuff.zikatnr == genstat.zikatnr) & (Zimbuff.sleeping)).order_by(Zimbuff._recid).all():
                        anz = anz + 1

                    if not issharer:
                        zkstat.zimmeranz = zkstat.zimmeranz + 1

                        if genstat.zipreis == 0:
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

            for t_segmentstat in query(t_segmentstat_data):

                segmentstat = get_cache (Segmentstat, {"datum": [(eq, t_segmentstat.datum)],"segmentcode": [(eq, t_segmentstat.segmentcode)]})

                if not segmentstat:
                    segmentstat = Segmentstat()
                    db_session.add(segmentstat)

                    segmentstat.datum = t_segmentstat.datum
                    segmentstat.segmentcode = t_segmentstat.segmentcode


                segmentstat.budlogis =  to_decimal(t_segmentstat.budlogis)
                segmentstat.budzimmeranz = t_segmentstat.budzimmeranz
                segmentstat.budpersanz = t_segmentstat.budpersanz

            for t_sources in query(t_sources_data):

                sources = get_cache (Sources, {"datum": [(eq, t_sources.datum)],"source_code": [(eq, t_sources.source_code)]})

                if not sources:
                    sources = Sources()
                    db_session.add(sources)

                    sources.datum = t_sources.datum
                    sources.source_code = t_sources.source_code


                sources.budlogis =  to_decimal(t_sources.budlogis)
                sources.budzimmeranz = t_sources.budzimmeranz
                sources.budpersanz = t_sources.budpersanz


    def reorg_guestat():

        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal fdate, tdate, rm_serv, rm_vat


        nonlocal t_segmentstat, t_sources
        nonlocal t_segmentstat_data, t_sources_data

        dd:date = None
        mm:int = 0
        yy:int = 0
        genbuff = None
        Genbuff =  create_buffer("Genbuff",Genstat)
        for mm in range(get_month(fdate),get_month(tdate)  + 1) :

            for genbuff in db_session.query(Genbuff).filter(
                     (get_year(Genbuff.datum) == get_year(fdate)) & (get_month(Genbuff.datum) == mm) & (Genbuff.zinr != "")).order_by(Genbuff._recid).all():

                guestat = get_cache (Guestat, {"monat": [(eq, mm)],"jahr": [(eq, get_year(fdate))],"gastnr": [(eq, genbuff.gastnr)]})

                if not guestat:
                    guestat = Guestat()
                    db_session.add(guestat)

                    guestat.monat = get_month(bill_date)
                    guestat.jahr = get_year(bill_date)
                    guestat.gastnr = genbuff.gastnr

                if genbuff.resstatus != 13:
                    guestat.room_nights = guestat.room_nights + 1
                pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    rm_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = htparam.flogical
    reorg_stat()
    reorg_guestat()

    return generate_output()