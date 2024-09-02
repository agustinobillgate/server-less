from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Segmentstat, Sources, Htparam, Nationstat, Natstat1, Landstat, Guestat1, Guestat, Zinrstat, Genstat, Zimmer, Zkstat, Arrangement, Artikel

def correct_statistic_btn_okbl(fdate:date, tdate:date, rm_serv:bool, rm_vat:bool):
    bill_date:date = None
    curr_i:int = 0
    vat:decimal = 0
    vat2:decimal = 0
    service:decimal = 0
    fact_scvat:decimal = 0
    segmentstat = sources = htparam = nationstat = natstat1 = landstat = guestat1 = guestat = zinrstat = genstat = zimmer = zkstat = arrangement = artikel = None

    t_segmentstat = t_sources = segbuff = natbuff = nsbuff = scbuff = landbuff = gsbuff = gubuff = zibuff = genbuff = zimbuff = zkbuff = None

    t_segmentstat_list, T_segmentstat = create_model_like(Segmentstat)
    t_sources_list, T_sources = create_model_like(Sources)

    Segbuff = Segmentstat
    Natbuff = Nationstat
    Nsbuff = Natstat1
    Scbuff = Sources
    Landbuff = Landstat
    Gsbuff = Guestat1
    Gubuff = Guestat
    Zibuff = Zinrstat
    Genbuff = Genstat
    Zimbuff = Zimmer
    Zkbuff = Zkstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff


        nonlocal t_segmentstat, t_sources, segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff
        nonlocal t_segmentstat_list, t_sources_list
        return {}

    def reorg_stat():

        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff


        nonlocal t_segmentstat, t_sources, segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff
        nonlocal t_segmentstat_list, t_sources_list

        anz:int = 0
        issharer:bool = False
        do_it:bool = True
        Segbuff = Segmentstat
        Natbuff = Nationstat
        Nsbuff = Natstat1
        Scbuff = Sources
        Landbuff = Landstat
        Gsbuff = Guestat1
        Gubuff = Guestat
        Zibuff = Zinrstat
        Genbuff = Genstat
        Zimbuff = Zimmer
        Zkbuff = Zkstat
        for bill_date in range(fdate,tdate + 1) :

            segmentstat = db_session.query(Segmentstat).filter(
                    (Segmentstat.datum == bill_date)).first()
            while None != segmentstat:

                segbuff = db_session.query(Segbuff).filter(
                            (Segbuff._recid == segmentstat._recid)).first()
                t_segmentstat = T_segmentstat()
                t_segmentstat_list.append(t_segmentstat)

                t_segmentstat.datum = bill_date
                t_segmentstat.segmentcode = segbuff.segmentcode
                t_segmentstat.budlogis = segbuff.budlogis
                t_segmentstat.budzimmeranz = segbuff.budzimmeranz
                t_segmentstat.budpersanz = segbuff.budpersanz


                db_session.delete(segbuff)

                segmentstat = db_session.query(Segmentstat).filter(
                        (Segmentstat.datum == bill_date)).first()

            nationstat = db_session.query(Nationstat).filter(
                    (Nationstat.datum == bill_date)).first()
            while None != nationstat:

                natbuff = db_session.query(Natbuff).filter(
                            (Natbuff._recid == nationstat._recid)).first()
                db_session.delete(natbuff)

                nationstat = db_session.query(Nationstat).filter(
                        (Nationstat.datum == bill_date)).first()

            natstat1 = db_session.query(Natstat1).filter(
                    (Natstat1.datum == bill_date)).first()
            while None != natstat1:

                nsbuff = db_session.query(Nsbuff).filter(
                            (Nsbuff._recid == natstat1._recid)).first()
                db_session.delete(nsbuff)

                natstat1 = db_session.query(Natstat1).filter(
                        (Natstat1.datum == bill_date)).first()

            sources = db_session.query(Sources).filter(
                    (Sources.datum == bill_date)).first()
            while None != sources:

                scbuff = db_session.query(Scbuff).filter(
                            (Scbuff._recid == sources._recid)).first()
                t_sources = T_sources()
                t_sources_list.append(t_sources)

                t_sources.datum = bill_date
                t_sources.source_code = scbuff.source_code
                t_sources.budlogis = scbuff.budlogis
                t_sources.budzimmeranz = scbuff.budzimmeranz
                t_sources.budpersanz = scbuff.budpersanz


                db_session.delete(scbuff)

                sources = db_session.query(Sources).filter(
                        (Sources.datum == bill_date)).first()

            landstat = db_session.query(Landstat).filter(
                    (Landstat.datum == bill_date)).first()
            while None != landstat:

                landbuff = db_session.query(Landbuff).filter(
                            (Landbuff._recid == landstat._recid)).first()
                db_session.delete(landstat)

                landstat = db_session.query(Landstat).filter(
                        (Landstat.datum == bill_date)).first()

            guestat1 = db_session.query(Guestat1).filter(
                    (Guestat1.datum == bill_date)).first()
            while None != guestat1:

                gsbuff = db_session.query(Gsbuff).filter(
                            (Gsbuff._recid == guestat1._recid)).first()
                db_session.delete(gsbuff)

                guestat1 = db_session.query(Guestat1).filter(
                        (Guestat1.datum == bill_date)).first()

            guestat = db_session.query(Guestat).filter(
                    (Guestat.jahr == get_year(bill_date)) &  (Guestat.monat == get_month(bill_date))).first()
            while None != guestat:

                gubuff = db_session.query(Gubuff).filter(
                            (Gubuff._recid == guestat._recid)).first()
                db_session.delete(gubuff)

                guestat = db_session.query(Guestat).filter(
                        (Guestat.jahr == get_year(bill_date)) &  (Guestat.monat == get_month(bill_date))).first()

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == bill_date)).first()
            while None != zinrstat:

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == zinrstat.zinr)).first()

                if zimmer:

                    zibuff = db_session.query(Zibuff).filter(
                            (Zibuff._recid == zinrstat._recid)).first()
                    db_session.delete(zibuff)


                zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum == bill_date)).first()

            zkstat = db_session.query(Zkstat).filter(
                    (Zkstat.datum == bill_date)).first()
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

                zkbuff = db_session.query(Zkbuff).first()

                zkstat = db_session.query(Zkstat).filter(
                        (Zkstat.datum == bill_date)).first()

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == bill_date) &  (Genstat.resstatus == 13) &  (Genstat.zipreis > 0)).all():

                genbuff = db_session.query(Genbuff).filter(
                        (Genbuff.datum == bill_date) &  (Genbuff.zinr == genstat.zinr) &  (Genbuff.resstatus == 6)).first()

                if not genbuff:

                    genbuff = db_session.query(Genbuff).filter(
                            (Genbuff._recid == genstat._recid)).first()
                    genbuff.resstatus = 6

                    genbuff = db_session.query(Genbuff).first()

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == bill_date) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                do_it = True

                if genstat.res_date[1] == bill_date and genstat.resstatus == 8 and genstat.zipreis == 0:

                    genbuff = db_session.query(Genbuff).filter(
                            (Genbuff._recid == genstat._recid)).first()
                    db_session.delete(genbuff)

                    do_it = False

                if do_it:

                    segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == bill_date) &  (Segmentstat.segmentcode == genstat.segmentcode)).first()

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
                    segmentstat.logis = segmentstat.logis + genstat.logis

                    segmentstat = db_session.query(Segmentstat).first()

                    if genstat.domestic != 0:

                        nationstat = db_session.query(Nationstat).filter(
                                (Nationstat.datum == bill_date) &  (Nationstat.nationnr == genstat.domestic)).first()

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

                        nationstat = db_session.query(Nationstat).first()

                    nationstat = db_session.query(Nationstat).filter(
                            (Nationstat.datum == bill_date) &  (Nationstat.nationnr == genstat.nationnr)).first()

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

                    nationstat = db_session.query(Nationstat).first()

                    natstat1 = db_session.query(Natstat1).filter(
                            (Natstat1.datum == bill_date) &  (Natstat1.nationnr == genstat.nationnr)).first()

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
                        natstat1.logis = natstat1.logis + genstat.logis

                    natstat1 = db_session.query(Natstat1).first()

                    if genstat.domestic != 0:

                        natstat1 = db_session.query(Natstat1).filter(
                                (Natstat1.datum == bill_date) &  (Natstat1.nationnr == genstat.domestic)).first()

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
                            natstat1.logis = natstat1.logis + genstat.logis

                        natstat1 = db_session.query(Natstat1).first()

                    sources = db_session.query(Sources).filter(
                            (Sources.datum == bill_date) &  (Sources.source_code == genstat.SOURCE)).first()

                    if not sources:
                        sources = Sources()
                        db_session.add(sources)

                        sources.datum = bill_date
                        sources.source_code = genstat.SOURCE

                    if not issharer:
                        sources.zimmeranz = sources.zimmeranz + 1

                        if genstat.zipreis == 0:
                            sources.betriebsnr = sources.betriebsnr + 1
                    sources.persanz = sources.persanz + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

                    if genstat.zipreis != 0:
                        sources.logis = sources.logis + genstat.logis

                    sources = db_session.query(Sources).first()

                    landstat = db_session.query(Landstat).filter(
                            (Landstat.datum == bill_date) &  (Landstat.nationnr == genstat.resident)).first()

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
                        landstat.logis = landstat.logis + genstat.logis

                    landstat = db_session.query(Landstat).first()

                    guestat1 = db_session.query(Guestat1).filter(
                            (Guestat1.datum == bill_date) &  (Guestat1.gastnr == genstat.gastnr)).first()

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
                        guestat1.logis = guestat1.logis + genstat.logis

                    guestat1 = db_session.query(Guestat1).first()

                    zinrstat = db_session.query(Zinrstat).filter(
                            (Zinrstat.datum == bill_date) &  (Zinrstat.zinr == genstat.zinr)).first()

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = bill_date
                        zinrstat.zinr = genstat.zinr

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == genstat.argt)).first()

                    if arrangement:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == arrangement.artnr_logis) &  (Artikel.departement == 0)).first()

                        if artikel:
                            service, vat, vat2, fact_scvat = get_output(calc_servtaxesbl(2, artikel.artnr, artikel.departement, bill_date))

                    if not issharer:
                        zinrstat.zimmeranz = zinrstat.zimmeranz + 1

                        if genstat.zipreis == 0:
                            zinrstat.betriebsnr = zinrstat.betriebsnr + 1
                    zinrstat.personen = zinrstat.personen + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3

                    if genstat.rate != 0:
                        zinrstat.logisumsatz = zinrstat.logisumsatz + genstat.logis
                        zinrstat.argtumsatz = zinrstat.argtumsatz + genstat.rateLocal / fact_scvat

                    if rm_serv:
                        zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal * fact_scvat
                    else:
                        zinrstat.gesamtumsatz = zinrstat.gesamtumsatz + genstat.rateLocal

                    zkstat = db_session.query(Zkstat).filter(
                            (Zkstat.zikatnr == genstat.zikatnr) &  (Zkstat.datum == bill_date)).first()

                    if not zkstat:
                        zkstat = Zkstat()
                        db_session.add(zkstat)

                        zkstat.datum = bill_date
                        zkstat.zikatnr = genstat.zikatnr


                    anz = 0

                    for zimbuff in db_session.query(Zimbuff).filter(
                            (Zimbuff.zikatnr == genstat.zikatnr) &  (Zimbuff.sleeping)).all():
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

                    zkstat = db_session.query(Zkstat).first()

            for t_segmentstat in query(t_segmentstat_list):

                segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.datum == t_Segmentstat.datum) &  (Segmentstat.segmentcode == t_Segmentstat.segmentcode)).first()

                if not segmentstat:
                    segmentstat = Segmentstat()
                    db_session.add(segmentstat)

                    segmentstat.datum = t_segmentstat.datum
                    segmentstat.segmentcode = t_segmentstat.segmentcode


                segmentstat.budlogis = t_segmentstat.budlogis
                segmentstat.budzimmeranz = t_segmentstat.budzimmeranz
                segmentstat.budpersanz = t_segmentstat.budpersanz

            for t_sources in query(t_sources_list):

                sources = db_session.query(Sources).filter(
                            (Sources.datum == t_Sources.datum) &  (Sources.source_code == t_Sources.source_code)).first()

                if not sources:
                    sources = Sources()
                    db_session.add(sources)

                    sources.datum = t_sources.datum
                    sources.source_code = t_sources.source_code


                sources.budlogis = t_sources.budlogis
                sources.budzimmeranz = t_sources.budzimmeranz
                sources.budpersanz = t_sources.budpersanz

    def reorg_guestat():

        nonlocal bill_date, curr_i, vat, vat2, service, fact_scvat, segmentstat, sources, htparam, nationstat, natstat1, landstat, guestat1, guestat, zinrstat, genstat, zimmer, zkstat, arrangement, artikel
        nonlocal segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff


        nonlocal t_segmentstat, t_sources, segbuff, natbuff, nsbuff, scbuff, landbuff, gsbuff, gubuff, zibuff, genbuff, zimbuff, zkbuff
        nonlocal t_segmentstat_list, t_sources_list

        dd:date = None
        mm:int = 0
        yy:int = 0
        Genbuff = Genstat
        for mm in range(get_month(fdate),get_month(tdate)  + 1) :

            for genbuff in db_session.query(Genbuff).filter(
                    (get_year(Genbuff.datum) == get_year(fdate)) &  (get_month(Genbuff.datum) == mm) &  (Genbuff.zinr != "")).all():

                guestat = db_session.query(Guestat).filter(
                        (Guestat.monat == mm) &  (Guestat.jahr == get_year(fdate)) &  (Guestat.gastnr == genbuff.gastnr)).first()

                if not guestat:
                    guestat = Guestat()
                    db_session.add(guestat)

                    guestat.monat = get_month(bill_date)
                    guestat.jahr = get_year(bill_date)
                    guestat.gastnr = genbuff.gastnr

                if genbuff.resstatus != 13:
                    guestat.room_nights = guestat.room_nights + 1

                guestat = db_session.query(Guestat).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 127)).first()
    rm_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 128)).first()
    rm_serv = htparam.flogical
    reorg_stat()
    reorg_guestat()


    return generate_output()