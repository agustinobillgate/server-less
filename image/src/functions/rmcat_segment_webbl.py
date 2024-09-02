from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Guest, Genstat, Zimmer, Zimkateg, Segment

def rmcat_segment_webbl(pvilanguage:int, cardtype:int, to_date:date, f_date:date, t_date:date, mi_ftd:bool, incl_comp:bool):
    rmcat_segm_list_list = []
    s_list_list = []
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
    price_decimal:int = 0
    lvcarea:str = "rmcat_segment_web"
    htparam = guest = genstat = zimmer = zimkateg = segment = None

    rmcat_segm_list = s_list = sbuff = None

    rmcat_segm_list_list, Rmcat_segm_list = create_model("Rmcat_segm_list", {"flag":int, "segment":str, "room":str, "pax":str, "logis":str, "proz":str, "avrgrate":str, "m_room":str, "m_pax":str, "m_logis":str, "m_proz":str, "m_avrgrate":str, "y_room":str, "y_pax":str, "y_logis":str, "y_proz":str, "y_avrgrate":str, "rmnite1":str, "rmrev1":str, "rmnite":str, "rmrev":str, "rmcat":str, "segm_code":int})
    s_list_list, S_list = create_model("S_list", {"segm_code":int, "segment":str, "catnr":int, "rmcat":str, "cat_bez":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list
        return {"rmcat-segm-list": rmcat_segm_list_list, "s-list": s_list_list}

    def create_umsatz():

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        i:int = 0
        s:str = ""
        curr_code:str = ""
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


        rmcat_segm_list_list.clear()
        s_list_list.clear()

        if mi_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
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

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == genstat.zikatnr)).first()

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

                s_list = query(s_list_list, filters=(lambda s_list :s_list.catnr == zimmer.zikatnr and s_list.segm_code == genstat.segmentcode), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.catnr = zimmer.zikatnr
                    s_list.rmcat = zimkateg.kurzbez
                    s_list.cat_bez = zimkateg.bezeich
                    s_list.segm_code = genstat.segmentcode
                    s_list.segment = segment.bezeich

                if genstat.datum == to_date:

                    if genstat.resstatus != 13:
                        s_list.room = s_list.room + 1
                        room = room + 1


                    s_list.pax = s_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                    s_list.logis = s_list.logis + genstat.logis
                    pax = pax + genstat.erwachs
                    logis = logis + genstat.logis
                    avrgrate = avrgrate + genstat.ratelocal

                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if genstat.resstatus != 13:
                        s_list.m_room = s_list.m_room + 1
                        m_room = m_room + 1


                    s_list.m_pax = s_list.m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                    s_list.m_logis = s_list.m_logis + genstat.logis
                    m_pax = m_pax + genstat.erwachs
                    m_logis = m_logis + genstat.logis
                    m_avrgrate = m_avrgrate + genstat.rateLocal

                if genstat.resstatus != 13:
                    s_list.y_room = s_list.y_room + 1
                    y_room = y_room + 1


                s_list.y_pax = s_list.y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.y_logis = s_list.y_logis + genstat.logis
                y_pax = y_pax + genstat.erwachs
                y_logis = y_logis + genstat.logis
                y_avrgrate = y_avrgrate + genstat.rateLocal

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
                    gtm_room = gtm_room + s_list.m_room
                    gtmc_room = gtmc_room + s_list.mc_room
                    gtm_pax = gtm_pax + s_list.m_pax
                    gtm_logis = gtm_logis + s_list.m_logis
                    gty_room = gty_room + s_list.y_room
                    gtyc_room = gtyc_room + s_list.yc_room
                    gty_pax = gty_pax + s_list.y_pax
                    gty_logis = gty_logis + s_list.y_logis


        create_output()

    def create_output():

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list

        tot_room:int = 0
        i:int = 0
        curr_rmtype:str = ""
        Sbuff = S_list

        for s_list in query(s_list_list):
            i = i + 1

            if curr_rmtype != s_list.rmcat and curr_rmtype != "":
                create_sub()

            if curr_rmtype != s_list.rmcat:

                for sbuff in query(sbuff_list, filters=(lambda sbuff :sbuff.rmcat == s_list.rmcat)):
                    tot_room = tot_room + sbuff.room
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_list.append(rmcat_segm_list)

                rmcat_segm_list.flag = 1
                rmcat_segm_list.segment = s_list.cat_bez
                rmcat_segm_list.logis = translateExtended ("Total Rooms :", lvcarea, "") +\
                        " " + trim(to_string(tot_room, "->>9"))


                tot_room = 0

            if price_decimal == 0:
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_list.append(rmcat_segm_list)

                count_sub1()
            else:
                rmcat_segm_list = Rmcat_segm_list()
                rmcat_segm_list_list.append(rmcat_segm_list)

                count_sub2()
            curr_rmtype = s_list.rmcat
        create_sub()
        gt_avrgrate = 0

        if (room - c_room) != 0:
            gt_avrgrate = gt_logis / (gt_room - gtc_room)
        gtm_avrgrate = 0

        if (m_room - mc_room) != 0:
            gtm_avrgrate = gtm_logis / (gtm_room - gtmc_room)
        gty_avrgrate = 0

        if (y_room - yc_room) != 0:
            gty_avrgrate = gty_logis / (gty_room - gtyc_room)
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_list.append(rmcat_segm_list)

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

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list


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


        proz = proz + s_list.proz
        m_proz = m_proz + s_list.m_proz
        y_proz = y_proz + s_list.y_proz
        st_room = st_room + s_list.room
        st_pax = st_pax + s_list.pax
        st_proz = st_proz + s_list.proz
        st_logis = st_logis + s_list.logis
        stm_room = stm_room + s_list.m_room
        stm_pax = stm_pax + s_list.m_pax
        stm_proz = stm_proz + s_list.m_proz
        stm_logis = stm_logis + s_list.m_logis
        sty_room = sty_room + s_list.y_room
        sty_pax = sty_pax + s_list.y_pax
        sty_proz = sty_proz + s_list.y_proz
        sty_logis = sty_logis + s_list.y_logis

    def create_sub():

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list

        ind:int = 0
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_list.append(rmcat_segm_list)

        rmcat_segm_list.flag = 1
        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_list.append(rmcat_segm_list)

        rmcat_segm_list.flag = 2
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
        rmcat_segm_list_list.append(rmcat_segm_list)

        init_val()

    def init_val():

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list


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

    def count_sub2():

        nonlocal rmcat_segm_list_list, s_list_list, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, price_decimal, lvcarea, htparam, guest, genstat, zimmer, zimkateg, segment
        nonlocal sbuff


        nonlocal rmcat_segm_list, s_list, sbuff
        nonlocal rmcat_segm_list_list, s_list_list


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

    DEFINE rectangle rect0 SIZE_CHAR 24 BY 3.5 NO_FILL EDGE_CHARS 0.5

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    create_umsatz()

    return generate_output()