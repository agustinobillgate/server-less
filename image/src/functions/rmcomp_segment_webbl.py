from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Guest, Genstat, Zimmer, Segment, Arrangement, Artikel, Queasy

def rmcomp_segment_webbl(pvilanguage:int, sorttype:int, cardtype:int, incl_comp:bool, mi_ftd:bool, f_date:date, t_date:date, to_date:date):
    rmcomp_segm_list_list = []
    s_list_list = []
    price_decimal:int = 0
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:decimal = 0
    avrgrate:decimal = 0
    proz:decimal = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:decimal = 0
    m_avrgrate:decimal = 0
    m_proz:decimal = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:decimal = 0
    y_avrgrate:decimal = 0
    y_proz:decimal = 0
    gt_room:int = 0
    gtc_room:int = 0
    gt_pax:int = 0
    gt_logis:decimal = 0
    gt_avrgrate:decimal = 0
    gtm_room:int = 0
    gtmc_room:int = 0
    gtm_pax:int = 0
    gtm_logis:decimal = 0
    gtm_avrgrate:decimal = 0
    gtm_proz:decimal = 0
    gty_room:int = 0
    gtyc_room:int = 0
    gty_pax:int = 0
    gty_logis:decimal = 0
    gty_avrgrate:decimal = 0
    gty_proz:decimal = 0
    st_room:int = 0
    stc_room:int = 0
    st_pax:int = 0
    st_logis:decimal = 0
    st_avrgrate:decimal = 0
    st_proz:decimal = 0
    stm_room:int = 0
    stmc_room:int = 0
    stm_pax:int = 0
    stm_logis:decimal = 0
    stm_avrgrate:decimal = 0
    stm_proz:decimal = 0
    sty_room:int = 0
    styc_room:int = 0
    sty_pax:int = 0
    sty_logis:decimal = 0
    sty_avrgrate:decimal = 0
    sty_proz:decimal = 0
    rm_serv:bool = False
    rm_vat:bool = False
    lvcarea:str = "rmcomp_segment_web"
    htparam = guest = genstat = zimmer = segment = arrangement = artikel = queasy = None

    rmcomp_segm_list = s_list = sbuff = None

    rmcomp_segm_list_list, Rmcomp_segm_list = create_model("Rmcomp_segm_list", {"flag":int, "segment":str, "room":str, "pax":str, "logis":str, "proz":str, "avrgrate":str, "m_room":str, "m_pax":str, "m_logis":str, "m_proz":str, "m_avrgrate":str, "y_room":str, "y_pax":str, "y_logis":str, "y_proz":str, "y_avrgrate":str, "rmnite1":str, "rmrev1":str, "rmnite":str, "rmrev":str, "segm_code":int, "gastnr":int})
    s_list_list, S_list = create_model("S_list", {"segm_code":int, "segm_grup":int, "segment":str, "segment1":str, "gastnr":int, "compname":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list
        return {"rmcomp-segm-list": rmcomp_segm_list_list, "s-list": s_list_list}

    def create_umsatz():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        rmrev:decimal = 0
        service:decimal = 0
        vat:decimal = 0
        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:str = ""
        curr_code:str = ""
        status_vat:bool = False
        fdate:date = None
        beg_date:date = None
        room = 0
        c_room = 0
        pax = 0
        logis = 0
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis = 0
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis = 0
        gt_room = 0
        gt_pax = 0
        gt_logis = 0
        gt_avrgrate = 0
        gtm_room = 0
        gtm_pax = 0
        gtm_logis = 0
        gtm_avrgrate = 0
        gtm_room = 0
        gtm_pax = 0
        gtm_logis = 0
        gtm_avrgrate = 0
        gty_room = 0
        gty_pax = 0
        gty_logis = 0
        gty_avrgrate = 0


        rmcomp_segm_list_list.clear()
        s_list_list.clear()

        if mi_ftd:
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
            beg_date = date_mdy(get_month(f_date) , 1, yy)

            if f_date > beg_date:
                beg_date = f_date

            if get_month(to_date) > get_month(f_date):
                beg_date = date_mdy(mm, 1, yy)


            from_date = beg_date
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
            fdate = date_mdy(get_month(t_date) , 1, get_year(t_date))

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.gastnr != 0) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == genstat.zinr)).first()

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == genstat.segmentcode)).first()

            if cardtype < 3:
                do_it = guest.karteityp == cardtype
            else:
                do_it = True

            if not incl_comp and genstat.zipreis == 0:

                if (genstat.gratis > 0):
                    do_it = False

                if (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13:
                    do_it = False

            if do_it:

                if genstat.zipreis == 0:

                    if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                        if genstat.datum == to_date:
                            c_room = c_room + 1

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            mc_room = mc_room + 1
                        yc_room = yc_room + 1

                s_list = query(s_list_list, filters=(lambda s_list :s_list.gastnr == genstat.gastnr and s_list.segm_code == genstat.segmentcode), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.gastnr = genstat.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma
                    s_list.segm_code = genstat.segmentcode

                    if segment:
                        s_list.segment = segment.bezeich
                    else:
                        s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")
                service = 0
                vat = 0

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 127)).first()

                if htparam:
                    status_vat = htparam.flogical

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()

                if artikel and status_vat :
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))
                rmrev = genstat.rateLocal

                if rm_serv:
                    rmrev = rmrev / (1 + service + vat)

                if mi_ftd and genstat.datum == t_date:

                    if incl_comp:
                        s_list.room = s_list.room + 1
                        room = room + 1
                        s_list.pax = s_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.logis = s_list.logis + genstat.logis
                        logis = logis + genstat.logis
                        avrgrate = avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis = s_list.logis + genstat.logis
                            logis = logis + genstat.logis
                            avrgrate = avrgrate + rmrev

                if not mi_ftd and genstat.datum == to_date:

                    if incl_comp:
                        s_list.room = s_list.room + 1
                        room = room + 1
                        s_list.pax = s_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.logis = s_list.logis + genstat.logis
                        logis = logis + genstat.logis
                        avrgrate = avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis = s_list.logis + genstat.logis
                            logis = logis + genstat.logis
                            avrgrate = avrgrate + rmrev

                if not mi_ftd and get_year(genstat.datum) == yy:

                    if incl_comp:

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.m_logis = s_list.m_logis + genstat.logis
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            m_logis = m_logis + genstat.logis
                            m_avrgrate = m_avrgrate + rmrev


                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis = s_list.y_logis + genstat.logis
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis = y_logis + genstat.logis
                        y_avrgrate = y_avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                s_list.m_room = s_list.m_room + 1
                                m_room = m_room + 1
                                s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                s_list.m_logis = s_list.m_logis + genstat.logis
                                m_pax = m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                m_logis = m_logis + genstat.logis
                                m_avrgrate = m_avrgrate + rmrev


                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.y_logis = s_list.y_logis + genstat.logis
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            y_logis = y_logis + genstat.logis
                            y_avrgrate = y_avrgrate + rmrev

                if mi_ftd and get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if incl_comp:
                        s_list.m_room = s_list.m_room + 1
                        m_room = m_room + 1
                        s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.m_logis = s_list.m_logis + genstat.logis
                        m_pax = m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        m_logis = m_logis + genstat.logis
                        m_avrgrate = m_avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.m_logis = s_list.m_logis + genstat.logis
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            m_logis = m_logis + genstat.logis
                            m_avrgrate = m_avrgrate + rmrev

                if mi_ftd and genstat.datum >= f_date and genstat.datum <= t_date:

                    if incl_comp:
                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis = s_list.y_logis + genstat.logis
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis = y_logis + genstat.logis
                        y_avrgrate = y_avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:
                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.y_logis = s_list.y_logis + genstat.logis
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            y_logis = y_logis + genstat.logis
                            y_avrgrate = y_avrgrate + rmrev

                for s_list in query(s_list_list):

                    if (s_list.room - s_list.c_room) != 0:
                        s_list.avrgrate = s_list.logis / (s_list.room - s_list.c_room)

                    if (s_list.m_room - s_list.mc_room) != 0:
                        s_list.m_avrgrate = s_list.m_logis / (s_list.m_room - s_list.mc_room)

                    if (s_list.y_room - s_list.yc_room) != 0:
                        s_list.y_avrgrate = s_list.y_logis / (s_list.y_room - s_list.yc_room)

                    if logis != 0:
                        s_list.proz = s_list.logis / logis * 100

                    if m_logis != 0:
                        s_list.m_proz = s_list.m_logis / m_logis * 100

                    if y_logis != 0:
                        s_list.y_proz = s_list.y_logis / y_logis * 100
                gt_room = 0
                gtc_room = 0
                gt_pax = 0
                gt_logis = 0
                gt_avrgrate = 0
                gtm_room = 0
                gtmc_room = 0
                gtm_pax = 0
                gtm_logis = 0
                gtm_avrgrate = 0
                gty_room = 0
                gty_pax = 0
                gtyc_room = 0
                gty_pax = 0
                gty_logis = 0
                gty_avrgrate = 0

                for s_list in query(s_list_list):
                    gt_room = gt_room + s_list.room
                    gtc_room = gtc_room + s_list.c_room
                    gt_pax = gt_pax + s_list.pax
                    gt_logis = gt_logis + s_list.logis
                    gt_avrgrate = gt_avrgrate + s_list.avrgrate
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis = gtm_logis + s_list.m_logis
                    gtm_avrgrate = gtm_avrgrate + s_list.m_avrgrate
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis = gty_logis + s_list.y_logis
                    gty_avrgrate = gty_avrgrate + s_list.y_avrgrate

        if sorttype == 0:
            create_output()
        else:
            create_output1()

    def create_umsatz2():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        rmrev:decimal = 0
        service:decimal = 0
        vat:decimal = 0
        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:str = ""
        curr_code:str = ""
        status_vat:bool = False
        beg_date:date = None
        room = 0
        c_room = 0
        pax = 0
        logis = 0
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis = 0
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis = 0
        gt_room = 0
        gt_pax = 0
        gt_logis = 0
        gt_avrgrate = 0
        gtm_room = 0
        gtm_pax = 0
        gtm_logis = 0
        gtm_avrgrate = 0
        gtm_room = 0
        gtm_pax = 0
        gtm_logis = 0
        gtm_avrgrate = 0
        gty_room = 0
        gty_pax = 0
        gty_logis = 0
        gty_avrgrate = 0


        rmcomp_segm_list_list.clear()
        s_list_list.clear()

        if mi_ftd:
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
            beg_date = date_mdy(get_month(f_date) , 1, yy)

            if f_date > beg_date:
                beg_date = f_date

            if get_month(to_date) > get_month(f_date):
                beg_date = date_mdy(mm, 1, yy)


            from_date = beg_date
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.gastnr != 0) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == genstat.zinr)).first()

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == genstat.segmentcode)).first()

            if cardtype < 3:
                do_it = guest.karteityp == cardtype
            else:
                do_it = True

            if not incl_comp and genstat.zipreis == 0:

                if genstat.gratis > 0:
                    do_it = False

                if (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13:
                    do_it = False

            if do_it:

                if genstat.zipreis == 0:

                    if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                        if genstat.datum == to_date:
                            c_room = c_room + 1

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            mc_room = mc_room + 1
                        yc_room = yc_room + 1

                segment = db_session.query(Segment).filter(
                        (genstat.segmentcode == Segmentcode)).first()

                if segment:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 26) &  (Queasy.number1 == segmentgrup)).first()

                s_list = query(s_list_list, filters=(lambda s_list :s_list.gastnr == genstat.gastnr and s_list.segm_code == genstat.segmentcode and s_list.segm_grup == queasy.number1), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.gastnr = genstat.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma
                    s_list.segm_code = genstat.segmentcode

                    if segment:
                        s_list.segment = segment.bezeich
                        s_list.segm_grup = segmentgrup


                    else:
                        s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")

                    if queasy:
                        s_list.segment1 = queasy.char3
                    else:
                        s_list.segment1 = translateExtended ("UNKNOWN", lvcarea, "")
                service = 0
                vat = 0

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 127)).first()

                if htparam:
                    status_vat = htparam.flogical

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()

                if artikel and status_vat :
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))
                rmrev = genstat.rateLocal

                if rm_serv:
                    rmrev = rmrev / (1 + service + vat)

                if genstat.datum == to_date:

                    if incl_comp:
                        s_list.room = s_list.room + 1
                        room = room + 1
                        s_list.pax = s_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.logis = s_list.logis + genstat.logis
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        logis = logis + genstat.logis
                        avrgrate = avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis = s_list.logis + genstat.logis
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            logis = logis + genstat.logis
                            avrgrate = avrgrate + rmrev

                if get_year(genstat.datum) == yy:

                    if incl_comp:

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.m_logis = s_list.m_logis + genstat.logis
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            m_logis = m_logis + genstat.logis
                            m_avrgrate = m_avrgrate + rmrev


                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis = s_list.y_logis + genstat.logis
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis = y_logis + genstat.logis
                        y_avrgrate = y_avrgrate + rmrev


                    else:

                        if genstat.gratis == 0:

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                s_list.m_room = s_list.m_room + 1
                                m_room = m_room + 1
                                s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                s_list.m_logis = s_list.m_logis + genstat.logis
                                m_pax = m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                m_logis = m_logis + genstat.logis
                                m_avrgrate = m_avrgrate + rmrev


                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.y_logis = s_list.y_logis + genstat.logis
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            y_logis = y_logis + genstat.logis
                            y_avrgrate = y_avrgrate + rmrev

                for s_list in query(s_list_list):

                    if (s_list.room - s_list.c_room) != 0:
                        s_list.avrgrate = s_list.logis / (s_list.room - s_list.c_room)

                    if (s_list.m_room - s_list.mc_room) != 0:
                        s_list.m_avrgrate = s_list.m_logis / (s_list.m_room - s_list.mc_room)

                    if (s_list.y_room - s_list.yc_room) != 0:
                        s_list.y_avrgrate = s_list.y_logis / (s_list.y_room - s_list.yc_room)

                    if logis != 0:
                        s_list.proz = s_list.logis / logis * 100

                    if m_logis != 0:
                        s_list.m_proz = s_list.m_logis / m_logis * 100

                    if y_logis != 0:
                        s_list.y_proz = s_list.y_logis / y_logis * 100
                gt_room = 0
                gtc_room = 0
                gt_pax = 0
                gt_logis = 0
                gt_avrgrate = 0
                gtm_room = 0
                gtmc_room = 0
                gtm_pax = 0
                gtm_logis = 0
                gtm_avrgrate = 0
                gty_room = 0
                gty_pax = 0
                gtyc_room = 0
                gty_pax = 0
                gty_logis = 0
                gty_avrgrate = 0

                for s_list in query(s_list_list):
                    gt_room = gt_room + s_list.room
                    gtc_room = gtc_room + s_list.c_room
                    gt_pax = gt_pax + s_list.pax
                    gt_logis = gt_logis + s_list.logis
                    gt_avrgrate = gt_avrgrate + s_list.avrgrate
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis = gtm_logis + s_list.m_logis
                    gtm_avrgrate = gtm_avrgrate + s_list.m_avrgrate
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis = gty_logis + s_list.y_logis
                    gty_avrgrate = gty_avrgrate + s_list.y_avrgrate


        create_output2()

    def create_output():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        tot_room:int = 0
        i:int = 0
        curr_rmtype:str = ""
        curr_gastnr:int = -1
        Sbuff = S_list

        for s_list in query(s_list_list):
            i = i + 1

            if curr_gastnr != s_list.gastnr and curr_gastnr != -1:
                create_sub()

            if curr_gastnr != s_list.gastnr:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.compname

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub2()
            curr_gastnr = s_list.gastnr
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        rmcomp_segm_list.segment = translateExtended ("T o t a l", lvcarea, "")
        rmcomp_segm_list.room = to_string(gt_room, "->>>,>>9")
        rmcomp_segm_list.pax = to_string(gt_pax, "->>>,>>9")
        rmcomp_segm_list.logis = to_string(gt_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.proz = "100.00"
        rmcomp_segm_list.avrgrate = to_string(gt_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_room = to_string(gtm_room, "->>>,>>9")
        rmcomp_segm_list.m_pax = to_string(gtm_pax, "->>>,>>9")
        rmcomp_segm_list.m_logis = to_string(gtm_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_proz = "100.00"
        rmcomp_segm_list.m_avrgrate = to_string(gtm_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_room = to_string(gty_room, "->>>,>>9")
        rmcomp_segm_list.y_pax = to_string(gty_pax, "->>>,>>9")
        rmcomp_segm_list.y_logis = to_string(gty_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_proz = "100.00"
        rmcomp_segm_list.y_avrgrate = to_string(gty_avrgrate, "->>,>>>,>>>,>>>,>>9")

    def create_output1():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        tot_room:int = 0
        i:int = 0
        curr_segment:int = 0
        Sbuff = S_list

        for s_list in query(s_list_list):
            i = i + 1

            if curr_segment != s_list.segm_code and curr_segment != 0:
                create_sub()

            if curr_segment != s_list.segm_code:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.segment

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub2()
            curr_segment = s_list.segm_code
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        rmcomp_segm_list.segment = translateExtended ("T o t a l", lvcarea, "")
        rmcomp_segm_list.room = to_string(gt_room, "->>>,>>9")
        rmcomp_segm_list.pax = to_string(gt_pax, "->>>,>>9")
        rmcomp_segm_list.logis = to_string(gt_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.proz = "100.00"
        rmcomp_segm_list.avrgrate = to_string(gt_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_room = to_string(gtm_room, "->>>,>>9")
        rmcomp_segm_list.m_pax = to_string(gtm_pax, "->>>,>>9")
        rmcomp_segm_list.m_logis = to_string(gtm_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_proz = "100.00"
        rmcomp_segm_list.m_avrgrate = to_string(gtm_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_room = to_string(gty_room, "->>>,>>9")
        rmcomp_segm_list.y_pax = to_string(gty_pax, "->>>,>>9")
        rmcomp_segm_list.y_logis = to_string(gty_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_proz = "100.00"
        rmcomp_segm_list.y_avrgrate = to_string(gty_avrgrate, "->>,>>>,>>>,>>>,>>9")

    def create_output2():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        tot_room:int = 0
        i:int = 0
        curr_segment:int = 0
        Sbuff = S_list

        for s_list in query(s_list_list):
            i = i + 1

            if curr_segment != s_list.segm_grup and curr_segment != 0:
                create_sub()

            if curr_segment != s_list.segm_grup:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.segment1

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_list.append(rmcomp_segm_list)

                count_sub2()
            curr_segment = s_list.segm_grup
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        rmcomp_segm_list.segment = translateExtended ("T o t a l", lvcarea, "")
        rmcomp_segm_list.room = to_string(gt_room, "->>>,>>9")
        rmcomp_segm_list.pax = to_string(gt_pax, "->>>,>>9")
        rmcomp_segm_list.logis = to_string(gt_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.proz = "100.00"
        rmcomp_segm_list.avrgrate = to_string(gt_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_room = to_string(gtm_room, "->>>,>>9")
        rmcomp_segm_list.m_pax = to_string(gtm_pax, "->>>,>>9")
        rmcomp_segm_list.m_logis = to_string(gtm_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_proz = "100.00"
        rmcomp_segm_list.m_avrgrate = to_string(gtm_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_room = to_string(gty_room, "->>>,>>9")
        rmcomp_segm_list.y_pax = to_string(gty_pax, "->>>,>>9")
        rmcomp_segm_list.y_logis = to_string(gty_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_proz = "100.00"
        rmcomp_segm_list.y_avrgrate = to_string(gty_avrgrate, "->>,>>>,>>>,>>>,>>9")

    def count_sub1():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        if sorttype == 0:
            rmcomp_segm_list.segment = s_list.segment
        else:
            rmcomp_segm_list.segment = s_list.compname
        rmcomp_segm_list.room = to_string(s_list.room, "->>>,>>9")
        rmcomp_segm_list.pax = to_string(s_list.pax, "->>>,>>9")
        rmcomp_segm_list.logis = to_string(s_list.logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.proz = to_string(s_list.proz, ">>9.99")
        rmcomp_segm_list.avrgrate = to_string(s_list.avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        rmcomp_segm_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        rmcomp_segm_list.m_logis = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        rmcomp_segm_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        rmcomp_segm_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        rmcomp_segm_list.y_logis = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        rmcomp_segm_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        rmcomp_segm_list.rmrev = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        rmcomp_segm_list.rmrev1 = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        rmcomp_segm_list.gastnr = s_list.gastnr
        rmcomp_segm_list.segm_code = s_list.segm_code


        proz = proz + s_list.proz
        m_proz = m_proz + s_list.m_proz
        y_proz = y_proz + s_list.y_proz
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz = st_proz + s_list.proz
        st_logis = st_logis + s_list.logis
        st_avrgrate = st_avrgrate + s_list.avrgrate
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz = stm_proz + s_list.m_proz
        stm_logis = stm_logis + s_list.m_logis
        stm_avrgrate = stm_avrgrate + s_list.m_avrgrate
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz = sty_proz + s_list.y_proz
        sty_logis = sty_logis + s_list.y_logis
        sty_avrgrate = sty_avrgrate + s_list.y_avrgrate

    def count_sub2():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        if sorttype == 0:
            rmcomp_segm_list.segment = s_list.segment
        else:
            rmcomp_segm_list.segment = s_list.compname
        rmcomp_segm_list.room = to_string(s_list.room, "->>>,>>9")
        rmcomp_segm_list.pax = to_string(s_list.pax, "->>>,>>9")
        rmcomp_segm_list.logis = to_string(s_list.logis, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.proz = to_string(s_list.proz, ">>9.99")
        rmcomp_segm_list.avrgrate = to_string(s_list.avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        rmcomp_segm_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        rmcomp_segm_list.m_logis = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        rmcomp_segm_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        rmcomp_segm_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        rmcomp_segm_list.y_logis = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        rmcomp_segm_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        rmcomp_segm_list.rmrev = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        rmcomp_segm_list.rmrev1 = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        rmcomp_segm_list.gastnr = s_list.gastnr
        rmcomp_segm_list.segm_code = s_list.segm_code


        proz = proz + s_list.proz
        m_proz = m_proz + s_list.m_proz
        y_proz = y_proz + s_list.y_proz
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz = st_proz + s_list.proz
        st_logis = st_logis + s_list.logis
        st_avrgrate = st_avrgrate + s_list.avrgrate
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz = stm_proz + s_list.m_proz
        stm_logis = stm_logis + s_list.m_logis
        stm_avrgrate = stm_avrgrate + s_list.m_avrgrate
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz = sty_proz + s_list.y_proz
        sty_logis = sty_logis + s_list.y_logis
        sty_avrgrate = sty_avrgrate + s_list.y_avrgrate

    def create_sub():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list

        ind:int = 0
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        rmcomp_segm_list.flag = 1
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        rmcomp_segm_list.flag = 2
        st_avrgrate = 0

        if (st_room - stc_room) != 0:
            st_avrgrate = st_logis / (st_room - stc_room)
        stm_avrgrate = 0

        if (stm_room - stmc_room) != 0:
            stm_avrgrate = stm_logis / (stm_room - stmc_room)
        sty_avrgrate = 0

        if (sty_room - styc_room) != 0:
            sty_avrgrate = sty_logis / (sty_room - styc_room)

        if price_decimal == 0:
            rmcomp_segm_list.segment = translateExtended ("s u b T o t a l", lvcarea, "")
            rmcomp_segm_list.room = to_string(st_room, "->>>,>>9")
            rmcomp_segm_list.pax = to_string(st_pax, "->>>,>>9")
            rmcomp_segm_list.logis = to_string(st_logis, "->>,>>>,>>>,>>>,>>9")
            rmcomp_segm_list.proz = to_string(st_proz, ">>9.99")
            rmcomp_segm_list.avrgrate = to_string(st_avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcomp_segm_list.m_room = to_string(stm_room, "->>>,>>9")
            rmcomp_segm_list.m_pax = to_string(stm_pax, "->>>,>>9")
            rmcomp_segm_list.m_logis = to_string(stm_logis, "->>,>>>,>>>,>>>,>>9")
            rmcomp_segm_list.m_proz = to_string(stm_proz, ">>9.99")
            rmcomp_segm_list.m_avrgrate = to_string(stm_avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcomp_segm_list.y_room = to_string(sty_room, "->>>,>>9")
            rmcomp_segm_list.y_pax = to_string(sty_pax, "->>>,>>9")
            rmcomp_segm_list.y_logis = to_string(sty_logis, "->>,>>>,>>>,>>>,>>9")
            rmcomp_segm_list.y_proz = to_string(sty_proz, ">>9.99")
            rmcomp_segm_list.y_avrgrate = to_string(sty_avrgrate, "->>,>>>,>>>,>>>,>>9")


        else:
            rmcomp_segm_list.segment = translateExtended ("s u b T o t a l", lvcarea, "")
            rmcomp_segm_list.room = to_string(st_room, "->>>,>>9")
            rmcomp_segm_list.pax = to_string(st_pax, "->>>,>>9")
            rmcomp_segm_list.logis = to_string(st_logis, "->>>,>>>,>>>,>>9.99")
            rmcomp_segm_list.proz = to_string(st_proz, ">>9.99")
            rmcomp_segm_list.avrgrate = to_string(st_avrgrate, "->>>,>>>,>>>,>>9.99")
            rmcomp_segm_list.m_room = to_string(stm_room, "->>>,>>9")
            rmcomp_segm_list.m_pax = to_string(stm_pax, "->>>,>>9")
            rmcomp_segm_list.m_logis = to_string(stm_logis, "->>>,>>>,>>>,>>9.99")
            rmcomp_segm_list.m_proz = to_string(stm_proz, ">>9.99")
            rmcomp_segm_list.m_avrgrate = to_string(stm_avrgrate, "->>>,>>>,>>>,>>9.99")
            rmcomp_segm_list.y_room = to_string(sty_room, "->>>,>>9")
            rmcomp_segm_list.y_pax = to_string(sty_pax, "->>>,>>9")
            rmcomp_segm_list.y_logis = to_string(sty_logis, "->>>,>>>,>>>,>>9.99")
            rmcomp_segm_list.y_proz = to_string(sty_proz, ">>9.99")
            rmcomp_segm_list.y_avrgrate = to_string(sty_avrgrate, "->>>,>>>,>>>,>>9.99")


        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_list.append(rmcomp_segm_list)

        init_val()

    def init_val():

        nonlocal rmcomp_segm_list_list, s_list_list, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal sbuff


        nonlocal rmcomp_segm_list, s_list, sbuff
        nonlocal rmcomp_segm_list_list, s_list_list


        st_room = 0
        st_pax = 0
        st_proz = 0
        st_logis = 0
        st_avrgrate = 0
        stm_room = 0
        stm_pax = 0
        stm_proz = 0
        stm_logis = 0
        stm_avrgrate = 0
        sty_room = 0
        sty_pax = 0
        sty_proz = 0
        sty_logis = 0
        sty_avrgrate = 0


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    if sorttype == 0 or sorttype == 1:
        create_umsatz()
    else:
        create_umsatz2()

    return generate_output()