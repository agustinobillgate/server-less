from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Zimkateg, Zimmer, Res_line, Reservation, Segment, Kontline, Reslin_queasy, Queasy, Guestseg, Resplan, Outorder

def dayfcastbl(pvilanguage:int, inhouse_flag:bool, disp_flag:bool, lessoo:bool, incl_tent:bool, curr_date:date, printer_nr:int, call_from:int, txt_file:str, vhp_limited:bool):
    room_list_list = []
    sum_list_list = []
    segm_list_list = []
    tab_label:List[str] = create_empty_list(19,"")
    datum:date = None
    ci_date:date = None
    wlist:str = ""
    dlist:str = ""
    curr_day:int = 0
    week_list:List[str] = [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]
    i:int = 0
    inhouse:List[int] = create_empty_list(19,0)
    tot_room:int = 0
    inactive:int = 0
    pax:int = 0
    from_date:date = None
    to_date:date = None
    lvcarea:str = "dayfcastBL"
    htparam = zimkateg = zimmer = res_line = reservation = segment = kontline = reslin_queasy = queasy = guestseg = resplan = outorder = None

    room_list = sum_list = segm_list = None

    room_list_list, Room_list = create_model("Room_list", {"nr":int, "flag":str, "bez1":str, "bezeich":str, "room":[decimal,19], "coom":[str,19]})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "summe":[int,19]})
    segm_list_list, Segm_list = create_model("Segm_list", {"segmentcode":int, "bezeich":str, "segm":[int,19]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, to_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
        nonlocal pvilanguage, inhouse_flag, disp_flag, lessoo, incl_tent, curr_date, printer_nr, call_from, txt_file, vhp_limited


        nonlocal room_list, sum_list, segm_list
        nonlocal room_list_list, sum_list_list, segm_list_list
        return {"room-list": room_list_list, "sum-list": sum_list_list, "segm-list": segm_list_list}

    def sum_rooms():

        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, to_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
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

        nonlocal room_list_list, sum_list_list, segm_list_list, tab_label, datum, ci_date, wlist, dlist, curr_day, week_list, i, inhouse, tot_room, inactive, pax, from_date, lvcarea, htparam, zimkateg, zimmer, res_line, reservation, segment, kontline, reslin_queasy, queasy, guestseg, resplan, outorder
        nonlocal pvilanguage, inhouse_flag, disp_flag, lessoo, incl_tent, curr_date, printer_nr, call_from, txt_file, vhp_limited


        nonlocal room_list, sum_list, segm_list
        nonlocal room_list_list, sum_list_list, segm_list_list

        to_date:date = None
        datum1:date = None
        datum2:date = None
        abreise1:date = None
        tmp_list:List[decimal] = create_empty_list(19,to_decimal("0"))
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
                 (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.active_flag <= 1) & (Res_line.kontignr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= tdate) & (not Res_line.abreise <= htparam.fdate)).order_by(Res_line._recid).all():

            if not vhp_limited:

                if not inhouse_flag:
                    do_it = True
                else:
                    do_it = res_line.active_flag == 0
            else:

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None ! == segment and segment.vip_level == 0

                if inhouse_flag and do_it:
                    do_it = res_line.active_flag == 0

            if do_it:
                for i in range(1,19 + 1) :
                    datum = curr_date + timedelta(days=i - 1)

                    if datum >= res_line.ankunft and datum < res_line.abreise:

                        kontline = db_session.query(Kontline).filter(
                                 (Kontline.betriebsnr == 0) & (Kontline.kontignr == res_line.kontignr) & (datum >= Kontline.ankunft) & (datum < Kontline.abreise) & (datum >= (ci_date + timedelta(days=Kontline.ruecktage)))).first()

                        if kontline:
                            res_allot[i - 1] = res_allot[i - 1] + res_line.zimmeranz

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger

        for segment in db_session.query(Segment).filter(
                 (Segment.segmentcode != black_list) & (func.lower(not Segment.bezeich).op("~")(("*$$0".lower().replace("*",".*"))))).order_by(Segment._recid).all():
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

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if last_resnr != res_line.resnr:

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()
            last_resnr = res_line.resnr

            if not vhp_limited:

                if not inhouse_flag:
                    do_it = True
                else:
                    do_it = res_line.active_flag == 0
            else:

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None ! == segment and segment.vip_level == 0

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

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy and reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3
                    do_it = False

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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

            queasy_obj_list = []
            for queasy, room in db_session.query(Queasy, Room).join(Room,(Room.zinr == Queasy.char1) & (Room.zimmer.sleeping)).filter(
                     (Queasy.key == 14) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy._recid in queasy_obj_list:
                    continue
                else:
                    queasy_obj_list.append(queasy._recid)


                room_list.room[i - 1] = room_list.room[i - 1] + 1
                pers_list[i - 1] = pers_list[i - 1] + queasy.number1

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == queasy.number3) & (Guestseg.reihenfolge == 1)).first()

                if not guestseg:

                    guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == queasy.number3)).first()

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

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None ! == segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zinr == res_line.zinr)).first()

                if not zimmer:
                    do_it = True
                else:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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

                        reservation = db_session.query(Reservation).filter(
                                 (Reservation.resnr == res_line.resnr)).first()
                    last_resnr = res_line.resnr
                    i = res_line.abreise - curr_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        i = res_line.ankunft - curr_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

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

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 297)).first()

        if htparam.finteger != 0:
            room_list.bezeich = to_string(htparam.finteger) + " " + translateExtended ("PM", lvcarea, "")
        last_resnr = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 2) & (Res_line.active_flag == 0) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < curr_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None ! == segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zinr == res_line.zinr)).first()

                if not zimmer:
                    do_it = True
                else:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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

                        reservation = db_session.query(Reservation).filter(
                                 (Reservation.resnr == res_line.resnr)).first()
                    last_resnr = res_line.resnr
                    i = res_line.abreise - curr_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        i = res_line.ankunft - curr_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

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

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None ! == segment and segment.vip_level == 0

            if do_it:
                do_it = False

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zinr == res_line.zinr)).first()

                if not zimmer:
                    do_it = True
                else:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

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

                        reservation = db_session.query(Reservation).filter(
                                 (Reservation.resnr == res_line.resnr)).first()
                    last_resnr = res_line.resnr
                    i = res_line.abreise - curr_date + 1

                    if i >= 1 and i <= 19:
                        avail_list[i - 1] = avail_list[i - 1] + res_line.zimmeranz
                    datum1 = curr_date
                    i = 1

                    if res_line.ankunft > curr_date:
                        datum1 = res_line.ankunft
                        i = res_line.ankunft - curr_date + 1
                    datum2 = curr_date + timedelta(days=18)
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum2:
                        datum2 = abreise1

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

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

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None ! == segment and segment.vip_level == 0

                if do_it:

                    if (res_line.resstatus != 11 and res_line.resstatus != 13):
                        room_list.room[i - 1] = room_list.room[i - 1] - res_line.zimmeranz

                    kontline = db_session.query(Kontline).filter(
                             (Kontline.gastnr == res_line.gastnr) & (Kontline.ankunft == datum) & (Kontline.zikatnr == res_line.zikatnr) & (Kontline.betriebsnr == 1)).first()

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

        outorder_obj_list = []
        for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)


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
                    coom[i - 1] = to_string(room_list.room[i - 1], "->>>9")
                else:
                    coom[i - 1] = to_string(room_list.room[i - 1], ">>9.9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = translateExtended ("Off-Market", lvcarea, "")

        outorder_obj_list = []
        for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr == 2)).order_by(Outorder._recid).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)


            datum = curr_date
            for i in range(1,19 + 1) :

                if datum >= outorder.gespstart and datum <= outorder.gespende:
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + 1
                    om_flag = True
                datum = datum + timedelta(days=1)

        if not om_flag:
            sum_list_list.remove(sum_list)


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    segm_list_list.clear()
    sum_list_list.clear()
    room_list_list.clear()
    sum_rooms()
    create_browse()

    return generate_output()