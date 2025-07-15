#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest, Genstat, Zimmer, Zimkateg, Segment

def purpose_stat_webbl(pvilanguage:int, mi_comp1:bool, mi_ftd1:bool, f_date:date, t_date:date, to_date:date, cardtype:int, price_decimal:int):

    prepare_cache ([Guest, Genstat, Zimkateg])

    pstay_list_data = []
    t_queasy_data = []
    mm:int = 0
    yy:int = 0
    from_date:date = None
    datum:date = None
    do_it:bool = False
    i:int = 0
    pur_nr:int = 0
    num:int = 0
    s:string = ""
    curr_code:string = ""
    incl_comp:bool = True
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
    lvcarea:string = "purpuse-stat-web"
    queasy = guest = genstat = zimmer = zimkateg = segment = None

    pstay_list = s_list = t_queasy = pstay_buff = sbuff = None

    pstay_list_data, Pstay_list = create_model("Pstay_list", {"flag":int, "purstr":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string, "rmnite1":string, "rmrev1":string, "rmnite":string, "rmrev":string, "rmcat":string, "segment":string})
    s_list_data, S_list = create_model("S_list", {"catnr":int, "purnr":int, "purstr":string, "rmcat":string, "cat_bez":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal})
    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data

        return {"pstay-list": pstay_list_data, "t-queasy": t_queasy_data}

    def create_output():

        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data

        tot_room:int = 0
        i:int = 0
        curr_rmtype:string = ""
        Pstay_buff = Pstay_list
        pstay_buff_data = pstay_list_data
        Sbuff = S_list
        sbuff_data = s_list_data

        for s_list in query(s_list_data, sort_by=[("purstr",False)]):
            i = i + 1

            if curr_rmtype != s_list.rmcat and curr_rmtype != "":
                create_sub()

            if price_decimal == 0:
                pstay_list = Pstay_list()
                pstay_list_data.append(pstay_list)

                count_sub1()
            else:
                pstay_list = Pstay_list()
                pstay_list_data.append(pstay_list)

                count_sub2()
            curr_rmtype = s_list.rmcat
        create_sub()
        pstay_list = Pstay_list()
        pstay_list_data.append(pstay_list)

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

        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data


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

        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data

        ind:int = 0
        pstay_list = Pstay_list()
        pstay_list_data.append(pstay_list)

        pstay_list.flag = 1
        pstay_list = Pstay_list()
        pstay_list_data.append(pstay_list)

        pstay_list.flag = 2
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
        pstay_list_data.append(pstay_list)

        init_val()


    def init_val():

        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data


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

        nonlocal pstay_list_data, t_queasy_data, mm, yy, from_date, datum, do_it, i, pur_nr, num, s, curr_code, incl_comp, room, c_room, pax, logis, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_avrgrate, y_proz, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, gt_room, gtc_room, gt_pax, gt_logis, gt_avrgrate, gtm_room, gtmc_room, gtm_pax, gtm_logis, gtm_avrgrate, gtm_proz, gty_room, gtyc_room, gty_pax, gty_logis, gty_avrgrate, gty_proz, lvcarea, queasy, guest, genstat, zimmer, zimkateg, segment
        nonlocal pvilanguage, mi_comp1, mi_ftd1, f_date, t_date, to_date, cardtype, price_decimal


        nonlocal pstay_list, s_list, t_queasy, pstay_buff, sbuff
        nonlocal pstay_list_data, s_list_data, t_queasy_data


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

    incl_comp = not mi_comp1
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


    pstay_list_data.clear()
    s_list_data.clear()

    if mi_ftd1:
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
    for genstat.zinr, genstat.zikatnr, genstat.segmentcode, genstat.resstatus, genstat.datum, genstat.res_char, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.kind3, genstat.logis, genstat.ratelocal, genstat.zipreis, genstat._recid, guest.karteityp, guest._recid in db_session.query(Genstat.zinr, Genstat.zikatnr, Genstat.segmentcode, Genstat.resstatus, Genstat.datum, Genstat.res_char, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.logis, Genstat.ratelocal, Genstat.zipreis, Genstat._recid, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
             (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr).all():
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
            pur_nr = 0
            for num in range(1,num_entries(genstat.res_char[1], ";")  + 1) :
                s = entry(num - 1, genstat.res_char[1], ";")

                if matches(s,r"SEGM_PUR*"):
                    pur_nr = to_int(substring(s, get_index(s, "SEGM_PUR") + 8 - 1))

            s_list = query(s_list_data, filters=(lambda s_list: s_list.purnr == pur_nr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.purnr = pur_nr
                s_list.cat_bez = zimkateg.bezeichnung

                queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, pur_nr)]})

                if queasy:
                    t_queasy = T_queasy()
                    t_queasy_data.append(t_queasy)

                    buffer_copy(queasy, t_queasy)
                    s_list.purstr = queasy.char3
                else:
                    s_list.purstr = translateExtended ("UNKNOWN", lvcarea, "")

            if genstat.datum == to_date:

                if genstat.resstatus != 13:
                    s_list.room = s_list.room + 1
                    room = room + 1


                s_list.pax = s_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.logis =  to_decimal(s_list.logis) + to_decimal(genstat.logis)
                pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                logis =  to_decimal(logis) + to_decimal(genstat.logis)
                avrgrate =  to_decimal(avrgrate) + to_decimal(genstat.ratelocal)

            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                if genstat.resstatus != 13:
                    s_list.m_room = s_list.m_room + 1
                    m_room = m_room + 1


                s_list.m_pax = s_list.m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                s_list.m_logis =  to_decimal(s_list.m_logis) + to_decimal(genstat.logis)
                m_pax = m_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)
                m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(genstat.ratelocal)

            if genstat.resstatus != 13:
                s_list.y_room = s_list.y_room + 1
                y_room = y_room + 1


            s_list.y_pax = s_list.y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
            s_list.y_logis =  to_decimal(s_list.y_logis) + to_decimal(genstat.logis)
            y_pax = y_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
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


    create_output()

    return generate_output()