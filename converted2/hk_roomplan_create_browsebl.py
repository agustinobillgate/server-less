#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Zimkateg, Outorder, Res_line, History

def hk_roomplan_create_browsebl(print_it:bool, from_room:string, curr_date:date, ci_date:date):

    prepare_cache ([Zimmer, Zimkateg, Outorder, Res_line])

    room_list_data = []
    stat_list:List[string] = ["VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS"]
    item_fgcol:List[int] = [15, 15, 15, 15, 15, 15, 15, 0, 15, 0, 0, 15, 0, 0, 0]
    datum:date = None
    zimmer = zimkateg = outorder = res_line = history = None

    room_list = None

    room_list_data, Room_list = create_model("Room_list", {"zistatus":int, "ststr":string, "build":string, "build_flag":string, "recid1":[int,17], "etage":int, "zinr":string, "c_char":string, "i_char":string, "zikatnr":int, "rmcat":string, "connec":string, "avtoday":string, "gstatus":[int,17], "bcol":[int,17], "fcol":[int,17], "room":[string,17]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, stat_list, item_fgcol, datum, zimmer, zimkateg, outorder, res_line, history
        nonlocal print_it, from_room, curr_date, ci_date


        nonlocal room_list
        nonlocal room_list_data

        return {"room-list": room_list_data}

    def create_browse():

        nonlocal room_list_data, stat_list, item_fgcol, datum, zimmer, zimkateg, outorder, res_line, history
        nonlocal print_it, from_room, curr_date, ci_date


        nonlocal room_list
        nonlocal room_list_data

        datum1:date = None
        datum2:date = None
        to_date:date = None
        depart:date = None
        i:int = 0
        j:int = 0
        do_it:bool = False
        room_list_data.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zinr >= (from_room).lower())).order_by(Zimmer._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.zistatus = zimmer.zistatus

            if zimmer.zistatus == 8:
                room_list.ststr = stat_list[4]
            else:
                room_list.ststr = stat_list[zimmer.zistatus + 1 - 1]
            room_list.etage = zimmer.etage
            room_list.zinr = zimmer.zinr
            room_list.connec = zimmer.verbindung[0]
            room_list.c_char = " " + zimmer.zikennz + " "

            if not zimmer.sleeping:
                room_list.i_char = " i "
            room_list.zikatnr = zimkateg.zikatnr
            room_list.rmcat = zimkateg.kurzbez

            if zimmer.build != "":
                room_list.build = zimmer.build
                room_list.build_flag = "*"

            if zimmer.zistatus == 6:

                outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, ci_date)]})

                if outorder and (outorder.betriebsnr == 3 or outorder.betriebsnr == 4):
                    room_list.zistatus = 9
                    room_list.ststr = stat_list[9]

        if curr_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.abreise == curr_date) & (Res_line.resstatus != 12) & (Res_line.zinr != "") & (Res_line.zinr >= (from_room).lower())).order_by(Res_line._recid).all():

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)

                if room_list:
                    room_list.avtoday = ">"

        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 2) & (Res_line.abreise == curr_date) & (Res_line.resstatus == 8) & (Res_line.zimmerfix == False) & (Res_line.zinr >= (from_room).lower())).order_by(Res_line.ankunft.desc()).all():

                if res_line.ankunft < res_line.abreise:
                    do_it = True
                else:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zi_wechsel": [(eq, False)]})
                    do_it = None != history

                if do_it:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)

                    if room_list:
                        room_list.avtoday = ">"

        to_date = curr_date + timedelta(days=16)

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.zinr != "") & (Res_line.zinr >= (from_room).lower()) & (Res_line.active_flag == 0) & not_ (Res_line.to_date < Res_line.ankunft) & not_ (Res_line.curr_date >= Res_line.abreise)) | (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.abreise > curr_date) & (Res_line.zinr >= (from_room).lower()))).order_by(Res_line._recid).all():

            if res_line.ankunft > curr_date:
                datum1 = res_line.ankunft
            else:
                datum1 = curr_date

            if res_line.abreise <= to_date:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = to_date

            if print_it:
                i = (datum1 - curr_date + 1).days

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)
                for datum in date_range(datum1,datum2) :

                    if res_line.resstatus == 13 and room_list.recid1[i - 1] != 0:
                        pass
                    else:
                        room_list.room[i - 1] = substring(res_line.name, 0, 5)
                    i = i + 1
            i = (datum1 - curr_date + 1).days
            j = 1

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)
            for datum in date_range(datum1,datum2) :

                if res_line.resstatus == 13 and room_list.recid1[i - 1] != 0:
                    pass
                else:

                    if length(res_line.name) >= j:
                        room_list.room[i - 1] = substring(res_line.name, j - 1, 5)

                    if res_line.resstatus <= 2 or res_line.resstatus == 5:
                        room_list.gstatus[i - 1] = 1

                    elif res_line.resstatus == 6:
                        room_list.gstatus[i - 1] = 2

                    elif res_line.resstatus == 13:
                        room_list.gstatus[i - 1] = 3
                    room_list.recid1[i - 1] = res_line._recid

                    if res_line.ziwech_zeit != 0:
                        room_list.bcol[i - 1] = res_line.ziwech_zeit
                        room_list.fcol[i - 1] = item_fgcol[room_list.bcol[i - 1]]
                i = i + 1
                j = j + 5

        if curr_date < ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.zinr >= (from_room).lower()) & (Res_line.abreise >= Res_line.ankunft) & not_ (Res_line.zimmerfix) & not_ (Res_line.to_date < Res_line.ankunft) & not_ (Res_line.curr_date >= Res_line.abreise)).order_by(Res_line.ankunft.desc()).all():

                if res_line.ankunft > curr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = curr_date

                if res_line.ankunft == res_line.abreise:
                    depart = res_line.abreise
                else:
                    depart = res_line.abreise - timedelta(days=1)

                if res_line.abreise <= to_date:
                    datum2 = depart
                else:
                    datum2 = to_date

                if res_line.ankunft < res_line.abreise:
                    do_it = True
                else:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zi_wechsel": [(eq, False)]})
                    do_it = None != history

                if do_it:

                    if print_it:
                        i = (datum1 - curr_date + 1).days

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)
                        for datum in date_range(datum1,datum2) :
                            room_list.room[i - 1] = substring(res_line.name, 0, length(res_line.name))
                            i = i + 1
                    i = (datum1 - curr_date + 1).days
                    j = 1

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)
                    for datum in date_range(datum1,datum2) :
                        room_list.room[i - 1] = substring(res_line.name, 0, length(res_line.name))
                        room_list.gstatus[i - 1] = 4
                        room_list.recid1[i - 1] = res_line._recid

                        if res_line.ziwech_zeit != 0:
                            room_list.bcol[i - 1] = res_line.ziwech_zeit
                            room_list.fcol[i - 1] = item_fgcol[room_list.bcol[i - 1]]
                        i = i + 1
                        j = j + 5


        for outorder in db_session.query(Outorder).filter(
                 (Outorder.gespende >= curr_date)).order_by(Outorder._recid).all():

            if outorder.gespstart > curr_date:
                datum1 = outorder.gespstart
            else:
                datum1 = curr_date

            if outorder.gespende < to_date:
                datum2 = outorder.gespende
            else:
                datum2 = to_date
            i = (datum1 - curr_date + 1).days

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == outorder.zinr), first=True)

            if room_list:

                if outorder.betriebsnr <= 1:
                    for datum in date_range(datum1,datum2) :
                        room_list.room[i - 1] = "O-O-O"
                        room_list.gstatus[i - 1] = 9
                        room_list.recid1[i - 1] = outorder._recid
                        i = i + 1

                elif outorder.betriebsnr == 2:
                    for datum in date_range(datum1,datum2) :

                        if room_list.recid1[i - 1] == 0:
                            room_list.room[i - 1] = " O-M "
                            room_list.gstatus[i - 1] = 10
                            room_list.recid1[i - 1] = outorder._recid
                        i = i + 1

                elif outorder.betriebsnr == 3 or outorder.betriebsnr == 4:
                    for datum in date_range(datum1,datum2) :
                        room_list.room[i - 1] = "O-O-S"
                        room_list.gstatus[i - 1] = 11
                        room_list.recid1[i - 1] = outorder._recid
                        i = i + 1

    create_browse()

    return generate_output()