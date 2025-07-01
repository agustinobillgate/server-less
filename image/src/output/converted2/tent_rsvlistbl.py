#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Zimkateg, Guest, Res_line

def tent_rsvlistbl(case_type:int, sorttype:int, from_date:date, to_date:date):

    prepare_cache ([Reservation, Zimkateg, Guest, Res_line])

    t_tent_rsvlist_list = []
    reservation = zimkateg = guest = res_line = None

    t_tent_rsvlist = None

    t_tent_rsvlist_list, T_tent_rsvlist = create_model("T_tent_rsvlist", {"ankunft":date, "abreise":date, "arrangement":string, "kurzbez":string, "rsvname":string, "rsname":string, "segmentcode":int, "nation1":string, "zimmeranz":int, "erwachs":int, "gratis":int, "resstatus":int, "bemerk":string, "l_zuordnung":[int,5], "resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        return {"t-tent-rsvlist": t_tent_rsvlist_list}

    def rsvlist1():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def disp_ankunft():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def disp_abreise():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.abreise).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.abreise).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.abreise).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def disp_name():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Reservation.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Reservation.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Reservation.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def disp_argt():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.arrangement).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.arrangement).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.arrangement).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def disp_rmcat():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


        nonlocal t_tent_rsvlist
        nonlocal t_tent_rsvlist_list

        if sorttype == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus == 3) | (Res_line.resstatus == 4)) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Zimkateg.kurzbez).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()

        elif sorttype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 3) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Zimkateg.kurzbez).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.name, res_line.resnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.l_zuordnung, res_line.bemerk, res_line._recid, reservation.name, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.nation1, guest._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.name, Res_line.resnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.l_zuordnung, Res_line.bemerk, Res_line._recid, Reservation.name, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.nation1, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 4) & (Res_line.active_flag == 0) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Zimkateg.kurzbez).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_tent_rsvlist()


    def create_tent_rsvlist():

        nonlocal t_tent_rsvlist_list, reservation, zimkateg, guest, res_line
        nonlocal case_type, sorttype, from_date, to_date


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
        pass

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