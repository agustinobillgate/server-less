from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Zimkateg, Guestseg, Segment, Res_line, Reservation, Guest

def vip_list_disp_arlist_webbl(show_rate:bool, sorttype:int, fdate:date, lname:str, room:str, ci_date:date, tdate:date):
    t_vip_list_list = []
    vip_nr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = zimkateg = guestseg = segment = res_line = reservation = guest = None

    t_vip_list = None

    t_vip_list_list, T_vip_list = create_model("T_vip_list", {"resnr":int, "zinr":str, "name":str, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":str, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":str, "zipreis":decimal, "ankzeit":int, "abreisezeit":int, "bezeich":str, "karteityp":int, "gastnr":int, "resname":str, "address":str, "city":str, "comments":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list
        return {"t-vip-list": t_vip_list_list}

    def disp_arlist():

        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list

        if show_rate:
            disp_arlist1()
        else:
            disp_arlist2()

    def fill_vipnr():

        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 700)).first()
        vip_nr[0] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 701)).first()
        vip_nr[1] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 702)).first()
        vip_nr[2] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 703)).first()
        vip_nr[3] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 704)).first()
        vip_nr[4] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 705)).first()
        vip_nr[5] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 706)).first()
        vip_nr[6] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 707)).first()
        vip_nr[7] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 708)).first()
        vip_nr[8] = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 712)).first()
        vip_nr[9] = htparam.finteger

    def disp_arlist1():

        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list

        if sorttype == 1:

            if fdate == None:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*"))).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif sorttype == 2:

            if lname == "" and room != "":

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()


        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                    ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.ankunft == ci_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.abreise == ci_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

        elif sorttype == 5:

            if fdate != None:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        (((Res_line. active_flag == 0) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))) |  ((Res_line.active_flag == 1) &  (Res_line.abreise >= fdate) &  (Res_line.abreise <= tdate) &  (Res_line.name.op("~")(".*" + lname + ".*")))) &  (Res_line.resstatus != 12)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()
            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.name.op("~")(".*" + lname + ".*"))).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def disp_arlist2():

        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list

        if sorttype == 1:

            if fdate == None:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*"))).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()
            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif sorttype == 2:

            if lname == "" and room != "":

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()
            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                    ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.ankunft == ci_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.name.op("~")(".*" + lname + ".*")) &  (Res_line.abreise == ci_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                assign_it()

        elif sorttype == 5:

            if fdate != None:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        (((Res_line. active_flag == 0) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))) |  ((Res_line.active_flag == 1) &  (Res_line.abreise >= fdate) &  (Res_line.abreise <= tdate) &  (Res_line.name.op("~")(".*" + lname + ".*")))) &  (Res_line.resstatus != 12)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()
            else:

                res_line_obj_list = []
                for res_line, zimkateg, guestseg, segment in db_session.query(Res_line, Zimkateg, Guestseg, Segment).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guestseg,(Guestseg.gastnr == Res_line.gastnrmember) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).join(Segment,(Segment.segmentcode == guestseg.segmentcode)).filter(
                        (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.name.op("~")(".*" + lname + ".*"))).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    assign_it()

    def assign_it():

        nonlocal t_vip_list_list, vip_nr, htparam, zimkateg, guestseg, segment, res_line, reservation, guest


        nonlocal t_vip_list
        nonlocal t_vip_list_list


        t_vip_list = T_vip_list()
        t_vip_list_list.append(t_vip_list)

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
        t_vip_list.zipreis = res_line.zipreis
        t_vip_list.ankzeit = res_line.ankzeit
        t_vip_list.abreisezeit = res_line.abreisezeit
        t_vip_list.bezeich = segment.bezeich

        if res_line:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr) &  (Reservation.gastnr == res_line.gastnr)).first()

            if reservation:
                t_vip_list.resname = reservation.name

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == reservation.gastnr)).first()
                t_vip_list.address = guest.adresse1
                t_vip_list.city = guest.wohnort + " " + guest.plz
                t_vip_list.comments = reservation.bemerk + chr (10) + res_line.bemerk

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()
                t_vip_list.karteityp = guest.karteityp
                t_vip_list.gastnr = guest.gastnr


    fill_vipnr()
    disp_arlist()

    return generate_output()