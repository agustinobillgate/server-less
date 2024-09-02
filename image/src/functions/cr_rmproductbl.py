from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Htparam, Waehrung, Guest, Genstat, Exrate, Bediener, Nation, Queasy, Sourccod

def cr_rmproductbl(pvilanguage:int, op_type:int, printer_nr:int, call_from:int, txt_file:str, disptype:int, cardtype_1:int, currency_type:int, ytd_flag:int, excl_comp:bool, last_sort:int, f_date:date, t_date:date, to_date:date):
    output_list_list = []
    lvcarea:str = "rm_product"
    cardtype:int = 0
    ota_only:bool = False
    foreign_nr:int = 0
    exchg_rate:decimal = 1
    price_decimal:int = 0
    incl_comp:bool = True
    message_it:bool = True
    ind:int = 0
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:decimal = 0
    avrgrate:decimal = 0
    exc_avrgrate:decimal = 0
    comp_room:int = 0
    comp_pax:int = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:decimal = 0
    m_avrgrate:decimal = 0
    exc_m_avrgrate:decimal = 0
    comp_m_room:int = 0
    comp_m_pax:int = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:decimal = 0
    y_avrgrate:decimal = 0
    exc_y_avrgrate:decimal = 0
    comp_y_room:int = 0
    comp_y_pax:int = 0
    from_bez:str = ""
    to_bez:str = ""
    curr_select:str = ""
    tot:str = ""
    htparam = waehrung = guest = genstat = exrate = bediener = nation = queasy = sourccod = None

    output_list = to_list = to_list1 = tmp_room = tmp_room1 = buf_nation = None

    output_list_list, Output_list = create_model("Output_list", {"name":str, "room":decimal, "pax":decimal, "logis":decimal, "proz":decimal, "avrgrate":decimal, "m_room":decimal, "m_pax":decimal, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":decimal, "y_pax":decimal, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal, "comp_room":decimal, "comp_pax":decimal, "comp_m_room":decimal, "comp_m_pax":decimal, "comp_y_room":decimal, "comp_y_pax":decimal, "exc_avrgrate":decimal, "exc_m_avrgrate":decimal, "exc_y_avrgrate":decimal, "flag":int, "name2":str, "rmnite1":int, "rmrev1":decimal, "rmnite":int, "rmrev":decimal})
    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":str, "zinr":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "exc_avrgrate":decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "exc_m_avrgrate":decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal, "exc_y_avrgrate":decimal, "comp_y_room":int, "comp_y_pax":int})
    to_list1_list, To_list1 = create_model("To_list1", {"gastnr":int, "name":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "exc_avrgrate":decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "exc_m_avrgrate":decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal, "exc_y_avrgrate":decimal, "comp_y_room":int, "comp_y_pax":int})
    tmp_room_list, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":str, "flag":int})
    tmp_room1_list, Tmp_room1 = create_model_like(Tmp_room)

    Buf_nation = Nation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list
        return {"output-list": output_list_list}

    def create_umsatz1():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        curr_zinr:str = ""
        prev_zinr:str = ""
        do_it:bool = False
        curr_gastnr:int = 0
        prev_gastnr:int = 0
        beg_date:date = None
        incl_comp = not excl_comp
        room = 0
        c_room = 0
        comp_room = 0
        pax = 0
        logis = 0
        m_room = 0
        mc_room = 0
        comp_m_room = 0
        m_pax = 0
        m_logis = 0
        y_room = 0
        yc_room = 0
        comp_y_room = 0
        y_pax = 0
        y_logis = 0

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()
        tmp_room_list.clear()
        tmp_room1_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)


            do_it = True

            if guest.karteityp == 2 and ota_only:
                do_it = guest.steuernr != ""

            if do_it:
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = db_session.query(Bediener).filter(
                            (Bediener.userinit == guest.phonetik3)).first()

                    if bediener:
                        to_list.name = to_list.name + " == " + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis = to_list.logis + genstat.logis / exchg_rate
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis = logis + genstat.logis / exchg_rate

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis = m_logis + genstat.logis / exchg_rate

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis = y_logis + genstat.logis / exchg_rate
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis = to_list.logis + genstat.logis / exchg_rate
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis = logis + genstat.logis / exchg_rate

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis = m_logis + genstat.logis / exchg_rate

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis = y_logis + genstat.logis / exchg_rate

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.gratis == 0) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)


            do_it = True

            if guest.karteityp == 2 and ota_only:
                do_it = guest.steuernr != ""

            if do_it:
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = db_session.query(Bediener).filter(
                            (Bediener.userinit == guest.phonetik3)).first()

                    if bediener:
                        to_list.name = to_list.name + " == " + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                else:

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list in query(to_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate
            output_list.name2 = to_list.name
            output_list.rmnite1 = to_list.y_room
            output_list.rmrev1 = to_list.y_logis
            output_list.rmnite = to_list.m_room
            output_list.rmrev = to_list.m_logis


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)

        if comp_room != 0:
            exc_avrgrate = logis / comp_room

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

    def create_umsatz11():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        curr_gastnr:int = 1
        do_it:bool = False
        beg_date:date = None
        incl_comp = not excl_comp
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
        comp_pax = 0
        comp_room = 0
        comp_y_room = 0
        comp_y_pax = 0
        comp_m_room = 0
        comp_m_pax = 0

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()
        tmp_room_list.clear()
        tmp_room1_list.clear()

        for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

            guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnr)).first()

            if guest:
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.userinit == guest.phonetik3)).first()

                    if bediener:
                        to_list.name = to_list.name + " == " + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis = to_list.logis + genstat.logis / exchg_rate
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis = logis + genstat.logis / exchg_rate

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis = m_logis + genstat.logis / exchg_rate
                    to_list.y_room = to_list.y_room + 1
                    to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                    y_room = y_room + 1
                    y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    y_logis = y_logis + genstat.logis / exchg_rate
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis = to_list.logis + genstat.logis / exchg_rate
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis = logis + genstat.logis / exchg_rate

                    if get_month(genstat.datum) == mm:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis = m_logis + genstat.logis / exchg_rate
                    to_list.y_room = to_list.y_room + 1
                    to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                    y_room = y_room + 1
                    y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    y_logis = y_logis + genstat.logis / exchg_rate
            else:

                guest = db_session.query(Guest).filter(
                            (Guest.gastnr == genstat.gastnrmember)).first()

                if guest:

                    to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_list.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma

                        bediener = db_session.query(Bediener).filter(
                                    (Bediener.userinit == guest.phonetik3)).first()

                        if bediener:
                            to_list.name = to_list.name + " == " + bediener.username

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                to_list.room = to_list.room + 1
                                room = room + 1
                                tmp_room = Tmp_room()
                                tmp_room_list.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnr
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.logis = to_list.logis + genstat.logis / exchg_rate
                            pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            logis = logis + genstat.logis / exchg_rate

                        if get_month(genstat.datum) == get_month(to_date):
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                            m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            m_logis = m_logis + genstat.logis / exchg_rate
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis = y_logis + genstat.logis / exchg_rate
                    else:

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                to_list.room = to_list.room + 1
                                room = room + 1
                                tmp_room = Tmp_room()
                                tmp_room_list.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnr
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.logis = to_list.logis + genstat.logis / exchg_rate
                            pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            logis = logis + genstat.logis / exchg_rate

                        if get_month(genstat.datum) == mm:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                            m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            m_logis = m_logis + genstat.logis / exchg_rate
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis = y_logis + genstat.logis / exchg_rate

        for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.gratis == 0) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

            guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnr)).first()

            if guest:
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.userinit == guest.phonetik3)).first()

                    if bediener:
                        to_list.name = to_list.name + " == " + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                else:

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                    if get_month(genstat.datum) == mm:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
            else:

                guest = db_session.query(Guest).filter(
                            (Guest.gastnr == genstat.gastnrmember)).first()

                if guest:

                    to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_list.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma

                        bediener = db_session.query(Bediener).filter(
                                    (Bediener.userinit == guest.phonetik3)).first()

                        if bediener:
                            to_list.name = to_list.name + " == " + bediener.username

                        if genstat.datum == to_date:

                            tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_list.append(tmp_room1)

                                tmp_room1.gastnr = genstat.gastnr
                                tmp_room1.zinr = genstat.zinr
                                tmp_room1.flag = 1


                            to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                            comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                        if get_month(genstat.datum) == get_month(to_date):
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                            comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_y_room = comp_y_room + 1
                        comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    else:

                        if genstat.datum == to_date:

                            tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_list.append(tmp_room1)

                                tmp_room1.gastnr = genstat.gastnr
                                tmp_room1.zinr = genstat.zinr
                                tmp_room1.flag = 1


                            to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                            comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                        if get_month(genstat.datum) == mm:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                            comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        comp_y_room = comp_y_room + 1
                        comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list in query(to_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate
            output_list.name2 = to_list.name
            output_list.rmnite1 = to_list.y_room
            output_list.rmrev1 = to_list.y_logis
            output_list.rmnite = to_list.m_room
            output_list.rmrev = to_list.m_logis


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)

        if comp_room != 0:
            exc_avrgrate = logis / comp_room

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

    def create_umsatz2():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()
        to_list1_list.clear()

        for nation in db_session.query(Nation).filter(
                (Nation.natcode == 0)).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nationnr

            if re.match(".*;.*",nation.bezeich):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1 :to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe) &  (Queasy.number2 == 0) &  (Queasy.deci2 == 0)).first()

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            for genstat in db_session.query(Genstat).filter(
                        (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr == nationnr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis = to_list.logis + genstat.logis / exchg_rate

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.logis = to_list1.logis + genstat.logis / exchg_rate
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis = logis + genstat.logis / exchg_rate

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.m_logis = to_list1.m_logis + genstat.logis / exchg_rate
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis = m_logis + genstat.logis / exchg_rate

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list1.y_logis = to_list1.y_logis + genstat.logis / exchg_rate
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis = y_logis + genstat.logis / exchg_rate

            for genstat in db_session.query(Genstat).filter(
                        (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.gratis == 0) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr == nationnr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                if genstat.datum == to_date:

                    tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                    if not tmp_room1:
                        to_list.comp_room = to_list.comp_room + 1
                        comp_room = comp_room + 1

                        if to_list1:
                            to_list1.comp_room = to_list1.comp_room + 1
                        tmp_room1 = Tmp_room1()
                        tmp_room1_list.append(tmp_room1)

                        tmp_room1.gastnr = genstat.gastnr
                        tmp_room1.zinr = genstat.zinr
                        tmp_room1.flag = 1


                    to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                    if to_list1:
                        to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                    comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.comp_m_room = to_list.comp_m_room + 1
                    to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.comp_m_room = to_list1.comp_m_room + 1
                        to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    comp_m_room = comp_m_room + 1
                    comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if to_list1:
                    to_list1.comp_y_room = to_list1.comp_y_room + 1
                    to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                to_list.comp_y_room = to_list.comp_y_room + 1
                to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                comp_y_room = comp_y_room + 1
                comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list1 in query(to_list1_list):

            if (to_list1.room - to_list1.c_room) != 0:
                to_list1.avrgrate = to_list1.logis / (to_list1.room - to_list1.c_room)

            if to_list1.comp_room != 0:
                to_list1.exc_avrgrate = to_list1.logis / to_list1.comp_room

            if logis != 0:
                to_list1.proz = to_list1.logis / logis * 100

            if (to_list1.m_room - to_list1.mc_room) != 0:
                to_list1.m_avrgrate = to_list1.m_logis / (to_list1.m_room - to_list1.mc_room)

            if to_list1.comp_m_room != 0:
                to_list1.exc_m_avrgrate = to_list1.m_logis / to_list1.comp_m_room

            if m_logis != 0:
                to_list1.m_proz = to_list1.m_logis / m_logis * 100

            if (to_list1.y_room - to_list1.yc_room) != 0:
                to_list1.y_avrgrate = to_list1.y_logis / (to_list1.y_room - to_list1.yc_room)

            if to_list1.comp_y_room != 0:
                to_list1.exc_y_avrgrate = to_list1.y_logis / to_list1.comp_y_room

            if y_logis != 0:
                to_list1.y_proz = to_list1.y_logis / y_logis * 100

        for to_list in query(to_list_list, filters=(lambda to_list :to_list.y_room != 0)):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 0
            output_list.rmnite = to_list.y_room
            output_list.rmrev = to_list.y_logis
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 = to_list.m_logis
            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        avrgrate = 0

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)
        exc_avrgrate = 0

        if comp_room != 0:
            exc_avrgrate = logis / comp_room
        m_avrgrate = 0

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)
        exc_m_avrgrate = 0

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room
        y_avrgrate = 0

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        exc_y_avrgrate = 0

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 3
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 5
                output_list.rmnite = to_list1.y_room
                output_list.rmrev = to_list1.y_logis
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 = to_list1.m_logis
                output_list.name = to_list1.name
                output_list.room = to_list1.room
                output_list.pax = to_list1.pax
                output_list.logis = to_list1.logis
                output_list.proz = to_list1.proz
                output_list.avrgrate = to_list1.avrgrate
                output_list.m_room = to_list1.m_room
                output_list.m_pax = to_list1.m_pax
                output_list.m_logis = to_list1.m_logis
                output_list.m_proz = to_list1.m_proz
                output_list.m_avrgrate = to_list1.m_avrgrate
                output_list.y_room = to_list1.y_room
                output_list.y_pax = to_list1.y_pax
                output_list.y_logis = to_list1.y_logis
                output_list.y_proz = to_list1.y_proz
                output_list.y_avrgrate = to_list1.y_avrgrate
                output_list.comp_room = to_list1.comp_room
                output_list.comp_pax = to_list1.comp_pax
                output_list.comp_m_room = to_list1.comp_m_room
                output_list.comp_m_pax = to_list1.comp_m_pax
                output_list.comp_y_room = to_list1.comp_y_room
                output_list.comp_y_pax = to_list1.comp_y_pax
                output_list.exc_avrgrate = to_list1.exc_avrgrate
                output_list.exc_m_avrgrate = to_list1.exc_m_avrgrate
                output_list.exc_y_avrgrate = to_list1.exc_y_avrgrate


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 6
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 7
            avrgrate = 0

            if (room - c_room) != 0:
                avrgrate = logis / (room - c_room)
            exc_avrgrate = 0

            if comp_room != 0:
                exc_avrgrate = logis / comp_room
            m_avrgrate = 0

            if (m_room - mc_room) != 0:
                m_avrgrate = m_logis / (m_room - mc_room)
            exc_m_avrgrate = 0

            if comp_m_room != 0:
                exc_m_avrgrate = m_logis / comp_m_room
            y_avrgrate = 0

            if (y_room - yc_room) != 0:
                y_avrgrate = y_logis / (y_room - yc_room)
            exc_y_avrgrate = 0

            if comp_y_room != 0:
                exc_y_avrgrate = y_logis / comp_y_room
            output_list.name = "T o t a l"
            output_list.room = room
            output_list.pax = pax
            output_list.logis = logis
            output_list.proz = 100
            output_list.avrgrate = avrgrate
            output_list.m_room = m_room
            output_list.m_pax = m_pax
            output_list.m_logis = m_logis
            output_list.m_proz = 100
            output_list.m_avrgrate = m_avrgrate
            output_list.y_room = y_room
            output_list.y_pax = y_pax
            output_list.y_logis = y_logis
            output_list.y_proz = 100
            output_list.y_avrgrate = y_avrgrate
            output_list.comp_room = comp_room
            output_list.comp_pax = comp_pax
            output_list.comp_m_room = comp_m_room
            output_list.comp_m_pax = comp_m_pax
            output_list.comp_y_room = comp_y_room
            output_list.comp_y_pax = comp_y_pax
            output_list.exc_avrgrate = exc_avrgrate
            output_list.exc_m_avrgrate = exc_m_avrgrate
            output_list.exc_y_avrgrate = exc_y_avrgrate

    def create_umsatz3():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        curr_code:int = 0
        do_it:bool = False
        beg_date:date = None
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()
        to_list1_list.clear()

        for sourccod in db_session.query(Sourccod).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = sourccod.source_code
            to_list.name = sourccod.bezeich

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.nationnr != 0) &  (Genstat.segmentcode != 0) &  (Genstat.source == sourccod.source_code) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis = to_list.logis + genstat.logis / exchg_rate
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis = logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == mm:
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis = m_logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis = y_logis + genstat.logis / exchg_rate

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list in query(to_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.name = to_string(to_list.name, "x(40)")
            output_list.rmnite = to_list.y_room
            output_list.rmrev = to_list.y_logis
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 = to_list.m_logis
            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 3
        avrgrate = 0

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)
        exc_avrgrate = 0

        if comp_room != 0:
            exc_avrgrate = logis / comp_room
        m_avrgrate = 0

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)
        exc_m_avrgrate = 0

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room
        y_avrgrate = 0

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        exc_y_avrgrate = 0

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

    def create_umsatz4():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()
        to_list1_list.clear()

        for nation in db_session.query(Nation).filter(
                (Nation.natcode == 0)).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nationnr

            if re.match(".*;.*",nation.bezeich):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1 :to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe) &  (Queasy.number2 == 0) &  (Queasy.deci2 == 0)).first()

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.resident != 0) &  (Genstat.segmentcode != 0) &  (Genstat.resident == nationnr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                datum = genstat.datum
                exchg_rate = 1

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == datum)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis = to_list.logis + genstat.logis / exchg_rate

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.logis = to_list1.logis + genstat.logis / exchg_rate
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis = logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                        if to_list1:
                            to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == mm:
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.m_logis = to_list1.m_logis + genstat.logis / exchg_rate
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis = m_logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                        if to_list1:
                            to_list1.comp_m_room = to_list1.comp_m_room + 1
                            to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list1.y_logis = to_list1.y_logis + genstat.logis / exchg_rate
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis = y_logis + genstat.logis / exchg_rate

                if genstat.gratis == 0:

                    if to_list1:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list1 in query(to_list1_list):

            if (to_list1.room - to_list1.c_room) != 0:
                to_list1.avrgrate = to_list1.logis / (to_list1.room - to_list1.c_room)

            if to_list1.comp_room != 0:
                to_list1.exc_avrgrate = to_list1.logis / to_list1.comp_room

            if logis != 0:
                to_list1.proz = to_list1.logis / logis * 100

            if (to_list1.m_room - to_list1.mc_room) != 0:
                to_list1.m_avrgrate = to_list1.m_logis / (to_list1.m_room - to_list1.mc_room)

            if to_list1.comp_m_room != 0:
                to_list1.exc_m_avrgrate = to_list1.m_logis / to_list1.comp_m_room

            if m_logis != 0:
                to_list1.m_proz = to_list1.m_logis / m_logis * 100

            if (to_list1.y_room - to_list1.yc_room) != 0:
                to_list1.y_avrgrate = to_list1.y_logis / (to_list1.y_room - to_list1.yc_room)

            if to_list1.comp_y_room != 0:
                to_list1.exc_y_avrgrate = to_list1.y_logis / to_list1.comp_y_room

            if y_logis != 0:
                to_list1.y_proz = to_list1.y_logis / y_logis * 100

        for to_list in query(to_list_list, filters=(lambda to_list :to_list.y_room != 0)):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev = to_list.y_logis
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 = to_list.m_logis
            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 3
        avrgrate = 0

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)
        exc_avrgrate = 0

        if comp_room != 0:
            exc_avrgrate = logis / comp_room
        m_avrgrate = 0

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)
        exc_m_avrgrate = 0

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room
        y_avrgrate = 0

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        exc_y_avrgrate = 0

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev = to_list1.y_logis
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 = to_list1.m_logis
                output_list.name = to_list1.name
                output_list.room = to_list1.room
                output_list.pax = to_list1.pax
                output_list.logis = to_list1.logis
                output_list.proz = to_list1.proz
                output_list.avrgrate = to_list1.avrgrate
                output_list.m_room = to_list1.m_room
                output_list.m_pax = to_list1.m_pax
                output_list.m_logis = to_list1.m_logis
                output_list.m_proz = to_list1.m_proz
                output_list.m_avrgrate = to_list1.m_avrgrate
                output_list.y_room = to_list1.y_room
                output_list.y_pax = to_list1.y_pax
                output_list.y_logis = to_list1.y_logis
                output_list.y_proz = to_list1.y_proz
                output_list.y_avrgrate = to_list1.y_avrgrate
                output_list.comp_room = to_list1.comp_room
                output_list.comp_pax = to_list1.comp_pax
                output_list.comp_m_room = to_list1.comp_m_room
                output_list.comp_m_pax = to_list1.comp_m_pax
                output_list.comp_y_room = to_list1.comp_y_room
                output_list.comp_y_pax = to_list1.comp_y_pax
                output_list.exc_avrgrate = to_list1.exc_avrgrate
                output_list.exc_m_avrgrate = to_list1.exc_m_avrgrate
                output_list.exc_y_avrgrate = to_list1.exc_y_avrgrate


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 8
            avrgrate = 0

            if (room - c_room) != 0:
                avrgrate = logis / (room - c_room)
            exc_avrgrate = 0

            if comp_room != 0:
                exc_avrgrate = logis / comp_room
            m_avrgrate = 0

            if (m_room - mc_room) != 0:
                m_avrgrate = m_logis / (m_room - mc_room)
            exc_m_avrgrate = 0

            if comp_m_room != 0:
                exc_m_avrgrate = m_logis / comp_m_room
            y_avrgrate = 0

            if (y_room - yc_room) != 0:
                y_avrgrate = y_logis / (y_room - yc_room)
            exc_y_avrgrate = 0

            if comp_y_room != 0:
                exc_y_avrgrate = y_logis / comp_y_room
            output_list.name = "T o t a l"
            output_list.room = room
            output_list.pax = pax
            output_list.logis = logis
            output_list.proz = 100
            output_list.avrgrate = avrgrate
            output_list.m_room = m_room
            output_list.m_pax = m_pax
            output_list.m_logis = m_logis
            output_list.m_proz = 100
            output_list.m_avrgrate = m_avrgrate
            output_list.y_room = y_room
            output_list.y_pax = y_pax
            output_list.y_logis = y_logis
            output_list.y_proz = 100
            output_list.y_avrgrate = y_avrgrate
            output_list.comp_room = comp_room
            output_list.comp_pax = comp_pax
            output_list.comp_m_room = comp_m_room
            output_list.comp_m_pax = comp_m_pax
            output_list.comp_y_room = comp_y_room
            output_list.comp_y_pax = comp_y_pax
            output_list.exc_avrgrate = exc_avrgrate
            output_list.exc_m_avrgrate = exc_m_avrgrate
            output_list.exc_y_avrgrate = exc_y_avrgrate

    def create_umsatz5():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal buf_nation


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1, buf_nation
        nonlocal output_list_list, to_list_list, to_list1_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        Buf_nation = Nation
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        to_list_list.clear()

        for nation in db_session.query(Nation).filter(
                (Nation.natcode > 0)).all():

            to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == nationnr), first=True)

            if not to_list:
                to_list = To_list()
                to_list_list.append(to_list)

                to_list.gastnr = nationnr
                to_list.name = nation.bezeich

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.domestic == nationnr) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room :tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis = to_list.logis + genstat.logis / exchg_rate
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis = logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1 :tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    m_room = m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis = to_list.m_logis + genstat.logis / exchg_rate
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis = m_logis + genstat.logis / exchg_rate

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis = to_list.y_logis + genstat.logis / exchg_rate
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis = y_logis + genstat.logis / exchg_rate

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_list):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate = to_list.logis / (to_list.room - to_list.c_room)

            if to_list.comp_room != 0:
                to_list.exc_avrgrate = to_list.logis / to_list.comp_room

            if logis != 0:
                to_list.proz = to_list.logis / logis * 100

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate = to_list.m_logis / to_list.comp_m_room

            if m_logis != 0:
                to_list.m_proz = to_list.m_logis / m_logis * 100

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate = to_list.y_logis / to_list.comp_y_room

            if y_logis != 0:
                to_list.y_proz = to_list.y_logis / y_logis * 100

        for to_list in query(to_list_list, filters=(lambda to_list :to_list.y_room != 0)):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev = to_list.y_logis
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 = to_list.m_logis
            output_list.name = to_list.name
            output_list.room = to_list.room
            output_list.pax = to_list.pax
            output_list.logis = to_list.logis
            output_list.proz = to_list.proz
            output_list.avrgrate = to_list.avrgrate
            output_list.m_room = to_list.m_room
            output_list.m_pax = to_list.m_pax
            output_list.m_logis = to_list.m_logis
            output_list.m_proz = to_list.m_proz
            output_list.m_avrgrate = to_list.m_avrgrate
            output_list.y_room = to_list.y_room
            output_list.y_pax = to_list.y_pax
            output_list.y_logis = to_list.y_logis
            output_list.y_proz = to_list.y_proz
            output_list.y_avrgrate = to_list.y_avrgrate
            output_list.comp_room = to_list.comp_room
            output_list.comp_pax = to_list.comp_pax
            output_list.comp_m_room = to_list.comp_m_room
            output_list.comp_m_pax = to_list.comp_m_pax
            output_list.comp_y_room = to_list.comp_y_room
            output_list.comp_y_pax = to_list.comp_y_pax
            output_list.exc_avrgrate = to_list.exc_avrgrate
            output_list.exc_m_avrgrate = to_list.exc_m_avrgrate
            output_list.exc_y_avrgrate = to_list.exc_y_avrgrate


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 3
        avrgrate = 0

        if (room - c_room) != 0:
            avrgrate = logis / (room - c_room)
        exc_avrgrate = 0

        if comp_room != 0:
            exc_avrgrate = logis / comp_room
        m_avrgrate = 0

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)
        exc_m_avrgrate = 0

        if comp_m_room != 0:
            exc_m_avrgrate = m_logis / comp_m_room
        y_avrgrate = 0

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        exc_y_avrgrate = 0

        if comp_y_room != 0:
            exc_y_avrgrate = y_logis / comp_y_room
        output_list.name = "T o t a l"
        output_list.room = room
        output_list.pax = pax
        output_list.logis = logis
        output_list.proz = 100
        output_list.avrgrate = avrgrate
        output_list.m_room = m_room
        output_list.m_pax = m_pax
        output_list.m_logis = m_logis
        output_list.m_proz = 100
        output_list.m_avrgrate = m_avrgrate
        output_list.y_room = y_room
        output_list.y_pax = y_pax
        output_list.y_logis = y_logis
        output_list.y_proz = 100
        output_list.y_avrgrate = y_avrgrate
        output_list.comp_room = comp_room
        output_list.comp_pax = comp_pax
        output_list.comp_m_room = comp_m_room
        output_list.comp_m_pax = comp_m_pax
        output_list.comp_y_room = comp_y_room
        output_list.comp_y_pax = comp_y_pax
        output_list.exc_avrgrate = exc_avrgrate
        output_list.exc_m_avrgrate = exc_m_avrgrate
        output_list.exc_y_avrgrate = exc_y_avrgrate

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev = to_list1.y_logis
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 = to_list1.m_logis
                output_list.name = to_list1.name
                output_list.room = to_list1.room
                output_list.pax = to_list1.pax
                output_list.logis = to_list1.logis
                output_list.proz = to_list1.proz
                output_list.avrgrate = to_list1.avrgrate
                output_list.m_room = to_list1.m_room
                output_list.m_pax = to_list1.m_pax
                output_list.m_logis = to_list1.m_logis
                output_list.m_proz = to_list1.m_proz
                output_list.m_avrgrate = to_list1.m_avrgrate
                output_list.y_room = to_list1.y_room
                output_list.y_pax = to_list1.y_pax
                output_list.y_logis = to_list1.y_logis
                output_list.y_proz = to_list1.y_proz
                output_list.y_avrgrate = to_list1.y_avrgrate
                output_list.comp_room = to_list1.comp_room
                output_list.comp_pax = to_list1.comp_pax
                output_list.comp_m_room = to_list1.comp_m_room
                output_list.comp_m_pax = to_list1.comp_m_pax
                output_list.comp_y_room = to_list1.comp_y_room
                output_list.comp_y_pax = to_list1.comp_y_pax
                output_list.exc_avrgrate = to_list1.exc_avrgrate
                output_list.exc_m_avrgrate = to_list1.exc_m_avrgrate
                output_list.exc_y_avrgrate = to_list1.exc_y_avrgrate


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 8
            avrgrate = 0

            if (room - c_room) != 0:
                avrgrate = logis / (room - c_room)
            exc_avrgrate = 0

            if comp_room != 0:
                exc_avrgrate = logis / comp_room
            m_avrgrate = 0

            if (m_room - mc_room) != 0:
                m_avrgrate = m_logis / (m_room - mc_room)
            exc_m_avrgrate = 0

            if comp_m_room != 0:
                exc_m_avrgrate = m_logis / comp_m_room
            y_avrgrate = 0

            if (y_room - yc_room) != 0:
                y_avrgrate = y_logis / (y_room - yc_room)
            exc_y_avrgrate = 0

            if comp_y_room != 0:
                exc_y_avrgrate = y_logis / comp_y_room

            if price_decimal == 0 and currency_type == 1:
                output_list.name = "T o t a l"
                output_list.room = room
                output_list.pax = pax
                output_list.logis = logis
                output_list.proz = 100
                output_list.avrgrate = avrgrate
                output_list.m_room = m_room
                output_list.m_pax = m_pax
                output_list.m_logis = m_logis
                output_list.m_proz = 100
                output_list.m_avrgrate = m_avrgrate
                output_list.y_room = y_room
                output_list.y_pax = y_pax
                output_list.y_logis = y_logis
                output_list.y_proz = 100
                output_list.y_avrgrate = y_avrgrate
                output_list.comp_room = comp_room
                output_list.comp_pax = comp_pax
                output_list.comp_m_room = comp_m_room
                output_list.comp_m_pax = comp_m_pax
                output_list.comp_y_room = comp_y_room
                output_list.comp_y_pax = comp_y_pax
                output_list.exc_avrgrate = exc_avrgrate
                output_list.exc_m_avrgrate = exc_m_avrgrate
                output_list.exc_y_avrgrate = exc_y_avrgrate


    tot = translateExtended ("T o t a l", lvcarea, "")

    if cardtype_1 >= 10:
        cardtype = cardtype_1 - 10
        ota_only = True


    else:
        cardtype = cardtype_1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr

    if op_type == 0:

        if disptype == 1:

            if cardtype < 3:
                create_umsatz1()
            else:
                create_umsatz11()

        elif disptype == 2:
            create_umsatz2()

        elif disptype == 3:
            create_umsatz3()

        elif disptype == 4:
            create_umsatz4()

        elif disptype == 5:
            create_umsatz5()

    return generate_output()