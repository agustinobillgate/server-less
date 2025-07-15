#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Outorder, Htparam, Zimmer, Zimkateg, History

def prepare_roomplan_2_webbl(from_room:string):

    prepare_cache ([Htparam, Zimmer, Zimkateg])

    to_date = None
    curr_date = None
    ci_date = None
    do_it = False
    t_res_line_data = []
    t_res_line2_data = []
    t_outorder_data = []
    t_outorder1_data = []
    room_list_data = []
    stat_list:List[string] = ["VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS"]
    a:int = 0
    item_fgcol:List[int] = [15, 15, 15, 15, 15, 15, 15, 0, 15, 0, 0, 15, 0, 0, 0]
    res_line = outorder = htparam = zimmer = zimkateg = history = None

    t_res_line = t_outorder = t_outorder1 = t_res_line2 = room_list = None

    t_res_line_data, T_res_line = create_model_like(Res_line, {"rec_id":int})
    t_outorder_data, T_outorder = create_model_like(Outorder, {"rec_id":int})
    t_outorder1_data, T_outorder1 = create_model_like(Outorder)
    t_res_line2_data, T_res_line2 = create_model("T_res_line2", {"resnr":int, "zinr":string, "name":string, "rec_id":int, "ziwech_zeit":int, "ankunft":date, "abreise":date})
    room_list_data, Room_list = create_model("Room_list", {"location":string, "zistatus":int, "ststr":string, "build":string, "build_flag":string, "etage":int, "zinr":string, "c_char":string, "i_char":string, "zikatnr":int, "rmcat":string, "bezeich":string, "connec":string, "avtoday":string, "recid1":[int,28], "gstatus":[int,28], "bcol":[int,28], "fcol":[int,28], "room":[string,28], "off_mkt":[bool,28], "resnr":[int,28]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_data, t_res_line2_data, t_outorder_data, t_outorder1_data, room_list_data, stat_list, a, item_fgcol, res_line, outorder, htparam, zimmer, zimkateg, history
        nonlocal from_room


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, room_list
        nonlocal t_res_line_data, t_outorder_data, t_outorder1_data, t_res_line2_data, room_list_data

        return {"to_date": to_date, "curr_date": curr_date, "ci_date": ci_date, "do_it": do_it, "t-res-line": t_res_line_data, "t-res-line2": t_res_line2_data, "t-outorder": t_outorder_data, "t-outorder1": t_outorder1_data, "room-list": room_list_data}

    def create_browse():

        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_data, t_res_line2_data, t_outorder_data, t_outorder1_data, room_list_data, stat_list, a, item_fgcol, res_line, outorder, htparam, zimmer, zimkateg, history
        nonlocal from_room


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, room_list
        nonlocal t_res_line_data, t_outorder_data, t_outorder1_data, t_res_line2_data, room_list_data

        datum1:date = None
        datum2:date = None
        depart:date = None
        i:int = 0
        j:int = 0
        do_it1:bool = False
        room_list_data.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zinr >= (from_room).lower())).order_by(Zimmer._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.location = zimmer.code
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
                room_list.bezeich = zimkateg.bezeichnung

                if zimmer.build != "":
                    room_list.build = zimmer.build
                    room_list.build_flag = "*"

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
                    do_it1 = True
                else:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zi_wechsel": [(eq, False)]})
                    do_it1 = None != history

                if do_it1:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == res_line.zinr), first=True)

                    if room_list:
                        room_list.avtoday = ">"

        to_date = curr_date + timedelta(days=27)

        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.zinr != "") & (Res_line.zinr >= (from_room).lower()) & (Res_line.active_flag == 0) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= curr_date)) | (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.abreise > curr_date) & (Res_line.zinr >= (from_room).lower()))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_data.append(t_res_line)

            buffer_copy(res_line, t_res_line)
            t_res_line.rec_id = res_line._recid

            if (res_line.resstatus <= 2 or res_line.resstatus == 5):

                outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"betriebsnr": [(eq, res_line.resnr)]})

                if outorder:
                    t_outorder1 = T_outorder1()
                    t_outorder1_data.append(t_outorder1)

                    buffer_copy(outorder, t_outorder1)

        if curr_date < ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.zinr >= (from_room).lower()) & (Res_line.abreise >= Res_line.ankunft) & not_ (Res_line.zimmerfix) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= curr_date)).order_by(Res_line.ankunft.desc()).all():

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
                    t_res_line2 = T_res_line2()
                    t_res_line2_data.append(t_res_line2)

                    t_res_line2.resnr = res_line.resnr
                    t_res_line2.zinr = res_line.zinr
                    t_res_line2.name = res_line.name
                    t_res_line2.rec_id = res_line._recid
                    t_res_line2.ziwech_zeit = res_line.ziwech_zeit


        for outorder in db_session.query(Outorder).filter(
                 (Outorder.gespende >= curr_date)).order_by(Outorder._recid).all():
            t_outorder = T_outorder()
            t_outorder_data.append(t_outorder)

            buffer_copy(outorder, t_outorder)
            t_outorder.rec_id = outorder._recid


    def create_browse1(print_it:bool):

        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_data, t_res_line2_data, t_outorder_data, t_outorder1_data, room_list_data, stat_list, a, item_fgcol, res_line, outorder, htparam, zimmer, zimkateg, history
        nonlocal from_room


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, room_list
        nonlocal t_res_line_data, t_outorder_data, t_outorder1_data, t_res_line2_data, room_list_data

        datum1:date = None
        datum2:date = None
        depart:date = None
        i:int = 0
        j:int = 0
        datum:date = None
        tmp_date:date = None
        tmp_date = curr_date - timedelta(days=1)

        for t_res_line in query(t_res_line_data):

            if t_res_line.ankunft > curr_date:
                datum1 = t_res_line.ankunft
            else:
                datum1 = curr_date

            if t_res_line.abreise <= to_date:
                datum2 = t_res_line.abreise - timedelta(days=1)
            else:
                datum2 = to_date

            if print_it:
                i = (datum1 - tmp_date).days

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == t_res_line.zinr), first=True)
                for datum in date_range(datum1,datum2) :

                    if t_res_line.resstatus == 13 and room_list.recid1[i - 1] != 0:
                        pass
                    else:
                        room_list.room[i - 1] = substring(t_res_line.name, 0, length(t_res_line.name))
                    i = i + 1
            i = (datum1 - tmp_date).days
            j = 1

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == t_res_line.zinr), first=True)
            for datum in date_range(datum1,datum2) :

                if t_res_line.resstatus == 13 and room_list.recid1[i - 1] != 0:
                    pass
                else:
                    room_list.room[i - 1] = substring(t_res_line.name, 0, length(t_res_line.name))

                    if (t_res_line.resstatus <= 2 or t_res_line.resstatus == 5):
                        room_list.gstatus[i - 1] = 1

                        if t_res_line.ankunft == datum:

                            t_outorder1 = query(t_outorder1_data, filters=(lambda t_outorder1: t_outorder1.zinr == t_res_line.zinr and t_outorder1.betriebsnr == t_res_line.resnr), first=True)

                            if t_outorder1:
                                room_list.off_mkt[i - 1] = True


                            else:
                                room_list.off_mkt[i - 1] = False

                    elif t_res_line.resstatus == 6:
                        room_list.gstatus[i - 1] = 2

                    elif t_res_line.resstatus == 13:
                        room_list.gstatus[i - 1] = 3
                    room_list.recid1[i - 1] = t_res_line.rec_id
                    room_list.resnr[i - 1] = t_res_line.resnr

                    if t_res_line.ziwech_zeit != 0:
                        room_list.bcol[i - 1] = t_res_line.ziwech_zeit
                        room_list.fcol[i - 1] = item_fgcol[room_list.bcol[i - 1]]
                i = i + 1
                j = j + 5

        for t_res_line2 in query(t_res_line2_data):

            if t_res_line2.ankunft > curr_date:
                datum1 = t_res_line2.ankunft
            else:
                datum1 = curr_date

            if t_res_line2.ankunft == t_res_line2.abreise:
                depart = t_res_line2.abreise
            else:
                depart = t_res_line2.abreise - timedelta(days=1)

            if t_res_line2.abreise <= to_date:
                datum2 = depart
            else:
                datum2 = to_date

            if print_it:
                i = (datum1 - tmp_date).days

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == t_res_line2.zinr), first=True)
                for datum in date_range(datum1,datum2) :
                    room_list.room[i - 1] = substring(t_res_line2.name, 0, length(t_res_line2.name))
                    i = i + 1
            i = (datum1 - tmp_date).days
            j = 1

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == t_res_line2.zinr), first=True)
            for datum in date_range(datum1,datum2) :
                room_list.room[i - 1] = substring(t_res_line2.name, 0, length(t_res_line2.name))
                room_list.gstatus[i - 1] = 4
                room_list.recid1[i - 1] = t_res_line2.rec_id
                room_list.resnr[i - 1] = t_res_line2.resnr

                if t_res_line2.ziwech_zeit != 0:
                    room_list.bcol[i - 1] = t_res_line2.ziwech_zeit
                    room_list.fcol[i - 1] = item_fgcol[room_list.bcol[i - 1]]
                i = i + 1
                j = j + 5

        for t_outorder in query(t_outorder_data):

            if t_outorder.gespstart > curr_date:
                datum1 = t_outorder.gespstart
            else:
                datum1 = curr_date

            if t_outorder.gespende < to_date:
                datum2 = t_outorder.gespende
            else:
                datum2 = to_date
            i = (datum1 - tmp_date).days

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zinr == t_outorder.zinr), first=True)

            if room_list:

                if t_outorder.betriebsnr <= 1:
                    for datum in date_range(datum1,datum2) :
                        room_list.room[i - 1] = "O-O-O"
                        room_list.gstatus[i - 1] = 9
                        room_list.recid1[i - 1] = t_outorder.rec_id
                        i = i + 1

                elif t_outorder.betriebsnr == 3 or t_outorder.betriebsnr == 4:
                    for datum in date_range(datum1,datum2) :
                        room_list.room[i - 1] = "O-O-S"
                        room_list.gstatus[i - 1] = 12
                        room_list.recid1[i - 1] = t_outorder.rec_id
                        room_list.zistatus = 9
                        i = i + 1

                elif t_outorder.betriebsnr == 2:
                    for datum in date_range(datum1,datum2) :

                        if room_list.recid1[i - 1] == 0:
                            room_list.room[i - 1] = " O-M "
                            room_list.gstatus[i - 1] = 10
                            room_list.recid1[i - 1] = t_outorder.rec_id
                        i = i + 1


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate
    ci_date = curr_date
    create_browse()
    create_browse1(False)

    return generate_output()