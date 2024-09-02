from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Reservation, Segment, Zimkateg, Res_line, Guest

def walkin_listbl(case_type:int, fdate:date, walk_in:int, wi_grp:int, walkin_flag:bool):
    t_walkin_list_list = []
    wi_int:int = 0
    htparam = reservation = segment = zimkateg = res_line = guest = None

    t_walkin_list = None

    t_walkin_list_list, T_walkin_list = create_model("T_walkin_list", {"resnr":int, "zinr":str, "name":str, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":str, "erwachs":int, "kind1":int, "gratis":int, "resstatus":int, "arrangement":str, "zipreis":decimal, "ankzeit":int, "abreisezeit":int, "bezeich":str, "bemerk":str, "gastnr":int, "res_address":str, "res_city":str, "res_bemerk":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_walkin_list_list, wi_int, htparam, reservation, segment, zimkateg, res_line, guest


        nonlocal t_walkin_list
        nonlocal t_walkin_list_list
        return {"t-walkin-list": t_walkin_list_list}

    def disp_arlist1():

        nonlocal t_walkin_list_list, wi_int, htparam, reservation, segment, zimkateg, res_line, guest


        nonlocal t_walkin_list
        nonlocal t_walkin_list_list

        if fdate == None:

            if not walkin_flag:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1) &  (Res_line.gastnr == wi_int)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode)) &  (((Segment.segmentcode == walk_in)) |  ((Segmentgrup == wi_grp) &  (Segment.wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()

        elif fdate != None:

            if not walkin_flag:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.ankunft == fdate) &  (Res_line.gastnr == wi_int) &  ((Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)) &  (Res_line.active_flag <= 2)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode)) &  (((Segment.segmentcode == walk_in)) |  ((Segmentgrup == wi_grp) &  (Segment.wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.ankunft == fdate) &  ((Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)) &  (Res_line.active_flag <= 2)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()

    def disp_arlist2():

        nonlocal t_walkin_list_list, wi_int, htparam, reservation, segment, zimkateg, res_line, guest


        nonlocal t_walkin_list
        nonlocal t_walkin_list_list

        if fdate == None:

            if not walkin_flag:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.gastnr == wi_int) &  (Res_line.active_flag == 1)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode)) &  (((Segment.segmentcode == walk_in)) |  ((Segmentgrup == wi_grp) &  (Segment.wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.active_flag == 1)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()

        elif fdate != None:

            if not walkin_flag:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.ankunft == fdate) &  (Res_line.gastnr == wi_int) &  ((Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)) &  (Res_line.active_flag <= 2)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()
            else:

                res_line_obj_list = []
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == reservation.segmentcode)) &  (((Segment.segmentcode == walk_in)) |  ((Segmentgrup == wi_grp) &  (Segment.wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                        (Res_line.ankunft == fdate) &  ((Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)) &  (Res_line.active_flag <= 2)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)


                    create_walkin_list()

    def create_walkin_list():

        nonlocal t_walkin_list_list, wi_int, htparam, reservation, segment, zimkateg, res_line, guest


        nonlocal t_walkin_list
        nonlocal t_walkin_list_list

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == reservation.gastnr)).first()
        t_walkin_list = T_walkin_list()
        t_walkin_list_list.append(t_walkin_list)

        buffer_copy(res_line, t_walkin_list)
        t_walkin_list.kurzbez = zimkateg.kurzbez
        t_walkin_list.bezeich = segment.bezeich
        t_walkin_list.res_address = guest.adresse1
        t_walkin_list.res_city = guest.wohnort + " " + guest.plz
        t_walkin_list.res_bemerk = reservation.bemerk

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 109) &  (Htparam.paramgruppe == 7)).first()
    wi_int = htparam.finteger

    if case_type == 1:
        disp_arlist1()
    elif case_type == 2:
        disp_arlist2()

    return generate_output()