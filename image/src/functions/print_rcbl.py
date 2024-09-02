from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Reservation, Guest, Segment, Zimkateg, Res_line

def print_rcbl(sorttype:int, last_sort:int, lname:str, fdate:date, lresnr:int, room:str):
    rc_list_list = []
    msg_str = ""
    ci_date:date = None
    inumofrec:int = 0
    htparam = reservation = guest = segment = zimkateg = res_line = None

    rc_list = None

    rc_list_list, Rc_list = create_model("Rc_list", {"grpflag":bool, "resnr":int, "reslinnr":int, "gastnrmember":int, "name":str, "zinr":str, "gname":str, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":str, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":str, "zipreis":decimal, "ankzeit":int, "abreisezeit":int, "groupname":str, "depositgef":decimal, "depositbez":decimal, "segment":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rc_list_list, msg_str, ci_date, inumofrec, htparam, reservation, guest, segment, zimkateg, res_line


        nonlocal rc_list
        nonlocal rc_list_list
        return {"rc-list": rc_list_list, "msg_str": msg_str}

    def cr_rc_list():

        nonlocal rc_list_list, msg_str, ci_date, inumofrec, htparam, reservation, guest, segment, zimkateg, res_line


        nonlocal rc_list
        nonlocal rc_list_list


        rc_list = Rc_list()
        rc_list_list.append(rc_list)

        rc_list.grpflag = reservation.grpflag
        rc_list.resnr = res_line.resnr
        rc_list.reslinnr = res_line.reslinnr
        rc_list.gastnrmember = res_line.gastnrmember
        rc_list.name = reservation.name
        rc_list.zinr = res_line.zinr
        rc_list.gname = res_line.name
        rc_list.ankunft = res_line.ankunft
        rc_list.anztage = res_line.anztage
        rc_list.abreise = res_line.abreise
        rc_list.zimmeranz = res_line.zimmeranz
        rc_list.kurzbez = zimkateg.kurzbez
        rc_list.erwachs = res_line.erwachs
        rc_list.gratis = res_line.gratis
        rc_list.resstatus = res_line.resstatus
        rc_list.arrangement = res_line.arrangement
        rc_list.zipreis = res_line.zipreis
        rc_list.ankzeit = res_line.ankzeit
        rc_list.abreisezeit = res_line.abreisezeit
        rc_list.groupname = reservation.groupname
        rc_list.depositgef = reservation.depositgef
        rc_list.depositbez = reservation.depositbez
        rc_list.segment = segment.bezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if sorttype == 1:

        if last_sort == 1:

            if fdate == None:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (func.lower(Res_line.name) >= (lname).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, guest, reservation, segment, zimkateg in db_session.query(Res_line, Guest, Reservation, Segment, Zimkateg).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (func.lower(Res_line.name) >= (lname).lower()) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        elif last_sort == 2:

            if fdate == None:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11))).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.resnr >= lresnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

    elif sorttype == 2:

        if last_sort == 1:

            if lname == "" and room != "":

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == ci_date) &  (func.lower(Res_line.name) >= (lname).lower()) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == ci_date) &  (func.lower(Res_line.name) >= (lname).lower()) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == ci_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == ci_date) &  (Res_line.resnr >= lresnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

    elif sorttype == 3:

        if last_sort == 1:

            if lname == "" and room != "":

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.name) >= (lname).lower()) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.name) >= (lname).lower()) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = []
            for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (func.lower(Res_line.zinr) >= (room).lower())).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = []
            for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.resnr >= lresnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

    elif sorttype == 4:

        if last_sort == 1:

            if fdate != None:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (Res_line.ankunft == fdate) &  (func.lower(Res_line.name) >= (lname).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (func.lower(Res_line.name) >= (lname).lower())).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        if last_sort == 2:

            if fdate != None:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.active_flag < 2) &  (Res_line.ankunft == fdate)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (func.lower(Reservation.name) >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.active_flag < 2)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (Res_line.resnr >= lresnr)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

    elif sorttype == 5:

        if last_sort == 1:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (Res_line.ankunft == (ci_date + 1))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = []
            for res_line, reservation, guest, zimkateg in db_session.query(Res_line, Reservation, Guest, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag < 2) &  (Res_line.ankunft == (ci_date + 1))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = []
            for res_line, reservation, guest, segment, zimkateg in db_session.query(Res_line, Reservation, Guest, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                    (Res_line.active_flag < 2) &  (Res_line.resstatus != 12) &  (Res_line.ankunft == (ci_date + 1))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                cr_rc_list()

    return generate_output()