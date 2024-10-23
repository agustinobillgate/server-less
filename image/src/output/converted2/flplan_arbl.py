from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Htparam, Zimmer, Zimkateg, Outorder, Res_line, Reservation, Queasy, Waehrung, Reslin_queasy

def flplan_arbl(pvilanguage:int):
    max_row = 0
    max_col = 1
    cr_list_list = []
    curr_i:int = 0
    ci_date:date = None
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
    lvcarea:str = "mk-resline"
    htparam = zimmer = zimkateg = outorder = res_line = reservation = queasy = waehrung = reslin_queasy = None

    cr_list = None

    cr_list_list, Cr_list = create_model("Cr_list", {"curr_row":int, "curr_col":int, "zistatus":int, "i_bgcol":int, "i_fgcol":int, "i_resnr":int, "i_reslinnr":int, "i_rstat":int, "rmcat":str, "ankunft":date, "abreise":date, "g_info":str, "r_info":str, "arrival":bool, "selectflag":bool, "room":str}, {"i_bgcol": 15, "i_rstat": None, "rmcat": "", "g_info": "", "r_info": "", "selectflag": True, "room": ""})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_row, max_col, cr_list_list, curr_i, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, lvcarea, htparam, zimmer, zimkateg, outorder, res_line, reservation, queasy, waehrung, reslin_queasy
        nonlocal pvilanguage


        nonlocal cr_list
        nonlocal cr_list_list
        return {"max_row": max_row, "max_col": max_col, "cr-list": cr_list_list}

    def cal_max_row():

        nonlocal max_row, max_col, cr_list_list, curr_i, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, lvcarea, htparam, zimmer, zimkateg, outorder, res_line, reservation, queasy, waehrung, reslin_queasy
        nonlocal pvilanguage


        nonlocal cr_list
        nonlocal cr_list_list

        s_floor:str = ""
        curr_max:int = 0
        l_floor:int = 0

        for zimmer in db_session.query(Zimmer).order_by(func.length(Zimmer.zinr), Zimmer.zinr).all():
            l_floor = len(to_string(zimmer.etage))

            if s_floor != substring(zimmer.zinr, 0, l_floor):

                if curr_max > max_row:
                    max_row = curr_max
                s_floor = substring(zimmer.zinr, 0, l_floor)
                curr_max = 1


            else:
                curr_max = curr_max + 1

        if curr_max > max_row:
            max_row = curr_max

        if max_row > 22:
            max_row = round(max_row / 2, 0)


    def create_r_list():

        nonlocal max_row, max_col, cr_list_list, curr_i, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, lvcarea, htparam, zimmer, zimkateg, outorder, res_line, reservation, queasy, waehrung, reslin_queasy
        nonlocal pvilanguage


        nonlocal cr_list
        nonlocal cr_list_list

        s_floor:str = ""
        l_floor:int = 0
        curr_row:int = 1

        for zimmer in db_session.query(Zimmer).order_by(func.length(Zimmer.zinr), Zimmer.zinr).all():

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == zimmer.zikatnr)).first()
            l_floor = len(to_string(zimmer.etage))

            if s_floor == "":
                s_floor = substring(zimmer.zinr, 0, l_floor)
            cr_list = Cr_list()
            cr_list_list.append(cr_list)

            cr_list.curr_row = curr_row
            cr_list.curr_col = max_col
            cr_list.room = zimmer.zinr
            cr_list.rmcat = zimkateg.kurzbez
            cr_list.zistatus = zimmer.zistatus
            curr_row = curr_row + 1

            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == zimmer.zinr) & (Outorder.gespstart <= ci_date) & (Outorder.gespende >= ci_date)).first()

            if outorder:

                if outorder.betriebsnr == 2:
                    cr_list.zistatus = 7

                elif outorder.betriebsnr == 3 or outorder.betriebsnr == 4:
                    cr_list.zistatus = 9

            if cr_list.zistatus == 0:
                cr_list.i_bgcol = 8
            elif cr_list.zistatus == 1:
                cr_list.i_bgcol = 11
            elif cr_list.zistatus == 2:
                cr_list.i_bgcol = 2
            elif cr_list.zistatus == 3:
                cr_list.i_bgcol = 1
            elif cr_list.zistatus == 4:
                cr_list.i_bgcol = 14
            elif cr_list.zistatus == 5:
                cr_list.i_bgcol = 15
            elif cr_list.zistatus == 6:
                cr_list.i_bgcol = 12
            elif cr_list.zistatus == 7:
                cr_list.i_bgcol = 4
            elif cr_list.zistatus == 8:
                cr_list.i_bgcol = 5
            elif cr_list.zistatus == 9:
                cr_list.i_bgcol = 13
            cr_list.i_fgcol = item_fgcol[cr_list.i_bgcol - 1]

            if cr_list.zistatus == 6:
                cr_list.g_info, cr_list.r_info = fill_ooo(cr_list.room)

            if s_floor != substring(zimmer.zinr, 0, l_floor):
                s_floor = substring(zimmer.zinr, 0, l_floor)

                if curr_row > 2 and substring(zimmer.zinr, 0, l_floor) == to_string(zimmer.etage):
                    curr_row = 1
                    max_col = max_col + 1

            elif curr_row > max_row:
                curr_row = 1
                max_col = max_col + 1

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "")).order_by(Res_line.active_flag.desc(), Res_line.ankunft, Res_line.resstatus).all():

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            cr_list = query(cr_list_list, filters=(lambda cr_list: cr_list.room == res_line.zinr), first=True)

            if cr_list.i_resnr == 0:
                cr_list.i_resnr = res_line.resnr
                cr_list.i_reslinnr = res_line.reslinnr
                cr_list.ankunft = res_line.ankunft
                cr_list.abreise = res_line.abreise
                cr_list.i_rstat = res_line.resstatus


                cr_list.g_info, cr_list.r_info = fill_res_info(1, cr_list.g_info, cr_list.r_info)

                if (res_line.active_flag == 0 and res_line.ankunft == ci_date):
                    cr_list.arrival = True

            elif cr_list.abreise == ci_date and (res_line.active_flag == 0 and res_line.ankunft == ci_date):
                cr_list.arrival = True


                cr_list.g_info, cr_list.r_info = fill_res_info(2, cr_list.g_info, cr_list.r_info)

            if cr_list.arrival :

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 162) & (Queasy.char1 == cr_list.room) & (Queasy.number1 == 0)).first()

                if queasy:
                    cr_list.i_bgcol = 6
                    cr_list.i_fgcol = 15


                else:

                    if cr_list.zistatus == 0:
                        cr_list.i_bgcol = 9
                        cr_list.i_fgcol = 15


                    else:
                        cr_list.i_bgcol = 10
                        cr_list.i_fgcol = 0

            elif cr_list.zistatus <= 2:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 162) & (Queasy.char1 == cr_list.room) & (Queasy.number1 == 0)).first()

                if queasy:
                    cr_list.i_bgcol = 6
                    cr_list.i_fgcol = 15


                else:

                    if cr_list.zistatus == 0:
                        cr_list.i_bgcol = 8
                        cr_list.i_fgcol = 0

                    elif cr_list.zistatus == 1:
                        cr_list.i_bgcol = 11
                        cr_list.i_fgcol = 0

                    elif cr_list.zistatus == 2:
                        cr_list.i_bgcol = 2
                        cr_list.i_fgcol = 0

            elif cr_list.zistatus >= 3 and cr_list.zistatus <= 5:

                if cr_list.arrival:
                    cr_list.i_bgcol = 14
                    cr_list.i_fgcol = 12

                elif (res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9):
                    cr_list.i_bgcol = 15
                    cr_list.i_fgcol = 12


    def fill_ooo(rmno:str):

        nonlocal max_row, max_col, cr_list_list, curr_i, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, lvcarea, htparam, zimmer, zimkateg, outorder, res_line, reservation, queasy, waehrung, reslin_queasy
        nonlocal pvilanguage


        nonlocal cr_list
        nonlocal cr_list_list

        g_info = ""
        r_info = ""

        def generate_inner_output():
            return (g_info, r_info)


        outorder = db_session.query(Outorder).filter(
                 (Outorder.zinr == rmno) & (not Outorder.gespstart > res_line.abreise) & (not Outorder.gespende <= res_line.ankunft)).first()

        if outorder:
            r_info = to_string(outorder.gespstart) + " - " + to_string(outorder.gespende) + chr(10) + outorder.gespgrund

        return generate_inner_output()


    def fill_res_info(i_case:int, g_info:str, r_info:str):

        nonlocal max_row, max_col, cr_list_list, curr_i, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, item_fgcol, lvcarea, htparam, zimmer, zimkateg, outorder, res_line, reservation, queasy, waehrung, reslin_queasy
        nonlocal pvilanguage


        nonlocal cr_list
        nonlocal cr_list_list

        rbuff = None
        rsvbuff = None

        def generate_inner_output():
            return (g_info, r_info)

        Rbuff =  create_buffer("Rbuff",Res_line)
        Rsvbuff =  create_buffer("Rsvbuff",Reservation)

        if i_case == 1:
            g_info = translateExtended ("ResNo:", lvcarea, "") + " " + to_string(res_line.resnr) + " " + translateExtended ("Room:", lvcarea, "") + " " + res_line.zinr + chr(10) + translateExtended ("Guest:", lvcarea, "") + " " + res_line.name + chr(10) + translateExtended ("Group:", lvcarea, "") + " " + reservation.groupname + chr(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(res_line.ankunft) + chr(10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(res_line.abreise) + chr(10) + translateExtended ("Adult:", lvcarea, "") + " " + to_string(res_line.erwachs) + chr(10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(res_line.zipreis)

            if res_line.betriebsnr > 0:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    g_info = g_info + " " + waehrung.wabkurz

            if reservation.bemerk != "" or res_line.bemerk != "":
                r_info = translateExtended ("Reservation Comment:", lvcarea, "") + chr(10) + reservation.bemerk + chr(10) + res_line.bemerk

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                r_info = r_info + chr(10) + translateExtended ("Special Request:", lvcarea, "") + " " + reslin_queasy.char3
        elif i_case == 2:

            rbuff = db_session.query(Rbuff).filter(
                     (Rbuff.active_flag == 0) & (Rbuff.ankunft == ci_date) & ((Rbuff.resstatus <= 2) | (Rbuff.resstatus == 5)) & (Rbuff.zinr == res_line.zinr)).first()

            if not rbuff:

                rbuff = db_session.query(Rbuff).filter(
                         (Rbuff.active_flag == 0) & (Rbuff.ankunft == ci_date) & (Rbuff.resstatus == 11) & (Rbuff.l_zuordnung[inc_value(2)] == 0) & (Rbuff.zinr == res_line.zinr)).first()

            if not rbuff:

                return generate_inner_output()

            rsvbuff = db_session.query(Rsvbuff).filter(
                     (Rsvbuff.resnr == rbuff.resnr)).first()
            g_info = g_info + chr(10) + chr(10) + translateExtended ("ResNo:", lvcarea, "") + " " + to_string(rbuff.resnr) + " " + translateExtended ("Room:", lvcarea, "") + " " + rbuff.zinr + chr(10) + translateExtended ("Guest:", lvcarea, "") + " " + rbuff.name + chr(10) + translateExtended ("Group:", lvcarea, "") + " " + rsvbuff.groupname + chr(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(rbuff.ankunft) + chr(10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(rbuff.abreise) + chr(10) + translateExtended ("Adult:", lvcarea, "") + " " + to_string(rbuff.erwachs) + chr(10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(rbuff.zipreis)

            if rbuff.betriebsnr > 0:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == rbuff.betriebsnr)).first()

                if waehrung:
                    g_info = g_info + " " + waehrung.wabkurz

            if rsvbuff.bemerk != "" or rbuff.bemerk != "":
                r_info = r_info + chr(10) + chr(10) + translateExtended ("Reservtion Comment:", lvcarea, "") + chr(10) + rsvbuff.bemerk + chr(10) + rbuff.bemerk

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) & (Reslin_queasy.resnr == rbuff.resnr) & (Reslin_queasy.reslinnr == rbuff.reslinnr)).first()

            if reslin_queasy:
                r_info = r_info + chr(10) + translateExtended ("Special Request:", lvcarea, "") + " " + reslin_queasy.char3

        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger
    ci_date = get_output(htpdate(87))
    cal_max_row()
    create_r_list()

    return generate_output()