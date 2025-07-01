#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam, Reservation, Segment, Zimkateg, Res_line

def print_rcbl(sorttype:int, last_sort:int, lname:string, fdate:date, lresnr:int, room:string):

    prepare_cache ([Guest, Htparam, Reservation, Segment, Zimkateg, Res_line])

    rc_list_list = []
    msg_str = ""
    ci_date:date = None
    inumofrec:int = 0
    guest = htparam = reservation = segment = zimkateg = res_line = None

    rc_list = gmember = None

    rc_list_list, Rc_list = create_model("Rc_list", {"grpflag":bool, "resnr":int, "reslinnr":int, "gastnrmember":int, "name":string, "zinr":string, "gname":string, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "ankzeit":int, "abreisezeit":int, "groupname":string, "depositgef":Decimal, "depositbez":Decimal, "segment":string, "gastnr":int, "karteityp":int})

    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rc_list_list, msg_str, ci_date, inumofrec, guest, htparam, reservation, segment, zimkateg, res_line
        nonlocal sorttype, last_sort, lname, fdate, lresnr, room
        nonlocal gmember


        nonlocal rc_list, gmember
        nonlocal rc_list_list

        return {"rc-list": rc_list_list, "msg_str": msg_str}

    def cr_rc_list():

        nonlocal rc_list_list, msg_str, ci_date, inumofrec, guest, htparam, reservation, segment, zimkateg, res_line
        nonlocal sorttype, last_sort, lname, fdate, lresnr, room
        nonlocal gmember


        nonlocal rc_list, gmember
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
        rc_list.zipreis =  to_decimal(res_line.zipreis)
        rc_list.ankzeit = res_line.ankzeit
        rc_list.abreisezeit = res_line.abreisezeit
        rc_list.groupname = reservation.groupname
        rc_list.depositgef =  to_decimal(reservation.depositgef)
        rc_list.depositbez =  to_decimal(reservation.depositbez)
        rc_list.segment = segment.bezeich
        rc_list.gastnr = res_line.gastnr

        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if gmember:
            rc_list.karteityp = gmember.karteityp


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if sorttype == 1:

        if last_sort == 1:

            if fdate == None:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.name >= (lname).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                guest = Guest()
                reservation = Reservation()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, guest.karteityp, guest._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Guest.karteityp, Guest._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.name >= (lname).lower()) & (Res_line.ankunft == fdate)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        elif last_sort == 2:

            if fdate == None:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11))).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == fdate)).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.resnr >= lresnr)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

    elif sorttype == 2:

        if last_sort == 1:

            if lname == "" and room != "":

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date)).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == ci_date) & (Res_line.resnr >= lresnr)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

    elif sorttype == 3:

        if last_sort == 1:

            if lname == "" and room != "":

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.name >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr >= (room).lower())).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.resnr >= lresnr)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

    elif sorttype == 4:

        if last_sort == 1:

            if fdate != None:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.ankunft == fdate) & (Res_line.name >= (lname).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        if last_sort == 2:

            if fdate != None:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag < 2) & (Res_line.ankunft == fdate)).order_by(Reservation.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()
            else:

                res_line_obj_list = {}
                res_line = Res_line()
                reservation = Reservation()
                guest = Guest()
                segment = Segment()
                zimkateg = Zimkateg()
                for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower())).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag < 2)).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.resnr >= lresnr)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

    elif sorttype == 5:

        if last_sort == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.ankunft == (ci_date + timedelta(days=1)))).order_by(Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

        if last_sort == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag < 2) & (Res_line.ankunft == (ci_date + timedelta(days=1)))).order_by((to_string(1 - to_int(Reservation.grpflag)) + Reservation.name + to_string(Reservation.resnr))).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

        elif last_sort == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            guest = Guest()
            segment = Segment()
            zimkateg = Zimkateg()
            for res_line.resnr, res_line.reslinnr, res_line.gastnrmember, res_line.zinr, res_line.name, res_line.ankunft, res_line.anztage, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.ankzeit, res_line.abreisezeit, res_line.gastnr, res_line._recid, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, guest.karteityp, guest._recid, segment.bezeich, segment._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.resnr, Res_line.reslinnr, Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.anztage, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.ankzeit, Res_line.abreisezeit, Res_line.gastnr, Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Guest.karteityp, Guest._recid, Segment.bezeich, Segment._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag < 2) & (Res_line.resstatus != 12) & (Res_line.ankunft == (ci_date + timedelta(days=1)))).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                cr_rc_list()

    return generate_output()