#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from sqlalchemy import func
from models import Htparam, Waehrung, Nation, Segment, Zimkateg, Res_line, Guest, Genstat, Guestseg, Exrate, Bediener, Queasy, Sourccod, Arrangement

def cr_rmproduct_3_webbl(pvilanguage:int, op_type:int, printer_nr:int, call_from:int, txt_file:string, disptype_1:int, cardtype_1:int, currency_type:int, ytd_flag:int, excl_comp:bool, last_sort:int, f_date:date, t_date:date, to_date:date, argt_code:string, dispopt:bool):

    prepare_cache ([Htparam, Waehrung, Nation, Segment, Zimkateg, Res_line, Genstat, Exrate, Bediener, Queasy, Sourccod, Arrangement])

    output_list_list = []
    lvcarea:string = "rm-product"
    cardtype:int = 0
    ota_only:bool = False
    comp_only:bool = False
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
    rmrev:Decimal = to_decimal("0.0")
    avrgrate:Decimal = to_decimal("0.0")
    exc_avrgrate:Decimal = to_decimal("0.0")
    comp_room:int = 0
    comp_pax:int = 0
    m_room:int = 0
    mc_room:int = 0
    m_pax:int = 0
    m_logis:Decimal = to_decimal("0.0")
    m_rmrev:Decimal = to_decimal("0.0")
    m_avrgrate:Decimal = to_decimal("0.0")
    exc_m_avrgrate:Decimal = to_decimal("0.0")
    comp_m_room:int = 0
    comp_m_pax:int = 0
    y_room:int = 0
    yc_room:int = 0
    y_pax:int = 0
    y_logis:Decimal = to_decimal("0.0")
    y_rmrev:Decimal = to_decimal("0.0")
    y_avrgrate:Decimal = to_decimal("0.0")
    exc_y_avrgrate:Decimal = to_decimal("0.0")
    comp_y_room:int = 0
    comp_y_pax:int = 0
    from_bez:string = ""
    to_bez:string = ""
    fdate_mtd:date = None
    from_date:date = None
    mm:int = 0
    yy:int = 0
    curr_select:string = ""
    rmrate:Decimal = to_decimal("0.0")
    m_rmrate:Decimal = to_decimal("0.0")
    y_rmrate:Decimal = to_decimal("0.0")
    d_child:int = 0
    m_child:int = 0
    y_child:int = 0
    d_los:Decimal = to_decimal("0.0")
    mtd_los:Decimal = to_decimal("0.0")
    ytd_los:Decimal = to_decimal("0.0")
    curr_d_reslinnr:int = 0
    curr_d_resnr:int = 0
    tot_d_room_resv:int = 0
    curr_m_reslinnr:int = 0
    curr_m_resnr:int = 0
    tot_m_room_resv:int = 0
    curr_y_reslinnr:int = 0
    curr_y_resnr:int = 0
    tot_y_room_resv:int = 0
    tot_d_anztage:int = 0
    tot_m_anztage:int = 0
    tot_y_anztage:int = 0
    curr_d_reslinnr1:int = 0
    curr_d_resnr1:int = 0
    tot_d_room_resv1:int = 0
    curr_m_reslinnr1:int = 0
    curr_m_resnr1:int = 0
    tot_m_room_resv1:int = 0
    curr_y_reslinnr1:int = 0
    curr_y_resnr1:int = 0
    do_it:bool = False
    datums:date = None
    curr_zinr:string = ""
    prev_zinr:string = ""
    curr_gastnr:int = 0
    prev_gastnr:int = 0
    tot:string = ""
    per_region:bool = False
    disptype:int = 0
    intsegment:int = 0
    ota_segment:string = ""
    default_country:int = 0
    tot_pax_d:int = 0
    tot_pax_m:int = 0
    tot_pax_y:int = 0
    htparam = waehrung = nation = segment = zimkateg = res_line = guest = genstat = guestseg = exrate = bediener = queasy = sourccod = arrangement = None

    output_list = to_list = to_list1 = segm1_list = zikat_list = tmp_room = tmp_room1 = None

    output_list_list, Output_list = create_model("Output_list", {"name":string, "room":Decimal, "pax":Decimal, "logis":Decimal, "trmrev":Decimal, "proz":Decimal, "avrgrate":Decimal, "m_room":Decimal, "m_pax":Decimal, "m_logis":Decimal, "m_rmrev":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":Decimal, "y_pax":Decimal, "y_logis":Decimal, "y_rmrev":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "comp_room":Decimal, "comp_pax":Decimal, "comp_m_room":Decimal, "comp_m_pax":Decimal, "comp_y_room":Decimal, "comp_y_pax":Decimal, "exc_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "flag":int, "name2":string, "rmnite1":int, "rmrev1":Decimal, "rmnite":int, "rmrev":Decimal, "refcode":string, "rmrate":Decimal, "m_rmrate":Decimal, "y_rmrate":Decimal, "d_child":int, "m_child":int, "y_child":int, "d_los":Decimal, "mtd_los":Decimal, "ytd_los":Decimal, "d_resv":int, "m_resv":int, "y_resv":int, "d_anztage":int, "m_anztage":int, "y_anztage":int, "tot_d_room_resv":int, "tot_m_room_resv":int, "tot_y_room_resv":int})
    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":string, "zinr":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "rmrev":Decimal, "proz":Decimal, "avrgrate":Decimal, "exc_avrgrate":Decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_rmrev":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_rmrev":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "comp_y_room":int, "comp_y_pax":int, "subgroup":int, "refcode":string, "rmrate":Decimal, "m_rmrate":Decimal, "y_rmrate":Decimal, "d_child":int, "m_child":int, "y_child":int, "d_los":Decimal, "mtd_los":Decimal, "ytd_los":Decimal, "d_resv":int, "m_resv":int, "y_resv":int, "d_anztage":int, "m_anztage":int, "y_anztage":int, "tot_d_room_resv":int, "tot_m_room_resv":int, "tot_y_room_resv":int})
    to_list1_list, To_list1 = create_model("To_list1", {"gastnr":int, "name":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "rmrev":Decimal, "proz":Decimal, "avrgrate":Decimal, "exc_avrgrate":Decimal, "comp_room":int, "comp_pax":int, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_rmrev":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "exc_m_avrgrate":Decimal, "comp_m_room":int, "comp_m_pax":int, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_rmrev":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal, "exc_y_avrgrate":Decimal, "comp_y_room":int, "comp_y_pax":int, "refcode":string, "rmrate":Decimal, "m_rmrate":Decimal, "y_rmrate":Decimal, "d_child":int, "m_child":int, "y_child":int, "d_los":Decimal, "mtd_los":Decimal, "ytd_los":Decimal, "d_resv":int, "m_resv":int, "y_resv":int, "d_anztage":int, "m_anztage":int, "y_anztage":int, "tot_d_room_resv":int, "tot_m_room_resv":int, "tot_y_room_resv":int})
    segm1_list_list, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":string, "bezeich1":string}, {"selected": True})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string}, {"selected": True})
    tmp_room_list, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":string, "flag":int})
    tmp_room1_list, Tmp_room1 = create_model_like(Tmp_room)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, from_date, mm, yy, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        return {"output-list": output_list_list}

    def create_umsatz1():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        beg_date:date = None
        incl_comp = not excl_comp
        room = 0
        c_room = 0
        comp_room = 0
        pax = 0
        logis =  to_decimal("0")
        rmrev =  to_decimal("0")
        m_room = 0
        mc_room = 0
        comp_m_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        m_rmrev =  to_decimal("0")
        y_room = 0
        yc_room = 0
        comp_y_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        y_rmrev =  to_decimal("0")
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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

        genstat_obj_list = {}
        for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr, Genstat.resnr, Genstat.res_int[inc_value(0)]).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 2 and ota_only:

                if ota_segment != "":

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
                    while None != guestseg:
                        do_it = matches(ota_segment, ("*" + to_string(guestseg.segmentcode)) + "*")

                        if do_it:
                            break

                        curr_recid = guestseg._recid
                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg._recid > curr_recid)).first()
                else:
                    do_it = guest.steuernr != ""

            elif guest.karteityp == 1 and comp_only:
                do_it = guest.steuernr != ""

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    to_list.refcode = guest.steuernr

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.d_anztage = to_list.d_anztage + 1
                        tot_d_anztage = tot_d_anztage + 1

                        if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                            to_list.d_resv = to_list.d_resv + 1
                            tot_d_room_resv = tot_d_room_resv + 1
                            curr_d_reslinnr = res_line.reslinnr
                            curr_d_resnr = genstat.resnr
                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                        to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                        d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                        to_list.m_anztage = to_list.m_anztage + 1
                        tot_m_anztage = tot_m_anztage + 1

                        if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                            to_list.m_resv = to_list.m_resv + 1
                            tot_m_room_resv = tot_m_room_resv + 1
                            curr_m_reslinnr = res_line.reslinnr
                            curr_m_resnr = genstat.resnr
                        to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                        mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                        to_list.y_anztage = to_list.y_anztage + 1
                        tot_y_anztage = tot_y_anztage + 1

                        if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                            to_list.y_resv = to_list.y_resv + 1
                            tot_y_room_resv = tot_y_room_resv + 1
                            curr_y_reslinnr = res_line.reslinnr
                            curr_y_resnr = genstat.resnr
                        to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                        ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                        y_child = y_child + genstat.kind1 + genstat.kind2
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.d_anztage = to_list.d_anztage + 1
                        tot_d_anztage = tot_d_anztage + 1

                        if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                            to_list.d_resv = to_list.d_resv + 1
                            tot_d_room_resv = tot_d_room_resv + 1
                            curr_d_reslinnr = res_line.reslinnr
                            curr_d_resnr = genstat.resnr
                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                        to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                        d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                        to_list.m_anztage = to_list.m_anztage + 1
                        tot_m_anztage = tot_m_anztage + 1

                        if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                            to_list.m_resv = to_list.m_resv + 1
                            tot_m_room_resv = tot_m_room_resv + 1
                            curr_m_reslinnr = res_line.reslinnr
                            curr_m_resnr = genstat.resnr
                        to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                        mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                        to_list.m_anztage = to_list.m_anztage + 1
                        tot_m_anztage = tot_m_anztage + 1

                        if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                            to_list.m_resv = to_list.m_resv + 1
                            tot_m_room_resv = tot_m_room_resv + 1
                            curr_m_reslinnr = res_line.reslinnr
                            curr_m_resnr = genstat.resnr
                        to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                        mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                        to_list.y_anztage = to_list.y_anztage + 1
                        tot_y_anztage = tot_y_anztage + 1

                        if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                            to_list.y_resv = to_list.y_resv + 1
                            tot_y_room_resv = tot_y_room_resv + 1
                            curr_y_reslinnr = res_line.reslinnr
                            curr_y_resnr = genstat.resnr
                        to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                        ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                        y_child = y_child + genstat.kind1 + genstat.kind2

        genstat_obj_list = {}
        for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.gratis == 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr, Genstat.resnr, Genstat.res_int[inc_value(0)]).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 2 and ota_only:

                if ota_segment != "":

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
                    while None != guestseg:
                        do_it = matches(ota_segment, ("*" + to_string(guestseg.segmentcode)) + "*")

                        if do_it:
                            break

                        curr_recid = guestseg._recid
                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg._recid > curr_recid)).first()
                else:
                    do_it = guest.steuernr != ""

            elif guest.karteityp == 1 and comp_only:
                do_it = guest.steuernr != ""

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                    to_list.refcode = guest.steuernr

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs
                else:

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.refcode = to_list.refcode
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage


    def create_umsatz1_1():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0

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

        genstat_obj_list = {}
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 1 and ota_only:

                if ota_segment != "":

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
                    while None != guestseg:
                        do_it = matches(ota_segment, ("*" + to_string(guestseg.segmentcode)) + "*")

                        if do_it:
                            break

                        curr_recid = guestseg._recid
                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg._recid > curr_recid)).first()
                else:
                    do_it = guest.steuernr != ""

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    to_list.refcode = guest.steuernr

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.d_los =  to_decimal(to_list.d_los) + to_decimal("1")
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        d_los =  to_decimal(d_los) + to_decimal("1")
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.mtd_los =  to_decimal(to_list.mtd_los) + to_decimal("1")
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        mtd_los =  to_decimal(mtd_los) + to_decimal("1")
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.ytd_los =  to_decimal(to_list.ytd_los) + to_decimal("1")
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        ytd_los =  to_decimal(ytd_los) + to_decimal("1")
                        y_child = y_child + genstat.kind1 + genstat.kind2
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.d_los =  to_decimal(to_list.d_los) + to_decimal("1")
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        d_los =  to_decimal(d_los) + to_decimal("1")
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.mtd_los =  to_decimal(to_list.mtd_los) + to_decimal("1")
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        mtd_los =  to_decimal(mtd_los) + to_decimal("1")
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.ytd_los =  to_decimal(to_list.ytd_los) + to_decimal("1")
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        ytd_los =  to_decimal(ytd_los) + to_decimal("1")
                        y_child = y_child + genstat.kind1 + genstat.kind2

        genstat_obj_list = {}
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.gratis == 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 1 and ota_only:

                if ota_segment != "":

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
                    while None != guestseg:
                        do_it = matches(ota_segment, ("*" + to_string(guestseg.segmentcode)) + "*")

                        if do_it:
                            break

                        curr_recid = guestseg._recid
                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg._recid > curr_recid)).first()
                else:
                    do_it = guest.steuernr != ""

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma
                    to_list.refcode = guest.steuernr

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs
                else:

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.refcode = to_list.refcode
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child


    def create_umsatz1_2():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0

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

        genstat_obj_list = {}
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 2 and ota_only:
                do_it = guest.steuernr == "1"

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.d_los =  to_decimal(to_list.d_los) + to_decimal("1")
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        d_los =  to_decimal(d_los) + to_decimal("1")
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.mtd_los =  to_decimal(to_list.mtd_los) + to_decimal("1")
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        mtd_los =  to_decimal(mtd_los) + to_decimal("1")
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.ytd_los =  to_decimal(to_list.ytd_los) + to_decimal("1")
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        ytd_los =  to_decimal(ytd_los) + to_decimal("1")
                        y_child = y_child + genstat.kind1 + genstat.kind2
                else:

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.d_los =  to_decimal(to_list.d_los) + to_decimal("1")
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        d_los =  to_decimal(d_los) + to_decimal("1")
                        d_child = d_child + genstat.kind1 + genstat.kind2

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.m_room = to_list.m_room + 1
                        m_room = m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.mtd_los =  to_decimal(to_list.mtd_los) + to_decimal("1")
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        mtd_los =  to_decimal(mtd_los) + to_decimal("1")
                        m_child = m_child + genstat.kind1 + genstat.kind2

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.y_room = to_list.y_room + 1
                        y_room = y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.ytd_los =  to_decimal(to_list.ytd_los) + to_decimal("1")
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        ytd_los =  to_decimal(ytd_los) + to_decimal("1")
                        y_child = y_child + genstat.kind1 + genstat.kind2

        genstat_obj_list = {}
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.gratis == 0) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Guest.gastnr, Genstat.zinr).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if guest.karteityp == 1 and ota_only:
                do_it = guest.steuernr != ""

            if do_it:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                prev_zinr = curr_zinr
                curr_zinr = genstat.zinr
                prev_gastnr = curr_gastnr
                curr_gastnr = genstat.gastnr

                to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                if not to_list:
                    to_list = To_list()
                    to_list_list.append(to_list)

                    to_list.gastnr = genstat.gastnr
                    to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                            guest.anrede1 + guest.anredefirma

                    bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                    if bediener:
                        to_list.name = to_list.name + "=" + bediener.username

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs
                else:

                    if genstat.datum == to_date:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == get_month(to_date):
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs

                    if ytd_flag == 1 or ytd_flag == 2:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child


    def create_umsatz11():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        curr_gastnr:int = 1
        beg_date:date = None
        incl_comp = not excl_comp
        room = 0
        c_room = 0
        pax = 0
        logis =  to_decimal("0")
        rmrev =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        m_rmrev =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        y_rmrev =  to_decimal("0")
        comp_pax = 0
        comp_room = 0
        comp_y_room = 0
        comp_y_pax = 0
        comp_m_room = 0
        comp_m_pax = 0
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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

        genstat_obj_list = {}
        for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode, Genstat.resnr, Genstat.res_int[0]).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")
                do_it = True

                if guest.karteityp == 1 and comp_only:
                    do_it = guest.steuernr != ""

                if do_it :

                    if currency_type == 2:

                        if foreign_nr != 0:

                            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                        else:

                            exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                        if exrate:
                            exchg_rate =  to_decimal(exrate.betrag)

                    to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_list.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                        to_list.refcode = guest.steuernr

                        bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                        if bediener:
                            to_list.name = to_list.name + "=" + bediener.username

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                to_list.room = to_list.room + 1
                                room = room + 1
                                tmp_room = Tmp_room()
                                tmp_room_list.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnrmember
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.d_anztage = to_list.d_anztage + 1
                            tot_d_anztage = tot_d_anztage + 1

                            if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                                to_list.d_resv = to_list.d_resv + 1
                                tot_d_room_resv = tot_d_room_resv + 1
                                curr_d_reslinnr = res_line.reslinnr
                                curr_d_resnr = genstat.resnr
                            to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                            to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                            to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                            to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs + genstat.gratis
                            logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                            d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                            d_child = d_child + genstat.kind1 + genstat.kind2

                        if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                            to_list.m_anztage = to_list.m_anztage + 1
                            tot_m_anztage = tot_m_anztage + 1

                            if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                to_list.m_resv = to_list.m_resv + 1
                                tot_m_room_resv = tot_m_room_resv + 1
                                curr_m_reslinnr = res_line.reslinnr
                                curr_m_resnr = genstat.resnr
                            to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                            to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                            m_pax = m_pax + genstat.erwachs + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                            mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                            m_child = m_child + genstat.kind1 + genstat.kind2

                        elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                            to_list.m_anztage = to_list.m_anztage + 1
                            tot_m_anztage = tot_m_anztage + 1

                            if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                to_list.m_resv = to_list.m_resv + 1
                                tot_m_room_resv = tot_m_room_resv + 1
                                curr_m_reslinnr = res_line.reslinnr
                                curr_m_resnr = genstat.resnr
                            to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                            to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                            m_pax = m_pax + genstat.erwachs + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                            mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                            m_child = m_child + genstat.kind1 + genstat.kind2
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                        to_list.y_anztage = to_list.y_anztage + 1
                        tot_y_anztage = tot_y_anztage + 1

                        if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                            to_list.y_resv = to_list.y_resv + 1
                            tot_y_room_resv = tot_y_room_resv + 1
                            curr_y_reslinnr = res_line.reslinnr
                            curr_y_resnr = genstat.resnr
                        to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                        ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                        y_child = y_child + genstat.kind1 + genstat.kind2
                    else:

                        if genstat.datum == to_date:

                            tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                            if not tmp_room:
                                tmp_room = Tmp_room()
                                tmp_room_list.append(tmp_room)

                                tmp_room.gastnr = genstat.gastnr
                                tmp_room.zinr = genstat.zinr
                                tmp_room.flag = 1


                            to_list.d_anztage = to_list.d_anztage + 1
                            tot_d_anztage = tot_d_anztage + 1

                            if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                                to_list.d_resv = to_list.d_resv + 1
                                tot_d_room_resv = tot_d_room_resv + 1
                                curr_d_reslinnr = res_line.reslinnr
                                curr_d_resnr = genstat.resnr
                            to_list.room = to_list.room + 1
                            room = room + 1
                            to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                            to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                            to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                            to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                            pax = pax + genstat.erwachs + genstat.gratis
                            logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                            d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                            d_child = d_child + genstat.kind1 + genstat.kind2

                        if get_month(genstat.datum) == mm and ytd_flag == 1:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                            to_list.m_anztage = to_list.m_anztage + 1
                            tot_m_anztage = tot_m_anztage + 1

                            if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                to_list.m_resv = to_list.m_resv + 1
                                tot_m_room_resv = tot_m_room_resv + 1
                                curr_m_reslinnr = res_line.reslinnr
                                curr_m_resnr = genstat.resnr
                            to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                            to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                            m_pax = m_pax + genstat.erwachs + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                            mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                            m_child = m_child + genstat.kind1 + genstat.kind2

                        elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                            to_list.m_room = to_list.m_room + 1
                            m_room = m_room + 1
                            to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                            to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                            to_list.m_anztage = to_list.m_anztage + 1
                            tot_m_anztage = tot_m_anztage + 1

                            if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                to_list.m_resv = to_list.m_resv + 1
                                tot_m_room_resv = tot_m_room_resv + 1
                                curr_m_reslinnr = res_line.reslinnr
                                curr_m_resnr = genstat.resnr
                            to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                            to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                            m_pax = m_pax + genstat.erwachs + genstat.gratis
                            m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                            mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                            m_child = m_child + genstat.kind1 + genstat.kind2
                        to_list.y_room = to_list.y_room + 1
                        to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                        to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                        to_list.y_anztage = to_list.y_anztage + 1
                        tot_y_anztage = tot_y_anztage + 1

                        if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                            to_list.y_resv = to_list.y_resv + 1
                            tot_y_room_resv = tot_y_room_resv + 1
                            curr_y_reslinnr = res_line.reslinnr
                            curr_y_resnr = genstat.resnr
                        to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                        to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                        y_room = y_room + 1
                        y_pax = y_pax + genstat.erwachs + genstat.gratis
                        y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                        ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                        y_child = y_child + genstat.kind1 + genstat.kind2
            else:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if guest:
                    do_it = True

                    if guest.karteityp == 1 and comp_only:
                        do_it = guest.steuernr != ""

                    if do_it :

                        to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                        if not to_list:
                            to_list = To_list()
                            to_list_list.append(to_list)

                            to_list.gastnr = genstat.gastnr
                            to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            to_list.refcode = guest.steuernr

                            bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                            if bediener:
                                to_list.name = to_list.name + "=" + bediener.username

                            if genstat.datum == to_date:

                                tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                                if not tmp_room:
                                    to_list.room = to_list.room + 1
                                    room = room + 1
                                    tmp_room = Tmp_room()
                                    tmp_room_list.append(tmp_room)

                                    tmp_room.gastnr = genstat.gastnr
                                    tmp_room.zinr = genstat.zinr
                                    tmp_room.flag = 1


                                to_list.d_anztage = to_list.d_anztage + 1
                                tot_d_anztage = tot_d_anztage + 1

                                if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                                    to_list.d_resv = to_list.d_resv + 1
                                    tot_d_room_resv = tot_d_room_resv + 1
                                    curr_d_reslinnr = res_line.reslinnr
                                    curr_d_resnr = genstat.resnr
                                to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                                to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                                to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                                to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                                pax = pax + genstat.erwachs + genstat.gratis
                                logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                                d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                                d_child = d_child + genstat.kind1 + genstat.kind2

                            if get_month(genstat.datum) == mm and ytd_flag == 1:
                                to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                                to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                                m_pax = m_pax + genstat.erwachs + genstat.gratis
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)

                            elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                                to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                                to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                                m_pax = m_pax + genstat.erwachs + genstat.gratis
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                            to_list.y_room = to_list.y_room + 1
                            to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                            to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                            to_list.y_anztage = to_list.y_anztage + 1
                            tot_y_anztage = tot_y_anztage + 1

                            if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                                to_list.y_resv = to_list.y_resv + 1
                                tot_y_room_resv = tot_y_room_resv + 1
                                curr_y_reslinnr = res_line.reslinnr
                                curr_y_resnr = genstat.resnr
                            to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                            to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                            y_room = y_room + 1
                            y_pax = y_pax + genstat.erwachs + genstat.gratis
                            y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                            ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                            y_child = y_child + genstat.kind1 + genstat.kind2
                        else:

                            if genstat.datum == to_date:

                                tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                                if not tmp_room:
                                    to_list.room = to_list.room + 1
                                    room = room + 1
                                    tmp_room = Tmp_room()
                                    tmp_room_list.append(tmp_room)

                                    tmp_room.gastnr = genstat.gastnr
                                    tmp_room.zinr = genstat.zinr
                                    tmp_room.flag = 1


                                to_list.d_anztage = to_list.d_anztage + 1
                                tot_d_anztage = tot_d_anztage + 1

                                if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                                    to_list.d_resv = to_list.d_resv + 1
                                    tot_d_room_resv = tot_d_room_resv + 1
                                    curr_d_reslinnr = res_line.reslinnr
                                    curr_d_resnr = genstat.resnr
                                to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                                to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                                to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                                to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                                pax = pax + genstat.erwachs + genstat.gratis
                                logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                                d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                                d_child = d_child + genstat.kind1 + genstat.kind2

                            if get_month(genstat.datum) == mm and ytd_flag == 1:
                                to_list.m_room = to_list.m_room + 1
                                m_room = m_room + 1
                                to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                                to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                                to_list.m_anztage = to_list.m_anztage + 1
                                tot_m_anztage = tot_m_anztage + 1

                                if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                    to_list.m_resv = to_list.m_resv + 1
                                    tot_m_room_resv = tot_m_room_resv + 1
                                    curr_m_reslinnr = res_line.reslinnr
                                    curr_m_resnr = genstat.resnr
                                to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                                to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                                m_pax = m_pax + genstat.erwachs + genstat.gratis
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                                mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                                m_child = m_child + genstat.kind1 + genstat.kind2

                            elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                                to_list.m_room = to_list.m_room + 1
                                m_room = m_room + 1
                                to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                                to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                                to_list.m_anztage = to_list.m_anztage + 1
                                tot_m_anztage = tot_m_anztage + 1

                                if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                                    to_list.m_resv = to_list.m_resv + 1
                                    tot_m_room_resv = tot_m_room_resv + 1
                                    curr_m_reslinnr = res_line.reslinnr
                                    curr_m_resnr = genstat.resnr
                                to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                                to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                                m_pax = m_pax + genstat.erwachs + genstat.gratis
                                m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                                m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                                m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                                mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                                m_child = m_child + genstat.kind1 + genstat.kind2
                            to_list.y_room = to_list.y_room + 1
                            to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                            to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                            to_list.y_anztage = to_list.y_anztage + 1
                            tot_y_anztage = tot_y_anztage + 1

                            if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                                to_list.y_resv = to_list.y_resv + 1
                                tot_y_room_resv = tot_y_room_resv + 1
                                curr_y_reslinnr = res_line.reslinnr
                                curr_y_resnr = genstat.resnr
                            to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                            to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                            y_room = y_room + 1
                            y_pax = y_pax + genstat.erwachs + genstat.gratis
                            y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                            y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                            y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                            ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                            y_child = y_child + genstat.kind1 + genstat.kind2

        genstat_obj_list = {}
        for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
            if not segm1_list:
                continue

            zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest:
                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)
                do_it = True

                if guest.karteityp == 1 and comp_only:
                    do_it = guest.steuernr != ""

                if do_it :

                    to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_list.append(to_list)

                        to_list.gastnr = genstat.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma
                        to_list.refcode = guest.steuernr

                        bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                        if bediener:
                            to_list.name = to_list.name + "=" + bediener.username

                        if genstat.datum == to_date:

                            tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_list.append(tmp_room1)

                                tmp_room1.gastnr = genstat.gastnrmember
                                tmp_room1.zinr = genstat.zinr
                                tmp_room1.flag = 1


                            to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                            comp_pax = comp_pax + genstat.erwachs

                        if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                            comp_m_pax = comp_m_pax + genstat.erwachs

                        elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                            comp_m_pax = comp_m_pax + genstat.erwachs
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs
                    else:

                        if genstat.datum == to_date:

                            tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_list.append(tmp_room1)

                                tmp_room1.gastnr = genstat.gastnrmember
                                tmp_room1.zinr = genstat.zinr
                                tmp_room1.flag = 1


                            to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                            comp_pax = comp_pax + genstat.erwachs

                        if get_month(genstat.datum) == mm and ytd_flag == 1:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                            comp_m_pax = comp_m_pax + genstat.erwachs

                        elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            comp_m_room = comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                            comp_m_pax = comp_m_pax + genstat.erwachs
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        comp_y_room = comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_pax = comp_y_pax + genstat.erwachs
            else:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if guest:
                    do_it = True

                    if guest.karteityp == 1 and comp_only:
                        do_it = guest.steuernr != ""

                    if do_it :

                        to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == genstat.gastnr), first=True)

                        if not to_list:
                            to_list = To_list()
                            to_list_list.append(to_list)

                            to_list.gastnr = genstat.gastnr
                            to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                    guest.anrede1 + guest.anredefirma
                            to_list.refcode = guest.steuernr

                            bediener = get_cache (Bediener, {"userinit": [(eq, guest.phonetik3)]})

                            if bediener:
                                to_list.name = to_list.name + "=" + bediener.username

                            if genstat.datum == to_date:

                                tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                                if not tmp_room1:
                                    to_list.comp_room = to_list.comp_room + 1
                                    comp_room = comp_room + 1
                                    tmp_room1 = Tmp_room1()
                                    tmp_room1_list.append(tmp_room1)

                                    tmp_room1.gastnr = genstat.gastnr
                                    tmp_room1.zinr = genstat.zinr
                                    tmp_room1.flag = 1


                                to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                                comp_pax = comp_pax + genstat.erwachs

                            if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                                to_list.comp_m_room = to_list.comp_m_room + 1
                                comp_m_room = comp_m_room + 1
                                to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                                comp_m_pax = comp_m_pax + genstat.erwachs

                            elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                                to_list.comp_m_room = to_list.comp_m_room + 1
                                comp_m_room = comp_m_room + 1
                                to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                                comp_m_pax = comp_m_pax + genstat.erwachs
                            to_list.comp_y_room = to_list.comp_y_room + 1
                            to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                            comp_y_room = comp_y_room + 1
                            comp_y_pax = comp_y_pax + genstat.erwachs
                        else:

                            if genstat.datum == to_date:

                                tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                                if not tmp_room1:
                                    to_list.comp_room = to_list.comp_room + 1
                                    comp_room = comp_room + 1
                                    tmp_room1 = Tmp_room1()
                                    tmp_room1_list.append(tmp_room1)

                                    tmp_room1.gastnr = genstat.gastnr
                                    tmp_room1.zinr = genstat.zinr
                                    tmp_room1.flag = 1


                                to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                                comp_pax = comp_pax + genstat.erwachs

                            if get_month(genstat.datum) == get_month(to_date) and ytd_flag == 1:
                                to_list.comp_m_room = to_list.comp_m_room + 1
                                comp_m_room = comp_m_room + 1
                                to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                                comp_m_pax = comp_m_pax + genstat.erwachs

                            elif ytd_flag == 2 and genstat.datum >= f_date and genstat.datum <= to_date:
                                to_list.comp_m_room = to_list.comp_m_room + 1
                                comp_m_room = comp_m_room + 1
                                to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                                comp_m_pax = comp_m_pax + genstat.erwachs
                            to_list.comp_y_room = to_list.comp_y_room + 1
                            comp_y_room = comp_y_room + 1
                            to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                            comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.refcode = to_list.refcode
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage


    def create_umsatz2():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nation.nationnr

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            genstat_obj_list = {}
            for genstat, zimkateg, res_line in db_session.query(Genstat, Zimkateg, Res_line).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if genstat.nationnr == default_country and genstat.domestic == 0:
                    continue

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.rmrev =  to_decimal(to_list1.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.d_resv = to_list.d_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.d_anztage = to_list1.d_anztage + 1
                        to_list1.d_los =  to_decimal(to_list1.d_anztage) / to_decimal(to_list1.d_resv)
                        to_list1.d_child = to_list1.d_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                                to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.m_rmrev =  to_decimal(to_list1.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.m_rmrate =  to_decimal(to_list1.m_rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.m_resv = to_list.m_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.m_anztage = to_list1.m_anztage + 1
                        to_list1.mtd_los =  to_decimal(to_list1.m_anztage) / to_decimal(to_list1.m_resv)
                        to_list1.m_child = to_list1.m_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_m_room = to_list1.comp_m_room + 1
                            to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + genstat.erwachs + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list1.y_rmrate =  to_decimal(to_list1.y_rmrate) + to_decimal(genstat.zipreis)

                    if curr_y_resnr1 != genstat.resnr or curr_y_reslinnr1 != genstat.res_int[0]:
                        to_list1.y_resv = to_list1.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list1.y_anztage = to_list1.y_anztage + 1
                    to_list1.ytd_los =  to_decimal(to_list1.y_anztage) / to_decimal(to_list1.y_resv)
                    to_list1.y_child = to_list1.y_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list1 in query(to_list1_list):

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

        for to_list in query(to_list_list, filters=(lambda to_list: to_list.room == 0 and to_list.pax == 0 and to_list.logis == 0 and to_list.proz == 0 and to_list.rmrev == 0 and to_list.avrgrate == 0 and to_list.m_room == 0 and to_list.m_pax == 0 and to_list.m_logis == 0 and to_list.m_rmrev == 0 and to_list.m_proz == 0 and to_list.m_avrgrate == 0 and to_list.y_room == 0 and to_list.y_pax == 0 and to_list.y_logis == 0 and to_list.y_rmrev == 0 and to_list.y_proz == 0 and to_list.y_avrgrate == 0 and to_list.comp_room == 0 and to_list.comp_pax == 0 and to_list.comp_m_room == 0 and to_list.comp_m_pax == 0 and to_list.comp_y_room == 0 and to_list.comp_y_pax == 0 and to_list.exc_avrgrate == 0 and to_list.exc_m_avrgrate == 0 and to_list.exc_y_avrgrate == 0)):
            to_list_list.remove(to_list)

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 0
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 3
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 5
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.trmrev =  to_decimal(to_list1.rmrev)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_rmrev =  to_decimal(to_list1.m_rmrev)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_rmrev =  to_decimal(to_list1.y_rmrev)
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
                output_list.rmrate =  to_decimal(to_list1.rmrate)
                output_list.m_rmrate =  to_decimal(to_list1.m_rmrate)
                output_list.y_rmrate =  to_decimal(to_list1.y_rmrate)
                output_list.d_los =  to_decimal(to_list1.d_los)
                output_list.mtd_los =  to_decimal(to_list1.mtd_los)
                output_list.ytd_los =  to_decimal(to_list1.ytd_los)
                output_list.d_child = to_list1.d_child
                output_list.m_child = to_list1.m_child
                output_list.y_child = to_list1.y_child
                output_list.d_resv = to_list1.d_resv
                output_list.m_resv = to_list1.m_resv
                output_list.y_resv = to_list1.y_resv
                output_list.d_anztage = to_list1.d_anztage
                output_list.m_anztage = to_list1.m_anztage
                output_list.y_anztage = to_list1.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 6
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.trmrev =  to_decimal(rmrev)
            output_list.proz =  to_decimal("100")
            output_list.avrgrate =  to_decimal(avrgrate)
            output_list.m_room =  to_decimal(m_room)
            output_list.m_pax =  to_decimal(m_pax)
            output_list.m_logis =  to_decimal(m_logis)
            output_list.m_rmrev =  to_decimal(m_rmrev)
            output_list.m_proz =  to_decimal("100")
            output_list.m_avrgrate =  to_decimal(m_avrgrate)
            output_list.y_room =  to_decimal(y_room)
            output_list.y_pax =  to_decimal(y_pax)
            output_list.y_logis =  to_decimal(y_logis)
            output_list.y_rmrev =  to_decimal(y_rmrev)
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
            output_list.rmrate =  to_decimal(rmrate)
            output_list.m_rmrate =  to_decimal(m_rmrate)
            output_list.y_rmrate =  to_decimal(y_rmrate)
            output_list.d_los =  to_decimal(d_los)
            output_list.mtd_los =  to_decimal(mtd_los)
            output_list.ytd_los =  to_decimal(ytd_los)
            output_list.d_child = d_child
            output_list.m_child = m_child
            output_list.y_child = y_child


    def create_umsatz3():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        curr_code:int = 0
        beg_date:date = None
        doit:bool = True
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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

        for sourccod in db_session.query(Sourccod).order_by(Sourccod._recid).all():
            doit = True

            if sourccod.betriebsnr != 0:

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == sourccod.source_code) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).first()

                if not genstat:
                    doit = False

            if doit:
                to_list = To_list()
                to_list_list.append(to_list)

                to_list.gastnr = sourccod.source_code
                to_list.name = sourccod.bezeich

                genstat_obj_list = {}
                for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.source == sourccod.source_code) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                    segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                    if not segm1_list:
                        continue

                    zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                    if not zikat_list:
                        continue

                    if genstat_obj_list.get(genstat._recid):
                        continue
                    else:
                        genstat_obj_list[genstat._recid] = True


                    datums = genstat.datum
                    exchg_rate =  to_decimal("1")

                    if currency_type == 2:

                        if foreign_nr != 0:

                            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                        else:

                            exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                        if exrate:
                            exchg_rate =  to_decimal(exrate.betrag)

                    if genstat.datum == to_date:

                        tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                        if not tmp_room:
                            to_list.room = to_list.room + 1
                            room = room + 1

                            if to_list1:
                                to_list1.room = to_list1.room + 1
                            tmp_room = Tmp_room()
                            tmp_room_list.append(tmp_room)

                            tmp_room.gastnr = genstat.gastnrmember
                            tmp_room.zinr = genstat.zinr
                            tmp_room.flag = 1


                        to_list.d_anztage = to_list.d_anztage + 1
                        tot_d_anztage = tot_d_anztage + 1

                        if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                            to_list.d_resv = to_list.d_resv + 1
                            tot_d_room_resv = tot_d_room_resv + 1
                            curr_d_reslinnr = res_line.reslinnr
                            curr_d_resnr = genstat.resnr
                        to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                        to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                        to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                        to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                        pax = pax + genstat.erwachs + genstat.gratis
                        logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                        d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                        d_child = d_child + genstat.kind1 + genstat.kind2

                        if genstat.gratis == 0:

                            tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                            if not tmp_room1:
                                to_list.comp_room = to_list.comp_room + 1
                                comp_room = comp_room + 1

                                if to_list1:
                                    to_list1.comp_room = to_list1.comp_room + 1
                                tmp_room1 = Tmp_room1()
                                tmp_room1_list.append(tmp_room1)

                                tmp_room1.gastnr = genstat.gastnrmember
                                tmp_room1.zinr = genstat.zinr
                                tmp_room1.flag = 1


                            to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                            comp_pax = comp_pax + genstat.erwachs

                    if get_month(genstat.datum) == mm:
                        to_list.m_room = to_list.m_room + 1
                        to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                        to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                        to_list.m_anztage = to_list.m_anztage + 1
                        tot_m_anztage = tot_m_anztage + 1

                        if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                            to_list.m_resv = to_list.m_resv + 1
                            tot_m_room_resv = tot_m_room_resv + 1
                            curr_m_reslinnr = res_line.reslinnr
                            curr_m_resnr = genstat.resnr
                        to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                        to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                        m_room = m_room + 1
                        m_pax = m_pax + genstat.erwachs + genstat.gratis
                        m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                        mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                        m_child = m_child + genstat.kind1 + genstat.kind2

                        if genstat.gratis == 0:
                            to_list.comp_m_room = to_list.comp_m_room + 1
                            to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                            comp_m_room = comp_m_room + 1
                            comp_m_pax = comp_m_pax + genstat.erwachs
                    to_list.y_room = to_list.y_room + 1
                    to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                    to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                    to_list.y_anztage = to_list.y_anztage + 1
                    tot_y_anztage = tot_y_anztage + 1

                    if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                        to_list.y_resv = to_list.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                    to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                    y_room = y_room + 1
                    y_pax = y_pax + genstat.erwachs + genstat.gratis
                    y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                    ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                    y_child = y_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_y_room = to_list.comp_y_room + 1
                        to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                        comp_y_room = comp_y_room + 1
                        comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.name = to_string(to_list.name, "x(24)")
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage


    def create_umsatz4():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nation.nationnr

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            genstat_obj_list = {}
            for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.resident != 0) & (Genstat.segmentcode != 0) & (Genstat.resident == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.rmrev =  to_decimal(to_list1.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.d_resv = to_list.d_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.d_anztage = to_list1.d_anztage + 1
                        to_list1.d_los =  to_decimal(to_list1.d_anztage) / to_decimal(to_list1.d_resv)
                        to_list1.d_child = to_list1.d_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

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


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs

                if get_month(genstat.datum) == mm:
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.m_rmrev =  to_decimal(to_list1.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.m_rmrate =  to_decimal(to_list1.m_rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.m_resv = to_list.m_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.m_anztage = to_list1.m_anztage + 1
                        to_list1.mtd_los =  to_decimal(to_list1.m_anztage) / to_decimal(to_list1.m_resv)
                        to_list1.m_child = to_list1.m_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_m_room = to_list1.comp_m_room + 1
                            to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + genstat.erwachs + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list1.y_rmrev =  to_decimal(to_list1.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list1.y_rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                    if curr_y_resnr1 != genstat.resnr or curr_y_reslinnr1 != genstat.res_int[0]:
                        to_list1.y_resv = to_list1.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list1.y_anztage = to_list1.y_anztage + 1
                    to_list1.ytd_los =  to_decimal(to_list1.y_anztage) / to_decimal(to_list1.y_resv)
                    to_list1.y_child = to_list1.y_child + genstat.kind1 + genstat.kind2

                if genstat.gratis == 0:

                    if to_list1:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list1 in query(to_list1_list):

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

        for to_list in query(to_list_list, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.trmrev =  to_decimal(to_list1.rmrev)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_rmrev =  to_decimal(to_list1.m_rmrev)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_rmrev =  to_decimal(to_list1.y_rmrev)
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
                output_list.rmrate =  to_decimal(to_list1.rmrate)
                output_list.m_rmrate =  to_decimal(to_list1.m_rmrate)
                output_list.y_rmrate =  to_decimal(to_list1.y_rmrate)
                output_list.d_los =  to_decimal(to_list1.d_los)
                output_list.mtd_los =  to_decimal(to_list1.mtd_los)
                output_list.ytd_los =  to_decimal(to_list1.ytd_los)
                output_list.d_child = to_list1.d_child
                output_list.m_child = to_list1.m_child
                output_list.y_child = to_list1.y_child
                output_list.d_resv = to_list1.d_resv
                output_list.m_resv = to_list1.m_resv
                output_list.y_resv = to_list1.y_resv
                output_list.d_anztage = to_list1.d_anztage
                output_list.m_anztage = to_list1.m_anztage
                output_list.y_anztage = to_list1.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.trmrev =  to_decimal(rmrev)
            output_list.proz =  to_decimal("100")
            output_list.avrgrate =  to_decimal(avrgrate)
            output_list.m_room =  to_decimal(m_room)
            output_list.m_pax =  to_decimal(m_pax)
            output_list.m_logis =  to_decimal(m_logis)
            output_list.m_rmrev =  to_decimal(m_rmrev)
            output_list.m_proz =  to_decimal("100")
            output_list.m_avrgrate =  to_decimal(m_avrgrate)
            output_list.y_room =  to_decimal(y_room)
            output_list.y_pax =  to_decimal(y_pax)
            output_list.y_logis =  to_decimal(y_logis)
            output_list.y_rmrev =  to_decimal(y_rmrev)
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
            output_list.rmrate =  to_decimal(rmrate)
            output_list.m_rmrate =  to_decimal(m_rmrate)
            output_list.y_rmrate =  to_decimal(y_rmrate)
            output_list.d_los =  to_decimal(d_los)
            output_list.mtd_los =  to_decimal(mtd_los)
            output_list.ytd_los =  to_decimal(ytd_los)
            output_list.d_child = d_child
            output_list.m_child = m_child
            output_list.y_child = y_child


    def create_umsatz5():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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
                 (Nation.natcode == default_country)).order_by(Nation._recid).all():

            to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == nation.nationnr), first=True)

            if not to_list:
                to_list = To_list()
                to_list_list.append(to_list)

                to_list.gastnr = nation.nationnr
                to_list.name = nation.bezeich

            genstat_obj_list = {}
            for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.natcode) & (Genstat.domestic == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    m_room = m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        comp_m_room = comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_pax = comp_m_pax + genstat.erwachs
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    comp_y_room = comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                    comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list in query(to_list_list, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 5
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 6
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.trmrev =  to_decimal(to_list1.rmrev)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_rmrev =  to_decimal(to_list1.m_rmrev)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_rmrev =  to_decimal(to_list1.y_rmrev)
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
                output_list.rmrate =  to_decimal(to_list1.rmrate)
                output_list.m_rmrate =  to_decimal(to_list1.m_rmrate)
                output_list.y_rmrate =  to_decimal(to_list1.y_rmrate)
                output_list.d_los =  to_decimal(to_list1.d_los)
                output_list.mtd_los =  to_decimal(to_list1.mtd_los)
                output_list.ytd_los =  to_decimal(to_list1.ytd_los)
                output_list.d_child = to_list1.d_child
                output_list.m_child = to_list1.m_child
                output_list.y_child = to_list1.y_child
                output_list.d_resv = to_list1.d_resv
                output_list.m_resv = to_list1.m_resv
                output_list.y_resv = to_list1.y_resv
                output_list.d_anztage = to_list1.d_anztage
                output_list.m_anztage = to_list1.m_anztage
                output_list.y_anztage = to_list1.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 7
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

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
                output_list.trmrev =  to_decimal(rmrev)
                output_list.proz =  to_decimal("100")
                output_list.avrgrate =  to_decimal(avrgrate)
                output_list.m_room =  to_decimal(m_room)
                output_list.m_pax =  to_decimal(m_pax)
                output_list.m_logis =  to_decimal(m_logis)
                output_list.m_rmrev =  to_decimal(m_rmrev)
                output_list.m_proz =  to_decimal("100")
                output_list.m_avrgrate =  to_decimal(m_avrgrate)
                output_list.y_room =  to_decimal(y_room)
                output_list.y_pax =  to_decimal(y_pax)
                output_list.y_logis =  to_decimal(y_logis)
                output_list.y_rmrev =  to_decimal(y_rmrev)
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
                output_list.rmrate =  to_decimal(rmrate)
                output_list.m_rmrate =  to_decimal(m_rmrate)
                output_list.y_rmrate =  to_decimal(y_rmrate)
                output_list.d_los =  to_decimal(d_los)
                output_list.mtd_los =  to_decimal(mtd_los)
                output_list.ytd_los =  to_decimal(ytd_los)
                output_list.d_child = d_child
                output_list.m_child = m_child
                output_list.y_child = y_child


    def create_umsatz6():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nation.nationnr

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            genstat_obj_list = {}
            for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.rmrev =  to_decimal(to_list1.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.d_resv = to_list.d_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.d_anztage = to_list1.d_anztage + 1
                        to_list1.d_los =  to_decimal(to_list1.d_anztage) / to_decimal(to_list1.d_resv)
                        to_list1.d_child = to_list1.d_child + genstat.kind1 + genstat.kind2

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.m_rmrev =  to_decimal(to_list1.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.m_rmrate =  to_decimal(to_list1.m_rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.m_resv = to_list.m_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.m_anztage = to_list1.m_anztage + 1
                        to_list1.mtd_los =  to_decimal(to_list1.m_anztage) / to_decimal(to_list1.m_resv)
                        to_list1.m_child = to_list1.m_child + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + to_list.pax + genstat.erwachs + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list1.y_rmrev =  to_decimal(to_list1.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list1.y_rmrate =  to_decimal(to_list1.y_rmrate) + to_decimal(genstat.zipreis)

                    if curr_y_resnr1 != genstat.resnr or curr_y_reslinnr1 != genstat.res_int[0]:
                        to_list1.y_resv = to_list1.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list1.y_anztage = to_list1.y_anztage + 1
                    to_list1.ytd_los =  to_decimal(to_list1.y_anztage) / to_decimal(to_list1.y_resv)
                    to_list1.y_child = to_list1.y_child + genstat.kind1 + genstat.kind2

            genstat_obj_list = {}
            for genstat in db_session.query(Genstat).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                    if not tmp_room1:
                        to_list.comp_room = to_list.comp_room + 1
                        comp_room = comp_room + 1

                        if to_list1:
                            to_list1.comp_room = to_list1.comp_room + 1
                        tmp_room1 = Tmp_room1()
                        tmp_room1_list.append(tmp_room1)

                        tmp_room1.gastnr = genstat.gastnrmember
                        tmp_room1.zinr = genstat.zinr
                        tmp_room1.flag = 1


                    to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                    comp_pax = comp_pax + genstat.erwachs

                    if to_list1:
                        to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.comp_m_room = to_list.comp_m_room + 1
                    to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                    comp_m_room = comp_m_room + 1
                    comp_m_pax = comp_m_pax + genstat.erwachs

                    if to_list1:
                        to_list1.comp_m_room = to_list1.comp_m_room + 1
                        to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs

                if to_list1:
                    to_list1.comp_y_room = to_list1.comp_y_room + 1
                    to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs
                to_list.comp_y_room = to_list.comp_y_room + 1
                to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                comp_y_room = comp_y_room + 1
                comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list1 in query(to_list1_list):

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

        for to_list in query(to_list_list, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 1
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage

        to_list1 = query(to_list1_list, first=True)

        if to_list1:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 3
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 4
            output_list.name = translateExtended ("*** STATISTIC BY REGION ***", lvcarea, "")

            for to_list1 in query(to_list1_list, sort_by=[("name",False)]):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 5
                output_list.rmnite = to_list1.y_room
                output_list.rmrev =  to_decimal(to_list1.y_logis)
                output_list.rmnite1 = to_list1.m_room
                output_list.rmrev1 =  to_decimal(to_list1.m_logis)
                output_list.name = to_list1.name
                output_list.room =  to_decimal(to_list1.room)
                output_list.pax =  to_decimal(to_list1.pax)
                output_list.logis =  to_decimal(to_list1.logis)
                output_list.trmrev =  to_decimal(to_list1.rmrev)
                output_list.proz =  to_decimal(to_list1.proz)
                output_list.avrgrate =  to_decimal(to_list1.avrgrate)
                output_list.m_room =  to_decimal(to_list1.m_room)
                output_list.m_pax =  to_decimal(to_list1.m_pax)
                output_list.m_logis =  to_decimal(to_list1.m_logis)
                output_list.m_rmrev =  to_decimal(to_list1.m_rmrev)
                output_list.m_proz =  to_decimal(to_list1.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
                output_list.y_room =  to_decimal(to_list1.y_room)
                output_list.y_pax =  to_decimal(to_list1.y_pax)
                output_list.y_logis =  to_decimal(to_list1.y_logis)
                output_list.y_rmrev =  to_decimal(to_list1.y_rmrev)
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
                output_list.rmrate =  to_decimal(to_list1.rmrate)
                output_list.m_rmrate =  to_decimal(to_list1.m_rmrate)
                output_list.y_rmrate =  to_decimal(to_list1.y_rmrate)
                output_list.d_los =  to_decimal(to_list1.d_los)
                output_list.mtd_los =  to_decimal(to_list1.mtd_los)
                output_list.ytd_los =  to_decimal(to_list1.ytd_los)
                output_list.d_child = to_list1.d_child
                output_list.m_child = to_list1.m_child
                output_list.y_child = to_list1.y_child
                output_list.d_resv = to_list1.d_resv
                output_list.m_resv = to_list1.m_resv
                output_list.y_resv = to_list1.y_resv
                output_list.d_anztage = to_list1.d_anztage
                output_list.m_anztage = to_list1.m_anztage
                output_list.y_anztage = to_list1.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 6
            for ind in range(1,280 + 1) :
                output_list.name = output_list.name + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

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
            output_list.trmrev =  to_decimal(rmrev)
            output_list.proz =  to_decimal("100")
            output_list.avrgrate =  to_decimal(avrgrate)
            output_list.m_room =  to_decimal(m_room)
            output_list.m_pax =  to_decimal(m_pax)
            output_list.m_logis =  to_decimal(m_logis)
            output_list.m_rmrev =  to_decimal(m_rmrev)
            output_list.m_proz =  to_decimal("100")
            output_list.m_avrgrate =  to_decimal(m_avrgrate)
            output_list.y_room =  to_decimal(y_room)
            output_list.y_pax =  to_decimal(y_pax)
            output_list.y_logis =  to_decimal(y_logis)
            output_list.y_rmrev =  to_decimal(y_rmrev)
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
            output_list.rmrate =  to_decimal(rmrate)
            output_list.m_rmrate =  to_decimal(m_rmrate)
            output_list.y_rmrate =  to_decimal(y_rmrate)
            output_list.d_los =  to_decimal(d_los)
            output_list.mtd_los =  to_decimal(mtd_los)
            output_list.ytd_los =  to_decimal(ytd_los)
            output_list.d_child = d_child
            output_list.m_child = m_child
            output_list.y_child = y_child


    def create_umsatz7():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        argtcode:string = ""
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
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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

        if entry(0, argt_code, " ") == ("ALL").lower() :
            argtcode = "*"
        else:
            argtcode = entry(0, argt_code, " ")

        for arrangement in db_session.query(Arrangement).filter(
                 (matches(Arrangement.arrangement,argtcode))).order_by(Arrangement.argt_bez).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = arrangement.argtnr
            to_list.name = arrangement.argt_bez

            to_list1 = query(to_list1_list, first=True)

            if not to_list1:
                to_list1 = To_list1()
                to_list1_list.append(to_list1)

                to_list1.gastnr = arrangement.argtnr
                to_list1.name = arrangement.argt_bez

            genstat_obj_list = {}
            for genstat, res_line in db_session.query(Genstat, Res_line).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.argt != "") & (Genstat.segmentcode != 0) & (Genstat.argt == arrangement.arrangement) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1


                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.rmrev =  to_decimal(to_list1.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.d_resv = to_list.d_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.d_anztage = to_list1.d_anztage + 1
                        to_list1.d_los =  to_decimal(to_list1.d_anztage) / to_decimal(to_list1.d_resv)
                        to_list1.d_child = to_list1.d_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnrmember and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnrmember
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs

                if get_month(genstat.datum) == mm:
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(genstat.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.m_rmrev =  to_decimal(to_list1.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.m_rmrate =  to_decimal(to_list1.m_rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.m_resv = to_list.m_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.m_anztage = to_list1.m_anztage + 1
                        to_list1.mtd_los =  to_decimal(to_list1.m_anztage) / to_decimal(to_list1.m_resv)
                        to_list1.m_child = to_list1.m_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_m_room = to_list1.comp_m_room + 1
                            to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + genstat.erwachs + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list1.y_rmrev =  to_decimal(to_list1.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list1.y_rmrate =  to_decimal(to_list1.y_rmrate) + to_decimal(genstat.zipreis)

                    if curr_y_resnr1 != genstat.resnr or curr_y_reslinnr1 != genstat.res_int[0]:
                        to_list1.y_resv = to_list1.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list1.y_anztage = to_list1.y_anztage + 1
                    to_list1.ytd_los =  to_decimal(to_list1.y_anztage) / to_decimal(to_list1.y_resv)
                    to_list1.y_child = to_list1.y_child + genstat.kind1 + genstat.kind2
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if genstat.gratis == 0:

                    if to_list1:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list1 in query(to_list1_list):

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

        for to_list in query(to_list_list, filters=(lambda to_list: to_list.y_room != 0), sort_by=[("name",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.rmnite = to_list.y_room
            output_list.rmrev =  to_decimal(to_list.y_logis)
            output_list.rmnite1 = to_list.m_room
            output_list.rmrev1 =  to_decimal(to_list.m_logis)
            output_list.name = to_list.name
            output_list.room =  to_decimal(to_list.room)
            output_list.pax =  to_decimal(to_list.pax)
            output_list.logis =  to_decimal(to_list.logis)
            output_list.trmrev =  to_decimal(to_list.rmrev)
            output_list.proz =  to_decimal(to_list.proz)
            output_list.avrgrate =  to_decimal(to_list.avrgrate)
            output_list.m_room =  to_decimal(to_list.m_room)
            output_list.m_pax =  to_decimal(to_list.m_pax)
            output_list.m_logis =  to_decimal(to_list.m_logis)
            output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
            output_list.m_proz =  to_decimal(to_list.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
            output_list.y_room =  to_decimal(to_list.y_room)
            output_list.y_pax =  to_decimal(to_list.y_pax)
            output_list.y_logis =  to_decimal(to_list.y_logis)
            output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list.rmrate)
            output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
            output_list.d_los =  to_decimal(to_list.d_los)
            output_list.mtd_los =  to_decimal(to_list.mtd_los)
            output_list.ytd_los =  to_decimal(to_list.ytd_los)
            output_list.d_child = to_list.d_child
            output_list.m_child = to_list.m_child
            output_list.y_child = to_list.y_child
            output_list.d_resv = to_list.d_resv
            output_list.m_resv = to_list.m_resv
            output_list.y_resv = to_list.y_resv
            output_list.d_anztage = to_list.d_anztage
            output_list.m_anztage = to_list.m_anztage
            output_list.y_anztage = to_list.y_anztage


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 2
        for ind in range(1,280 + 1) :
            output_list.name = output_list.name + "-"
        output_list = Output_list()
        output_list_list.append(output_list)

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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child
        output_list.d_resv = tot_d_room_resv
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv
        output_list.d_anztage = tot_d_anztage
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage


    def create_umsatz21():

        nonlocal output_list_list, lvcarea, cardtype, ota_only, comp_only, foreign_nr, exchg_rate, price_decimal, incl_comp, message_it, ind, room, c_room, pax, logis, rmrev, avrgrate, exc_avrgrate, comp_room, comp_pax, m_room, mc_room, m_pax, m_logis, m_rmrev, m_avrgrate, exc_m_avrgrate, comp_m_room, comp_m_pax, y_room, yc_room, y_pax, y_logis, y_rmrev, y_avrgrate, exc_y_avrgrate, comp_y_room, comp_y_pax, from_bez, to_bez, fdate_mtd, curr_select, rmrate, m_rmrate, y_rmrate, d_child, m_child, y_child, d_los, mtd_los, ytd_los, curr_d_reslinnr, curr_d_resnr, tot_d_room_resv, curr_m_reslinnr, curr_m_resnr, tot_m_room_resv, curr_y_reslinnr, curr_y_resnr, tot_y_room_resv, tot_d_anztage, tot_m_anztage, tot_y_anztage, curr_d_reslinnr1, curr_d_resnr1, tot_d_room_resv1, curr_m_reslinnr1, curr_m_resnr1, tot_m_room_resv1, curr_y_reslinnr1, curr_y_resnr1, do_it, datums, curr_zinr, prev_zinr, curr_gastnr, prev_gastnr, tot, per_region, disptype, intsegment, ota_segment, default_country, tot_pax_d, tot_pax_m, tot_pax_y, htparam, waehrung, nation, segment, zimkateg, res_line, guest, genstat, guestseg, exrate, bediener, queasy, sourccod, arrangement
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, disptype_1, cardtype_1, currency_type, ytd_flag, excl_comp, last_sort, f_date, t_date, to_date, argt_code, dispopt


        nonlocal output_list, to_list, to_list1, segm1_list, zikat_list, tmp_room, tmp_room1
        nonlocal output_list_list, to_list_list, to_list1_list, segm1_list_list, zikat_list_list, tmp_room_list, tmp_room1_list

        mm:int = 0
        yy:int = 0
        from_date:date = None
        datum:date = None
        beg_date:date = None
        subgrup:int = 0
        incl_comp = not excl_comp
        room = 0
        c_room = 0
        pax = 0
        logis =  to_decimal("0")
        rmrev =  to_decimal("0")
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis =  to_decimal("0")
        m_rmrev =  to_decimal("0")
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis =  to_decimal("0")
        y_rmrev =  to_decimal("0")
        d_los =  to_decimal("0")
        mtd_los =  to_decimal("0")
        ytd_los =  to_decimal("0")
        d_child = 0
        m_child = 0
        y_child = 0
        tot_d_room_resv = 0
        tot_m_room_resv = 0
        tot_y_room_resv = 0
        curr_d_resnr = 0
        curr_m_resnr = 0
        curr_y_resnr = 0
        curr_d_resnr1 = 0
        curr_m_resnr1 = 0
        curr_y_resnr1 = 0
        curr_d_reslinnr = 0
        curr_m_reslinnr = 0
        curr_y_reslinnr = 0
        curr_d_reslinnr1 = 0
        curr_m_reslinnr1 = 0
        curr_y_reslinnr1 = 0
        tot_d_anztage = 0
        tot_m_anztage = 0
        tot_y_anztage = 0

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
                 (Nation.natcode == 0)).order_by(Nation.untergruppe).all():
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.gastnr = nation.nationnr
            to_list.subgroup = nation.untergruppe

            if matches(nation.bezeich,r"*;*"):
                to_list.name = entry(0, nation.bezeich, ";")


            else:
                to_list.name = nation.bezeich

            to_list1 = query(to_list1_list, filters=(lambda to_list1: to_list1.gastnr == nation.untergruppe), first=True)

            if not to_list1:

                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)],"number2": [(eq, 0)],"deci2": [(eq, 0)]})

                if queasy:
                    to_list1 = To_list1()
                    to_list1_list.append(to_list1)

                    to_list1.gastnr = queasy.number1
                    to_list1.name = queasy.char1

            genstat_obj_list = {}
            for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.land == nation.kurzbez)).filter(
                         (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr == nation.nationnr) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.land, Genstat.resnr, Genstat.res_int[0]).all():
                segm1_list = query(segm1_list_list, (lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                if not segm1_list:
                    continue

                zikat_list = query(zikat_list_list, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                datums = genstat.datum
                exchg_rate =  to_decimal("1")

                if currency_type == 2:

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, datums)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, datums)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if genstat.datum == to_date:

                    tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnrmember and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                    if not tmp_room:
                        to_list.room = to_list.room + 1
                        room = room + 1

                        if to_list1:
                            to_list1.room = to_list1.room + 1
                        tmp_room = Tmp_room()
                        tmp_room_list.append(tmp_room)

                        tmp_room.gastnr = genstat.gastnrmember
                        tmp_room.zinr = genstat.zinr
                        tmp_room.flag = 1

                    if to_list1:
                        to_list1.pax = to_list1.pax + genstat.erwachs + genstat.gratis
                        to_list1.logis =  to_decimal(to_list1.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.rmrev =  to_decimal(to_list1.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.rmrate =  to_decimal(to_list1.rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.d_resv = to_list.d_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.d_anztage = to_list1.d_anztage + 1
                        to_list1.d_los =  to_decimal(to_list1.d_anztage) / to_decimal(to_list1.d_resv)
                        to_list1.d_child = to_list1.d_child + genstat.kind1 + genstat.kind2
                    to_list.d_anztage = to_list.d_anztage + 1
                    tot_d_anztage = tot_d_anztage + 1

                    if curr_d_resnr != genstat.resnr or curr_d_reslinnr != genstat.res_int[0]:
                        to_list.d_resv = to_list.d_resv + 1
                        tot_d_room_resv = tot_d_room_resv + 1
                        curr_d_reslinnr = res_line.reslinnr
                        curr_d_resnr = genstat.resnr
                    pax = pax + genstat.erwachs + genstat.gratis
                    logis =  to_decimal(logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    rmrev =  to_decimal(rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    rmrate =  to_decimal(rmrate) + to_decimal(genstat.zipreis)
                    d_los =  to_decimal(tot_d_anztage) / to_decimal(tot_d_room_resv)
                    d_child = d_child + genstat.kind1 + genstat.kind2
                    to_list.pax = to_list.pax + genstat.erwachs + genstat.gratis
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.rmrev =  to_decimal(to_list.rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.rmrate =  to_decimal(to_list.rmrate) + to_decimal(genstat.zipreis)
                    to_list.d_los =  to_decimal(to_list.d_anztage) / to_decimal(to_list.d_resv)
                    to_list.d_child = to_list.d_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:

                        tmp_room1 = query(tmp_room1_list, filters=(lambda tmp_room1: tmp_room1.gastnr == genstat.gastnr and tmp_room1.zinr == genstat.zinr and tmp_room1.flag == 1), first=True)

                        if not tmp_room1:
                            to_list.comp_room = to_list.comp_room + 1
                            comp_room = comp_room + 1

                            if to_list1:
                                to_list1.comp_room = to_list1.comp_room + 1
                                to_list1.comp_pax = to_list1.comp_pax + genstat.erwachs
                            tmp_room1 = Tmp_room1()
                            tmp_room1_list.append(tmp_room1)

                            tmp_room1.gastnr = genstat.gastnr
                            tmp_room1.zinr = genstat.zinr
                            tmp_room1.flag = 1


                        to_list.comp_pax = to_list.comp_pax + genstat.erwachs
                        comp_pax = comp_pax + genstat.erwachs

                if get_month(genstat.datum) == get_month(to_date):
                    to_list.m_room = to_list.m_room + 1
                    to_list.m_pax = to_list.m_pax + genstat.erwachs + genstat.gratis
                    to_list.m_logis =  to_decimal(to_list.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list.m_rmrev =  to_decimal(to_list.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list.m_rmrate =  to_decimal(to_list.m_rmrate) + to_decimal(genstat.zipreis)
                    to_list.m_anztage = to_list.m_anztage + 1
                    tot_m_anztage = tot_m_anztage + 1

                    if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                        to_list.m_resv = to_list.m_resv + 1
                        tot_m_room_resv = tot_m_room_resv + 1
                        curr_m_reslinnr = res_line.reslinnr
                        curr_m_resnr = genstat.resnr
                    to_list.mtd_los =  to_decimal(to_list.m_anztage) / to_decimal(to_list.m_resv)
                    to_list.m_child = to_list.m_child + genstat.kind1 + genstat.kind2
                    m_room = m_room + 1
                    m_pax = m_pax + genstat.erwachs + genstat.gratis
                    m_logis =  to_decimal(m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    m_rmrev =  to_decimal(m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    m_rmrate =  to_decimal(m_rmrate) + to_decimal(gensta.zipreis)
                    mtd_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
                    m_child = m_child + genstat.kind1 + genstat.kind2

                    if to_list1:
                        to_list1.m_room = to_list1.m_room + 1
                        to_list1.m_pax = to_list1.m_pax + genstat.erwachs + genstat.gratis
                        to_list1.m_logis =  to_decimal(to_list1.m_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                        to_list1.m_rmrev =  to_decimal(to_list1.m_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                        to_list1.m_rmrate =  to_decimal(to_list1.m_rmrate) + to_decimal(genstat.zipreis)

                        if curr_d_resnr1 != genstat.resnr or curr_d_reslinnr1 != genstat.res_int[0]:
                            to_list1.m_resv = to_list.m_resv + 1
                            tot_d_room_resv1 = tot_d_room_resv1 + 1
                            curr_d_reslinnr1 = res_line.reslinnr
                            curr_d_resnr1 = genstat.resnr
                        to_list1.m_anztage = to_list1.m_anztage + 1
                        to_list1.mtd_los =  to_decimal(to_list1.m_anztage) / to_decimal(to_list1.m_resv)
                        to_list1.m_child = to_list1.m_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list.comp_m_room = to_list.comp_m_room + 1
                        to_list.comp_m_pax = to_list.comp_m_pax + genstat.erwachs
                        comp_m_room = comp_m_room + 1
                        comp_m_pax = comp_m_pax + genstat.erwachs

                        if to_list1:
                            to_list1.comp_m_room = to_list1.comp_m_room + 1
                            to_list1.comp_m_pax = to_list1.comp_m_pax + genstat.erwachs
                to_list.y_room = to_list.y_room + 1
                to_list.y_pax = to_list.y_pax + genstat.erwachs + genstat.gratis
                to_list.y_logis =  to_decimal(to_list.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                to_list.y_rmrev =  to_decimal(to_list.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                to_list.y_rmrate =  to_decimal(to_list.y_rmrate) + to_decimal(genstat.zipreis)
                to_list.y_anztage = to_list.y_anztage + 1
                tot_y_anztage = tot_y_anztage + 1

                if curr_y_resnr != genstat.resnr or curr_y_reslinnr != genstat.res_int[0]:
                    to_list.y_resv = to_list.y_resv + 1
                    tot_y_room_resv = tot_y_room_resv + 1
                    curr_y_reslinnr = res_line.reslinnr
                    curr_y_resnr = genstat.resnr
                to_list.ytd_los =  to_decimal(to_list.y_anztage) / to_decimal(to_list.y_resv)
                to_list.y_child = to_list.y_child + genstat.kind1 + genstat.kind2
                y_room = y_room + 1
                y_pax = y_pax + genstat.erwachs + genstat.gratis
                y_logis =  to_decimal(y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                y_rmrev =  to_decimal(y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                y_rmrate =  to_decimal(y_rmrate) + to_decimal(genstat.zipreis)
                ytd_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
                y_child = y_child + genstat.kind1 + genstat.kind2

                if genstat.gratis == 0:
                    to_list.comp_y_room = to_list.comp_y_room + 1
                    to_list.comp_y_pax = to_list.comp_y_pax + genstat.erwachs
                    comp_y_room = comp_y_room + 1
                    comp_y_pax = comp_y_pax + genstat.erwachs

                if to_list1:
                    to_list1.y_room = to_list1.y_room + 1
                    to_list1.y_pax = to_list1.y_pax + to_list.pax + genstat.erwachs + genstat.gratis
                    to_list1.y_logis =  to_decimal(to_list1.y_logis) + to_decimal(genstat.logis) / to_decimal(exchg_rate)
                    to_list1.y_rmrev =  to_decimal(to_list1.y_rmrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    to_list1.y_rmrate =  to_decimal(to_list1.y_rmrate) + to_decimal(genstat.zipreis)

                    if curr_y_resnr1 != genstat.resnr or curr_y_reslinnr1 != genstat.res_int[0]:
                        to_list1.y_resv = to_list1.y_resv + 1
                        tot_y_room_resv = tot_y_room_resv + 1
                        curr_y_reslinnr = res_line.reslinnr
                        curr_y_resnr = genstat.resnr
                    to_list1.y_anztage = to_list1.y_anztage + 1
                    to_list1.ytd_los =  to_decimal(to_list1.y_anztage) / to_decimal(to_list1.y_resv)
                    to_list1.y_child = to_list1.y_child + genstat.kind1 + genstat.kind2

                    if genstat.gratis == 0:
                        to_list1.comp_y_room = to_list1.comp_y_room + 1
                        to_list1.comp_y_pax = to_list1.comp_y_pax + genstat.erwachs

        for to_list in query(to_list_list):

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

        for to_list1 in query(to_list1_list):

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

        for to_list1 in query(to_list1_list):

            for to_list in query(to_list_list, filters=(lambda to_list: to_list.comp_y_pax != 0 and to_list.subgroup == to_list1.gastnr), sort_by=[("subgroup",False),("gastnr",False)]):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 0
                output_list.rmnite = to_list.y_room
                output_list.rmrev =  to_decimal(to_list.y_logis)
                output_list.rmnite1 = to_list.m_room
                output_list.rmrev1 =  to_decimal(to_list.m_logis)
                output_list.name = to_list.name
                output_list.room =  to_decimal(to_list.room)
                output_list.pax =  to_decimal(to_list.pax)
                output_list.logis =  to_decimal(to_list.logis)
                output_list.trmrev =  to_decimal(to_list.rmrev)
                output_list.proz =  to_decimal(to_list.proz)
                output_list.avrgrate =  to_decimal(to_list.avrgrate)
                output_list.m_room =  to_decimal(to_list.m_room)
                output_list.m_pax =  to_decimal(to_list.m_pax)
                output_list.m_logis =  to_decimal(to_list.m_logis)
                output_list.m_rmrev =  to_decimal(to_list.m_rmrev)
                output_list.m_proz =  to_decimal(to_list.m_proz)
                output_list.m_avrgrate =  to_decimal(to_list.m_avrgrate)
                output_list.y_room =  to_decimal(to_list.y_room)
                output_list.y_pax =  to_decimal(to_list.y_pax)
                output_list.y_logis =  to_decimal(to_list.y_logis)
                output_list.y_rmrev =  to_decimal(to_list.y_rmrev)
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
                output_list.rmrate =  to_decimal(to_list.rmrate)
                output_list.m_rmrate =  to_decimal(to_list.m_rmrate)
                output_list.y_rmrate =  to_decimal(to_list.y_rmrate)
                output_list.d_los =  to_decimal(to_list.d_los)
                output_list.mtd_los =  to_decimal(to_list.mtd_los)
                output_list.ytd_los =  to_decimal(to_list.ytd_los)
                output_list.d_child = to_list.d_child
                output_list.m_child = to_list.m_child
                output_list.y_child = to_list.y_child
                output_list.d_resv = to_list.d_resv
                output_list.m_resv = to_list.m_resv
                output_list.y_resv = to_list.y_resv
                output_list.d_anztage = to_list.d_anztage
                output_list.m_anztage = to_list.m_anztage
                output_list.y_anztage = to_list.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 2
            output_list.rmnite = to_list1.y_room
            output_list.rmrev =  to_decimal(to_list1.y_logis)
            output_list.rmnite1 = to_list1.m_room
            output_list.rmrev1 =  to_decimal(to_list1.m_logis)
            output_list.name = chr_unicode(10) + to_list1.name
            output_list.room =  to_decimal(to_list1.room)
            output_list.pax =  to_decimal(to_list1.pax)
            output_list.logis =  to_decimal(to_list1.logis)
            output_list.trmrev =  to_decimal(to_list1.rmrev)
            output_list.proz =  to_decimal(to_list1.proz)
            output_list.avrgrate =  to_decimal(to_list1.avrgrate)
            output_list.m_room =  to_decimal(to_list1.m_room)
            output_list.m_pax =  to_decimal(to_list1.m_pax)
            output_list.m_logis =  to_decimal(to_list1.m_logis)
            output_list.m_rmrev =  to_decimal(to_list1.m_rmrev)
            output_list.m_proz =  to_decimal(to_list1.m_proz)
            output_list.m_avrgrate =  to_decimal(to_list1.m_avrgrate)
            output_list.y_room =  to_decimal(to_list1.y_room)
            output_list.y_pax =  to_decimal(to_list1.y_pax)
            output_list.y_logis =  to_decimal(to_list1.y_logis)
            output_list.y_rmrev =  to_decimal(to_list1.y_rmrev)
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
            output_list.rmrate =  to_decimal(to_list1.rmrate)
            output_list.m_rmrate =  to_decimal(to_list1.m_rmrate)
            output_list.y_rmrate =  to_decimal(to_list1.y_rmrate)
            output_list.d_los =  to_decimal(to_list1.d_los)
            output_list.mtd_los =  to_decimal(to_list1.mtd_los)
            output_list.ytd_los =  to_decimal(to_list1.ytd_los)
            output_list.d_child = to_list1.d_child
            output_list.m_child = to_list1.m_child
            output_list.y_child = to_list1.y_child
            output_list.d_resv = to_list1.d_resv
            output_list.m_resv = to_list1.m_resv
            output_list.y_resv = to_list1.y_resv
            output_list.d_anztage = to_list1.d_anztage
            output_list.m_anztage = to_list1.m_anztage
            output_list.y_anztage = to_list1.y_anztage


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 3
            output_list.name = ""
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = 4
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
        output_list.trmrev =  to_decimal(rmrev)
        output_list.proz =  to_decimal("100")
        output_list.avrgrate =  to_decimal(avrgrate)
        output_list.m_room =  to_decimal(m_room)
        output_list.m_pax =  to_decimal(m_pax)
        output_list.m_logis =  to_decimal(m_logis)
        output_list.m_rmrev =  to_decimal(m_rmrev)
        output_list.m_proz =  to_decimal("100")
        output_list.m_avrgrate =  to_decimal(m_avrgrate)
        output_list.y_room =  to_decimal(y_room)
        output_list.y_pax =  to_decimal(y_pax)
        output_list.y_logis =  to_decimal(y_logis)
        output_list.y_rmrev =  to_decimal(y_rmrev)
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
        output_list.rmrate =  to_decimal(rmrate)
        output_list.m_rmrate =  to_decimal(m_rmrate)
        output_list.y_rmrate =  to_decimal(y_rmrate)
        output_list.d_los =  to_decimal(d_los)
        output_list.mtd_los =  to_decimal(mtd_los)
        output_list.ytd_los =  to_decimal(ytd_los)
        output_list.d_child = d_child
        output_list.m_child = m_child
        output_list.y_child = y_child

    tot = translateExtended ("T o t a l", lvcarea, "")

    if cardtype_1 >= 10 and cardtype_1 < 20:
        cardtype = cardtype_1 - 10
        ota_only = True

    elif cardtype_1 >= 20:
        cardtype = cardtype_1 - 20
        comp_only = True


    else:
        cardtype = cardtype_1

    if disptype_1 >= 20:
        disptype = disptype_1 - 20
        per_region = True


    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 485)]})
    ota_segment = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    if htparam:

        nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

        if nation:
            default_country = nation.nationnr

    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr <= 2)).order_by(Segment.segmentcode).all():
        segm1_list = Segm1_list()
        segm1_list_list.append(segm1_list)

        segm1_list.segm = segment.segmentcode
        segm1_list.bezeich = to_string(segment.segmentcode, ">>9 ") + entry(0, segment.bezeich, "$$0")


        segm1_list.bezeich1 = entry(0, segment.bezeich, "$$0")

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_list.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    if op_type == 0:

        if disptype == 1:

            if cardtype < 3:
                create_umsatz1()
            else:
                create_umsatz11()

        elif disptype == 2:

            if per_region :
                create_umsatz21()
            else:
                create_umsatz2()

        elif disptype == 3:
            create_umsatz3()

        elif disptype == 4:
            create_umsatz4()

        elif disptype == 5:
            create_umsatz5()

        elif disptype == 6:
            create_umsatz6()

        elif disptype == 7:
            create_umsatz7()

    for output_list in query(output_list_list, filters=(lambda output_list: output_list.name.lower()  != ("T o t a l").lower())):
        tot_pax_d = tot_pax_d + output_list.pax
        tot_pax_m = tot_pax_m + output_list.m_pax
        tot_pax_y = tot_pax_y + output_list.y_pax

    output_list = query(output_list_list, filters=(lambda output_list: output_list.name.lower()  == ("T o t a l").lower()), first=True)

    if output_list:
        pass
        output_list.pax =  to_decimal(tot_pax_d)
        output_list.m_pax =  to_decimal(tot_pax_m)
        output_list.y_pax =  to_decimal(tot_pax_y)
        pass

    return generate_output()