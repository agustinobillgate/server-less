#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Outorder, Htparam, Zimmer, Zimkateg, History

def prepare_roomplanbl(from_room:string):

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
    res_line = outorder = htparam = zimmer = zimkateg = history = None

    t_res_line = t_outorder = t_outorder1 = t_res_line2 = room_list = None

    t_res_line_data, T_res_line = create_model_like(Res_line, {"rec_id":int})
    t_outorder_data, T_outorder = create_model_like(Outorder, {"rec_id":int})
    t_outorder1_data, T_outorder1 = create_model_like(Outorder)
    t_res_line2_data, T_res_line2 = create_model("T_res_line2", {"zinr":string, "name":string, "rec_id":int, "ziwech_zeit":int, "ankunft":date, "abreise":date})
    room_list_data, Room_list = create_model("Room_list", {"location":string, "zistatus":int, "ststr":string, "build":string, "build_flag":string, "etage":int, "zinr":string, "c_char":string, "i_char":string, "zikatnr":int, "rmcat":string, "connec":string, "avtoday":string, "recid1":[int,28], "gstatus":[int,28], "bcol":[int,28], "fcol":[int,28], "room":[string,28], "off_mkt":[bool,28]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_data, t_res_line2_data, t_outorder_data, t_outorder1_data, room_list_data, stat_list, a, res_line, outorder, htparam, zimmer, zimkateg, history
        nonlocal from_room


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, room_list
        nonlocal t_res_line_data, t_outorder_data, t_outorder1_data, t_res_line2_data, room_list_data

        return {"to_date": to_date, "curr_date": curr_date, "ci_date": ci_date, "do_it": do_it, "t-res-line": t_res_line_data, "t-res-line2": t_res_line2_data, "t-outorder": t_outorder_data, "t-outorder1": t_outorder1_data, "room-list": room_list_data}

    def create_browse():

        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_data, t_res_line2_data, t_outorder_data, t_outorder1_data, room_list_data, stat_list, a, res_line, outorder, htparam, zimmer, zimkateg, history
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
                 (((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.zinr != "") & (Res_line.zinr >= (from_room).lower()) & (Res_line.active_flag == 0) & not_ (Res_line.to_date < Res_line.ankunft) & not_ (Res_line.curr_date >= Res_line.abreise)) | (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.abreise > curr_date) & (Res_line.zinr >= (from_room).lower()))).order_by(Res_line._recid).all():
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
                    t_res_line2 = T_res_line2()
                    t_res_line2_data.append(t_res_line2)

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate
    ci_date = curr_date
    create_browse()

    return generate_output()