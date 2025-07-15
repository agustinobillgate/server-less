#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Guest, Genstat, Zimmer, Zimkateg, Segment

def rmcat_segment_webbl(pvilanguage:int, cardtype:int, to_date:date, f_date:date, t_date:date, mi_ftd:bool, incl_comp:bool):

    prepare_cache ([Htparam, Guest, Genstat, Zimmer, Zimkateg, Segment])

    rmcat_segm_list_data = []
    s_list_data = []
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
    price_decimal:int = 0
    count_i:int = 0
    lvcarea:string = "rmcat-segment-web"
    queasy = htparam = guest = genstat = zimmer = zimkateg = segment = None

    rmcat_segm_list = s_list = bqueasy = tqueasy = sbuff = None

    rmcat_segm_list_data, Rmcat_segm_list = create_model("Rmcat_segm_list", {"flag":int, "segment":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string, "rmnite1":string, "rmrev1":string, "rmnite":string, "rmrev":string, "rmcat":string, "segm_code":int})
    s_list_data, S_list = create_model("S_list", {"segm_code":int, "segment":string, "catnr":int, "rmcat":string, "cat_bez":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data

        return {"rmcat-segm-list": rmcat_segm_list_data, "s-list": s_list_data}

    def create_umsatz():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:string = ""
        curr_code:string = ""
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


        rmcat_segm_list_data.clear()
        s_list_data.clear()

        if mi_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.zinr, genstat.zikatnr, genstat.segmentcode, genstat.resstatus, genstat.datum, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.kind3, genstat.logis, genstat.ratelocal, genstat.zipreis, genstat._recid, guest.karteityp, guest._recid in db_session.query(Genstat.zinr, Genstat.zikatnr, Genstat.segmentcode, Genstat.resstatus, Genstat.datum, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.logis, Genstat.ratelocal, Genstat.zipreis, Genstat._recid, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr != "") & (Genstat.gastnr != 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

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

                s_list = query(s_list_data, filters=(lambda s_list: s_list.catnr == zimmer.zikatnr and s_list.segm_code == genstat.segmentcode), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.catnr = zimmer.zikatnr
                    s_list.rmcat = zimkateg.kurzbez
                    s_list.cat_bez = zimkateg.bezeichnung
                    s_list.segm_code = genstat.segmentcode
                    s_list.segment = segment.bezeich

                if genstat.datum == to_date:

                    if genstat.resstatus != 13:
                        s_list.room = s_list.room + 1
                        room = room + 1


                    s_list.pax = s_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                    s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                    pax = pax + genstat.erwachs
                    logis =  to_decimal(logis) + to_decimal(genstat.logis)
                    avrgrate =  to_decimal(avrgrate) + to_decimal(genstat.ratelocal)

                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if genstat.resstatus != 13:
                        s_list.m_room = s_list.m_room + 1
                        m_room = m_room + 1


                    s_list.m_pax = s_list.m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                    s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                    m_pax = m_pax + genstat.erwachs
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                    m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(genstat.ratelocal)

                if genstat.resstatus != 13:
                    s_list.y_room = s_list.y_room + 1
                    y_room = y_room + 1


                s_list.y_pax = s_list.y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
                y_pax = y_pax + genstat.erwachs
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)
                y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(genstat.ratelocal)

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
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis =  to_decimal(gtm_logis) + to_decimal(s_list.m_logis)
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis =  to_decimal(gty_logis) + to_decimal(s_list.y_logis)


        create_output()


    def create_output():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data

        tot_room:int = 0
        i:int = 0
        curr_rmtype:string = ""
        Sbuff = S_list
        sbuff_data = s_list_data

        for s_list in query(s_list_data, sort_by=[("cat_bez",False),("segment",False)]):
            i = i + 1

            if curr_rmtype != s_list.rmcat and curr_rmtype != "":
                create_sub()

            if curr_rmtype != s_list.rmcat:

                for sbuff in query(sbuff_data, filters=(lambda sbuff: sbuff.rmcat == s_list.rmcat)):
                    tot_room = tot_room + sbuff.room
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_data.append(rmcat_segm_list)

                rmcat_segm_list.flag = 1
                rmcat_segm_list.segment = s_list.cat_bez
                rmcat_segm_list.logis = translateExtended ("Total Rooms :", lvcarea, "") +\
                        " " + trim(to_string(tot_room, "->>9"))


                tot_room = 0

            if price_decimal == 0:
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_data.append(rmcat_segm_list)

                count_sub1()
            else:
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_data.append(rmcat_segm_list)

                count_sub2()
            curr_rmtype = s_list.rmcat
        create_sub()
        gt_avrgrate =  to_decimal("0")

        if (room - c_room) != 0:
            gt_avrgrate =  to_decimal(gt_logis) / to_decimal((gt_room) - to_decimal(gtc_room))
        gtm_avrgrate =  to_decimal("0")

        if (m_room - mc_room) != 0:
            gtm_avrgrate =  to_decimal(gtm_logis) / to_decimal((gtm_room) - to_decimal(gtmc_room))
        gty_avrgrate =  to_decimal("0")

        if (y_room - yc_room) != 0:
            gty_avrgrate =  to_decimal(gty_logis) / to_decimal((gty_room) - to_decimal(gtyc_room))
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_data.append(rmcat_segm_list)

        rmcat_segm_list.segment = translateExtended ("T o t a l", lvcarea, "")
        rmcat_segm_list.room = to_string(gt_room, "->>>,>>9")
        rmcat_segm_list.pax = to_string(gt_pax, "->>>,>>9")
        rmcat_segm_list.logis = to_string(gt_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.proz = "100.00"
        rmcat_segm_list.avrgrate = to_string(gt_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.m_room = to_string(gtm_room, "->>>,>>9")
        rmcat_segm_list.m_pax = to_string(gtm_pax, "->>>,>>9")
        rmcat_segm_list.m_logis = to_string(gtm_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.m_proz = "100.00"
        rmcat_segm_list.m_avrgrate = to_string(gtm_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.y_room = to_string(gty_room, "->>>,>>9")
        rmcat_segm_list.y_pax = to_string(gty_pax, "->>>,>>9")
        rmcat_segm_list.y_logis = to_string(gty_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.y_proz = "100.00"
        rmcat_segm_list.y_avrgrate = to_string(gty_avrgrate, "->>,>>>,>>>,>>>,>>9")


    def count_sub1():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data


        rmcat_segm_list.segment = s_list.segment
        rmcat_segm_list.room = to_string(s_list.room, "->>>,>>9")
        rmcat_segm_list.pax = to_string(s_list.pax, "->>>,>>9")
        rmcat_segm_list.logis = to_string(s_list.logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.proz = to_string(s_list.proz, ">>9.99")
        rmcat_segm_list.avrgrate = to_string(s_list.avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        rmcat_segm_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        rmcat_segm_list.m_logis = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        rmcat_segm_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        rmcat_segm_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        rmcat_segm_list.y_logis = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        rmcat_segm_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        rmcat_segm_list.rmrev = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        rmcat_segm_list.rmrev1 = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        rmcat_segm_list.rmcat = s_list.rmcat
        rmcat_segm_list.segm_code = s_list.segm_code


        proz =  to_decimal(proz) + to_decimal(s_list.proz)
        m_proz =  to_decimal(m_proz) + to_decimal(s_list.m_proz)
        y_proz =  to_decimal(y_proz) + to_decimal(s_list.y_proz)
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz =  to_decimal(st_proz) + to_decimal(s_list.proz)
        st_logis =  to_decimal(st_logis) + to_decimal(s_list.logis)
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz =  to_decimal(stm_proz) + to_decimal(s_list.m_proz)
        stm_logis =  to_decimal(stm_logis) + to_decimal(s_list.m_logis)
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz =  to_decimal(sty_proz) + to_decimal(s_list.y_proz)
        sty_logis =  to_decimal(sty_logis) + to_decimal(s_list.y_logis)


    def create_sub():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data

        ind:int = 0
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_data.append(rmcat_segm_list)

        rmcat_segm_list.flag = 1
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_data.append(rmcat_segm_list)

        rmcat_segm_list.flag = 2
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
            rmcat_segm_list.segment = translateExtended ("s u b T o t a l", lvcarea, "")
            rmcat_segm_list.room = to_string(st_room, "->>>,>>9")
            rmcat_segm_list.pax = to_string(st_pax, "->>>,>>9")
            rmcat_segm_list.logis = to_string(st_logis, "->>,>>>,>>>,>>>,>>9")
            rmcat_segm_list.proz = to_string(st_proz, ">>9.99")
            rmcat_segm_list.avrgrate = to_string(st_avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcat_segm_list.m_room = to_string(stm_room, "->>>,>>9")
            rmcat_segm_list.m_pax = to_string(stm_pax, "->>>,>>9")
            rmcat_segm_list.m_logis = to_string(stm_logis, "->>,>>>,>>>,>>>,>>9")
            rmcat_segm_list.m_proz = to_string(stm_proz, ">>9.99")
            rmcat_segm_list.m_avrgrate = to_string(stm_avrgrate, "->>,>>>,>>>,>>>,>>9")
            rmcat_segm_list.y_room = to_string(sty_room, "->>>,>>9")
            rmcat_segm_list.y_pax = to_string(sty_pax, "->>>,>>9")
            rmcat_segm_list.y_logis = to_string(sty_logis, "->>,>>>,>>>,>>>,>>9")
            rmcat_segm_list.y_proz = to_string(sty_proz, ">>9.99")
            rmcat_segm_list.y_avrgrate = to_string(sty_avrgrate, "->>,>>>,>>>,>>>,>>9")


        else:
            rmcat_segm_list.segment = translateExtended ("s u b T o t a l", lvcarea, "")
            rmcat_segm_list.room = to_string(st_room, "->>>,>>9")
            rmcat_segm_list.pax = to_string(st_pax, "->>>,>>9")
            rmcat_segm_list.logis = to_string(st_logis, "->>>,>>>,>>>,>>9.99")
            rmcat_segm_list.proz = to_string(st_proz, ">>9.99")
            rmcat_segm_list.avrgrate = to_string(st_avrgrate, "->>>,>>>,>>>,>>9.99")
            rmcat_segm_list.m_room = to_string(stm_room, "->>>,>>9")
            rmcat_segm_list.m_pax = to_string(stm_pax, "->>>,>>9")
            rmcat_segm_list.m_logis = to_string(stm_logis, "->>>,>>>,>>>,>>9.99")
            rmcat_segm_list.m_proz = to_string(stm_proz, ">>9.99")
            rmcat_segm_list.m_avrgrate = to_string(stm_avrgrate, "->>>,>>>,>>>,>>9.99")
            rmcat_segm_list.y_room = to_string(sty_room, "->>>,>>9")
            rmcat_segm_list.y_pax = to_string(sty_pax, "->>>,>>9")
            rmcat_segm_list.y_logis = to_string(sty_logis, "->>>,>>>,>>>,>>9.99")
            rmcat_segm_list.y_proz = to_string(sty_proz, ">>9.99")
            rmcat_segm_list.y_avrgrate = to_string(sty_avrgrate, "->>>,>>>,>>>,>>9.99")


        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_data.append(rmcat_segm_list)

        init_val()


    def init_val():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data


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


    def count_sub2():

        nonlocal rmcat_segm_list_data, s_list_data, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, count_i, lvcarea, queasy, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, cardtype, to_date, f_date, t_date, mi_ftd, incl_comp
        nonlocal bqueasy, tqueasy


        nonlocal rmcat_segm_list, s_list, bqueasy, tqueasy, sbuff
        nonlocal rmcat_segm_list_data, s_list_data


        rmcat_segm_list.segment = s_list.segment
        rmcat_segm_list.room = to_string(s_list.room, "->>>,>>9")
        rmcat_segm_list.pax = to_string(s_list.pax, "->>>,>>9")
        rmcat_segm_list.logis = to_string(s_list.logis, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.proz = to_string(s_list.proz, ">>9.99")
        rmcat_segm_list.avrgrate = to_string(s_list.avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        rmcat_segm_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        rmcat_segm_list.m_logis = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        rmcat_segm_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        rmcat_segm_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        rmcat_segm_list.y_logis = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        rmcat_segm_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        rmcat_segm_list.rmrev = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        rmcat_segm_list.rmrev1 = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        rmcat_segm_list.rmcat = s_list.rmcat
        rmcat_segm_list.segm_code = s_list.segm_code


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

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 285) & (Queasy.number1 == 1)).order_by(Queasy._recid).all():

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy._recid == queasy._recid)).first()
        db_session.delete(tqueasy)
        pass

    bqueasy = db_session.query(Bqueasy).filter(
             (Bqueasy.key == 285) & (Bqueasy.char1 == ("Guest Segment By room Type").lower())).first()

    if bqueasy:
        pass
        bqueasy.number1 = 1


        pass
        pass

    elif not bqueasy:
        bqueasy = Queasy()
        db_session.add(bqueasy)

        bqueasy.key = 285
        bqueasy.char1 = "Guest Segment By room Type"
        bqueasy.number1 = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    create_umsatz()

    rmcat_segm_list = query(rmcat_segm_list_data, first=True)

    if rmcat_segm_list:

        for rmcat_segm_list in query(rmcat_segm_list_data):
            count_i = count_i + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Guest Segment By room Type"
            queasy.char3 = "PROCESS"
            queasy.number1 = count_i
            queasy.char2 = to_string(rmcat_segm_list.flag) + "|" +\
                    rmcat_segm_list.segment + "|" +\
                    rmcat_segm_list.room + "|" +\
                    rmcat_segm_list.pax + "|" +\
                    rmcat_segm_list.logis + "|" +\
                    rmcat_segm_list.proz + "|" +\
                    rmcat_segm_list.avrgrate + "|" +\
                    rmcat_segm_list.m_room + "|" +\
                    rmcat_segm_list.m_pax + "|" +\
                    rmcat_segm_list.m_logis + "|" +\
                    rmcat_segm_list.m_proz + "|" +\
                    rmcat_segm_list.m_avrgrate + "|" +\
                    rmcat_segm_list.y_room + "|" +\
                    rmcat_segm_list.y_pax + "|" +\
                    rmcat_segm_list.y_logis + "|" +\
                    rmcat_segm_list.y_proz + "|" +\
                    rmcat_segm_list.y_avrgrate + "|" +\
                    rmcat_segm_list.rmnite + "|" +\
                    rmcat_segm_list.rmrev + "|" +\
                    rmcat_segm_list.rmnite1 + "|" +\
                    rmcat_segm_list.rmrev1 + "|" +\
                    rmcat_segm_list.rmcat + "|" +\
                    to_string(rmcat_segm_list.segm_code)

    bqueasy = db_session.query(Bqueasy).filter(
             (Bqueasy.key == 285) & (Bqueasy.char1 == ("Guest Segment By room Type").lower())).first()

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()