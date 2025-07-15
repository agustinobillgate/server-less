#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Guest, Genstat, Zimmer, Segment, Arrangement, Artikel, Queasy

def rmcomp_segment_webbl(pvilanguage:int, sorttype:int, cardtype:int, incl_comp:bool, mi_ftd:bool, f_date:date, t_date:date, to_date:date):

    prepare_cache ([Htparam, Guest, Genstat, Segment, Arrangement, Artikel, Queasy])

    rmcomp_segm_list_data = []
    s_list_data = []
    price_decimal:int = 0
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:Decimal = to_decimal("0.0")
    avrgrate:Decimal = to_decimal("0.0")
    proz:Decimal = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:Decimal = to_decimal("0.0")
    m_avrgrate:Decimal = to_decimal("0.0")
    m_proz:Decimal = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:Decimal = to_decimal("0.0")
    y_avrgrate:Decimal = to_decimal("0.0")
    y_proz:Decimal = 0
    gt_room:int = 0
    gtc_room:int = 0
    gt_pax:int = 0
    gt_logis:Decimal = to_decimal("0.0")
    gt_avrgrate:Decimal = to_decimal("0.0")
    gtm_room:int = 0
    gtmc_room:int = 0
    gtm_pax:int = 0
    gtm_logis:Decimal = to_decimal("0.0")
    gtm_avrgrate:Decimal = to_decimal("0.0")
    gtm_proz:Decimal = 0
    gty_room:int = 0
    gtyc_room:int = 0
    gty_pax:int = 0
    gty_logis:Decimal = to_decimal("0.0")
    gty_avrgrate:Decimal = to_decimal("0.0")
    gty_proz:Decimal = to_decimal("0.0")
    st_room:int = 0
    stc_room:int = 0
    st_pax:int = 0
    st_logis:Decimal = to_decimal("0.0")
    st_avrgrate:Decimal = to_decimal("0.0")
    st_proz:Decimal = to_decimal("0.0")
    stm_room:int = 0
    stmc_room:int = 0
    stm_pax:int = 0
    stm_logis:Decimal = to_decimal("0.0")
    stm_avrgrate:Decimal = to_decimal("0.0")
    stm_proz:Decimal = 0
    sty_room:int = 0
    styc_room:int = 0
    sty_pax:int = 0
    sty_logis:Decimal = to_decimal("0.0")
    sty_avrgrate:Decimal = to_decimal("0.0")
    sty_proz:Decimal = to_decimal("0.0")
    rm_serv:bool = False
    rm_vat:bool = False
    lvcarea:string = "rmcomp-segment-web"
    htparam = guest = genstat = zimmer = segment = arrangement = artikel = queasy = None

    rmcomp_segm_list = s_list = sbuff = sbuff = sbuff = None

    rmcomp_segm_list_data, Rmcomp_segm_list = create_model("Rmcomp_segm_list", {"flag":int, "segment":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string, "rmnite1":string, "rmrev1":string, "rmnite":string, "rmrev":string, "segm_code":int, "gastnr":int})
    s_list_data, S_list = create_model("S_list", {"segm_code":int, "segm_grup":int, "segment":string, "segment1":string, "gastnr":int, "compname":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        return {"rmcomp-segm-list": rmcomp_segm_list_data, "s-list": s_list_data}

    def create_umsatz():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        rmrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        fdate:date = None
        beg_date:date = None
        room = 0
        c_room = 0
        pax = 0
        logis =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        gt_room = 0
        gt_pax = 0
        gt_logis =  to_decimal("0")
        gt_avrgrate =  to_decimal("0")
        gtm_room = 0
        gtm_pax = 0
        gtm_logis =  to_decimal("0")
        gtm_avrgrate =  to_decimal("0")
        gtm_room = 0
        gtm_pax = 0
        gtm_logis =  to_decimal("0")
        gtm_avrgrate =  to_decimal("0")
        gty_room = 0
        gty_pax = 0
        gty_logis =  to_decimal("0")
        gty_avrgrate =  to_decimal("0")


        rmcomp_segm_list_data.clear()
        s_list_data.clear()

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
            htparam.fdate = date_mdy(get_month(t_date) , 1, get_year(t_date))

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.zinr, genstat.segmentcode, genstat.resstatus, genstat.datum, genstat.gastnr, genstat.argt, genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.zipreis, genstat.gratis, genstat.kind1, genstat.kind2, genstat._recid, guest.karteityp, guest.name, guest.vorname1, guest._recid in db_session.query(Genstat.zinr, Genstat.segmentcode, Genstat.resstatus, Genstat.datum, Genstat.gastnr, Genstat.argt, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.zipreis, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.karteityp, Guest.name, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr != "") & (Genstat.gastnr != 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

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

                s_list = query(s_list_data, filters=(lambda s_list: s_list.gastnr == genstat.gastnr and s_list.segm_code == genstat.segmentcode), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.gastnr = genstat.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma
                    s_list.segm_code = genstat.segmentcode

                    if segment:
                        s_list.segment = segment.bezeich
                    else:
                        s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")
                service =  to_decimal("0")
                vat =  to_decimal("0")

                htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

                if htparam:
                    status_vat = htparam.flogical

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

                if artikel and status_vat :
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))
                rmrev =  to_decimal(genstat.ratelocal)

                if rm_serv:
                    rmrev =  to_decimal(rmrev) / to_decimal((1) + to_decimal(service) + to_decimal(vat))

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
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                        logis =  to_decimal(logis) + to_decimal(genstat.logis)
                        avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                            logis =  to_decimal(logis) + to_decimal(genstat.logis)
                            avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)

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
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                        logis =  to_decimal(logis) + to_decimal(genstat.logis)
                        avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                            logis =  to_decimal(logis) + to_decimal(genstat.logis)
                            avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)

                if not mi_ftd and get_year(genstat.datum) == yy:

                    if incl_comp:

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                            m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)


                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                s_list.m_room = s_list.m_room + 1
                                m_room = m_room + 1
                                s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                                m_pax = m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)


                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                            y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)

                if mi_ftd and get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if incl_comp:
                        s_list.m_room = s_list.m_room + 1
                        m_room = m_room + 1
                        s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                        m_pax = m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                            m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)

                if mi_ftd and genstat.datum >= f_date and genstat.datum <= t_date:

                    if incl_comp:
                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:
                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                            y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)

                for s_list in query(s_list_data):

                    if (s_list.room - s_list.c_room) != 0:
                        s_list.avrgrate =  to_decimal(s_list.logis) / to_decimal((s_list.room) - to_decimal(s_list.c_room))

                    if (s_list.m_room - s_list.mc_room) != 0:
                        s_list.m_avrgrate =  to_decimal(s_list.m_logis) / to_decimal((s_list.m_room) - to_decimal(s_list.mc_room))

                    if (s_list.y_room - s_list.yc_room) != 0:
                        s_list.y_avrgrate =  to_decimal(s_list.y_logis) / to_decimal((s_list.y_room) - to_decimal(s_list.yc_room))

                    if logis != 0:
                        s_list.proz =  to_decimal(s_list.logis) / to_decimal(logis) * to_decimal("100")

                    if m_logis != 0:
                        s_list.m_proz =  to_decimal(s_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

                    if y_logis != 0:
                        s_list.y_proz =  to_decimal(s_list.y_logis) / to_decimal(y_logis) * to_decimal("100")
                gt_room = 0
                gtc_room = 0
                gt_pax = 0
                gt_logis =  to_decimal("0")
                gt_avrgrate =  to_decimal("0")
                gtm_room = 0
                gtmc_room = 0
                gtm_pax = 0
                gtm_logis =  to_decimal("0")
                gtm_avrgrate =  to_decimal("0")
                gty_room = 0
                gty_pax = 0
                gtyc_room = 0
                gty_pax = 0
                gty_logis =  to_decimal("0")
                gty_avrgrate =  to_decimal("0")

                for s_list in query(s_list_data):
                    gt_room = gt_room + s_list.room
                    gtc_room = gtc_room + s_list.c_room
                    gt_pax = gt_pax + s_list.pax
                    gt_logis =  to_decimal(gt_logis) + to_decimal(s_list.logis)
                    gt_avrgrate =  to_decimal(gt_avrgrate) + to_decimal(s_list.avrgrate)
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis =  to_decimal(gtm_logis) + to_decimal(s_list.m_logis)
                    gtm_avrgrate =  to_decimal(gtm_avrgrate) + to_decimal(s_list.m_avrgrate)
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis =  to_decimal(gty_logis) + to_decimal(s_list.y_logis)
                    gty_avrgrate =  to_decimal(gty_avrgrate) + to_decimal(s_list.y_avrgrate)

        if sorttype == 0:
            create_output()
        else:
            create_output1()


    def create_umsatz2():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        rmrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        beg_date:date = None
        room = 0
        c_room = 0
        pax = 0
        logis =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        gt_room = 0
        gt_pax = 0
        gt_logis =  to_decimal("0")
        gt_avrgrate =  to_decimal("0")
        gtm_room = 0
        gtm_pax = 0
        gtm_logis =  to_decimal("0")
        gtm_avrgrate =  to_decimal("0")
        gtm_room = 0
        gtm_pax = 0
        gtm_logis =  to_decimal("0")
        gtm_avrgrate =  to_decimal("0")
        gty_room = 0
        gty_pax = 0
        gty_logis =  to_decimal("0")
        gty_avrgrate =  to_decimal("0")


        rmcomp_segm_list_data.clear()
        s_list_data.clear()

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

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.zinr, genstat.segmentcode, genstat.resstatus, genstat.datum, genstat.gastnr, genstat.argt, genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.zipreis, genstat.gratis, genstat.kind1, genstat.kind2, genstat._recid, guest.karteityp, guest.name, guest.vorname1, guest._recid in db_session.query(Genstat.zinr, Genstat.segmentcode, Genstat.resstatus, Genstat.datum, Genstat.gastnr, Genstat.argt, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.zipreis, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.karteityp, Guest.name, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr != "") & (Genstat.gastnr != 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

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

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:

                    queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, segment.segmentgrup)]})

                s_list = query(s_list_data, filters=(lambda s_list: s_list.gastnr == genstat.gastnr and s_list.segm_code == genstat.segmentcode and s_list.segm_grup == queasy.number1), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.gastnr = genstat.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma
                    s_list.segm_code = genstat.segmentcode

                    if segment:
                        s_list.segment = segment.bezeich
                        s_list.segm_grup = segment.segmentgrup


                    else:
                        s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")

                    if queasy:
                        s_list.segment1 = queasy.char3
                    else:
                        s_list.segment1 = translateExtended ("UNKNOWN", lvcarea, "")
                service =  to_decimal("0")
                vat =  to_decimal("0")

                htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

                if htparam:
                    status_vat = htparam.flogical

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

                if artikel and status_vat :
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))
                rmrev =  to_decimal(genstat.ratelocal)

                if rm_serv:
                    rmrev =  to_decimal(rmrev) / to_decimal((1) + to_decimal(service) + to_decimal(vat))

                if genstat.datum == to_date:

                    if incl_comp:
                        s_list.room = s_list.room + 1
                        room = room + 1
                        s_list.pax = s_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis)
                        avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:
                            s_list.room = s_list.room + 1
                            room = room + 1
                            s_list.pax = s_list.pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                            pax = pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            logis =  to_decimal(logis) + to_decimal(genstat.logis)
                            avrgrate =  to_decimal(avrgrate) + to_decimal(rmrev)

                if get_year(genstat.datum) == yy:

                    if incl_comp:

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            s_list.m_room = s_list.m_room + 1
                            m_room = m_room + 1
                            s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                            m_pax = m_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 +\
                                    genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                            m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)


                        s_list.y_room = s_list.y_room + 1
                        y_room = y_room + 1
                        s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                        y_pax = y_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 +\
                                genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)


                    else:

                        if genstat.gratis == 0:

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                s_list.m_room = s_list.m_room + 1
                                m_room = m_room + 1
                                s_list.m_pax = s_list.m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                                m_pax = m_pax + genstat.erwachs +\
                                        genstat.kind1 + genstat.kind2
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(rmrev)


                            s_list.y_room = s_list.y_room + 1
                            y_room = y_room + 1
                            s_list.y_pax = s_list.y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                            y_pax = y_pax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2
                            y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                            y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(rmrev)

                for s_list in query(s_list_data):

                    if (s_list.room - s_list.c_room) != 0:
                        s_list.avrgrate =  to_decimal(s_list.logis) / to_decimal((s_list.room) - to_decimal(s_list.c_room))

                    if (s_list.m_room - s_list.mc_room) != 0:
                        s_list.m_avrgrate =  to_decimal(s_list.m_logis) / to_decimal((s_list.m_room) - to_decimal(s_list.mc_room))

                    if (s_list.y_room - s_list.yc_room) != 0:
                        s_list.y_avrgrate =  to_decimal(s_list.y_logis) / to_decimal((s_list.y_room) - to_decimal(s_list.yc_room))

                    if logis != 0:
                        s_list.proz =  to_decimal(s_list.logis) / to_decimal(logis) * to_decimal("100")

                    if m_logis != 0:
                        s_list.m_proz =  to_decimal(s_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

                    if y_logis != 0:
                        s_list.y_proz =  to_decimal(s_list.y_logis) / to_decimal(y_logis) * to_decimal("100")
                gt_room = 0
                gtc_room = 0
                gt_pax = 0
                gt_logis =  to_decimal("0")
                gt_avrgrate =  to_decimal("0")
                gtm_room = 0
                gtmc_room = 0
                gtm_pax = 0
                gtm_logis =  to_decimal("0")
                gtm_avrgrate =  to_decimal("0")
                gty_room = 0
                gty_pax = 0
                gtyc_room = 0
                gty_pax = 0
                gty_logis =  to_decimal("0")
                gty_avrgrate =  to_decimal("0")

                for s_list in query(s_list_data):
                    gt_room = gt_room + s_list.room
                    gtc_room = gtc_room + s_list.c_room
                    gt_pax = gt_pax + s_list.pax
                    gt_logis =  to_decimal(gt_logis) + to_decimal(s_list.logis)
                    gt_avrgrate =  to_decimal(gt_avrgrate) + to_decimal(s_list.avrgrate)
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis =  to_decimal(gtm_logis) + to_decimal(s_list.m_logis)
                    gtm_avrgrate =  to_decimal(gtm_avrgrate) + to_decimal(s_list.m_avrgrate)
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis =  to_decimal(gty_logis) + to_decimal(s_list.y_logis)
                    gty_avrgrate =  to_decimal(gty_avrgrate) + to_decimal(s_list.y_avrgrate)


        create_output2()


    def create_output():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        tot_room:int = 0
        i:int = 0
        curr_rmtype:string = ""
        curr_gastnr:int = -1
        Sbuff = S_list
        sbuff_data = s_list_data

        for s_list in query(s_list_data, sort_by=[("compname",False),("segment",False)]):
            i = i + 1

            if curr_gastnr != s_list.gastnr and curr_gastnr != -1:
                create_sub()

            if curr_gastnr != s_list.gastnr:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.compname

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub2()
            curr_gastnr = s_list.gastnr
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

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

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        tot_room:int = 0
        i:int = 0
        curr_segment:int = 0
        Sbuff = S_list
        sbuff_data = s_list_data

        for s_list in query(s_list_data, sort_by=[("segment",False),("compname",False)]):
            i = i + 1

            if curr_segment != s_list.segm_code and curr_segment != 0:
                create_sub()

            if curr_segment != s_list.segm_code:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.segment

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub2()
            curr_segment = s_list.segm_code
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

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

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        tot_room:int = 0
        i:int = 0
        curr_segment:int = 0
        Sbuff = S_list
        sbuff_data = s_list_data

        for s_list in query(s_list_data, sort_by=[("segment",False),("compname",False)]):
            i = i + 1

            if curr_segment != s_list.segm_grup and curr_segment != 0:
                create_sub()

            if curr_segment != s_list.segm_grup:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                rmcomp_segm_list.flag = 1
                rmcomp_segm_list.segment = s_list.segment1

            if price_decimal == 0:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub1()
            else:
                rmcomp_segm_list = Rmcomp_segm_list()
                rmcomp_segm_list_data.append(rmcomp_segm_list)

                count_sub2()
            curr_segment = s_list.segm_grup
        create_sub()
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

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

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

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


        proz =  to_decimal(proz) + to_decimal(s_list.proz)
        m_proz =  to_decimal(m_proz) + to_decimal(s_list.m_proz)
        y_proz =  to_decimal(y_proz) + to_decimal(s_list.y_proz)
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz =  to_decimal(st_proz) + to_decimal(s_list.proz)
        st_logis =  to_decimal(st_logis) + to_decimal(s_list.logis)
        st_avrgrate =  to_decimal(st_avrgrate) + to_decimal(s_list.avrgrate)
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz =  to_decimal(stm_proz) + to_decimal(s_list.m_proz)
        stm_logis =  to_decimal(stm_logis) + to_decimal(s_list.m_logis)
        stm_avrgrate =  to_decimal(stm_avrgrate) + to_decimal(s_list.m_avrgrate)
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz =  to_decimal(sty_proz) + to_decimal(s_list.y_proz)
        sty_logis =  to_decimal(sty_logis) + to_decimal(s_list.y_logis)
        sty_avrgrate =  to_decimal(sty_avrgrate) + to_decimal(s_list.y_avrgrate)


    def count_sub2():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

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


        proz =  to_decimal(proz) + to_decimal(s_list.proz)
        m_proz =  to_decimal(m_proz) + to_decimal(s_list.m_proz)
        y_proz =  to_decimal(y_proz) + to_decimal(s_list.y_proz)
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz =  to_decimal(st_proz) + to_decimal(s_list.proz)
        st_logis =  to_decimal(st_logis) + to_decimal(s_list.logis)
        st_avrgrate =  to_decimal(st_avrgrate) + to_decimal(s_list.avrgrate)
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz =  to_decimal(stm_proz) + to_decimal(s_list.m_proz)
        stm_logis =  to_decimal(stm_logis) + to_decimal(s_list.m_logis)
        stm_avrgrate =  to_decimal(stm_avrgrate) + to_decimal(s_list.m_avrgrate)
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz =  to_decimal(sty_proz) + to_decimal(s_list.y_proz)
        sty_logis =  to_decimal(sty_logis) + to_decimal(s_list.y_logis)
        sty_avrgrate =  to_decimal(sty_avrgrate) + to_decimal(s_list.y_avrgrate)


    def create_sub():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data

        ind:int = 0
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

        rmcomp_segm_list.flag = 1
        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

        rmcomp_segm_list.flag = 2
        st_avrgrate =  to_decimal("0")

        if (st_room - stc_room) != 0:
            st_avrgrate =  to_decimal(st_logis) / to_decimal((st_room) - to_decimal(stc_room))
        stm_avrgrate =  to_decimal("0")

        if (stm_room - stmc_room) != 0:
            stm_avrgrate =  to_decimal(stm_logis) / to_decimal((stm_room) - to_decimal(stmc_room))
        sty_avrgrate =  to_decimal("0")

        if (sty_room - styc_room) != 0:
            sty_avrgrate =  to_decimal(sty_logis) / to_decimal((sty_room) - to_decimal(styc_room))

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
        rmcomp_segm_list_data.append(rmcomp_segm_list)

        init_val()


    def init_val():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, rm_serv, rm_vat, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date


        nonlocal rmcomp_segm_list, s_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data


        st_room = 0
        st_pax = 0
        st_proz =  to_decimal("0")
        st_logis =  to_decimal("0")
        st_avrgrate =  to_decimal("0")
        stm_room = 0
        stm_pax = 0
        stm_proz =  to_decimal("0")
        stm_logis =  to_decimal("0")
        stm_avrgrate =  to_decimal("0")
        sty_room = 0
        sty_pax = 0
        sty_proz =  to_decimal("0")
        sty_logis =  to_decimal("0")
        sty_avrgrate =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    if sorttype == 0 or sorttype == 1:
        create_umsatz()
    else:
        create_umsatz2()

    return generate_output()