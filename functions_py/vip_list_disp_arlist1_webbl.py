#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 18-09-2025
# Recompile program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Zimkateg, Guestseg, Segment, Res_line, Htparam, Reservation, Guest

def vip_list_disp_arlist1_webbl(show_rate:bool, sorttype:int, fdate:date, lname:string, room:string, ci_date:date, tdate:date, by_period:bool):

    prepare_cache ([Zimkateg, Segment, Res_line, Htparam, Reservation, Guest])

    t_vip_list_data = []
    vip_nr:List[int] = create_empty_list(10,0)
    zimkateg = guestseg = segment = res_line = htparam = reservation = guest = None

    t_vip_list = None

    t_vip_list_data, T_vip_list = create_model("T_vip_list", {"resnr":int, "zinr":string, "name":string, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "ankzeit":int, "abreisezeit":int, "bezeich":string, "karteityp":int, "gastnr":int, "resname":string, "address":string, "city":string, "comments":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_vip_list_data, vip_nr, zimkateg, guestseg, segment, res_line, htparam, reservation, guest
        nonlocal show_rate, sorttype, fdate, lname, room, ci_date, tdate, by_period


        nonlocal t_vip_list
        nonlocal t_vip_list_data

        return {"t-vip-list": t_vip_list_data}

    def disp_arlist():

        nonlocal t_vip_list_data, vip_nr, zimkateg, guestseg, segment, res_line, htparam, reservation, guest
        nonlocal show_rate, sorttype, fdate, lname, room, ci_date, tdate, by_period


        nonlocal t_vip_list
        nonlocal t_vip_list_data

        if sorttype == 1:

            if fdate == None:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

            else:

                if by_period :

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()
                else:

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft == fdate)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

        elif sorttype == 2:

            if lname == "" and room != "":

                if by_period :

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft <= tdate) & (Res_line.abreise >= fdate)).order_by(Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                else:

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft <= fdate) & (Res_line.abreise >= fdate)).order_by(Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

            else:

                if by_period :

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft <= tdate) & (Res_line.abreise >= fdate)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                else:

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft <= fdate) & (Res_line.abreise >= fdate)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()


        elif sorttype == 3:

            if by_period :

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()
            else:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft == fdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

        elif sorttype == 4:

            if by_period :

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()
            else:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.abreise == fdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

        elif sorttype == 5:

            if fdate != None:

                if by_period :

                    res_line_obj_list = {}
                    for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                             ((Res_line.abreise >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 4) & (Res_line.resstatus != 5)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()
                else:

                    if ci_date <= fdate:

                        res_line_obj_list = {}
                        for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                                 ((Res_line.abreise >= fdate) & (Res_line.ankunft <= fdate) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 4) & (Res_line.resstatus != 5)).order_by(Res_line.name).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            assign_it()
                    else:

                        res_line_obj_list = {}
                        for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                                 ((Res_line.abreise >= fdate) & (Res_line.ankunft <= fdate) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 4) & (Res_line.resstatus != 5)).order_by(Res_line.name).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            assign_it()
            else:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 4) & (Res_line.resstatus != 5) & (Res_line.name >= (lname).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

        elif sorttype == 6:

            if by_period :

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()
            else:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         ((Res_line.resstatus <= 3) | (Res_line.resstatus == 6) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft == fdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

        elif sorttype == 7:

            if by_period :

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         (Res_line.active_flag == 1) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.zinr >= (room).lower()) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line.abreise, Res_line.resnr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()
            else:

                res_line_obj_list = {}
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                         (Res_line.active_flag == 1) & (Res_line.abreise <= fdate) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.zinr >= (room).lower()) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line.abreise, Res_line.resnr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()


    def fill_vipnr():

        nonlocal t_vip_list_data, vip_nr, zimkateg, guestseg, segment, res_line, htparam, reservation, guest
        nonlocal show_rate, sorttype, fdate, lname, room, ci_date, tdate, by_period


        nonlocal t_vip_list
        nonlocal t_vip_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
        vip_nr[0] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
        vip_nr[1] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
        vip_nr[2] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
        vip_nr[3] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
        vip_nr[4] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
        vip_nr[5] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
        vip_nr[6] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
        vip_nr[7] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
        vip_nr[8] = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
        vip_nr[9] = htparam.finteger


    def assign_it():

        nonlocal t_vip_list_data, vip_nr, zimkateg, guestseg, segment, res_line, htparam, reservation, guest
        nonlocal show_rate, sorttype, fdate, lname, room, ci_date, tdate, by_period


        nonlocal t_vip_list
        nonlocal t_vip_list_data


        t_vip_list = T_vip_list()
        t_vip_list_data.append(t_vip_list)

        t_vip_list.resnr = res_line.resnr
        t_vip_list.zinr = res_line.zinr
        t_vip_list.name = res_line.name
        t_vip_list.ankunft = res_line.ankunft
        t_vip_list.anztage = res_line.anztage
        t_vip_list.abreise = res_line.abreise
        t_vip_list.zimmeranz = res_line.zimmeranz
        t_vip_list.kurzbez = zimkateg.kurzbez
        t_vip_list.erwachs = res_line.erwachs
        t_vip_list.gratis = res_line.gratis
        t_vip_list.resstatus = res_line.resstatus
        t_vip_list.arrangement = res_line.arrangement
        t_vip_list.ankzeit = res_line.ankzeit
        t_vip_list.abreisezeit = res_line.abreisezeit
        t_vip_list.bezeich = segment.bezeich

        if show_rate :
            t_vip_list.zipreis =  to_decimal(res_line.zipreis)

        if res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)],"gastnr": [(eq, res_line.gastnr)]})

            if reservation:
                t_vip_list.resname = reservation.name

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                t_vip_list.address = guest.adresse1
                t_vip_list.city = guest.wohnort + " " + guest.plz
                t_vip_list.comments = reservation.bemerk + chr_unicode(10) + res_line.bemerk

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                t_vip_list.karteityp = guest.karteityp
                t_vip_list.gastnr = guest.gastnr

    fill_vipnr()
    disp_arlist()

    return generate_output()