from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Zimkateg, Guest, Res_line

def tent_rsvlistbl(case_type:int, sorttype:int, from_date:date, to_date:date):
    t_tent_rsvlist_list = []
    reservation = zimkateg = guest = res_line = None

    t_tent_rsvlist = None

    t_tent_rsvlist_list, T_tent_rsvlist = create_model("T_tent_rsvlist", {"ankunft":date, "abreise":date, "arrangement":str, "kurzbez":str, "rsvname":str, "rsname":str, "segmentcode":int, "nation1":str, "zimmeranz":int, "erwachs":int, "gratis":int, "resstatus":int, "bemerk":str, "l_zuordnung":[int], "resnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list
        return {"t-tent-rsvlist": t_tent_rsvlist_list}

    def rsvlist1():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def disp_ankunft():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def disp_abreise():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def disp_name():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def disp_argt():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def disp_rmcat():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 3) |  (Res_line.resstatus == 4)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 3) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()
        else:

            res_line_obj_list = []
            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 4) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                create_tent_rsvlist()

    def create_tent_rsvlist():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list


        t_tent_rsvlist = T_tent_rsvlist()
        t_tent_rsvlist_list.append(t_tent_rsvlist)

        t_tent_rsvlist.ankunft = res_line.ankunft
        t_tent_rsvlist.abreise = res_line.abreise
        t_tent_rsvlist.arrangement = res_line.arrangement
        t_tent_rsvlist.kurzbez = zimkateg.kurzbez
        t_tent_rsvlist.rsvname = reservation.name
        t_tent_rsvlist.rsname = res_line.name
        t_tent_rsvlist.resnr = res_line.resnr
        t_tent_rsvlist.segmentcode = reservation.segmentcode
        t_tent_rsvlist.nation1 = guest.nation1
        t_tent_rsvlist.zimmeranz = res_line.zimmeranz
        t_tent_rsvlist.erwachs = res_line.erwachs
        t_tent_rsvlist.gratis = res_line.gratis
        t_tent_rsvlist.resstatus = res_line.resstatus
        t_tent_rsvlist.l_zuordnung = res_line.l_zuordnung[2]
        t_tent_rsvlist.bemerk = res_line.bemerk

    for t_tent_rsvlist in query(t_tent_rsvlist_list):
        t_tent_rsvlist_list.remove(t_tent_rsvlist)


    if case_type == 1:
        rsvlist1()
    elif case_type == 2:
        disp_ankunft()
    elif case_type == 3:
        disp_abreise()
    elif case_type == 4:
        disp_name()
    elif case_type == 5:
        disp_argt()
    elif case_type == 6:
        disp_rmcat()

    return generate_output()