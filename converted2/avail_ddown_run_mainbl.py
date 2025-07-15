#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimkateg, Zimmer, Reservation, Segment, Outorder, Kontline

rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool, "kurzbez":string, "bezeich":string, "zinr":string}, {"sleeping": True})

def avail_ddown_run_mainbl(case_type:int, incl_tentative:bool, mi_inactive:bool, datum:date, rmcat_list_data:[Rmcat_list]):

    prepare_cache ([Res_line, Zimkateg, Zimmer, Reservation, Outorder, Kontline])

    room_list_data = []
    vhp_limited:bool = False
    do_it:bool = False
    tot_room:int = 0
    res_line = zimkateg = zimmer = reservation = segment = outorder = kontline = None

    rmcat_list = room_list = rline1 = None

    room_list_data, Room_list = create_model("Room_list", {"datum":date, "zikatnr":int, "sleeping":bool, "bezeich":string, "room":int, "t_avail":int, "t_room":int, "t_ooo":int, "t_occ":int, "t_alot":int, "t_lnight":int, "t_arrival":int, "t_depart":int, "resnr":string, "name":string, "groupname":string, "rmno":string, "depart":date, "arrival":date, "rmcat":string, "kurzbez":string, "pax":int, "qty":int, "adult":int, "ch1":int, "ch2":int, "compli":int, "nat":string, "argt":string, "company":string, "currency":string, "segment":string, "nights":int, "alot":int, "pocc":Decimal, "rentable":int}, {"sleeping": True})

    Rline1 = create_buffer("Rline1",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, vhp_limited, do_it, tot_room, res_line, zimkateg, zimmer, reservation, segment, outorder, kontline
        nonlocal case_type, incl_tentative, mi_inactive, datum
        nonlocal rline1


        nonlocal rmcat_list, room_list, rline1
        nonlocal room_list_data

        return {"room-list": room_list_data}

    def run_main():

        nonlocal room_list_data, vhp_limited, do_it, tot_room, res_line, zimkateg, zimmer, reservation, segment, outorder, kontline
        nonlocal case_type, incl_tentative, mi_inactive, datum
        nonlocal rline1


        nonlocal rmcat_list, room_list, rline1
        nonlocal room_list_data

        tot_actroom:int = 0
        tot_occrm:int = 0
        tot_ooo:int = 0
        tot_alot:int = 0
        tot_avail:int = 0
        tot_avail2:int = 0
        tot_rent:int = 0
        count_rmcateg()

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.verfuegbarkeit)).order_by(Zimkateg.zikatnr).all():

            rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimkateg.zikatnr and rmcat_list.sleeping), first=True)

            if rmcat_list:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.room = rmcat_list.anzahl
                room_list.t_avail = rmcat_list.anzahl
                room_list.t_room = rmcat_list.anzahl
                room_list.zikatnr = zimkateg.zikatnr
                room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
                room_list.datum = datum


                room_list.rentable = room_list.t_room

        zimkateg_obj_list = {}
        for zimkateg in db_session.query(Zimkateg).filter(
                 ((Zimkateg.zikatnr.in_(list(set([rmcat_list.zikatnr for rmcat_list in rmcat_list_data if ~rmcat_list.sleeping])))))).order_by(Zimkateg.zikatnr).all():
            if zimkateg_obj_list.get(zimkateg._recid):
                continue
            else:
                zimkateg_obj_list[zimkateg._recid] = True

            rmcat_list = query(rmcat_list_data, (lambda rmcat_list: (zimkateg.zikatnr == rmcat_list.zikatnr)), first=True)
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.sleeping = False
            room_list.room = rmcat_list.anzahl
            room_list.t_avail = rmcat_list.anzahl
            room_list.t_room = rmcat_list.anzahl
            room_list.zikatnr = zimkateg.zikatnr
            room_list.bezeich = to_string(zimkateg.kurzbez, "x(6)")
            room_list.datum = datum


            room_list.rentable = room_list.t_room

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.resnr, res_line.zinr, res_line.zimmeranz, res_line.resstatus, res_line.zikatnr, res_line.abreise, res_line.ankunft, res_line._recid, zimmer.sleeping, zimmer.zikatnr, zimmer._recid in db_session.query(Res_line.resnr, Res_line.zinr, Res_line.zimmeranz, Res_line.resstatus, Res_line.zikatnr, Res_line.abreise, Res_line.ankunft, Res_line._recid, Zimmer.sleeping, Zimmer.zikatnr, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & not_ (Zimmer.sleeping)).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.zikatnr == room_list.zikatnr) & (Res_line.zinr != "") & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:
                room_list.room = room_list.room - 1
                room_list.t_avail = room_list.t_avail - 1

        if case_type == 1:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.sleeping)):

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.zikatnr == room_list.zikatnr) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_list.t_occ = room_list.t_occ + res_line.zimmeranz
                        room_list.room = room_list.room - res_line.zimmeranz
                        room_list.t_avail = room_list.t_avail - res_line.zimmeranz

        elif case_type == 9:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.sleeping)):

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resstatus == 6) & (Res_line.active_flag == 1) & (Res_line.zikatnr == room_list.zikatnr) & (Res_line.abreise > datum) & (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_list.t_occ = room_list.t_occ + res_line.zimmeranz
                        room_list.room = room_list.room - res_line.zimmeranz
                        room_list.t_avail = room_list.t_avail - res_line.zimmeranz
                        room_list.rentable = room_list.t_room - room_list.t_occ

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer.zikatnr, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer.zikatnr, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.sleeping), first=True)

            if datum >= outorder.gespstart and datum <= outorder.gespende:
                room_list.t_ooo = room_list.t_ooo + 1
                room_list.rentable = room_list.rentable - 1
                room_list.room = room_list.room - 1
                room_list.t_avail = room_list.t_avail - 1

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.zikatnr == room_list.zikatnr) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
            room_list.t_alot = room_list.t_alot + kontline.zimmeranz
            room_list.t_avail = room_list.room
            room_list.room = room_list.room - kontline.zimmeranz

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.sleeping)):

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                if res_line.abreise == datum and res_line.resstatus != 3 and res_line.zikatnr == room_list.zikatnr:
                    room_list.t_depart = room_list.t_depart + res_line.zimmeranz

                if res_line.ankunft == datum and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tentative)):
                    room_list.t_arrival = room_list.t_arrival + res_line.zimmeranz


            tot_actroom = tot_actroom + room_list.t_room
            tot_occrm = tot_occrm + room_list.t_occ
            tot_ooo = tot_ooo + room_list.t_ooo
            tot_alot = tot_alot + room_list.t_alot
            tot_avail = tot_avail + room_list.t_avail
            tot_avail2 = tot_avail2 + room_list.room
            tot_rent = tot_rent + room_list.rentable

        if tot_actroom != 0:
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.bezeich = "TOTAL"
            room_list.room = tot_avail2
            room_list.t_avail = tot_avail
            room_list.t_room = tot_actroom
            room_list.t_ooo = tot_ooo
            room_list.t_occ = tot_occrm
            room_list.t_alot = tot_alot
            room_list.rentable = tot_rent


    def count_rmcateg():

        nonlocal room_list_data, vhp_limited, do_it, tot_room, res_line, zimkateg, zimmer, reservation, segment, outorder, kontline
        nonlocal case_type, incl_tentative, mi_inactive, datum
        nonlocal rline1


        nonlocal rmcat_list, room_list, rline1
        nonlocal room_list_data

        zikatnr:int = 0
        rmcat_list_data.clear()
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:
                tot_room = tot_room + 1

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    zikatnr = zimkateg.zikatnr
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1

        if not mi_inactive:

            return
        zikatnr = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping == False)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    rmcat_list.sleeping = False
                    zikatnr = zimkateg.zikatnr
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1


    run_main()

    return generate_output()