#using conversion tools version: 1.0.0.112

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_res_linebl import read_res_linebl
from functions.read_reservationbl import read_reservationbl
from functions.read_waehrungbl import read_waehrungbl
from functions.read_outorderbl import read_outorderbl
from models import Zimmer, Res_line, Reservation, Waehrung, Outorder, Htparam, Queasy

gstat_list_list, Gstat_list = create_model("Gstat_list", {"selected":bool, "resstatus":int, "bezeich":string})
zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})
zistat_list_list, Zistat_list = create_model("Zistat_list", {"selected":bool, "zistatus":int, "bezeich":string})

def floorplan_webbl(gstat_list_list:[Gstat_list], zikat_list_list:[Zikat_list], zistat_list_list:[Zistat_list], location:int, floor:int, all_gstat:bool, all_zikat:bool, all_zistat:bool, ci_date:date, pvilanguage:int):

    prepare_cache ([Zimmer, Res_line, Outorder, Htparam, Queasy])

    florplan_list_list = []
    lvcarea:string = "TS-rzinr"
    do_it:bool = False
    curr_n:int = 0
    zistatus:int = 0
    bcol:int = 0
    fcol:int = 0
    g_info:string = ""
    r_info:string = ""
    n_edit:string = ""
    c_edit:string = ""
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    item_fgcol:List[int] = [15, 15, 15, 15, 15, 15, 15, 0, 15, 0, 0, 15, 0, 0, 0]
    zimmer = res_line = reservation = waehrung = outorder = htparam = queasy = None

    florplan_list = gstat_list = zikat_list = zistat_list = t_zimmer = t_res_line = t_reservation = t_waehrung = t_outorder = gtbuff = zkbuff = stbuff = None

    florplan_list_list, Florplan_list = create_model("Florplan_list", {"char1":string, "deci1":Decimal, "deci2":Decimal, "curr_n":int, "bcol":int, "fcol":int, "zistatus":int, "g_info":string, "r_info":string})
    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    t_res_line_list, T_res_line = create_model_like(Res_line)
    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_outorder_list, T_outorder = create_model_like(Outorder)

    Gtbuff = Gstat_list
    gtbuff_list = gstat_list_list

    Zkbuff = Zikat_list
    zkbuff_list = zikat_list_list

    Stbuff = Zistat_list
    stbuff_list = zistat_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal florplan_list_list, lvcarea, do_it, curr_n, zistatus, bcol, fcol, g_info, r_info, n_edit, c_edit, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, zimmer, res_line, reservation, waehrung, outorder, htparam, queasy
        nonlocal location, floor, all_gstat, all_zikat, all_zistat, ci_date, pvilanguage
        nonlocal gtbuff, zkbuff, stbuff


        nonlocal florplan_list, gstat_list, zikat_list, zistat_list, t_zimmer, t_res_line, t_reservation, t_waehrung, t_outorder, gtbuff, zkbuff, stbuff
        nonlocal florplan_list_list, t_zimmer_list, t_res_line_list, t_reservation_list, t_waehrung_list, t_outorder_list

        return {"florplan-list": florplan_list_list}

    def fill_ooo(curr_room:string):

        nonlocal florplan_list_list, lvcarea, do_it, curr_n, zistatus, bcol, fcol, g_info, r_info, n_edit, c_edit, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, zimmer, res_line, reservation, waehrung, outorder, htparam, queasy
        nonlocal location, floor, all_gstat, all_zikat, all_zistat, ci_date, pvilanguage
        nonlocal gtbuff, zkbuff, stbuff


        nonlocal florplan_list, gstat_list, zikat_list, zistat_list, t_zimmer, t_res_line, t_reservation, t_waehrung, t_outorder, gtbuff, zkbuff, stbuff
        nonlocal florplan_list_list, t_zimmer_list, t_res_line_list, t_reservation_list, t_waehrung_list, t_outorder_list

        n_edit = ""
        c_edit = ""

        def generate_inner_output():
            return (n_edit, c_edit)

        t_res_line_list.clear()
        t_reservation_list.clear()
        t_waehrung_list.clear()
        t_outorder_list.clear()
        t_res_line_list = get_output(read_res_linebl(20, None, None, 6, 1, curr_room, None, None, None, None, ""))

        t_res_line = query(t_res_line_list, first=True)

        if not t_res_line:
            t_res_line_list = get_output(read_res_linebl(20, None, None, 13, 1, curr_room, None, None, None, None, ""))

        if not t_res_line:
            t_res_line_list = get_output(read_res_linebl(55, None, None, None, None, curr_room, ci_date, None, None, None, ""))

        t_res_line = query(t_res_line_list, first=True)

        if not t_res_line:
            t_res_line_list = get_output(read_res_linebl(56, None, None, None, None, curr_room, None, None, None, None, ""))

        if t_res_line:
            t_reservation_list = get_output(read_reservationbl(1, t_res_line.resnr, None, ""))

            t_reservation = query(t_reservation_list, first=True)
            n_edit = translateExtended ("ResNo:", lvcarea, "") + " " + to_string(t_res_line.resnr) + " " + translateExtended ("Room:", lvcarea, "") + " " + t_res_line.zinr + chr_unicode(10) + translateExtended ("Guest:", lvcarea, "") + " " + t_res_line.name + chr_unicode(10) + translateExtended ("Group:", lvcarea, "") + " " + t_reservation.groupname + chr_unicode(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(t_res_line.ankunft) + chr_unicode(10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(t_res_line.abreise) + chr_unicode(10) + translateExtended ("Adult:", lvcarea, "") + " " + to_string(t_res_line.erwachs) + chr_unicode(10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(t_res_line.zipreis)

            if t_res_line.betriebsnr > 0:
                t_waehrung_list = get_output(read_waehrungbl(1, t_res_line.betriebsnr, ""))

                t_waehrung = query(t_waehrung_list, first=True)

                if t_waehrung:
                    n_edit = n_edit + " " + t_waehrung.wabkurz
            c_edit = translateExtended ("Reservation Comment:", lvcarea, "") + chr_unicode(10) + t_reservation.bemerk + chr_unicode(10) + t_res_line.bemerk

            zimmer = get_cache (Zimmer, {"zinr": [(eq, curr_room)]})

            if zimmer:
                t_outorder_list = get_output(read_outorderbl(4, zimmer.zinr, None, ci_date, None))

                t_outorder = query(t_outorder_list, first=True)

                if t_outorder:
                    c_edit = to_string(t_outorder.gespstart) + " - " + to_string(t_outorder.gespende) + chr_unicode(10) + t_outorder.gespgrund

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 25) & (Queasy.number1 == location) & (Queasy.number2 == floor)).order_by(Queasy.char1).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})
        do_it = True
        curr_n = curr_n + 1

        if not zimmer:
            do_it = False
        else:

            if not all_gstat:
                do_it = False

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.zinr == zimmer.zinr) & (Res_line.ankunft <= ci_date) & (Res_line.resstatus != 12) & (Res_line.abreise >= ci_date)).order_by(Res_line._recid).all():

                    if res_line.active_flag == 0 and res_line.ankunft == ci_date:

                        gtbuff = query(gtbuff_list, filters=(lambda gtbuff: gtbuff.selected and gtbuff.resstatus == 0), first=True)

                        if gtbuff:
                            do_it = True

                    elif res_line.active_flag == 1 and res_line.abreise > ci_date:

                        gtbuff = query(gtbuff_list, filters=(lambda gtbuff: gtbuff.selected and gtbuff.resstatus == 1), first=True)

                        if gtbuff:
                            do_it = True

                    elif res_line.active_flag == 1 and res_line.abreise == ci_date:

                        gtbuff = query(gtbuff_list, filters=(lambda gtbuff: gtbuff.selected and gtbuff.resstatus == 2), first=True)

                        if gtbuff:
                            do_it = True

            if do_it and not all_zikat:

                zkbuff = query(zkbuff_list, filters=(lambda zkbuff: zkbuff.selected and zkbuff.zikatnr == zimmer.zikatnr), first=True)

                if not zkbuff:
                    do_it = False

            if do_it and not all_zistat:

                stbuff = query(stbuff_list, filters=(lambda stbuff: stbuff.selected and stbuff.zistatus == zimmer.zistatus), first=True)

                if not stbuff:
                    do_it = False

            if do_it:
                florplan_list = Florplan_list()
                florplan_list_list.append(florplan_list)

                florplan_list.char1 = queasy.char1
                florplan_list.deci1 =  to_decimal(queasy.deci1)
                florplan_list.deci2 =  to_decimal(queasy.deci2)
                florplan_list.curr_n = curr_n

        if zimmer and do_it:
            florplan_list.zistatus = zimmer.zistatus

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})

            if outorder:

                if outorder.betriebsnr == 2:
                    florplan_list.zistatus = 7

                elif outorder.betriebsnr == 3 or outorder.betriebsnr == 4:
                    florplan_list.zistatus = 9

            if florplan_list.zistatus == 0:
                florplan_list.bcol = 8

            elif florplan_list.zistatus == 1:
                florplan_list.bcol = 11

            elif florplan_list.zistatus == 2:
                florplan_list.bcol = 2

            elif florplan_list.zistatus == 3:
                florplan_list.bcol = 1

            elif florplan_list.zistatus == 4:
                florplan_list.bcol = 14

            elif florplan_list.zistatus == 5:
                florplan_list.bcol = 15

            elif florplan_list.zistatus == 6:
                florplan_list.bcol = 12

            elif florplan_list.zistatus == 7:
                florplan_list.bcol = 4

            elif florplan_list.zistatus == 8:
                florplan_list.bcol = 5

            elif florplan_list.zistatus == 9:
                florplan_list.bcol = 13
            florplan_list.fcol = item_fgcol[florplan_list.bcol - 1]

            if zimmer.zistatus == 0:

                res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"ankunft": [(eq, ci_date)],"zinr": [(eq, zimmer.zinr)]})

                if res_line:
                    florplan_list.bcol = 9
                    florplan_list.fcol = 15

            elif zimmer.zistatus >= 1 and zimmer.zistatus <= 2:

                res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"ankunft": [(eq, ci_date)],"zinr": [(eq, zimmer.zinr)]})

                if res_line:
                    florplan_list.bcol = 10
                    florplan_list.fcol = 0

            elif zimmer.zistatus >= 3 and zimmer.zistatus <= 5:

                res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, zimmer.zinr)]})

                if res_line and (res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9):
                    florplan_list.bcol = 15
                    florplan_list.fcol = 12
            florplan_list.g_info, florplan_list.r_info = fill_ooo(zimmer.zinr)

    return generate_output()