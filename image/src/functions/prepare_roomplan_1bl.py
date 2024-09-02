from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Outorder, Htparam, Zimmer, Zimkateg, History

def prepare_roomplan_1bl(from_room:str):
    to_date = None
    curr_date = None
    ci_date = None
    do_it = False
    t_res_line_list = []
    t_res_line2_list = []
    t_outorder_list = []
    t_outorder1_list = []
    room_list_list = []
    t_res_line3_list = []
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", ""]
    a:int = 0
    res_line = outorder = htparam = zimmer = zimkateg = history = None

    t_res_line = t_outorder = t_outorder1 = t_res_line2 = t_res_line3 = room_list = None

    t_res_line_list, T_res_line = create_model_like(Res_line, {"rec_id":int})
    t_outorder_list, T_outorder = create_model_like(Outorder, {"rec_id":int})
    t_outorder1_list, T_outorder1 = create_model_like(Outorder)
    t_res_line2_list, T_res_line2 = create_model("T_res_line2", {"zinr":str, "name":str, "rec_id":int, "ziwech_zeit":int, "ankunft":date, "abreise":date})
    t_res_line3_list, T_res_line3 = create_model_like(Res_line, {"rec_id":int})
    room_list_list, Room_list = create_model("Room_list", {"location":str, "zistatus":int, "ststr":str, "build":str, "build_flag":str, "etage":int, "zinr":str, "c_char":str, "i_char":str, "zikatnr":int, "rmcat":str, "bezeich":str, "connec":str, "avtoday":str, "recid1":[int, 28], "gstatus":[int, 28], "bcol":[int, 28], "fcol":[int, 28], "room":[str, 28], "off_mkt":[bool, 28]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_list, t_res_line2_list, t_outorder_list, t_outorder1_list, room_list_list, t_res_line3_list, stat_list, a, res_line, outorder, htparam, zimmer, zimkateg, history


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, t_res_line3, room_list
        nonlocal t_res_line_list, t_outorder_list, t_outorder1_list, t_res_line2_list, t_res_line3_list, room_list_list
        return {"to_date": to_date, "curr_date": curr_date, "ci_date": ci_date, "do_it": do_it, "t-res-line": t_res_line_list, "t-res-line2": t_res_line2_list, "t-outorder": t_outorder_list, "t-outorder1": t_outorder1_list, "room-list": room_list_list, "t-res-line3": t_res_line3_list}

    def create_browse():

        nonlocal to_date, curr_date, ci_date, do_it, t_res_line_list, t_res_line2_list, t_outorder_list, t_outorder1_list, room_list_list, t_res_line3_list, stat_list, a, res_line, outorder, htparam, zimmer, zimkateg, history


        nonlocal t_res_line, t_outorder, t_outorder1, t_res_line2, t_res_line3, room_list
        nonlocal t_res_line_list, t_outorder_list, t_outorder1_list, t_res_line2_list, t_res_line3_list, room_list_list

        datum1:date = None
        datum2:date = None
        depart:date = None
        i:int = 0
        j:int = 0
        do_it1:bool = False
        room_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                (func.lower(Zimmer.zinr) >= (from_room).lower())).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.location = zimmer.CODE
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
                room_list.bezeich = zimmer.bezeich

                if zimmer.build != "":
                    room_list.build = zimmer.build
                    room_list.build_flag = "*"

        if curr_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.abreise == curr_date) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.zinr) != "") &  (func.lower(Res_line.zinr) >= (from_room).lower())).all():

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zinr == res_line.zinr), first=True)

                if room_list:
                    room_list.avtoday = ">"

        else:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag == 2) &  (Res_line.abreise == curr_date) &  (Res_line.resstatus == 8) &  (Res_line.zimmerfix == False) &  (func.lower(Res_line.zinr) >= (from_room).lower())).all():

                if res_line.ankunft < res_line.abreise:
                    do_it1 = True
                else:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.zi_wechsel == False)).first()
                    do_it1 = None != history

                if do_it1:

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.zinr == res_line.zinr), first=True)

                    if room_list:
                        room_list.avtoday = ">"

        to_date = curr_date + 27

        for res_line in db_session.query(Res_line).filter(
                (((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (func.lower(Res_line.zinr) != "") &  (func.lower(Res_line.zinr) >= (from_room).lower()) &  (Res_line.active_flag == 0) &  (not Res_line.to_date < Res_line.ankunft) &  (not Res_line.curr_date >= Res_line.abreise)) |  (((Res_line. resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1) &  (Res_line.abreise > curr_date) &  (func.lower(Res_line.zinr) >= (from_room).lower() ))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
            t_res_line.rec_id = res_line._recid

            history = db_session.query(History).filter(
                    (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.zi_wechsel == False)).first()

            if history:
                t_res_line3 = T_res_line3()
                t_res_line3_list.append(t_res_line3)

                buffer_copy(res_line, t_res_line3)
                t_res_line3.rec_id = res_line._recid
                t_res_line3.zinr = history.zinr

            if (res_line.resstatus <= 2 or res_line.resstatus == 5):

                outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == res_line.zinr) &  (Outorder.betriebsnr == res_line.resnr)).first()

                if outorder:
                    t_outorder1 = T_outorder1()
                    t_outorder1_list.append(t_outorder1)

                    buffer_copy(outorder, t_outorder1)

        if curr_date < ci_date:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.zinr) >= (from_room).lower()) &  (Res_line.abreise >= Res_line.ankunft) &  (not Res_line.zimmerfix) &  (not Res_line.to_date < Res_line.ankunft) &  (not Res_line.curr_date >= Res_line.abreise)).all():

                if res_line.ankunft > curr_date:
                    datum1 = res_line.ankunft
                else:
                    datum1 = curr_date

                if res_line.ankunft == res_line.abreise:
                    depart = res_line.abreise
                else:
                    depart = res_line.abreise - 1

                if res_line.abreise <= to_date:
                    datum2 = depart
                else:
                    datum2 = to_date

                if res_line.ankunft < res_line.abreise:
                    do_it = True
                else:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.zi_wechsel == False)).first()
                    do_it = None != history

                if do_it:
                    t_res_line2 = T_res_line2()
                    t_res_line2_list.append(t_res_line2)

                    t_res_line2.zinr = res_line.zinr
                    t_res_line2.name = res_line.name
                    t_res_line2.rec_id = res_line._recid
                    t_res_line2.ziwech_zeit = res_line.ziwech_zeit


        for outorder in db_session.query(Outorder).filter(
                (Outorder.gespende >= curr_date)).all():
            t_outorder = T_outorder()
            t_outorder_list.append(t_outorder)

            buffer_copy(outorder, t_outorder)
            t_outorder.rec_id = outorder._recid


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    curr_date = htparam.fdate
    ci_date = curr_date
    create_browse()

    return generate_output()