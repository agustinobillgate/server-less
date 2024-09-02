from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Queasy, Guest, Genstat, Zimmer, Zimkateg, Segment

def purpose_stat_webbl(pvilanguage:int, mi_comp1:bool, mi_ftd1:bool, f_date:date, t_date:date, to_date:date, cardtype:int, price_decimal:int):
    pstay_list_list = []
    t_queasy_list = []
    mm:int = 0
    yy:int = 0
    from_date:date = None
    datum:date = None
    do_it:bool = False
    i:int = 0
    pur_nr:int = 0
    num:int = 0
    s:str = ""
    curr_code:str = ""
    incl_comp:bool = True
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
    lvcarea:str = "purpuse_stat_web"
    queasy = guest = genstat = zimmer = zimkateg = segment = None

    pstay_list = s_list = t_queasy = pstay_buff = sbuff = None

    pstay_list_list, Pstay_list = create_model("Pstay_list", {"flag":int, "purstr":str, "room":str, "pax":str, "logis":str, "proz":str, "avrgrate":str, "m_room":str, "m_pax":str, "m_logis":str, "m_proz":str, "m_avrgrate":str, "y_room":str, "y_pax":str, "y_logis":str, "y_proz":str, "y_avrgrate":str, "rmnite1":str, "rmrev1":str, "rmnite":str, "rmrev":str, "rmcat":str, "segment":str})
    s_list_list, S_list = create_model("S_list", {"catnr":int, "purnr":int, "purstr":str, "rmcat":str, "cat_bez":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})
    t_queasy_list, T_queasy = create_model_like(Queasy)

    Pstay_buff = Pstay_list
    pstay_buff_list = pstay_list_list

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list
        return {"pstay-list": pstay_list_list, "t-queasy": t_queasy_list}

    def create_output():

        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list

        tot_room:int = 0
        i:int = 0
        curr_rmtype:str = ""
        Pstay_buff = Pstay_list
        Sbuff = S_list

        for s_list in query(s_list_list):
            i = i + 1

            if curr_rmtype != s_list.rmcat and curr_rmtype != "":
                create_sub()

            if price_decimal == 0:
                pstay_list = Pstay_list()
                pstay_list_list.append(pstay_list)

                count_sub1()
            else:
                pstay_list = Pstay_list()
                pstay_list_list.append(pstay_list)

                count_sub2()
            curr_rmtype = s_list.rmcat
        create_sub()
        pstay_list = Pstay_list()
        pstay_list_list.append(pstay_list)

        pstay_list.purstr = translateExtended ("T o t a l", lvcarea, "")
        pstay_list.room = to_string(gt_room, "->>>,>>9")
        pstay_list.pax = to_string(gt_pax, "->>>,>>9")
        pstay_list.logis = to_string(gt_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.proz = "100.00"
        pstay_list.avrgrate = to_string(gt_avrgrate, "->>,>>>,>>>,>>>,>>9")
        pstay_list.m_room = to_string(gtm_room, "->>>,>>9")
        pstay_list.m_pax = to_string(gtm_pax, "->>>,>>9")
        pstay_list.m_logis = to_string(gtm_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.m_proz = "100.00"
        pstay_list.m_avrgrate = to_string(gtm_avrgrate, "->>,>>>,>>>,>>>,>>9")
        pstay_list.y_room = to_string(gty_room, "->>>,>>9")
        pstay_list.y_pax = to_string(gty_pax, "->>>,>>9")
        pstay_list.y_logis = to_string(gty_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.y_proz = "100.00"
        pstay_list.y_avrgrate = to_string(gty_avrgrate, "->>,>>>,>>>,>>>,>>9")

    def count_sub1():

        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list


        pstay_list.purstr = s_list.purstr
        pstay_list.room = to_string(s_list.room, "->>>,>>9")
        pstay_list.pax = to_string(s_list.pax, "->>>,>>9")
        pstay_list.logis = to_string(s_list.logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.proz = to_string(s_list.proz, ">>9.99")
        pstay_list.avrgrate = to_string(s_list.avrgrate, "->>,>>>,>>>,>>>,>>9")
        pstay_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        pstay_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        pstay_list.m_logis = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        pstay_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>,>>>,>>>,>>>,>>9")
        pstay_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        pstay_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        pstay_list.y_logis = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        pstay_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>,>>>,>>>,>>>,>>9")
        pstay_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        pstay_list.rmrev = to_string(s_list.y_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        pstay_list.rmrev1 = to_string(s_list.m_logis, "->>,>>>,>>>,>>>,>>9")
        pstay_list.rmcat = s_list.rmcat


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

        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list

        ind:int = 0
        pstay_list = Pstay_list()
        pstay_list_list.append(pstay_list)

        pstay_list.flag = 1
        pstay_list = Pstay_list()
        pstay_list_list.append(pstay_list)

        pstay_list.flag = 2
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
            pstay_list.purstr = translateExtended ("s u b T o t a l", lvcarea, "")
            pstay_list.room = to_string(st_room, "->>>,>>9")
            pstay_list.pax = to_string(st_pax, "->>>,>>9")
            pstay_list.logis = to_string(st_logis, "->>,>>>,>>>,>>>,>>9")
            pstay_list.proz = to_string(st_proz, ">>9.99")
            pstay_list.avrgrate = to_string(st_avrgrate, "->>,>>>,>>>,>>>,>>9")
            pstay_list.m_room = to_string(stm_room, "->>>,>>9")
            pstay_list.m_pax = to_string(stm_pax, "->>>,>>9")
            pstay_list.m_logis = to_string(stm_logis, "->>,>>>,>>>,>>>,>>9")
            pstay_list.m_proz = to_string(stm_proz, ">>9.99")
            pstay_list.m_avrgrate = to_string(stm_avrgrate, "->>,>>>,>>>,>>>,>>9")
            pstay_list.y_room = to_string(sty_room, "->>>,>>9")
            pstay_list.y_pax = to_string(sty_pax, "->>>,>>9")
            pstay_list.y_logis = to_string(sty_logis, "->>,>>>,>>>,>>>,>>9")
            pstay_list.y_proz = to_string(sty_proz, ">>9.99")
            pstay_list.y_avrgrate = to_string(sty_avrgrate, "->>,>>>,>>>,>>>,>>9")


        else:
            pstay_list.purstr = translateExtended ("s u b T o t a l", lvcarea, "")
            pstay_list.room = to_string(st_room, "->>>,>>9")
            pstay_list.pax = to_string(st_pax, "->>>,>>9")
            pstay_list.logis = to_string(st_logis, "->>>,>>>,>>>,>>9.99")
            pstay_list.proz = to_string(st_proz, ">>9.99")
            pstay_list.avrgrate = to_string(st_avrgrate, "->>>,>>>,>>>,>>9.99")
            pstay_list.m_room = to_string(stm_room, "->>>,>>9")
            pstay_list.m_pax = to_string(stm_pax, "->>>,>>9")
            pstay_list.m_logis = to_string(stm_logis, "->>>,>>>,>>>,>>9.99")
            pstay_list.m_proz = to_string(stm_proz, ">>9.99")
            pstay_list.m_avrgrate = to_string(stm_avrgrate, "->>>,>>>,>>>,>>9.99")
            pstay_list.y_room = to_string(sty_room, "->>>,>>9")
            pstay_list.y_pax = to_string(sty_pax, "->>>,>>9")
            pstay_list.y_logis = to_string(sty_logis, "->>>,>>>,>>>,>>9.99")
            pstay_list.y_proz = to_string(sty_proz, ">>9.99")
            pstay_list.y_avrgrate = to_string(sty_avrgrate, "->>>,>>>,>>>,>>9.99")


        pstay_list = Pstay_list()
        pstay_list_list.append(pstay_list)

        init_val()

    def init_val():

        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list


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

        nonlocal pstay_list_list, t_queasy_list, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pstay_buff, sbuff


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_list, s_list_list, t_queasy_list


        pstay_list.purstr = s_list.purstr
        pstay_list.room = to_string(s_list.room, "->>>,>>9")
        pstay_list.pax = to_string(s_list.pax, "->>>,>>9")
        pstay_list.logis = to_string(s_list.logis, "->>>,>>>,>>>,>>9.99")
        pstay_list.proz = to_string(s_list.proz, ">>9.99")
        pstay_list.avrgrate = to_string(s_list.avrgrate, "->>>,>>>,>>>,>>9.99")
        pstay_list.m_room = to_string(s_list.m_room, "->>>,>>9")
        pstay_list.m_pax = to_string(s_list.m_pax, "->>>,>>9")
        pstay_list.m_logis = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        pstay_list.m_proz = to_string(s_list.m_proz, ">>9.99")
        pstay_list.m_avrgrate = to_string(s_list.m_avrgrate, "->>>,>>>,>>>,>>9.99")
        pstay_list.y_room = to_string(s_list.y_room, "->>>,>>9")
        pstay_list.y_pax = to_string(s_list.y_pax, "->>>,>>9")
        pstay_list.y_logis = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        pstay_list.y_proz = to_string(s_list.y_proz, ">>9.99")
        pstay_list.y_avrgrate = to_string(s_list.y_avrgrate, "->>>,>>>,>>>,>>9.99")
        pstay_list.rmnite = to_string(s_list.y_room, "->>>,>>9")
        pstay_list.rmrev = to_string(s_list.y_logis, "->>>,>>>,>>>,>>9.99")
        pstay_list.rmnite1 = to_string(s_list.m_room, "->>>,>>9")
        pstay_list.rmrev1 = to_string(s_list.m_logis, "->>>,>>>,>>>,>>9.99")
        pstay_list.rmcat = s_list.rmcat


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


    incl_comp = not mi_comp1
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


    pstay_list_list.clear()
    s_list_list.clear()

    if mi_ftd1:
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
            (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
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
            pur_nr = 0
            for num in range(1,num_entries(genstat.res_char[1], ";")  + 1) :
                s = entry(num - 1, genstat.res_char[1], ";")

                if re.match("SEGM__PUR.*",s):
                    pur_nr = to_int(substring(s,0 + get_index(s, "SEGM__PUR") + 8))

            s_list = query(s_list_list, filters=(lambda s_list :s_list.purnr == pur_nr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.purnr = pur_nr
                s_list.cat_bez = zimkateg.bezeich

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 143) &  (Queasy.number1 == pur_nr)).first()

                if queasy:
                    buffer_copy(queasy, t_queasy)
                    s_list.purstr = queasy.char3
                else:
                    s_list.purstr = translateExtended ("UNKNOWN", lvcarea, "")

            if genstat.datum == to_date:

                if genstat.resstatus != 13:
                    s_list.room = s_list.room + 1
                    room = room + 1


                s_list.pax = s_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.logis = s_list.logis + genstat.logis
                pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                logis = logis + genstat.logis
                avrgrate = avrgrate + genstat.ratelocal

            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                if genstat.resstatus != 13:
                    s_list.m_room = s_list.m_room + 1
                    m_room = m_room + 1


                s_list.m_pax = s_list.m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.m_logis = s_list.m_logis + genstat.logis
                m_pax = m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                m_logis = m_logis + genstat.logis
                m_avrgrate = m_avrgrate + genstat.rateLocal

            if genstat.resstatus != 13:
                s_list.y_room = s_list.y_room + 1
                y_room = y_room + 1


            s_list.y_pax = s_list.y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
            s_list.y_logis = s_list.y_logis + genstat.logis
            y_pax = y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
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


    create_output()

    return generate_output()