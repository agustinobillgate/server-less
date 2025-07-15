#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Guest, Genstat, Exrate, Bediener, Nation, Queasy, Sourccod

def cr_rmproductbl(pvilanguage:int, op_type:int, printer_nr:int, call_from:int, txt_file:string, disptype:int, cardtype_1:int, currency_type:int, ytd_flag:int, excl_comp:bool, last_sort:int, f_date:date, t_date:date, to_date:date):

    prepare_cache ([Htparam, Waehrung, Guest, Genstat, Exrate, Bediener, Nation, Queasy, Sourccod])

    output_list_data = []
    lvcarea:string = "rm-product"
    cardtype:int = 0
    ota_only:bool = False
    foreign_nr:int = 0
    exchg_rate:Decimal = 1
    price_decimal:int = 0
    incl_comp:bool = True
    message_it:bool = True
    ind:int = 0
    room:int = 0
    c_room:int = 0
    pax:int = 0
    logis:Decimal = to_decimal("0.0")
    avrgrate:Decimal = to_decimal("0.0")
    exc_avrgrate:Decimal = to_decimal("0.0")
    comp_room:int = 0
    comp_pax:int = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:Decimal = to_decimal("0.0")
    m_avrgrate:Decimal = to_decimal("0.0")
    exc_m_avrgrate:Decimal = to_decimal("0.0")
    comp_m_room:int = 0
    comp_m_pax:int = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:Decimal = to_decimal("0.0")
    y_avrgrate:Decimal = to_decimal("0.0")
    exc_y_avrgrate:Decimal = to_decimal("0.0")
    comp_y_room:int = 0
    comp_y_pax:int = 0
    from_bez:string = ""
    to_bez:string = ""
    curr_select:string = ""
    tot:string = ""
    htparam = waehrung = guest = genstat = exrate = bediener = nation = queasy = sourccod = None

    output_list = to_list = to_list1 = tmp_room = tmp_room1 = None

    output_list_data, Output_list = create_model("Output_list", {"name":string, "room":Decimal, "pax":Decimal, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":Decimal, "m_pax":Decimal, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":Decimal, "y_pax":Decimal, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "comp_room":Decimal, "comp_pax":Decimal, "comp_m_room":Decimal, "comp_m_pax":Decimal, "comp_y_room":Decimal, "comp_y_pax":Decimal, "exc_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "flag":int, "name2":string, "rmnite1":int, "rmrev1":Decimal, "rmnite":int, "rmrev":Decimal})
    to_list_data, To_list = create_model("To_list", {"gastnr":int, "name":string, "zinr":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "exc_avrgrate":Decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "comp_y_room":int, "comp_y_pax":int})
    to_list1_data, To_list1 = create_model("To_list1", {"gastnr":int, "name":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "exc_avrgrate":Decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "comp_y_room":int, "comp_y_pax":int})
    tmp_room_data, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":string, "flag":int})
    tmp_room1_data, Tmp_room1 = create_model_like(Tmp_room)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

        return {"output-list": output_list_data}

    def create_umsatz1():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        curr_zinr:string = ""
        prev_zinr:string = ""
        do_it:bool = False
        curr_gastnr:int = 0
        prev_gastnr:int = 0
        beg_date:date = None
        incl_comp = not excl_comp
        room = 0
        c_room = 0
        comp_room = 0
        pax = 0
        logis =  to_decimal("0")
        m_room = 0
        mc_room = 0
        comp_m_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        y_room = 0
        yc_room = 0
        comp_y_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        to_list_data.clear()
        tmp_room_data.clear()
        tmp_room1_data.clear()

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.zinr, genstat.gastnr, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.gastnrmember, genstat.kind3, genstat._recid, guest.steuernr, guest.name, guest.vorname1, guest.phonetik3, guest.karteityp, guest._recid in db_session.query(Genstat.datum, Genstat.zinr, Genstat.gastnr, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.gastnrmember, Genstat.kind3, Genstat._recid, Guest.steuernr, Guest.name, Guest.vorname1, Guest.phonetik3, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 2 and ota_only:
                do_it = guest.steuernr != ""

            if do_it:
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_data.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_data.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_data.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.zinr, genstat.gastnr, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.gastnrmember, genstat.kind3, genstat._recid, guest.steuernr, guest.name, guest.vorname1, guest.phonetik3, guest.karteityp, guest._recid in db_session.query(Genstat.datum, Genstat.zinr, Genstat.gastnr, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.gastnrmember, Genstat.kind3, Genstat._recid, Guest.steuernr, Guest.name, Guest.vorname1, Guest.phonetik3, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.gratis == 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 2 and ota_only:
                do_it = guest.steuernr != ""

            if do_it:
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_data.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

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

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

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

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)
            output_list.name2 = to_list.name
            output_list.rmnite1 = to_list.y_room
            output_list.rmrev1 =  to_decimal(to_list.y_logis)
            output_list.rmnite = to_list.m_room
            output_list.rmrev =  to_decimal(to_list.m_logis)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)


    def create_umsatz11():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

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
        logis =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
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
        output_list_data.clear()
        to_list_data.clear()
        tmp_room_data.clear()
        tmp_room1_data.clear()

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest:
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_data.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_data.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.y_room = to_list.y_room + 1
                    to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    y_room = y_room + 1
                    y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_data.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnr
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if get_month(genstat.datum) == mm:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.y_room = to_list.y_room + 1
                    to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    y_room = y_room + 1
                    y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
            else:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if guest:

                    to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_data.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma

                        bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                        if bediener:
                            to_list.name = to_list.name + "=" + bediener.username

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                to_list.room = to_list.room + 1
                                room = room + 1
                                tmp_room = Tmp_room()
                                tmp_room_data.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnr
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                        if get_month(genstat.datum) == get_month(to_date):
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    else:

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                to_list.room = to_list.room + 1
                                room = room + 1
                                tmp_room = Tmp_room()
                                tmp_room_data.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnr
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                        if get_month(genstat.datum) == mm:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest:
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_data.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

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

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

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

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if guest:

                    to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_data.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma

                        bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                        if bediener:
                            to_list.name = to_list.name + "=" + bediener.username

                        if genstat.datum == to_date:

                            tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_data.append(tmp_room1)

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

                            tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_data.append(tmp_room1)

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

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)
            output_list.name2 = to_list.name
            output_list.rmnite1 = to_list.y_room
            output_list.rmrev1 =  to_decimal(to_list.y_logis)
            output_list.rmnite = to_list.m_room
            output_list.rmrev =  to_decimal(to_list.m_logis)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)


    def create_umsatz2():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        to_list_data.clear()
        to_list1_data.clear()

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            to_list = To_list()
            to_list_data.append(to_list)

            to_list.gastnr = nation.nationnr

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_data, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_data.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_data.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

            for genstat in db_session.query(Genstat).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                    if not tmp_room1:
                        to_list.comp_room = to_list.comp_room + 1
                        comp_room = comp_room + 1

                        if to_list1:
                            to_list1.comp_room = to_list1.comp_room + 1
                        tmp_room1 = Tmp_room1()
                        tmp_room1_data.append(tmp_room1)

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

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list1 in query(to_list1_data):

            if (to_list1.room - to_list1.c_room) != 0:
                to_list1.avrgrate =  to_decimal(to_list1.logis) / to_decimal((to_list1.room) - to_decimal(to_list1.c_room))

            if to_list1.comp_room != 0:
                to_list1.exc_avrgrate =  to_decimal(to_list1.logis) / to_decimal(to_list1.comp_room)

            if logis != 0:
                to_list1.proz =  to_decimal(to_list1.logis) / to_decimal(logis) * to_decimal("100")

            if (to_list1.m_room - to_list1.mc_room) != 0:
                to_list1.m_avrgrate =  to_decimal(to_list1.m_logis) / to_decimal((to_list1.m_room) - to_decimal(to_list1.mc_room))

            if to_list1.comp_m_room != 0:
                to_list1.exc_m_avrgrate =  to_decimal(to_list1.m_logis) / to_decimal(to_list1.comp_m_room)

            if m_logis != 0:
                to_list1.m_proz =  to_decimal(to_list1.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if (to_list1.y_room - to_list1.yc_room) != 0:
                to_list1.y_avrgrate =  to_decimal(to_list1.y_logis) / to_decimal((to_list1.y_room) - to_decimal(to_list1.yc_room))

            if to_list1.comp_y_room != 0:
                to_list1.exc_y_avrgrate =  to_decimal(to_list1.y_logis) / to_decimal(to_list1.comp_y_room)

            if y_logis != 0:
                to_list1.y_proz =  to_decimal(to_list1.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 0
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2
        avrgrate =  to_decimal("0")

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
        exc_avrgrate =  to_decimal("0")

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
        m_avrgrate =  to_decimal("0")

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
        exc_m_avrgrate =  to_decimal("0")

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
        y_avrgrate =  to_decimal("0")

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
        exc_y_avrgrate =  to_decimal("0")

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)

        to_list1 = query(to_list1_data, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 3
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 4
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_data, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 5
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_proz =  to_decimal(to_list1.y_proz)
                output_list.y_avrgrate =  to_decimal(to_list1.y_avrgrate)
                output_list.comp_room =  to_decimal(to_list1.comp_room)
                output_list.comp_pax =  to_decimal(to_list1.comp_pax)
                output_list.comp_m_room =  to_decimal(to_list1.comp_m_room)
                output_list.comp_m_pax =  to_decimal(to_list1.comp_m_pax)
                output_list.comp_y_room =  to_decimal(to_list1.comp_y_room)
                output_list.comp_y_pax =  to_decimal(to_list1.comp_y_pax)
                output_list.exc_avrgrate =  to_decimal(to_list1.exc_avrgrate)
                output_list.exc_m_avrgrate =  to_decimal(to_list1.exc_m_avrgrate)
                output_list.exc_y_avrgrate =  to_decimal(to_list1.exc_y_avrgrate)


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 6
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 7
            avrgrate =  to_decimal("0")

            if (room - c_room) != 0:
                avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
            exc_avrgrate =  to_decimal("0")

            if comp_room != 0:
                exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
            m_avrgrate =  to_decimal("0")

            if (m_room - mc_room) != 0:
                m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
            exc_m_avrgrate =  to_decimal("0")

            if comp_m_room != 0:
                exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
            y_avrgrate =  to_decimal("0")

            if (y_room - yc_room) != 0:
                y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
            exc_y_avrgrate =  to_decimal("0")

            if comp_y_room != 0:
                exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
            output_list.name = "T o t a l"
            output_list.room =  to_decimal(room)
            output_list.pax =  to_decimal(pax)
            output_list.logis =  to_decimal(logis)
            output_list.proz =  to_decimal("100")
            output_list.avrgrate =  to_decimal(avrgrate)
            output_list.m_room =  to_decimal(m_room)
            output_list.m_pax =  to_decimal(m_pax)
            output_list.m_logis =  to_decimal(m_logis)
            output_list.m_proz =  to_decimal("100")
            output_list.m_avrgrate =  to_decimal(m_avrgrate)
            output_list.y_room =  to_decimal(y_room)
            output_list.y_pax =  to_decimal(y_pax)
            output_list.y_logis =  to_decimal(y_logis)
            output_list.y_proz =  to_decimal("100")
            output_list.y_avrgrate =  to_decimal(y_avrgrate)
            output_list.comp_room =  to_decimal(comp_room)
            output_list.comp_pax =  to_decimal(comp_pax)
            output_list.comp_m_room =  to_decimal(comp_m_room)
            output_list.comp_m_pax =  to_decimal(comp_m_pax)
            output_list.comp_y_room =  to_decimal(comp_y_room)
            output_list.comp_y_pax =  to_decimal(comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)


    def create_umsatz3():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

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
        logis =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        to_list_data.clear()
        to_list1_data.clear()

        for sourccod in db_session.query(Sourccod).order_by(Sourccod._recid).all():
            to_list = To_list()
            to_list_data.append(to_list)

            to_list.gastnr = sourccod.source_code
            to_list.name = sourccod.bezeich

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == sourccod.source_code) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_data.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == mm:
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 1
            output_list.name = to_string(to_list.name, "x(40)")
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 3
        avrgrate =  to_decimal("0")

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
        exc_avrgrate =  to_decimal("0")

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
        m_avrgrate =  to_decimal("0")

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
        exc_m_avrgrate =  to_decimal("0")

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
        y_avrgrate =  to_decimal("0")

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
        exc_y_avrgrate =  to_decimal("0")

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)


    def create_umsatz4():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        to_list_data.clear()
        to_list1_data.clear()

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            to_list = To_list()
            to_list_data.append(to_list)

            to_list.gastnr = nation.nationnr

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_data, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_data.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.resident != 0) & (Genstat.segmentcode != 0) & (Genstat.resident == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                datum = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datum)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_data.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

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
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

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
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                if genstat.gratis == 0:

                    if to_list1:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list1 in query(to_list1_data):

            if (to_list1.room - to_list1.c_room) != 0:
                to_list1.avrgrate =  to_decimal(to_list1.logis) / to_decimal((to_list1.room) - to_decimal(to_list1.c_room))

            if to_list1.comp_room != 0:
                to_list1.exc_avrgrate =  to_decimal(to_list1.logis) / to_decimal(to_list1.comp_room)

            if logis != 0:
                to_list1.proz =  to_decimal(to_list1.logis) / to_decimal(logis) * to_decimal("100")

            if (to_list1.m_room - to_list1.mc_room) != 0:
                to_list1.m_avrgrate =  to_decimal(to_list1.m_logis) / to_decimal((to_list1.m_room) - to_decimal(to_list1.mc_room))

            if to_list1.comp_m_room != 0:
                to_list1.exc_m_avrgrate =  to_decimal(to_list1.m_logis) / to_decimal(to_list1.comp_m_room)

            if m_logis != 0:
                to_list1.m_proz =  to_decimal(to_list1.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if (to_list1.y_room - to_list1.yc_room) != 0:
                to_list1.y_avrgrate =  to_decimal(to_list1.y_logis) / to_decimal((to_list1.y_room) - to_decimal(to_list1.yc_room))

            if to_list1.comp_y_room != 0:
                to_list1.exc_y_avrgrate =  to_decimal(to_list1.y_logis) / to_decimal(to_list1.comp_y_room)

            if y_logis != 0:
                to_list1.y_proz =  to_decimal(to_list1.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 3
        avrgrate =  to_decimal("0")

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
        exc_avrgrate =  to_decimal("0")

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
        m_avrgrate =  to_decimal("0")

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
        exc_m_avrgrate =  to_decimal("0")

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
        y_avrgrate =  to_decimal("0")

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
        exc_y_avrgrate =  to_decimal("0")

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)

        to_list1 = query(to_list1_data, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_data, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_proz =  to_decimal(to_list1.y_proz)
                output_list.y_avrgrate =  to_decimal(to_list1.y_avrgrate)
                output_list.comp_room =  to_decimal(to_list1.comp_room)
                output_list.comp_pax =  to_decimal(to_list1.comp_pax)
                output_list.comp_m_room =  to_decimal(to_list1.comp_m_room)
                output_list.comp_m_pax =  to_decimal(to_list1.comp_m_pax)
                output_list.comp_y_room =  to_decimal(to_list1.comp_y_room)
                output_list.comp_y_pax =  to_decimal(to_list1.comp_y_pax)
                output_list.exc_avrgrate =  to_decimal(to_list1.exc_avrgrate)
                output_list.exc_m_avrgrate =  to_decimal(to_list1.exc_m_avrgrate)
                output_list.exc_y_avrgrate =  to_decimal(to_list1.exc_y_avrgrate)


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 8
            avrgrate =  to_decimal("0")

            if (room - c_room) != 0:
                avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
            exc_avrgrate =  to_decimal("0")

            if comp_room != 0:
                exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
            m_avrgrate =  to_decimal("0")

            if (m_room - mc_room) != 0:
                m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
            exc_m_avrgrate =  to_decimal("0")

            if comp_m_room != 0:
                exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
            y_avrgrate =  to_decimal("0")

            if (y_room - yc_room) != 0:
                y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
            exc_y_avrgrate =  to_decimal("0")

            if comp_y_room != 0:
                exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
            output_list.name = "T o t a l"
            output_list.room =  to_decimal(room)
            output_list.pax =  to_decimal(pax)
            output_list.logis =  to_decimal(logis)
            output_list.proz =  to_decimal("100")
            output_list.avrgrate =  to_decimal(avrgrate)
            output_list.m_room =  to_decimal(m_room)
            output_list.m_pax =  to_decimal(m_pax)
            output_list.m_logis =  to_decimal(m_logis)
            output_list.m_proz =  to_decimal("100")
            output_list.m_avrgrate =  to_decimal(m_avrgrate)
            output_list.y_room =  to_decimal(y_room)
            output_list.y_pax =  to_decimal(y_pax)
            output_list.y_logis =  to_decimal(y_logis)
            output_list.y_proz =  to_decimal("100")
            output_list.y_avrgrate =  to_decimal(y_avrgrate)
            output_list.comp_room =  to_decimal(comp_room)
            output_list.comp_pax =  to_decimal(comp_pax)
            output_list.comp_m_room =  to_decimal(comp_m_room)
            output_list.comp_m_pax =  to_decimal(comp_m_pax)
            output_list.comp_y_room =  to_decimal(comp_y_room)
            output_list.comp_y_pax =  to_decimal(comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)


    def create_umsatz5():

        nonlocal output_list_data, lvcarea, cardtype, ota_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, curr_select, tot, htparam, waehrung, guest, genstat, exrate, bediener, nation, queasy, sourccod
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date


        nonlocal output_list, to_list, to_list1, tmp_room, tmp_room1
        nonlocal output_list_data, to_list_data, to_list1_data, tmp_room_data, tmp_room1_data

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        buf_nation = None
        beg_date:date = None
        Buf_nation =  create_buffer("Buf_nation",Nation)
        incl_comp = not excl_comp
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

        if ytd_flag == 2:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        to_list_data.clear()

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode > 0)).order_by(Nation._recid).all():

            to_list = query(to_list_data, filters=(lambda to_list: to_list.gastnr == nation.nationnr), first=True)

            if not to_list:
                to_list = To_list()
                to_list_data.append(to_list)

                to_list.gastnr = nation.nationnr
                to_list.name = nation.bezeich

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.datum, genstat.zinr, genstat.gastnr, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.logis, genstat.gastnrmember, genstat.kind3, genstat._recid, guest.steuernr, guest.name, guest.vorname1, guest.phonetik3, guest.karteityp, guest._recid in db_session.query(Genstat.datum, Genstat.zinr, Genstat.gastnr, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.logis, Genstat.gastnrmember, Genstat.kind3, Genstat._recid, Guest.steuernr, Guest.name, Guest.vorname1, Guest.phonetik3, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.domestic == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_data, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1
                        tmp_room = Tmp_room()
                        tmp_room_data.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnr
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.pax = to_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    pax = pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_data, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_data.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_pax = comp_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    m_room = m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_pax = m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        comp_m_pax = comp_m_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs + genstat.kind1 + genstat.kind2

        for to_list in query(to_list_data):

            if (to_list.room - to_list.c_room) != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal((to_list.room) - to_decimal(to_list.c_room))

            if to_list.comp_room != 0:
                to_list.exc_avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.comp_room)

            if logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(logis) * to_decimal("100")

            if (to_list.m_room - to_list.mc_room) != 0:
                to_list.m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal((to_list.m_room) - to_decimal(to_list.mc_room))

            if to_list.comp_m_room != 0:
                to_list.exc_m_avrgrate =  to_decimal(to_list.m_logis) / to_decimal(to_list.comp_m_room)

            if m_logis != 0:
                to_list.m_proz =  to_decimal(to_list.m_logis) / to_decimal(m_logis) * to_decimal("100")

            if (to_list.y_room - to_list.yc_room) != 0:
                to_list.y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal((to_list.y_room) - to_decimal(to_list.yc_room))

            if to_list.comp_y_room != 0:
                to_list.exc_y_avrgrate =  to_decimal(to_list.y_logis) / to_decimal(to_list.comp_y_room)

            if y_logis != 0:
                to_list.y_proz =  to_decimal(to_list.y_logis) / to_decimal(y_logis) * to_decimal("100")

        for to_list in query(to_list_data, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_proz =  to_decimal(to_list.y_proz)
            output_list.y_avrgrate =  to_decimal(to_list.y_avrgrate)
            output_list.comp_room =  to_decimal(to_list.comp_room)
            output_list.comp_pax =  to_decimal(to_list.comp_pax)
            output_list.comp_m_room =  to_decimal(to_list.comp_m_room)
            output_list.comp_m_pax =  to_decimal(to_list.comp_m_pax)
            output_list.comp_y_room =  to_decimal(to_list.comp_y_room)
            output_list.comp_y_pax =  to_decimal(to_list.comp_y_pax)
            output_list.exc_avrgrate =  to_decimal(to_list.exc_avrgrate)
            output_list.exc_m_avrgrate =  to_decimal(to_list.exc_m_avrgrate)
            output_list.exc_y_avrgrate =  to_decimal(to_list.exc_y_avrgrate)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = 3
        avrgrate =  to_decimal("0")

        if (room - c_room) != 0:
            avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
        exc_avrgrate =  to_decimal("0")

        if comp_room != 0:
            exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
        m_avrgrate =  to_decimal("0")

        if (m_room - mc_room) != 0:
            m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
        exc_m_avrgrate =  to_decimal("0")

        if comp_m_room != 0:
            exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
        y_avrgrate =  to_decimal("0")

        if (y_room - yc_room) != 0:
            y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
        exc_y_avrgrate =  to_decimal("0")

        if comp_y_room != 0:
            exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)
        output_list.name = "T o t a l"
        output_list.room =  to_decimal(room)
        output_list.pax =  to_decimal(pax)
        output_list.logis =  to_decimal(logis)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_proz =  to_decimal("100")
        output_list.y_avrgrate =  to_decimal(y_avrgrate)
        output_list.comp_room =  to_decimal(comp_room)
        output_list.comp_pax =  to_decimal(comp_pax)
        output_list.comp_m_room =  to_decimal(comp_m_room)
        output_list.comp_m_pax =  to_decimal(comp_m_pax)
        output_list.comp_y_room =  to_decimal(comp_y_room)
        output_list.comp_y_pax =  to_decimal(comp_y_pax)
        output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
        output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
        output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)

        to_list1 = query(to_list1_data, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_data, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_proz =  to_decimal(to_list1.y_proz)
                output_list.y_avrgrate =  to_decimal(to_list1.y_avrgrate)
                output_list.comp_room =  to_decimal(to_list1.comp_room)
                output_list.comp_pax =  to_decimal(to_list1.comp_pax)
                output_list.comp_m_room =  to_decimal(to_list1.comp_m_room)
                output_list.comp_m_pax =  to_decimal(to_list1.comp_m_pax)
                output_list.comp_y_room =  to_decimal(to_list1.comp_y_room)
                output_list.comp_y_pax =  to_decimal(to_list1.comp_y_pax)
                output_list.exc_avrgrate =  to_decimal(to_list1.exc_avrgrate)
                output_list.exc_m_avrgrate =  to_decimal(to_list1.exc_m_avrgrate)
                output_list.exc_y_avrgrate =  to_decimal(to_list1.exc_y_avrgrate)


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 8
            avrgrate =  to_decimal("0")

            if (room - c_room) != 0:
                avrgrate =  to_decimal(logis) / to_decimal((room) - to_decimal(c_room))
            exc_avrgrate =  to_decimal("0")

            if comp_room != 0:
                exc_avrgrate =  to_decimal(logis) / to_decimal(comp_room)
            m_avrgrate =  to_decimal("0")

            if (m_room - mc_room) != 0:
                m_avrgrate =  to_decimal(m_logis) / to_decimal((m_room) - to_decimal(mc_room))
            exc_m_avrgrate =  to_decimal("0")

            if comp_m_room != 0:
                exc_m_avrgrate =  to_decimal(m_logis) / to_decimal(comp_m_room)
            y_avrgrate =  to_decimal("0")

            if (y_room - yc_room) != 0:
                y_avrgrate =  to_decimal(y_logis) / to_decimal((y_room) - to_decimal(yc_room))
            exc_y_avrgrate =  to_decimal("0")

            if comp_y_room != 0:
                exc_y_avrgrate =  to_decimal(y_logis) / to_decimal(comp_y_room)

            if price_decimal == 0 and currency_type == 1:
                output_list.name = "T o t a l"
                output_list.room =  to_decimal(room)
                output_list.pax =  to_decimal(pax)
                output_list.logis =  to_decimal(logis)
                output_list.proz =  to_decimal("100")
                output_list.avrgrate =  to_decimal(avrgrate)
                output_list.m_room =  to_decimal(m_room)
                output_list.m_pax =  to_decimal(m_pax)
                output_list.m_logis =  to_decimal(m_logis)
                output_list.m_proz =  to_decimal("100")
                output_list.m_avrgrate =  to_decimal(m_avrgrate)
                output_list.y_room =  to_decimal(y_room)
                output_list.y_pax =  to_decimal(y_pax)
                output_list.y_logis =  to_decimal(y_logis)
                output_list.y_proz =  to_decimal("100")
                output_list.y_avrgrate =  to_decimal(y_avrgrate)
                output_list.comp_room =  to_decimal(comp_room)
                output_list.comp_pax =  to_decimal(comp_pax)
                output_list.comp_m_room =  to_decimal(comp_m_room)
                output_list.comp_m_pax =  to_decimal(comp_m_pax)
                output_list.comp_y_room =  to_decimal(comp_y_room)
                output_list.comp_y_pax =  to_decimal(comp_y_pax)
                output_list.exc_avrgrate =  to_decimal(exc_avrgrate)
                output_list.exc_m_avrgrate =  to_decimal(exc_m_avrgrate)
                output_list.exc_y_avrgrate =  to_decimal(exc_y_avrgrate)

    tot = translateExtended ("T o t a l", lvcarea, "")

    if cardtype_1 >= 10:
        cardtype = cardtype_1 - 10
        ota_only = True


    else:
        cardtype = cardtype_1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

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