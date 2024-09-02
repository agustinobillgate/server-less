from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Guest, Genstat, Queasy

def rm_productrate_create_umsatz1_webbl(disptype:int, mi_ftd:bool, f_date:date, t_date:date, to_date:date, cardtype:int, incl_comp:bool, sales_id:str):
    to_list_list = []
    ind:int = 0
    price_decimal:int = 0
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
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:decimal = 0
    rmrate:decimal = 0
    avrgrate:decimal = 0
    proz:decimal = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:decimal = 0
    m_rmrate:decimal = 0
    m_avrgrate:decimal = 0
    m_proz:decimal = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:decimal = 0
    y_rmrate:decimal = 0
    y_avrgrate:decimal = 0
    y_proz:decimal = 0
    i:int = 0
    guest = genstat = queasy = None

    to_list = buff_list = None

    to_list_list, To_list = create_model("To_list", {"flag":int, "counter":int, "gastnr":int, "name":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "ratecode":str, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})

    Buff_list = To_list
    buff_list_list = to_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_list_list, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, guest, genstat, queasy
        nonlocal buff_list


        nonlocal to_list, buff_list
        nonlocal to_list_list
        return {"to-list": to_list_list}

    def create_umsatz1():

        nonlocal to_list_list, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, guest, genstat, queasy
        nonlocal buff_list


        nonlocal to_list, buff_list
        nonlocal to_list_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        s:str = ""
        curr_code:str = ""
        curr_userid:str = ""
        room = 0
        c_room = 0
        pax = 0
        logis = 0
        proz = 0
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis = 0
        m_proz = 0
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis = 0
        y_proz = 0

        if mi_ftd:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        to_list_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if re.match(".*\$CODE\$.*",genstat.res_char[1]):
                s = substring(genstat.res_char[1], (1 + get_index(res_char[1], "$CODE$") + 6) - 1)
                curr_code = trim(entry(0, s, ";"))
            else:
                curr_code = "UNKNOWN"
            datum = genstat.datum
            do_it = True

            if cardtype < 3:
                do_it = guest.karteityp == cardtype

            if not incl_comp and genstat.zipreis == 0:

                if (genstat.gratis > 0):
                    do_it = False

                if (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13:
                    do_it = False

            if do_it and sales_id != "":
                do_it = guest.phonetik3 == trim(entry(0, sales_id, "-"))

            if do_it:

                if genstat.zipreis == 0:

                    if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                        if genstat.datum == to_date:
                            c_room = c_room + 1

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            mc_room = mc_room + 1
                        yc_room = yc_room + 1

                to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr and to_list.ratecode.lower()  == (curr_code).lower()), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.ratecode = curr_code
                    to_list.gastnr = guest.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                if genstat.datum == to_date:

                    if genstat.resstatus != 13:
                        to_list.room = to_list.room + 1
                        room = room + 1

                    if genstat.gratis > 0:
                        to_list.pax = to_list.pax + genstat.gratis
                        pax = pax + genstat.gratis
                        avrgrate = avrgrate + genstat.rateLocal


                    else:
                        to_list.pax = to_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        avrgrate = avrgrate + genstat.rateLocal

                    if disptype == 0:
                        to_list.logis = to_list.logis + genstat.logis
                        logis = logis + genstat.logis


                    else:
                        to_list.logis = to_list.logis + genstat.rateLocal
                        logis = logis + genstat.rateLocal

                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if genstat.resstatus != 13:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1

                    if genstat.gratis > 0:
                        to_list.m_pax = to_list.m_pax + genstat.gratis
                        m_pax = m_pax + genstat.gratis
                        m_avrgrate = m_avrgrate + genstat.rateLocal


                    else:
                        to_list.m_pax = to_list.m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        m_avrgrate = m_avrgrate + genstat.rateLocal

                    if disptype == 0:
                        to_list.m_logis = to_list.m_logis + genstat.logis
                        m_logis = m_logis + genstat.logis


                    else:
                        to_list.m_logis = to_list.m_logis + genstat.rateLocal
                        m_logis = m_logis + genstat.rateLocal

                if genstat.resstatus != 13:
                    to_list.y_room = to_list.y_room + 1
                    y_room = y_room + 1

                if genstat.gratis > 0:
                    to_list.y_pax = to_list.y_pax + genstat.gratis
                    y_pax = y_pax + genstat.gratis
                    y_avrgrate = y_avrgrate + genstat.rateLocal


                else:
                    to_list.y_pax = to_list.y_pax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2
                    y_pax = y_pax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2
                    y_avrgrate = y_avrgrate + genstat.rateLocal

                if disptype == 0:
                    to_list.y_logis = to_list.y_logis + genstat.logis
                    y_logis = y_logis + genstat.logis


                else:
                    to_list.y_logis = to_list.y_logis + genstat.rateLocal
                    y_logis = y_logis + genstat.rateLocal

                if genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                    if genstat.datum == to_date:
                        to_list.c_room = to_list.c_room + 1

                    if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                        to_list.mc_room = to_list.mc_room + 1
                    to_list.yc_room = to_list.yc_room + 1

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100
        create_output()
        i = i + 1
        to_list = To_list()
        to_list_list.append(to_list)

        to_list.counter = i

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        i = i + 1
        to_list = To_list()
        to_list_list.append(to_list)

        to_list.counter = i
        to_list.flag = 1
        to_list.name = "T O T A L"
        to_list.room = room
        to_list.pax = pax
        to_list.logis = logis
        to_list.proz = proz
        to_list.avrgrate = avrgrate
        to_list.m_room = m_room
        to_list.m_pax = m_pax
        to_list.m_logis = m_logis
        to_list.m_proz = m_proz
        to_list.m_avrgrate = m_avrgrate
        to_list.y_room = y_room
        to_list.y_pax = y_pax
        to_list.y_logis = y_logis
        to_list.y_proz = y_proz
        to_list.y_avrgrate = y_avrgrate

    def create_output():

        nonlocal to_list_list, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, guest, genstat, queasy
        nonlocal buff_list


        nonlocal to_list, buff_list
        nonlocal to_list_list

        curr_code:str = ""
        Buff_list = To_list

        for to_list in query(to_list_list):

            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == to_list.ratecode)).first()

            if to_list.ratecode.lower()  != (curr_code).lower()  and (curr_code).lower()  != "":
                i = i + 1
                buff_list = Buff_list()
                buff_list_list.append(buff_list)

                buff_list.counter = i


                i = i + 1
                st_avrgrate = 0

                if (st_room - stc_room) != 0:
                    st_avrgrate = st_logis / (st_room - stc_room)
                stm_avrgrate = 0

                if (stm_room - stmc_room) != 0:
                    stm_avrgrate = stm_logis / (stm_room - stmc_room)
                sty_avrgrate = 0

                if (sty_room - styc_room) != 0:
                    sty_avrgrate = sty_logis / (sty_room - styc_room)
                buff_list = Buff_list()
                buff_list_list.append(buff_list)

                buff_list.counter = i
                buff_list.flag = 1
                buff_list.name = "s u b T o t a l"
                buff_list.room = st_room
                buff_list.pax = st_pax
                buff_list.logis = st_logis
                buff_list.proz = st_proz
                buff_list.avrgrate = st_avrgrate
                buff_list.m_room = stm_room
                buff_list.m_pax = stm_pax
                buff_list.m_logis = stm_logis
                buff_list.m_proz = stm_proz
                buff_list.m_avrgrate = stm_avrgrate
                buff_list.y_room = sty_room
                buff_list.y_pax = sty_pax
                buff_list.y_logis = sty_logis
                buff_list.y_proz = sty_proz
                buff_list.y_avrgrate = sty_avrgrate


                init_val()
                i = i + 1
                buff_list = Buff_list()
                buff_list_list.append(buff_list)

                buff_list.counter = i

            if curr_code == "" or curr_code != to_list.ratecode:
                i = i + 1
                buff_list = Buff_list()
                buff_list_list.append(buff_list)

                buff_list.counter = i
                buff_list.ratecode = to_list.ratecode

                if to_list.ratecode.lower()  == "UNKNOWN":
                    buff_list.name = "UNKNOWN"

                elif queasy:
                    buff_list.name = queasy.char2
            curr_code = to_list.ratecode

            if curr_code == "" or curr_code == to_list.ratecode:
                i = i + 1
                to_list.counter = i
                to_list.ratecode = ""
                to_list.flag = 1
                proz = proz + to_list.proz
                m_proz = m_proz + to_list.m_proz
                y_proz = y_proz + to_list.y_proz
                st_room = st_room + TO_list.room
                st_pax = st_pax + to_list.pax
                st_proz = st_proz + to_list.proz
                st_logis = st_logis + to_list.logis
                st_avrgrate = st_avrgrate + to_list.avrgrate
                stm_room = stm_room + to_list.m_room
                stm_pax = stm_pax + to_list.m_pax
                stm_proz = stm_proz + to_list.m_proz
                stm_logis = stm_logis + to_list.m_logis
                stm_avrgrate = stm_avrgrate + to_list.m_avrgrate
                sty_room = sty_room + to_list.y_room
                sty_pax = sty_pax + to_list.y_pax
                sty_proz = sty_proz + to_list.y_proz
                sty_logis = sty_logis + to_list.y_logis
                sty_avrgrate = sty_avrgrate + to_list.y_avrgrate

    def init_val():

        nonlocal to_list_list, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, guest, genstat, queasy
        nonlocal buff_list


        nonlocal to_list, buff_list
        nonlocal to_list_list


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


    create_umsatz1()

    for to_list in query(to_list_list, filters=(lambda to_list :to_list.flag == 1)):

    return generate_output()