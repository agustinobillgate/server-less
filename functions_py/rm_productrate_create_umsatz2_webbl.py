#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 22/7/2025
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Genstat, Res_line, Ratecode, Queasy

def rm_productrate_create_umsatz2_webbl(disptype:int, mi_ftd:bool, f_date:date, t_date:date, to_date:date, cardtype:int, incl_comp:bool, sales_id:string, excl_expired_rate:bool):

    prepare_cache ([Guest, Genstat, Queasy])

    to_list_data = []
    ind:int = 0
    price_decimal:int = 0
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
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:Decimal = to_decimal("0.0")
    rmrate:Decimal = to_decimal("0.0")
    avrgrate:Decimal = to_decimal("0.0")
    proz:Decimal = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:Decimal = to_decimal("0.0")
    m_rmrate:Decimal = to_decimal("0.0")
    m_avrgrate:Decimal = to_decimal("0.0")
    m_proz:Decimal = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:Decimal = to_decimal("0.0")
    y_rmrate:Decimal = to_decimal("0.0")
    y_avrgrate:Decimal = to_decimal("0.0")
    y_proz:Decimal = 0
    i:int = 0
    exist_rate:bool = False
    guest = genstat = res_line = ratecode = queasy = None

    to_list = buff_list = None

    to_list_data, To_list = create_model("To_list", {"flag":int, "counter":int, "gastnr":int, "name":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "ratecode":string, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_list_data, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, exist_rate, guest, genstat, res_line, ratecode, queasy
        nonlocal disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id, excl_expired_rate


        nonlocal to_list, buff_list
        nonlocal to_list_data

        return {"to-list": to_list_data}

    def create_umsatz1():

        nonlocal to_list_data, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, exist_rate, guest, genstat, res_line, ratecode, queasy
        nonlocal disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id, excl_expired_rate

        nonlocal to_list, buff_list
        nonlocal to_list_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        do_it:bool = False
        s:string = ""
        curr_code:string = ""
        curr_userid:string = ""
        room = 0
        c_room = 0
        pax = 0
        logis =  to_decimal("0")
        proz =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        m_proz =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        y_proz =  to_decimal("0")

        if mi_ftd:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        to_list_data.clear()

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.res_char, genstat.resnr, genstat.res_int, genstat.datum, genstat.resstatus, genstat.gastnr, genstat.gratis, \
            genstat.ratelocal, genstat.erwachs, genstat.logis, genstat.kind1, genstat.kind2, genstat.zipreis, genstat._recid, \
            guest.karteityp, guest.phonetik3, guest.gastnr, guest.name, guest.vorname1, guest._recid \
            in db_session.query(Genstat.res_char, Genstat.resnr, Genstat.res_int, Genstat.datum, Genstat.resstatus, Genstat.gastnr, \
                                Genstat.gratis, Genstat.ratelocal, Genstat.erwachs, Genstat.logis, Genstat.kind1, Genstat.kind2, \
                                Genstat.zipreis, Genstat._recid, Guest.karteityp, Guest.phonetik3, Guest.gastnr, Guest.name, \
                                Guest.vorname1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr))\
                .filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & 
                 (Genstat.zinr != "") & 
                 (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            # Rd 22/7/2025
            # res_char ->genstat.res_char
            if matches(genstat.res_char[1],r"*$CODE$*"):
                # s = substring(genstat.res_char[1], (get_index(res_char[1], "$CODE$") + 6) - 1)
                s = substring(genstat.res_char[1], (get_index(genstat.res_char[1], "$CODE$") + 6) - 1)
                curr_code = trim(entry(0, s, ";"))
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if res_line:
                    # Rd 22/7/2025
                    # s = substring(zimmer_wunsch, (get_index(zimmer_wunsch, "$CODE$") + 6) - 1)
                    s = substring(res_line.zimmer_wunsch, (get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
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

            if excl_expired_rate:

                if curr_code.lower()  != ("UNKNOWN").lower() :
                    exist_rate = False

                    for ratecode in db_session.query(Ratecode).filter(
                             (Ratecode.code == (curr_code).lower()) & (Ratecode.endperiode > to_date)).order_by(Ratecode._recid).all():
                        exist_rate = True
                        break

                    if not exist_rate:
                        do_it = False

            if do_it:

                if genstat.zipreis == 0:

                    if (genstat.gratis > 0) or ((genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                        if genstat.datum == to_date:
                            c_room = c_room + 1

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            mc_room = mc_room + 1
                        yc_room = yc_room + 1

                # to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr and to_list.ratecode.lower()  == (curr_code).lower()), first=True)
                tmp_to_list = query(
                    to_list_data,
                    filters=lambda tl: tl.gastnr == genstat.gastnr and tl.ratecode == curr_code,
                    first=True
                )
                # if not to_list:
                #     to_list = To_list()
                #     to_list_data.append(to_list)

                #     to_list.ratecode = curr_code
                #     to_list.gastnr = guest.gastnr
                #     to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                #             guest.anrede1 + guest.anredefirma

                if genstat.datum == to_date:

                    if genstat.resstatus != 13:
                        to_list.room = to_list.room + 1
                        room = room + 1

                    if genstat.gratis > 0:
                        to_list.pax = to_list.pax + genstat.gratis
                        pax = pax + genstat.gratis
                        avrgrate =  to_decimal(avrgrate) + to_decimal(genstat.ratelocal)


                    else:
                        to_list.pax = to_list.pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        avrgrate =  to_decimal(avrgrate) + to_decimal(genstat.ratelocal)

                    if disptype == 0:
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis)
                        logis =  to_decimal(logis) + to_decimal(genstat.logis)


                    else:
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.ratelocal)
                        logis =  to_decimal(logis) + to_decimal(genstat.ratelocal)

                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                    if genstat.resstatus != 13:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1

                    if genstat.gratis > 0:
                        to_list.m_pax = to_list.m_pax + genstat.gratis
                        m_pax = m_pax + genstat.gratis
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(genstat.ratelocal)


                    else:
                        to_list.m_pax = to_list.m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2
                        m_avrgrate =  to_decimal(m_avrgrate) + to_decimal(genstat.ratelocal)

                    if disptype == 0:
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis)
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis)


                    else:
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.ratelocal)
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.ratelocal)

                if genstat.resstatus != 13:
                    to_list.y_room = to_list.y_room + 1
                    y_room = y_room + 1

                if genstat.gratis > 0:
                    to_list.y_pax = to_list.y_pax + genstat.gratis
                    y_pax = y_pax + genstat.gratis
                    y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(genstat.ratelocal)


                else:
                    to_list.y_pax = to_list.y_pax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2
                    y_pax = y_pax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2
                    y_avrgrate =  to_decimal(y_avrgrate) + to_decimal(genstat.ratelocal)

                if disptype == 0:
                    to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis)
                    y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis)


                else:
                    to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.ratelocal)
                    y_logis =  to_decimal(y_logis) + to_decimal(genstat.ratelocal)

                if genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13):

                    if genstat.datum == to_date:
                        to_list.c_room = to_list.c_room + 1

                    if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                        to_list.mc_room = to_list.mc_room + 1
                    to_list.yc_room = to_list.yc_room + 1

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")
        create_output()
        i = i + 1
        to_list = To_list()
        to_list_data.append(to_list)

        to_list.counter = i

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
        i = i + 1
        to_list = To_list()
        to_list_data.append(to_list)

        to_list.counter = i
        to_list.flag = 1
        to_list.name = "T O T A L"
        to_list.room = room
        to_list.pax = pax
        to_list.logis =  to_decimal(logis)
        to_list.proz =  to_decimal(proz)
        to_list.avrgrate =  to_decimal(avrgrate)
        to_list.m_room = m_room
        to_list.m_pax = m_pax
        to_list.m_logis =  to_decimal(m_logis)
        to_list.m_proz =  to_decimal(m_proz)
        to_list.m_avrgrate =  to_decimal(m_avrgrate)
        to_list.y_room = y_room
        to_list.y_pax = y_pax
        to_list.y_logis =  to_decimal(y_logis)
        to_list.y_proz =  to_decimal(y_proz)
        to_list.y_avrgrate =  to_decimal(y_avrgrate)


    def create_output():

        nonlocal to_list_data, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, exist_rate, guest, genstat, res_line, ratecode, queasy
        nonlocal disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id, excl_expired_rate


        nonlocal to_list, buff_list
        nonlocal to_list_data

        curr_code:string = ""
        Buff_list = To_list
        buff_list_data = to_list_data

        for to_list in query(to_list_data, sort_by=[("ratecode",False),("name",False)]):

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, to_list.ratecode)]})

            if to_list.ratecode.lower()  != (curr_code).lower()  and (curr_code).lower()  != "":
                i = i + 1
                buff_list = Buff_list()
                buff_list_data.append(buff_list)

                buff_list.counter = i


                i = i + 1
                st_avrgrate =  to_decimal("0")

                if (st_room - stc_room) != 0:
                    st_avrgrate =  to_decimal(st_logis) / to_decimal((st_room) - to_decimal(stc_room))
                stm_avrgrate =  to_decimal("0")

                if (stm_room - stmc_room) != 0:
                    stm_avrgrate =  to_decimal(stm_logis) / to_decimal((stm_room) - to_decimal(stmc_room))
                sty_avrgrate =  to_decimal("0")

                if (sty_room - styc_room) != 0:
                    sty_avrgrate =  to_decimal(sty_logis) / to_decimal((sty_room) - to_decimal(styc_room))
                buff_list = Buff_list()
                buff_list_data.append(buff_list)

                buff_list.counter = i
                buff_list.flag = 1
                buff_list.name = "s u b T o t a l"
                buff_list.room = st_room
                buff_list.pax = st_pax
                buff_list.logis =  to_decimal(st_logis)
                buff_list.proz =  to_decimal(st_proz)
                buff_list.avrgrate =  to_decimal(st_avrgrate)
                buff_list.m_room = stm_room
                buff_list.m_pax = stm_pax
                buff_list.m_logis =  to_decimal(stm_logis)
                buff_list.m_proz =  to_decimal(stm_proz)
                buff_list.m_avrgrate =  to_decimal(stm_avrgrate)
                buff_list.y_room = sty_room
                buff_list.y_pax = sty_pax
                buff_list.y_logis =  to_decimal(sty_logis)
                buff_list.y_proz =  to_decimal(sty_proz)
                buff_list.y_avrgrate =  to_decimal(sty_avrgrate)


                init_val()
                i = i + 1
                buff_list = Buff_list()
                buff_list_data.append(buff_list)

                buff_list.counter = i

            if curr_code == "" or curr_code != to_list.ratecode:
                i = i + 1
                buff_list = Buff_list()
                buff_list_data.append(buff_list)

                buff_list.counter = i
                buff_list.ratecode = to_list.ratecode

                if to_list.ratecode.lower()  == ("UNKNOWN").lower() :
                    buff_list.name = "UNKNOWN"

                elif queasy:
                    buff_list.name = queasy.char2
            curr_code = to_list.ratecode

            if curr_code == "" or curr_code == to_list.ratecode:
                i = i + 1
                to_list.counter = i
                to_list.ratecode = ""
                to_list.flag = 1
                proz =  to_decimal(proz) + to_decimal(to_list.proz)
                m_proz =  to_decimal(m_proz) + to_decimal(to_list.m_proz)
                y_proz =  to_decimal(y_proz) + to_decimal(to_list.y_proz)

                # Rd 22/7/2025
                # st_room = st_room + TO_list.room
                st_room = st_room + to_list.room
                st_pax = st_pax + to_list.pax
                st_proz =  to_decimal(st_proz) + to_decimal(to_list.proz)
                st_logis =  to_decimal(st_logis) + to_decimal(to_list.logis)
                st_avrgrate =  to_decimal(st_avrgrate) + to_decimal(to_list.avrgrate)
                stm_room = stm_room + to_list.m_room
                stm_pax = stm_pax + to_list.m_pax
                stm_proz =  to_decimal(stm_proz) + to_decimal(to_list.m_proz)
                stm_logis =  to_decimal(stm_logis) + to_decimal(to_list.m_logis)
                stm_avrgrate =  to_decimal(stm_avrgrate) + to_decimal(to_list.m_avrgrate)
                sty_room = sty_room + to_list.y_room
                sty_pax = sty_pax + to_list.y_pax
                sty_proz =  to_decimal(sty_proz) + to_decimal(to_list.y_proz)
                sty_logis =  to_decimal(sty_logis) + to_decimal(to_list.y_logis)
                sty_avrgrate =  to_decimal(sty_avrgrate) + to_decimal(to_list.y_avrgrate)


    def init_val():

        nonlocal to_list_data, ind, price_decimal, st_room, stc_room, st_pax, st_logis, st_avrgrate, st_proz, stm_room, stmc_room, stm_pax, stm_logis, stm_avrgrate, stm_proz, sty_room, styc_room, sty_pax, sty_logis, sty_avrgrate, sty_proz, room, c_room, pax, logis, rmrate, avrgrate, proz, m_room, mc_room, m_pax, m_logis, m_rmrate, m_avrgrate, m_proz, y_room, yc_room, y_pax, y_logis, y_rmrate, y_avrgrate, y_proz, i, exist_rate, guest, genstat, res_line, ratecode, queasy
        nonlocal disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id, excl_expired_rate


        nonlocal to_list, buff_list
        nonlocal to_list_data


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


    if sales_id == None or sales_id == " ":
        sales_id = ""
    create_umsatz1()

    return generate_output()