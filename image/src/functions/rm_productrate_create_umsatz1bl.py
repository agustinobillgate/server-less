from functions.additional_functions import *
import decimal
from datetime import date
import re
from functions.calc_servvat import calc_servvat
from models import Guest, Genstat, Queasy, Htparam, Artikel, Umsatz

def rm_productrate_create_umsatz1bl(disptype:int, mi_ftd:bool, mi_cust:bool, f_date:date, t_date:date, to_date:date, cardtype:int, incl_comp:bool, sales_id:str):
    output_list2_list = []
    to_list_list = []
    ind:int = 0
    price_decimal:int = 0
    othrev:decimal = 0
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
    sty_revenue:decimal = 0
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
    revenue:decimal = 0
    bfast:decimal = 0
    lunch:decimal = 0
    dinner:decimal = 0
    guest = genstat = queasy = htparam = artikel = umsatz = None

    to_list = output_list2 = output_buff = None

    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "ratecode":str, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal, "revenue":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal})
    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":int, "name":str, "rmnite1":int, "rmrev1":decimal, "rmnite":int, "rmrev":decimal, "str2":str, "rate":str})

    Output_buff = Output_list2
    output_buff_list = output_list2_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list
        return {"output-list2": output_list2_list, "to-list": to_list_list}

    def create_umsatz1():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        tdatum:date = None
        do_dat:bool = False
        do_it:bool = False
        do_cust:bool = False
        i:int = 0
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
        revenue = 0

        if mi_ftd:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)

        if mi_cust:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        output_list2_list.clear()
        to_list_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.datum != tdatum:
                tdatum = genstat.datum
                do_dat = True
            else:
                do_dat = False

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

            if do_it and sales_id != None:
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


                    to_list.revenue = to_list.revenue + genstat.logis
                    revenue = revenue + genstat.logis

                    if do_dat:
                        othrev = calc_othrev(genstat.datum)
                        to_list.revenue = to_list.revenue + othrev


                        revenue = revenue + othrev
                else:
                    to_list.y_logis = to_list.y_logis + genstat.rateLocal
                    y_logis = y_logis + genstat.rateLocal


                    to_list.revenue = to_list.revenue + genstat.rateLocal
                    revenue = revenue + genstat.rateLocal

                    if do_dat:
                        othrev = calc_othrev(genstat.datum)
                        to_list.revenue = to_list.revenue + othrev


                        revenue = revenue + othrev

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
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.flag = 3
        for ind in range(1,235 + 1) :
            output_list2.str2 = output_list2.str2 + "-"
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.flag = 4

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)

        if price_decimal == 0:
            output_list2.str2 = to_string("T o t a l", "x(24)") + to_string(room, "->>,>>9") + to_string(pax, "->>,>>9") + to_string(logis, "->>,>>>,>>>,>>9") + to_string(proz, "->>9.99") + to_string(avrgrate, "->,>>>,>>>,>>9") + to_string(m_room, "->>,>>9") + to_string(m_pax, "->>,>>9") + to_string(m_logis, "->>,>>>,>>>,>>9") + to_string(m_proz, "->>9.99") + to_string(m_avrgrate, "->,>>>,>>>,>>9") + to_string(y_room, "->>>,>>9") + to_string(y_pax, "->>>,>>9") + to_string(y_logis, "->,>>>,>>>,>>>,>>9") + to_string(y_proz, "->>9.99") + to_string(y_avrgrate, "->,>>>,>>>,>>9") + "                  " + to_string(sty_logis, " ->,>>>,>>>,>>9.99")
            output_list2.rmrev = revenue
        else:
            output_list2.str2 = to_string("T o t a l", "x(24)") + to_string(room, "->>,>>9") + to_string(pax, "->>,>>9") + to_string(logis, " ->>,>>>,>>9.99") + to_string(proz, "->>9.99") + to_string(avrgrate, "->>,>>>,>>9.99") + to_string(m_room, "->>,>>9") + to_string(m_pax, "->>,>>9") + to_string(m_logis, " ->>,>>>,>>9.99") + to_string(m_proz, "->>9.99") + to_string(m_avrgrate, "->>,>>>,>>9.99") + to_string(y_room, "->>>,>>9") + to_string(y_pax, "->>>,>>9") + to_string(y_logis, " ->,>>>,>>>,>>9.99") + to_string(y_proz, "->>9.99") + to_string(y_avrgrate, "->>,>>>,>>9.99")
            output_list2.rmrev = revenue

    def create_output():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list

        i:int = 0
        a:int = 0
        ratecode_bez:str = ""
        Output_buff = Output_list2

        for to_list in query(to_list_list):

            queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == trim(to_list.ratecode))).first()

            if queasy:
                ratecode_bez = queasy.char2
            else:
                ratecode_bez = ""
            i = i + 1

            output_buff = query(output_buff_list, filters=(lambda output_buff :output_buff.rate == to_list.ratecode), first=True)

            if not output_buff:

                if i != 1:
                    create_sub()
                output_list2 = Output_list2()
                output_list2_list.append(output_list2)


                if len(ratecode_bez) != 24:
                    a = 179 - len(ratecode_bez)
                    ratecode_bez = ratecode_bez + fill(" ", a)

                if price_decimal == 0:
                    output_list2.str2 = ratecode_bez + to_string(to_list.ratecode, "x(18)")
                    output_list2 = Output_list2()
                    output_list2_list.append(output_list2)

                    count_sub1()
                else:
                    output_list2.str2 = ratecode_bez + to_string(to_list.ratecode, "x(18)")
                    output_list2 = Output_list2()
                    output_list2_list.append(output_list2)

                    count_sub2()
            else:
                output_list2 = Output_list2()
                output_list2_list.append(output_list2)


                if price_decimal == 0:
                    count_sub1()
                else:
                    count_sub2()
        create_sub()

    def create_sub():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list


        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.flag = 1
        for ind in range(1,235 + 1) :
            output_list2.str2 = output_list2.str2 + "-"
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.flag = 2
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
            output_list2.str2 = to_string("s u b T o t a l", "x(24)") + to_string(st_room, "->>,>>9") + to_string(st_pax, "->>,>>9") + to_string(st_logis, "->>,>>>,>>>,>>9") + to_string(st_proz, "->>9.99") + to_string(st_avrgrate, "->,>>>,>>>,>>9") + to_string(stm_room, "->>,>>9") + to_string(stm_pax, "->>,>>9") + to_string(stm_logis, "->>,>>>,>>>,>>9") + to_string(stm_proz, "->>9.99") + to_string(stm_avrgrate, "->,>>>,>>>,>>9") + to_string(sty_room, "->>>,>>9") + to_string(sty_pax, "->>>,>>9") + to_string(sty_logis, "->,>>>,>>>,>>>,>>9") + to_string(sty_proz, "->>9.99") + to_string(sty_avrgrate, "->,>>>,>>>,>>9")
            output_list2.rmrev = sty_revenue
        else:
            output_list2.str2 = to_string("s u b T o t a l", "x(24)") + to_string(st_room, "->>,>>9") + to_string(st_pax, "->>,>>9") + to_string(st_logis, " ->>,>>>,>>9.99") + to_string(st_proz, "->>9.99") + to_string(st_avrgrate, "->>,>>>,>>9.99") + to_string(stm_room, "->>,>>9") + to_string(stm_pax, "->>,>>9") + to_string(stm_logis, " ->>,>>>,>>9.99") + to_string(stm_proz, "->>9.99") + to_string(stm_avrgrate, "->>,>>>,>>9.99") + to_string(sty_room, "->>>,>>9") + to_string(sty_pax, "->>>,>>9") + to_string(sty_logis, " ->,>>>,>>>,>>9.99") + to_string(sty_proz, "->>9.99") + to_string(sty_avrgrate, "->>,>>>,>>9.99")
            output_list2.rmrev = sty_revenue
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.str2 = fill(" ", 30)
        init_val()

    def init_val():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list


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
        sty_revenue = 0

    def count_sub2():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list


        output_list2.str2 = to_string(to_list.name, "x(24)") + to_string(to_list.room, "->>,>>9") + to_string(to_list.pax, "->>,>>9") + to_string(to_list.logis, " ->>,>>>,>>9.99") + to_string(to_list.proz, "->>9.99") + to_string(to_list.avrgrate, "->>,>>>,>>9.99") + to_string(to_list.m_room, "->>,>>9") + to_string(to_list.m_pax, "->>,>>9") + to_string(to_list.m_logis, " ->>,>>>,>>9.99") + to_string(to_list.m_proz, "->>9.99") + to_string(to_list.m_avrgrate, "->>,>>>,>>9.99") + to_string(to_list.y_room, "->>>,>>9") + to_string(to_list.y_pax, "->>>,>>9") + to_string(to_list.y_logis, " ->,>>>,>>>,>>9.99") + to_string(to_list.y_proz, "->>9.99") + to_string(to_list.y_avrgrate, "->>,>>>,>>9.99")
        output_list2.rate = to_list.ratecode
        output_list2.name = to_string(to_list.name, "x(24)")
        output_list2.rmnite = to_list.y_room
        output_list2.rmrev = to_list.revenue
        output_list2.rmnite1 = to_list.m_room
        output_list2.rmrev1 = to_list.m_logis
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
        sty_revenue = sty_revenue + to_list.revenue

    def count_sub1():

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list


        output_list2.str2 = to_string(to_list.name, "x(24)") + to_string(to_list.room, "->>,>>9") + to_string(to_list.pax, "->>,>>9") + to_string(to_list.logis, "->>,>>>,>>>,>>9") + to_string(to_list.proz, "->>9.99") + to_string(to_list.avrgrate, "->,>>>,>>>,>>9") + to_string(to_list.m_room, "->>,>>9") + to_string(to_list.m_pax, "->>,>>9") + to_string(to_list.m_logis, "->>,>>>,>>>,>>9") + to_string(to_list.m_proz, "->>9.99") + to_string(to_list.m_avrgrate, "->,>>>,>>>,>>9") + to_string(to_list.y_room, "->>>,>>9") + to_string(to_list.y_pax, "->>>,>>9") + to_string(to_list.y_logis, "->,>>>,>>>,>>>,>>9") + to_string(to_list.y_proz, "->>9.99") + to_string(to_list.y_avrgrate, "->,>>>,>>>,>>9")
        output_list2.name = to_string(to_list.name, "x(24)")
        output_list2.rmnite = to_list.y_room
        output_list2.rmrev = to_list.revenue
        output_list2.rmnite1 = to_list.m_room
        output_list2.rmrev1 = to_list.m_logis
        output_list2.rate = to_list.ratecode
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
        sty_revenue = sty_revenue + to_list.revenue

    def calc_othrev(datum:date):

        nonlocal output_list2_list, to_list_list, ind, price_decimal, othrev, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, sty_revenue, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, revenue, bfast, lunch, dinner, guest, genstat, queasy, htparam, artikel, umsatz
        nonlocal output_buff


        nonlocal to_list, output_list2, output_buff
        nonlocal to_list_list, output_list2_list

        othrev = 0
        i:int = 0
        max_i:int = 0
        art_list:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        serv_vat:bool = False
        fact:decimal = 0
        serv:decimal = 0
        vat:decimal = 0

        def generate_inner_output():
            return othrev

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artart == 0) &  (Artikel.umsatzart == 1)).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        for i in range(1,max_i + 1) :

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == art_list[i - 1]) &  (Artikel.departement == 0)).first()

            if artikel:
                serv = 0
                vat = 0

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact = 1.00 + serv + vat
                    othrev = othrev + umsatz.betrag / fact


        return generate_inner_output()

    create_umsatz1()

    return generate_output()