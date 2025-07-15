#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zimmer, Zimkateg, Outorder, Res_line, Kontline

def notif_availability_webbl():

    prepare_cache ([Queasy, Htparam, Zimmer, Zimkateg, Outorder, Res_line, Kontline])

    room_summary_data = []
    show_notif = False
    start_date:date = None
    end_date:date = None
    i:int = 0
    check_date:date = None
    process_room:bool = False
    billing_date:date = None
    ooo_count_list:List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    day_names:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    current_max_avail:int = -100
    show_all_data:bool = False
    total_room_count:int = 0
    current_type_number:int = 0
    queasy = htparam = zimmer = zimkateg = outorder = res_line = kontline = None

    room_summary = room_type_list = room_availability_list = avail_config = None

    room_summary_data, Room_summary = create_model("Room_summary", {"room_number":int, "room_type_name":string, "overbook":int, "availability":int, "ooo_rooms":int, "total_rooms":int, "max_avail":int, "date":string})
    room_type_list_data, Room_type_list = create_model("Room_type_list", {"room_number":int, "room_count":int, "is_sleeping_room":bool}, {"is_sleeping_room": True})
    room_availability_list_data, Room_availability_list = create_model("Room_availability_list", {"avail_flag":bool, "allot_flag":bool, "room_number":int, "type_index":int, "is_sleeping_room":bool, "allotment":[int,30], "descriptions":string, "available_rooms":[int,30], "coom":[string,30], "sort_priority":int}, {"is_sleeping_room": True})

    Avail_config = create_buffer("Avail_config",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_summary_data, show_notif, start_date, end_date, i, check_date, process_room, billing_date, ooo_count_list, day_names, current_max_avail, show_all_data, total_room_count, current_type_number, queasy, htparam, zimmer, zimkateg, outorder, res_line, kontline
        nonlocal avail_config


        nonlocal room_summary, room_type_list, room_availability_list, avail_config
        nonlocal room_summary_data, room_type_list_data, room_availability_list_data

        return {"room-summary": room_summary_data, "show_notif": show_notif}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        start_date = htparam.fdate


    end_date = add_interval(start_date, 1, "months")
    check_date = start_date
    while check_date < end_date and not show_all_data:
        room_type_list_data.clear()
        room_availability_list_data.clear()
        for i in range(1,30 + 1) :
            ooo_count_list[i - 1] = 0
        total_room_count = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:
                total_room_count = total_room_count + 1

                if current_type_number != zimkateg.zikatnr:
                    room_type_list = Room_type_list()
                    room_type_list_data.append(room_type_list)

                    room_type_list.room_number = zimkateg.zikatnr
                    room_type_list.room_count = 1
                    current_type_number = zimkateg.zikatnr
                else:
                    room_type_list.room_count = room_type_list.room_count + 1

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.verfuegbarkeit)).order_by(Zimkateg.typ, Zimkateg.zikatnr).all():

            room_type_list = query(room_type_list_data, filters=(lambda room_type_list: room_type_list.room_number == zimkateg.zikatnr and room_type_list.is_sleeping_room), first=True)

            if room_type_list:
                room_availability_list = Room_availability_list()
                room_availability_list_data.append(room_availability_list)

                i = 1
                while i <= 30:
                    room_availability_list.available_rooms[i - 1] = room_type_list.room_count
                    i = i + 1
                room_availability_list.room_number = zimkateg.zikatnr
                room_availability_list.type_index = zimkateg.typ
                room_availability_list.descriptions = zimkateg.kurzbez + " - " + to_string(zimkateg.overbooking)
                room_availability_list.sort_priority = 0

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:

                room_availability_list = query(room_availability_list_data, filters=(lambda room_availability_list: room_availability_list.room_number == zimmer.zikatnr), first=True)

                if room_availability_list and check_date >= outorder.gespstart and check_date <= outorder.gespende:
                    ooo_count_list[0] = ooo_count_list[0] + 1
                    room_availability_list.available_rooms[0] = room_availability_list.available_rooms[0] - 1

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= check_date) & (Res_line.abreise > check_date)) | ((Res_line.ankunft == check_date) & (Res_line.abreise == check_date))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            room_availability_list = query(room_availability_list_data, filters=(lambda room_availability_list: room_availability_list.is_sleeping_room and room_availability_list.room_number == res_line.zikatnr), first=True)

            if room_availability_list:
                process_room = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    process_room = zimmer.sleeping

                if process_room:
                    room_availability_list.available_rooms[0] = room_availability_list.available_rooms[0] - res_line.zimmeranz

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.betriebsnr == 1) & (Kontline.ankunft <= check_date) & (Kontline.abreise >= check_date) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

            room_availability_list = query(room_availability_list_data, filters=(lambda room_availability_list: room_availability_list.is_sleeping_room and room_availability_list.room_number == kontline.zikatnr), first=True)

            if room_availability_list:
                room_availability_list.available_rooms[0] = room_availability_list.available_rooms[0] - kontline.zimmeranz

        for room_availability_list in query(room_availability_list_data, filters=(lambda room_availability_list: room_availability_list.is_sleeping_room)):
            current_max_avail = -100

            avail_config = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, room_availability_list.room_number)]})

            if avail_config and avail_config.number3 > 0:
                current_max_avail = avail_config.number3

            if room_availability_list.available_rooms[0] < current_max_avail:
                show_notif = True


            room_summary = Room_summary()
            room_summary_data.append(room_summary)

            else:
                room_summary.room_number = room_availability_list.room_number
                room_summary.room_type_name = substring(room_availability_list.descriptions, 0, get_index(room_availability_list.descriptions, " - ") - 1)
                room_summary.overbook = to_int(substring(room_availability_list.descriptions, get_index(room_availability_list.descriptions, " - ") + 3 - 1))
                room_summary.availability = room_availability_list.available_rooms[0]
                room_summary.max_avail = (IF current_max_avail == -100 THEN
                0
                ELSE
                current_max_avail)
                room_summary.total_rooms = total_room_count
                room_summary.ooo_rooms = ooo_count_list[0]
                room_summary.date = day_names[get_weekday(check_date) - 1] + " " +\
                    to_string(get_day(check_date) , "99") + "/" +\
                    to_string(get_month(check_date) , "99") + "/" +\
                    to_string(get_year(check_date))


            room_summary.ooo_rooms = 0

            outorder_obj_list = {}
            outorder = Outorder()
            zimmer = Zimmer()
            for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.zikatnr == room_summary.room_number) & (Zimmer.sleeping)).filter(
                     (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True

                if check_date >= outorder.gespstart and check_date <= outorder.gespende:
                    room_summary.ooo_rooms = room_summary.ooo_rooms + 1
        check_date = check_date + timedelta(days=1)

    return generate_output()