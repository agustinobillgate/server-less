#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Zimkateg, Zimmer, Res_line, Reservation, Segment, Kontline, Reslin_queasy, Queasy, Guestseg, Resplan, Outorder

def dayfcastbl(pvilanguage:int, inhouse_flag:bool, disp_flag:bool, lessoo:bool, incl_tent:bool, curr_date:date, printer_nr:int, call_from:int, txt_file:string, vhp_limited:bool):

    prepare_cache ([Htparam, Zimkateg, Zimmer, Res_line, Reservation, Kontline, Reslin_queasy, Queasy, Guestseg, Resplan, Outorder])

    room_list_list = []
    sum_list_list = []
    segm_list_list = []
    tab_label:List[string] = create_empty_list(19,"")
    datum:date = None
    ci_date:date = None
    wlist:string = ""
    dlist:string = ""
    curr_day:int = 0
    week_list:List[string] = [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]
    i:int = 0
    inhouse:List[int] = create_empty_list(19,0)
    tot_room:int = 0
    inactive:int = 0
    pax:int = 0
    from_date:date = None
    to_date:date = None
    tmp_date:int = 0
    lvcarea:string = "dayfcastBL"
    htparam = zimkateg = zimmer = res_line = reservation = segment = kontline = reslin_queasy = queasy = guestseg = resplan = outorder = None

    room_list = sum_list = segm_list = None

    room_list_list, Room_list = create_model("Room_list", {"nr":int, "flag":string, "bez1":string, "bezeich":string, "room":[Decimal,19], "coom":[string,19]})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":string, "summe":[int,19]})
    segm_list_list, Segm_list = create_model("Segm_list", {"segmentcode":int, "bezeich":string, "segm":[int,19]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, to_date, tmp_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
        nonlocal pvilanguage, inhouse_flag, disp_flag, lessoo, incl_tent, curr_date, printer_nr, call_from, txt_file, vhp_limited


        nonlocal room_list, sum_list, segm_list
        nonlocal room_list_list, sum_list_list, segm_list_list

        return {"room-list": room_list_list, "sum-list": sum_list_list, "segm-list": segm_list_list}

    def sum_rooms():

        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, to_date, tmp_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
        nonlocal pvilanguage, inhouse_flag, disp_flag, lessoo, incl_tent, curr_date, printer_nr, call_from, txt_file, vhp_limited


        nonlocal room_list, sum_list, segm_list
        nonlocal room_list_list, sum_list_list, segm_list_list


        tot_room = 0
        inactive = 0

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():

                if zimmer.sleeping:
                    tot_room = tot_room + 1
                else:
                    inactive = inactive + 1


    def create_browse():

        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, tmp_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
        nonlocal pvilanguage, inhouse_flag, disp_flag, lessoo, incl_tent, curr_date, printer_nr, call_from, txt_file, vhp_limited


        nonlocal room_list, sum_list, segm_list
        nonlocal room_list_list, sum_list_list, segm_list_list

        to_date:date = None
        datum1:date = None
        datum2:date = None
        abreise1:date = None
        tmp_list:List[Decimal] = create_empty_list(19,to_decimal("0"))
        pers_list:List[int] = create_empty_list(19,0)
        avail_list:List[int] = create_empty_list(19,0)
        black_list:int = 0
        last_resnr:int = 0
        fdate:date = None
        tdate:date = None
        res_allot:List[int] = create_empty_list(19,0)
        om_flag:bool = False
        glob_res:List[int] = create_empty_list(19,0)
        ooo_tot:List[int] = create_empty_list(19,0)
        avl_tot:List[int] = create_empty_list(19,0)
        do_it:bool = False
        room = None
        Room =  create_buffer("Room",Zimmer)
        to_date = curr_date + timedelta(days=18)
        room_list_list.clear()
        sum_list_list.clear()
        segm_list_list.clear()
        for i in range(1,19 + 1) :
            res_allot[i - 1] = 0
            inhouse[i - 1] = 0
        htparam.fdate = curr_date
        tdate = curr_date + timedelta(days=18)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.active_flag <= 1) & (Res_line.kontignr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & not_ (Res_line.ankunft > tdate) & not_ (Res_line.abreise <= curr_date)).order_by(Res_line._recid).all():

            if not vhp_limited:

                if not inhouse_flag:
                    do_it = True
                else:
                    do_it = res_line.active_flag == 0
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

                if inhouse_flag and do_it:
                    do_it = res_line.active_flag == 0

            if do_it:
                for i in range(1,19 + 1) :
                    datum = curr_date + timedelta(days=i - 1)

                    if datum >= res_line.ankunft and datum < res_line.abreise:

                        kontline = get_cache (Kontline, {"betriebsnr": [(eq, 0)],"kontignr": [(eq, res_line.kontignr)],"ankunft": [(le, datum)],"abreise": [(gt, datum)],"ruecktage ": [(le, datum)]})

                        if kontline:
                            res_allot[i - 1] = res_allot[i - 1] + res_line.zimmeranz

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger

        for segment in db_session.query(Segment).filter(
                 (Segment.segmentcode != black_list) & (not_(matches(Segment.bezeich,"*$$0")))).order_by(Segment._recid).all():
            segm_list = Segm_list()
            segm_list_list.append(segm_list)

            segm_list.segmentcode = segment.segmentcode
            segm_list.bezeich = entry(0, segment.bezeich, "$$0")
        segm_list = Segm_list()
        segm_list_list.append(segm_list)

        segm_list.segmentcode = 99999
        segm_list.bezeich = translateExtended ("Global Reserve", lvcarea, "")


        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 1
        room_list.bezeich = translateExtended ("Total Rooms", lvcarea, "")
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = tot_room + inactive
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 2
        room_list.bezeich = translateExtended ("Active Rooms", lvcarea, "")
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = tot_room
            tmp_list[i - 1] = 0
            pers_list[i - 1] = 0
            avail_list[i - 1] = 0
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 3
        room_list.bez1 = "Resident"
        room_list.bezeich = translateExtended ("Resident", lvcarea, "")
        last_resnr = 0

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.active_flag, res_line.resnr, res_line.ankunft, res_line.abreise, res_line.kontignr, res_line.zimmeranz, res_line.erwachs, res_line.reslinnr, res_line.zinr, res_line.gastnr, res_line.zipreis, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.gratis, res_line.resstatus, res_line.zikatnr, res_line._recid, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.active_flag, Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.kontignr, Res_line.zimmeranz, Res_line.erwachs, Res_line.reslinnr, Res_line.zinr, Res_line.gastnr, Res_line.zipreis, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.gratis, Res_line.resstatus, Res_line.zikatnr, Res_line._recid, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if last_resnr != res_line.resnr:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            last_resnr = res_line.resnr

            if not vhp_limited:

                if not inhouse_flag:
                    do_it = True
                else:
                    do_it = res_line.active_flag == 0
            else:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

                if inhouse_flag and do_it:
                    do_it = res_line.active_flag == 0

            if do_it:
                i = 1
                datum1 = curr_date

                if res_line.ankunft > datum1:
                    datum1 = res_line.ankunft
                datum2 = to_date

                if res_line.abreise < datum2:
                    datum2 = res_line.abreise
                for datum in date_range(datum1,datum2) :
                    pax = res_line.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    do_it = False

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if not queasy:
                            do_it = True

                        elif queasy and queasy.number3 != res_line.gastnr:
                            do_it = True
                    else:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            do_it = True

                    if res_line.abreise > datum and do_it:

                        if res_line.resstatus != 13:
                            tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz
                            room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz

                        segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == reservation.segmentcode), first=True)

                        if segm_list and res_line.resstatus != 13:
                            segm_list.segm[i - 1] = segm_list.segm[i - 1] + res_line.zimmeranz
                        pers_list[i - 1] = pers_list[i - 1] + pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis

                    elif res_line.abreise == datum and do_it and res_line.resstatus != 13:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    i = i + 1
        i = 0
        for datum in date_range(curr_date,to_date) :
            i = i + 1

            queasy_obj_list = {}
            queasy = Queasy()
            room = Zimmer()
            for queasy.number1, queasy.number3, queasy._recid, room.sleeping, room._recid in db_session.query(Queasy.number1, Queasy.number3, Queasy._recid, Room.sleeping, Room._recid).join(Room,(Room.zinr == Queasy.char1) & (Room.sleeping)).filter(
                     (Queasy.key == 14) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy_obj_list.get(queasy._recid):
                    continue
                else:
                    queasy_obj_list[queasy._recid] = True


                room_list.room[i - 1] = room_list.room[i - 1] + 1
                pers_list[i - 1] = pers_list[i - 1] + queasy.number1

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, queasy.number3)],"reihenfolge": [(eq, 1)]})

                if not guestseg:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, queasy.number3)]})

                if guestseg:

                    segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == guestseg.segmentcode), first=True)

                    if segm_list:
                        segm_list.segm[i - 1] = segm_list.segm[i - 1] + 1
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 4
        room_list.bezeich = translateExtended ("Guaranted", lvcarea, "")
        last_resnr = 0

        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 1)) & (Res_line.active_flag == 0) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if not zimmer:
                    do_it = True
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if not queasy:
                            do_it = True

                        elif queasy and queasy.number3 != res_line.gastnr:
                            do_it = True
                    else:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            do_it = True

                if do_it:

                    if last_resnr != res_line.resnr:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    last_resnr = res_line.resnr
                    tmp_date = (res_line.abreise - curr_date).days
                    i = tmp_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        tmp_date = (res_line.ankunft - curr_date).days
                        i = tmp_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3

                        if res_line.resstatus == 1:

                            if disp_flag:

                                if res_line.ankunft < datum:
                                    inhouse[i - 1] = inhouse[i - 1] + res_line.zimmeranz
                                else:
                                    room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                            else:
                                room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                            tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz

                            segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == reservation.segmentcode), first=True)

                            if segm_list:
                                segm_list.segm[i - 1] = segm_list.segm[i - 1] + res_line.zimmeranz
                        pers_list[i - 1] = pers_list[i - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                        i = i + 1
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 5
        room_list.bezeich = translateExtended ("6 PM", lvcarea, "")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})

        if htparam.finteger != 0:
            room_list.bezeich = to_string(htparam.finteger) + " " + translateExtended ("PM", lvcarea, "")
        last_resnr = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 2) & (Res_line.active_flag == 0) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if not zimmer:
                    do_it = True
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if not queasy:
                            do_it = True

                        elif queasy and queasy.number3 != res_line.gastnr:
                            do_it = True
                    else:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            do_it = True

                if do_it:

                    if last_resnr != res_line.resnr:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    last_resnr = res_line.resnr
                    tmp_date = (res_line.abreise - curr_date).days
                    i = tmp_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        tmp_date = (res_line.ankunft - curr_date).days
                        i = tmp_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3

                        if disp_flag:

                            if res_line.ankunft < datum:
                                inhouse[i - 1] = inhouse[i - 1] + res_line.zimmeranz
                            else:
                                room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                        else:
                            room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz
                        pers_list[i - 1] = pers_list[i - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                        segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == reservation.segmentcode), first=True)

                        if segm_list:
                            segm_list.segm[i - 1] = segm_list.segm[i - 1] + res_line.zimmeranz
                        i = i + 1
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 6
        room_list.bezeich = translateExtended ("Verbal Confirmed", lvcarea, "")
        last_resnr = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 5) & (Res_line.active_flag == 0) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if not zimmer:
                    do_it = True
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if not queasy:
                            do_it = True

                        elif queasy and queasy.number3 != res_line.gastnr:
                            do_it = True
                    else:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            do_it = True

                if do_it:

                    if last_resnr != res_line.resnr:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    last_resnr = res_line.resnr
                    tmp_date = (res_line.abreise - curr_date).days
                    i = tmp_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        tmp_date = (res_line.ankunft - curr_date).days
                        i = tmp_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3

                        if disp_flag:

                            if res_line.ankunft < datum:
                                inhouse[i - 1] = inhouse[i - 1] + res_line.zimmeranz
                            else:
                                room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                        else:
                            room_list.room[i - 1] = room_list.room[i - 1] + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz
                        pers_list[i - 1] = pers_list[i - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz

                        segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == reservation.segmentcode), first=True)

                        if segm_list:
                            segm_list.segm[i - 1] = segm_list.segm[i - 1] + res_line.zimmeranz
                        i = i + 1
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 7
        room_list.bezeich = translateExtended ("Global Reserve", lvcarea, "")
        i = 0
        for datum in date_range(curr_date,to_date) :
            i = i + 1

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                room_list.room[i - 1] = room_list.room[i - 1] + kontline.zimmeranz
                tmp_list[i - 1] = tmp_list[i - 1] + kontline.zimmeranz
                pers_list[i - 1] = pers_list[i - 1] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz

                segm_list = query(segm_list_list, filters=(lambda segm_list: segm_list.segmentcode == 99999), first=True)
                segm_list.segm[i - 1] = segm_list.segm[i - 1] + kontline.zimmeranz
                tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    do_it = None != segment and segment.vip_level == 0

                if do_it:

                    if (res_line.resstatus != 11 and res_line.resstatus != 13):
                        room_list.room[i - 1] = room_list.room[i - 1] - res_line.zimmeranz

                    kontline = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(eq, datum)],"zikatnr": [(eq, res_line.zikatnr)],"betriebsnr": [(eq, 1)]})

                    if kontline:
                        pers_list[i - 1] = pers_list[i - 1] - (kontline.erwachs + kontline.kind1) * res_line.zimmeranz
                    else:
                        pers_list[i - 1] = pers_list[i - 1] - res_line.erwachs * res_line.zimmeranz
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Tentative", lvcarea, "")
        i = 1
        datum = curr_date
        while i <= 19:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.resstatus == 3) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                sum_list.summe[i - 1] = sum_list.summe[i - 1] + res_line.zimmeranz

                if incl_tent:
                    pers_list[i - 1] = pers_list[i - 1] + res_line.erwachs * res_line.zimmeranz


            i = i + 1
            datum = datum + timedelta(days=1)

        room_list = query(room_list_list, filters=(lambda room_list: room_list.bez1.lower()  == ("Resident").lower()), first=True)
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = room_list.room[i - 1] + inhouse[i - 1]
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 8
        room_list.bezeich = translateExtended ("Total Guests", lvcarea, "")
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = pers_list[i - 1]
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 9
        room_list.bezeich = translateExtended ("Total OCC Rooms", lvcarea, "")
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = tmp_list[i - 1]
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 10
        room_list.bezeich = translateExtended ("Room Occ. in %", lvcarea, "")
        room_list.flag = "*"
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = (tmp_list[i - 1] / tot_room) * 100
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 11
        room_list.bezeich = translateExtended ("Available Rooms", lvcarea, "")
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = tot_room - tmp_list[i - 1]
            avl_tot[i - 1] = room_list.room[i - 1]
        from_date = curr_date
        to_date = from_date + timedelta(days=18)
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 12
        room_list.bezeich = translateExtended ("Allotments", lvcarea, "")

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1) & (not_ (Kontline.ankunft > to_date)) & (not_ (Kontline.abreise <= from_date))).order_by(Kontline._recid).all():
            i = 1
            for datum in date_range(from_date,to_date) :

                if datum >= kontline.ankunft and datum < kontline.abreise and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                    room_list.room[i - 1] = room_list.room[i - 1] + kontline.zimmeranz
                    tmp_list[i - 1] = tmp_list[i - 1] + kontline.zimmeranz
                i = i + 1
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = room_list.room[i - 1] - res_allot[i - 1]
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.nr = 13
        room_list.bezeich = translateExtended ("Occ w/ Allotm %", lvcarea, "")
        room_list.flag = "*"
        for i in range(1,19 + 1) :
            room_list.room[i - 1] = (tmp_list[i - 1] / tot_room) * 100
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Waiting List", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= 19:

                for resplan in db_session.query(Resplan).filter(
                         (Resplan.datum == datum) & (Resplan.zikatnr == zimkateg.zikatnr)).order_by(Resplan._recid).all():
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + resplan.anzzim[3]
                i = i + 1
                datum = datum + timedelta(days=1)
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Expect Departure", lvcarea, "")
        for i in range(1,19 + 1) :
            sum_list.summe[i - 1] = avail_list[i - 1]
        for i in range(1,19 + 1) :
            ooo_tot[i - 1] = 0
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Out-of-order", lvcarea, "")

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True


            datum = curr_date
            for i in range(1,19 + 1) :

                if datum >= outorder.gespstart and datum <= outorder.gespende:
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + 1
                    ooo_tot[i - 1] = ooo_tot[i - 1] + 1
                datum = datum + timedelta(days=1)

        if lessoo:
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.bezeich = translateExtended ("AVL less by OOO", lvcarea, "")
            room_list.nr = 14


            for i in range(1,19 + 1) :
                room_list.room[i - 1] = avl_tot[i - 1] - ooo_tot[i - 1]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.bezeich != ""), sort_by=[("nr",False)]):
            for i in range(1,19 + 1) :

                if room_list.flag == "":
                    room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>9")
                else:
                    room_list.coom[i - 1] = to_string(room_list.room[i - 1], ">>9.9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Off-Market", lvcarea, "")

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr == 2)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True


            datum = curr_date
            for i in range(1,19 + 1) :

                if datum >= outorder.gespstart and datum <= outorder.gespende:
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + 1
                    om_flag = True
                datum = datum + timedelta(days=1)

        if not om_flag:
            sum_list_list.remove(sum_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate
    segm_list_list.clear()
    sum_list_list.clear()
    room_list_list.clear()
    sum_rooms()
    create_browse()

    return generate_output()