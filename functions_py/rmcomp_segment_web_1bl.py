#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 5/8/2025
# loadRmcompSegmentList1
# debug, data output beda.
# Optimasi
# Rd 8-9-2025, beda data
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Guest, Genstat, Zimmer, Segment, Arrangement, Artikel, Queasy, Res_line, Reservation, Bill_line, Reslin_queasy, Umsatz

def rmcomp_segment_web_1bl(pvilanguage:int, sorttype:int, cardtype:int, incl_comp:bool, mi_ftd:bool, f_date:date, t_date:date, to_date:date, sales_id:string, vhp_limited:bool):

    prepare_cache ([Htparam, Guest, Genstat, Arrangement, Artikel, Queasy, Res_line, Reservation, Reslin_queasy, Umsatz])

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
    revenue:Decimal = to_decimal("0.0")
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
    gty_revenue:Decimal = to_decimal("0.0")
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
    sty_revenue:Decimal = to_decimal("0.0")
    rmrevsubt:Decimal = to_decimal("0.0")
    rm_serv:bool = False
    rm_vat:bool = False
    othrev:Decimal = to_decimal("0.0")
    datum:date = None
    ci_date:date = None
    mm:int = 0
    yy:int = 0
    from_date:date = None
    fdate:date = None
    beg_date:date = None
    d1:date = None
    d2:date = None
    tdate:date = None
    tmpdate:date = None
    lvcarea:string = "rmcomp-segment"
    htparam = guest = genstat = zimmer = segment = arrangement = artikel = queasy = res_line = reservation = bill_line = reslin_queasy = umsatz = None

    rmcomp_segm_list = s_list = tmp_room = t_list = sbuff = sbuff = sbuff = None

    rmcomp_segm_list_data, Rmcomp_segm_list = create_model("Rmcomp_segm_list", {"flag":int, "segment":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string, "rmnite1":string, "rmrev1":string, "rmnite":string, "rmrev":string, "segm_code":int, "gastnr":int, "revenue":string})
    s_list_data, S_list = create_model("S_list", {"segm_code":int, "segm_grup":int, "segment":string, "segment1":string, "gastnr":int, "compname":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "revenue":Decimal})
    tmp_room_data, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":string, "flag":int})
    t_list_data, T_list = create_model("T_list", {"gastnr":int, "logis_guaranteed":Decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":Decimal, "pax_tentative":int, "room_tentative":int, "mlogis_guaranteed":Decimal, "mpax_guaranteed":int, "mroom_guaranteed":int, "mlogis_tentative":Decimal, "mpax_tentative":int, "mroom_tentative":int, "ylogis_guaranteed":Decimal, "ypax_guaranteed":int, "yroom_guaranteed":int, "ylogis_tentative":Decimal, "ypax_tentative":int, "yroom_tentative":int, "resstatus":int, "zipreis":Decimal})

    db_session = local_storage.db_session

    # Rd 8/9/2025
    sales_id = sales_id.strip()

    def generate_output():
        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        return {"rmcomp-segm-list": rmcomp_segm_list_data, "s-list": s_list_data}

    def create_umsatz(date1:date, date2:date):

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, from_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        rmrev:Decimal = to_decimal("0.0")
        otherrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        mm:int = 0
        yy:int = 0
        tdatum:date = None
        do_dat:bool = False
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        bydate:int = 0
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
        revenue =  to_decimal("0")
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
        gty_revenue =  to_decimal("0")

        if mi_ftd:

            if date2 < (ci_date - timedelta(days=1)):
                d2 = date2
            else:
                d2 = (ci_date - timedelta(days=1))
        else:
            d2 = date2
        mm = get_month(d2)
        yy = get_year(d2)
        f_date = date_mdy(get_month(d2) , 1, get_year(d2))
        beg_date = date_mdy(get_month(date1) , 1, yy)

        if date1 != ci_date and date1 >= ci_date:
            d1 = date1
        else:
            d1 = date1
        mm = get_month(d2)


        yy = get_year(d2)
        f_date = date_mdy(get_month(d2) , 1, get_year(d2))
        # tmpdate = d1 + timedelta(days=1)
        bydate = (d2 - d1).days
        tdate = d2

        print("Bydate:", bydate, d1, d2)
        while bydate != 0:
            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            # for genstat.datum, genstat.zinr, genstat.segmentcode, genstat.resstatus, genstat.gastnr, genstat.argt, \
            #     genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.zipreis, genstat.gratis, genstat.kind1, \
            #     genstat.kind2, genstat._recid, guest.karteityp, guest.phonetik3, guest.name, guest.vorname1, guest._recid \
            #         in db_session.query(Genstat.datum, Genstat.zinr, Genstat.segmentcode, Genstat.resstatus, Genstat.gastnr, \
            #                             Genstat.argt, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.zipreis, \
            #                             Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.karteityp, \
            #                             Guest.phonetik3, Guest.name, Guest.vorname1, Guest._recid)\
            #                         .join(Guest,(Guest.gastnr == Genstat.gastnr))\
            #                         .filter(
            #                             (Genstat.datum == tdate) & 
            #                             (Genstat.zinr != "") & 
            #                             (Genstat.gastnr != 0) & 
            #                             (Genstat.resstatus != 13) & 
            #                             (Genstat.segmentcode != 0) & 
            #                             (Genstat.res_logic[inc_value(1)]))\
            #                         .order_by(Guest.name, Guest.gastnr).all():
            
            recs = db_session.query(Genstat.datum, Genstat.zinr, Genstat.segmentcode, Genstat.resstatus, Genstat.gastnr, \
                                        Genstat.argt, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.zipreis, \
                                        Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.karteityp, \
                                        Guest.phonetik3, Guest.name, Guest.vorname1, Guest._recid)\
                                    .join(Guest,(Guest.gastnr == Genstat.gastnr))\
                                    .filter(
                                        (Genstat.datum == tdate) & 
                                        (Genstat.zinr != "") & 
                                        (Genstat.gastnr != 0) & 
                                        (Genstat.resstatus != 13) & 
                                        (Genstat.segmentcode != 0) & 
                                        (Genstat.res_logic[inc_value(1)]))\
                                    .order_by(Guest.name, Guest.gastnr).all()
            
            for genstat.datum, genstat.zinr, genstat.segmentcode, genstat.resstatus, genstat.gastnr, genstat.argt, \
                genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.zipreis, genstat.gratis, genstat.kind1, \
                genstat.kind2, genstat._recid, guest.karteityp, guest.phonetik3, guest.name, guest.vorname1, guest._recid \
                    in recs:
                
                # if genstat_obj_list.get(genstat._recid):
                #     continue
                # else:
                #     genstat_obj_list[genstat._recid] = True

                if genstat.datum != tdatum:
                    tdatum = genstat.datum
                    do_dat = True
                else:
                    do_dat = False

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

                if do_it and sales_id != None and sales_id != "":
                    do_it = guest.phonetik3 == trim(entry(0, sales_id, "-"))

                if do_it:

                    if genstat.zipreis == 0:

                        if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                            if genstat.datum == d2:
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

                    if mi_ftd and d2 < ci_date:

                        if genstat.datum == d2:

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

                        if get_month(genstat.datum) == mm:

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

                        if genstat.datum >= d1 and genstat.datum <= d2:

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


                                s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)
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


                                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)

                    elif not mi_ftd and d2 < ci_date:

                        if genstat.datum == to_date:

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


                                s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)
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


                                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)

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
                    gty_revenue =  to_decimal("0")

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
                        gty_revenue =  to_decimal(gty_revenue) + to_decimal(s_list.revenue)

            tdate = tdate - timedelta(days=1)
            bydate = bydate - 1


    def create_umsatz2(date1:date, date2:date):

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        rmrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        beg_date:date = None
        tdatum:date = None
        do_dat:bool = False
        bydate:int = 0
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
        revenue =  to_decimal("0")
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
        gty_revenue =  to_decimal("0")

        if mi_ftd:

            if date2 < (ci_date - timedelta(days=1)):
                d2 = date2
            else:
                d2 = (ci_date - timedelta(days=1))
        else:
            d2 = date2
        mm = get_month(d2)
        yy = get_year(d2)
        f_date = date_mdy(get_month(d2) , 1, get_year(d2))
        beg_date = date_mdy(get_month(date1) , 1, yy)

        if date1 != ci_date and date1 >= ci_date:
            d1 = date1
        else:
            d1 = date1
        mm = get_month(d2)


        yy = get_year(d2)
        f_date = date_mdy(get_month(d2) , 1, get_year(d2))
        tmpdate = d1 + timedelta(days=1)
        bydate = (d2 - d1).days
        tdate = d2
        while bydate != 0:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.datum, genstat.zinr, genstat.segmentcode, genstat.resstatus, genstat.gastnr, genstat.argt, genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.zipreis, genstat.gratis, genstat.kind1, genstat.kind2, genstat._recid, guest.karteityp, guest.phonetik3, guest.name, guest.vorname1, guest._recid in db_session.query(Genstat.datum, Genstat.zinr, Genstat.segmentcode, Genstat.resstatus, Genstat.gastnr, Genstat.argt, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.zipreis, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.karteityp, Guest.phonetik3, Guest.name, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                     (Genstat.datum == tdate) & (Genstat.zinr != "") & (Genstat.gastnr != 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.datum != tdatum:
                    tdatum = genstat.datum
                    do_dat = True
                else:
                    do_dat = False

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

                if do_it and sales_id != None and sales_id != "":
                    do_it = guest.phonetik3 == trim(entry(0, sales_id, "-"))

                if do_it:

                    if genstat.zipreis == 0:

                        if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                            if genstat.datum == date2:
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

                    if mi_ftd and d2 < ci_date:

                        if genstat.datum == d1:

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

                        if get_month(genstat.datum) == mm:

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

                        if genstat.datum >= d1 and genstat.datum <= d2:

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


                                s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)
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


                                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)

                    elif not mi_ftd and d2 < ci_date:

                        if genstat.datum == to_date:

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


                                s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)
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


                                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(genstat.logis)

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
                    gty_revenue =  to_decimal("0")

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
                        gty_revenue =  to_decimal(gty_revenue) + to_decimal(s_list.revenue)


            tdate = tdate - timedelta(days=1)
            bydate = bydate - 1


    def create_fcast(date1:date, date2:date):

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, ci_date, from_date, d1, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        rmrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        mm:int = 0
        yy:int = 0
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        fdate:date = None
        beg_date:date = None
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        t_pax:int = 0
        a:int = 0
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        rline1 = None
        gmember = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Gmember =  create_buffer("Gmember",Guest)
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
        gty_revenue =  to_decimal("0")


        mm = get_month(date2)
        yy = get_year(date2)
        f_date = date_mdy(get_month(date2) , 1, get_year(date2))

        if date1 < ci_date:
            d1 = ci_date
        else:
            d1 = date1
        datum1 = d1

        if date2 <= (ci_date - timedelta(days=1)):
            d2 = ci_date
        else:
            d2 = date2

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.resnr, res_line.zinr, res_line.arrangement, res_line.reslinnr, res_line.resstatus, res_line.gastnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line._recid, res_line.zimmeranz, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.zipreis, res_line.gratis, guest.karteityp, guest.phonetik3, guest.name, guest.vorname1, guest._recid in db_session.query(Res_line.resnr, Res_line.zinr, Res_line.arrangement, Res_line.reslinnr, Res_line.resstatus, Res_line.gastnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line._recid, Res_line.zimmeranz, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.zipreis, Res_line.gratis, Guest.karteityp, Guest.phonetik3, Guest.name, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > d2)) & (not_ (Res_line.abreise < d1))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Guest.name, Guest.gastnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:
                dayuse_flag = True

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line

            if cardtype < 3:
                do_it = guest.karteityp == cardtype
            else:
                do_it = True

            if not incl_comp and res_line.zipreis == 0:

                if (res_line.gratis > 0):
                    do_it = False

                if (res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis == 0) and res_line.resstatus != 13:
                    do_it = False

            if do_it and sales_id != None and sales_id != "":
                do_it = guest.phonetik3 == trim(entry(0, sales_id, "-"))

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                if datum != None:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.gastnr = res_line.gastnr
                t_list.resstatus = res_line.resstatus

                s_list = query(s_list_data, filters=(lambda s_list: s_list.gastnr == res_line.gastnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.gastnr = res_line.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma
                    s_list.segm_code = reservation.segmentcode

                segment = get_cache (Segment, {"segmentcode": [(eq, s_list.segm_code)]})

                if segment:
                    s_list.segment = segment.bezeich
                else:
                    s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")

                if res_line.ankunft >= d1:
                    datum1 = res_line.ankunft
                else:
                    datum1 = d1

                if res_line.abreise <= d2:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = d2
                for datum in date_range(datum1,datum2) :
                    a = a + 1
                    t_pax = res_line.erwachs
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")
                    tot_rmrev =  to_decimal("0")


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, from_date))

                    if tot_rmrev == 0:
                        local_net_lodg =  to_decimal("0")
                        net_lodg =  to_decimal("0")


                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal((tot_rmrev) * to_decimal(res_line.zimmeranz))
                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(local_net_lodg)

                    if res_line.zipreis == 0:

                        if (res_line.gratis > 0) or ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis == 0) and res_line.resstatus != 13):

                            if datum == date2:
                                c_room = c_room + 1

                            if get_month(datum) == mm and get_year(datum) == yy:
                                mc_room = mc_room + 1
                                yc_room = yc_room + 1

                    if mi_ftd and datum == d1 and from_date >= d1 and consider_it:
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                        logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                        s_list.room = s_list.room + res_line.zimmeranz
                        room = room + res_line.zimmeranz
                        s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                                logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                                s_list.room = s_list.room + res_line.zimmeranz
                                room = room + res_line.zimmeranz
                                s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                    if not mi_ftd and datum == d2 and consider_it:
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                        logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                        s_list.room = s_list.room + res_line.zimmeranz
                        room = room + res_line.zimmeranz
                        s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                                logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                                s_list.room = s_list.room + res_line.zimmeranz
                                room = room + res_line.zimmeranz
                                s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                    if mi_ftd and get_month(datum) == get_month(d2) and get_year(datum) == get_year(d2):
                        s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                        m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                        s_list.m_room = s_list.m_room + res_line.zimmeranz
                        m_room = m_room + res_line.zimmeranz
                        s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                                m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                                s_list.m_room = s_list.m_room + res_line.zimmeranz
                                m_room = m_room + res_line.zimmeranz
                                s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                    if mi_ftd and datum >= d1 and datum <= d2:
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                        y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                        s_list.y_room = s_list.y_room + res_line.zimmeranz
                        y_room = y_room + res_line.zimmeranz
                        s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                                y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                                s_list.y_room = s_list.y_room + res_line.zimmeranz
                                y_room = y_room + res_line.zimmeranz
                                s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                    if not mi_ftd and get_month(datum) == get_month(d2) and get_year(datum) == get_year(d2):
                        s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                        m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                        s_list.m_room = s_list.m_room + res_line.zimmeranz
                        m_room = m_room + res_line.zimmeranz
                        s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                                m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                                s_list.m_room = s_list.m_room + res_line.zimmeranz
                                m_room = m_room + res_line.zimmeranz
                                s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                    if not mi_ftd and datum >= d1 and datum <= d2:
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                        y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                        s_list.y_room = s_list.y_room + res_line.zimmeranz
                        y_room = y_room + res_line.zimmeranz
                        s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                                y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                                s_list.y_room = s_list.y_room + res_line.zimmeranz
                                y_room = y_room + res_line.zimmeranz
                                s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

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
                gty_revenue =  to_decimal("0")

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
                    gty_revenue =  to_decimal(gty_revenue) + to_decimal(s_list.revenue)


    def create_fcast2(date1:date, date2:date):

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, ci_date, from_date, d1, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        rmrev:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        mm:int = 0
        yy:int = 0
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
        status_vat:bool = False
        fdate:date = None
        beg_date:date = None
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        t_pax:int = 0
        a:int = 0
        dayuse_flag:bool = False
        consider_it:bool = False
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        rline1 = None
        gmember = None
        Rline1 =  create_buffer("Rline1",Res_line)
        Gmember =  create_buffer("Gmember",Guest)
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
        gty_revenue =  to_decimal("0")


        mm = get_month(date2)
        yy = get_year(date2)
        f_date = date_mdy(get_month(date2) , 1, get_year(date2))

        if date1 < ci_date:
            d1 = ci_date
        else:
            d1 = date1
        datum1 = d1

        if date2 <= (ci_date - timedelta(days=1)):
            d2 = ci_date
        else:
            d2 = date2

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.resnr, res_line.zinr, res_line.arrangement, res_line.reslinnr, res_line.resstatus, res_line.gastnr, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line._recid, res_line.zimmeranz, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.zipreis, res_line.gratis, guest.karteityp, guest.phonetik3, guest.name, guest.vorname1, guest._recid in db_session.query(Res_line.resnr, Res_line.zinr, Res_line.arrangement, Res_line.reslinnr, Res_line.resstatus, Res_line.gastnr, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line._recid, Res_line.zimmeranz, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.zipreis, Res_line.gratis, Guest.karteityp, Guest.phonetik3, Guest.name, Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > d2)) & (not_ (Res_line.abreise < d1))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Guest.name, Guest.gastnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:
                dayuse_flag = True

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line

            if cardtype < 3:
                do_it = guest.karteityp == cardtype
            else:
                do_it = True

            if not incl_comp and res_line.zipreis == 0:

                if (res_line.gratis > 0):
                    do_it = False

                if (res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis == 0) and res_line.resstatus != 13:
                    do_it = False

            if do_it and sales_id != None and sales_id != "":
                do_it = guest.phonetik3 == trim(entry(0, sales_id, "-"))

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if do_it:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.gastnr = res_line.gastnr
                t_list.resstatus = res_line.resstatus

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:

                    queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, segment.segmentgrup)]})

                s_list = query(s_list_data, filters=(lambda s_list: s_list.gastnr == res_line.gastnr and s_list.segm_code == segment.segmentcode and s_list.segm_grup == queasy.number1), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.gastnr = res_line.gastnr
                    s_list.compname = guest.name + " " + guest.vorname1 +\
                            " " + guest.anrede1 + guest.anredefirma

                    if segment:
                        s_list.segment = segment.bezeich
                        s_list.segm_code = reservation.segmentcode
                        s_list.segm_grup = segment.segmentgrup


                    else:
                        s_list.segment = translateExtended ("UNKNOWN", lvcarea, "")

                    if queasy:
                        s_list.segment1 = queasy.char3
                    else:
                        s_list.segment1 = translateExtended ("UNKNOWN", lvcarea, "")

                if res_line.ankunft >= d1:
                    datum1 = res_line.ankunft
                else:
                    datum1 = d1

                if res_line.abreise <= d2:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = d2
                for datum in date_range(datum1,datum2) :
                    a = a + 1
                    t_pax = res_line.erwachs
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    consider_it = True

                    if res_line.zimmerfix:

                        rline1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 8)],"abreise": [(gt, datum)]})

                        if rline1:
                            consider_it = False
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")
                    tot_rmrev =  to_decimal("0")


                    net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, from_date))

                    if tot_rmrev == 0:
                        local_net_lodg =  to_decimal("0")
                        net_lodg =  to_decimal("0")


                    t_list.zipreis =  to_decimal(t_list.zipreis) + to_decimal((tot_rmrev) * to_decimal(res_line.zimmeranz))
                    s_list.revenue =  to_decimal(s_list.revenue) + to_decimal(local_net_lodg)

                    if res_line.zipreis == 0:

                        if (res_line.gratis > 0) or ((res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis == 0) and res_line.resstatus != 13):

                            if datum == d2:
                                c_room = c_room + 1

                            if get_month(datum) == mm and get_year(datum) == yy:
                                mc_room = mc_room + 1
                                yc_room = yc_room + 1

                    if mi_ftd and datum == d2 and from_date >= d1 and consider_it:
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                        logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                        s_list.room = s_list.room + res_line.zimmeranz
                        room = room + res_line.zimmeranz
                        s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                                logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                                s_list.room = s_list.room + res_line.zimmeranz
                                room = room + res_line.zimmeranz
                                s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                    if not mi_ftd and datum == d2 and consider_it:
                        s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                        logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                        s_list.room = s_list.room + res_line.zimmeranz
                        room = room + res_line.zimmeranz
                        s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.logis =  to_decimal(s_list.logis) + to_decimal(local_net_lodg)
                                logis =  to_decimal(logis) + to_decimal(local_net_lodg)
                                s_list.room = s_list.room + res_line.zimmeranz
                                room = room + res_line.zimmeranz
                                s_list.pax = s_list.pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                pax = pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                avrgrate =  to_decimal(avrgrate) + to_decimal(t_list.zipreis)

                    if not mi_ftd and get_year(datum) == get_year(d2):

                        if get_month(datum) == get_month(d2) and get_year(datum) == get_year(d2):
                            s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                            m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                            s_list.m_room = s_list.m_room + res_line.zimmeranz
                            m_room = m_room + res_line.zimmeranz
                            s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)


                            s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                            y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                            s_list.y_room = s_list.y_room + res_line.zimmeranz
                            y_room = y_room + res_line.zimmeranz
                            s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:

                                if get_month(datum) == get_month(d2) and get_year(datum) == get_year(d2):
                                    s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                                    m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                                    s_list.m_room = s_list.m_room + res_line.zimmeranz
                                    m_room = m_room + res_line.zimmeranz
                                    s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz
                                    m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz
                                    m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)


                                    s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                                    y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                                    s_list.y_room = s_list.y_room + res_line.zimmeranz
                                    y_room = y_room + res_line.zimmeranz
                                    s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz
                                    y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz
                                    y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                    if mi_ftd and get_month(datum) == get_month(d2) and get_year(datum) == get_year(d2):
                        s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                        m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                        s_list.m_room = s_list.m_room + res_line.zimmeranz
                        m_room = m_room + res_line.zimmeranz
                        s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(local_net_lodg)
                                m_logis =  to_decimal(m_logis) + to_decimal(local_net_lodg)
                                s_list.m_room = s_list.m_room + res_line.zimmeranz
                                m_room = m_room + res_line.zimmeranz
                                s_list.m_pax = s_list.m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_pax = m_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(t_list.zipreis)

                    if mi_ftd and datum >= d1 and datum <= d2:
                        s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                        y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                        s_list.y_room = s_list.y_room + res_line.zimmeranz
                        y_room = y_room + res_line.zimmeranz
                        s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

                        if not incl_comp:

                            if res_line.zipreis == 0:
                                s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(local_net_lodg)
                                y_logis =  to_decimal(y_logis) + to_decimal(local_net_lodg)
                                s_list.y_room = s_list.y_room + res_line.zimmeranz
                                y_room = y_room + res_line.zimmeranz
                                s_list.y_pax = s_list.y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_pax = y_pax + (t_pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(t_list.zipreis)

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
                gty_revenue =  to_decimal("0")

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
                    gty_revenue =  to_decimal(gty_revenue) + to_decimal(s_list.revenue)


    def create_output():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
        gt_avrgrate =  to_decimal("0")

        if (gt_room - gtc_room) != 0:
            gt_avrgrate =  to_decimal(gt_logis) / to_decimal((gt_room) - to_decimal(gtc_room))
        gtm_avrgrate =  to_decimal("0")

        if (gtm_room - gtmc_room) != 0:
            gtm_avrgrate =  to_decimal(gtm_logis) / to_decimal((gtm_room) - to_decimal(gtmc_room))
        gty_avrgrate =  to_decimal("0")

        if (gty_room - gtyc_room) != 0:
            gty_avrgrate =  to_decimal(gty_logis) / to_decimal((gty_room) - to_decimal(gtyc_room))
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
        rmcomp_segm_list.revenue = to_string(gty_revenue, "->>,>>>,>>>,>>>,>>9")


    def create_output1():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
        gt_avrgrate =  to_decimal("0")

        if (gt_room - gtc_room) != 0:
            gt_avrgrate =  to_decimal(gt_logis) / to_decimal((gt_room) - to_decimal(gtc_room))
        gtm_avrgrate =  to_decimal("0")

        if (gtm_room - gtmc_room) != 0:
            gtm_avrgrate =  to_decimal(gtm_logis) / to_decimal((gtm_room) - to_decimal(gtmc_room))
        gty_avrgrate =  to_decimal("0")

        if (gty_room - gtyc_room) != 0:
            gty_avrgrate =  to_decimal(gty_logis) / to_decimal((gty_room) - to_decimal(gtyc_room))
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
        rmcomp_segm_list.revenue = to_string(gty_revenue, "->>,>>>,>>>,>>>,>>9")


    def create_output2():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
        gt_avrgrate =  to_decimal("0")

        if (gt_room - gtc_room) != 0:
            gt_avrgrate =  to_decimal(gt_logis) / to_decimal((gt_room) - to_decimal(gtc_room))
        gtm_avrgrate =  to_decimal("0")

        if (gtm_room - gtmc_room) != 0:
            gtm_avrgrate =  to_decimal(gtm_logis) / to_decimal((gtm_room) - to_decimal(gtmc_room))
        gty_avrgrate =  to_decimal("0")

        if (gty_room - gtyc_room) != 0:
            gty_avrgrate =  to_decimal(gty_logis) / to_decimal((gty_room) - to_decimal(gtyc_room))
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
        rmcomp_segm_list.revenue = to_string(gty_revenue, "->>,>>>,>>>,>>>,>>9")


    def count_sub1():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
        rmcomp_segm_list.revenue = to_string(s_list.revenue, "->>,>>>,>>>,>>>,>>9")
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
        sty_revenue =  to_decimal(sty_revenue) + to_decimal(s_list.revenue)
        rmrevsubt =  to_decimal(rmrevsubt) + to_decimal(sty_revenue)


    def count_sub2():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
        rmcomp_segm_list.revenue = to_string(s_list.revenue, "->>>,>>>,>>>,>>9.99")
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
        sty_revenue =  to_decimal(sty_revenue) + to_decimal(s_list.revenue)
        rmrevsubt =  to_decimal(rmrevsubt) + to_decimal(sty_revenue)


    def create_sub():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

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
            rmcomp_segm_list.segment = translateExtended ("S u b T o t a l", lvcarea, "")
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
            rmcomp_segm_list.revenue = to_string(sty_revenue, "->>,>>>,>>>,>>>,>>9")


        else:
            rmcomp_segm_list.segment = translateExtended ("S u b T o t a l", lvcarea, "")
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
            rmcomp_segm_list.revenue = to_string(sty_revenue, "->>>,>>>,>>>,>>9.99")


        rmcomp_segm_list = Rmcomp_segm_list()
        rmcomp_segm_list_data.append(rmcomp_segm_list)

        init_val()


    def calc_othrev(datum:date):

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data

        othrev = to_decimal("0.0")
        i:int = 0
        max_i:int = 0
        art_list:List[int] = create_empty_list(200,0)
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (othrev)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        for i in range(1,max_i + 1) :

            artikel = get_cache (Artikel, {"artnr": [(eq, art_list[i - 1])],"departement": [(eq, 0)]})

            if artikel:
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    othrev =  to_decimal(othrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

        return generate_inner_output()


    def init_val():

        nonlocal rmcomp_segm_list_data, s_list_data, price_decimal, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, revenue, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, gty_revenue, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, rmrevsubt, rm_serv, rm_vat, othrev, datum, ci_date, mm, yy, from_date, fdate, beg_date, d1, d2, tdate, tmpdate, lvcarea, htparam, guest, genstat, zimmer, segment, arrangement, artikel, queasy, res_line, reservation, bill_line, reslin_queasy, umsatz
        nonlocal pvilanguage, sorttype, cardtype, incl_comp, mi_ftd, f_date, t_date, to_date, sales_id, vhp_limited


        nonlocal rmcomp_segm_list, s_list, tmp_room, t_list, sbuff, sbuff, sbuff
        nonlocal rmcomp_segm_list_data, s_list_data, tmp_room_data, t_list_data


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
        sty_revenue =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if mi_ftd:
        from_date = f_date
        to_date = t_date
        mm = get_month(to_date)
        yy = get_year(to_date)

    else:
        mm = get_month(to_date)
        yy = get_year(to_date)
        from_date = date_mdy(1, 1, yy)
        f_date = date_mdy(get_month(t_date) , 1, get_year(t_date))

    print("From/To:", from_date, to_date, ci_date)
    if (from_date < ci_date) and (to_date < ci_date):

        if sorttype == 0 or sorttype == 1:
            create_umsatz(from_date, to_date)

            if sorttype == 0:
                create_output()
            else:
                create_output1()
        else:
            create_umsatz2(from_date, to_date)
            create_output2()

    elif (from_date < ci_date) and (to_date >= ci_date):
        if sorttype == 0 or sorttype == 1:
            tmpdate = ci_date - timedelta(days=1)
            create_umsatz(from_date, tmpdate)
            create_fcast(ci_date, to_date)

            if sorttype == 0:
                create_output()
            else:
                create_output1()
        else:
            tmpdate = ci_date - timedelta(days=1)
            create_umsatz2(from_date, tmpdate)
            create_fcast2(ci_date, to_date)
            create_output2()

    elif (from_date >= ci_date) and (to_date >= ci_date):
        if sorttype == 0 or sorttype == 1:
            create_fcast(from_date, to_date)

            if sorttype == 0:
                create_output()
            else:
                create_output1()
        else:
            create_fcast2(from_date, to_date)
            create_output2()

    return generate_output()