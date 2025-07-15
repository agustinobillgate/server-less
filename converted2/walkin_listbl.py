#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Reservation, Segment, Zimkateg, Res_line, Guest

def walkin_listbl(case_type:int, fdate:date, walk_in:int, wi_grp:int, walkin_flag:bool):

    prepare_cache ([Htparam, Reservation, Segment, Zimkateg, Guest])

    t_walkin_list_data = []
    wi_int:int = 0
    htparam = reservation = segment = zimkateg = res_line = guest = None

    t_walkin_list = None

    t_walkin_list_data, T_walkin_list = create_model("T_walkin_list", {"resnr":int, "zinr":string, "name":string, "ankunft":date, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":string, "erwachs":int, "kind1":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "ankzeit":int, "abreisezeit":int, "bezeich":string, "bemerk":string, "gastnr":int, "res_address":string, "res_city":string, "res_bemerk":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_walkin_list_data, wi_int, htparam, reservation, segment, zimkateg, res_line, guest
        nonlocal case_type, fdate, walk_in, wi_grp, walkin_flag


        nonlocal t_walkin_list
        nonlocal t_walkin_list_data

        return {"t-walkin-list": t_walkin_list_data}

    def disp_arlist1():

        nonlocal t_walkin_list_data, wi_int, htparam, reservation, segment, zimkateg, res_line, guest
        nonlocal case_type, fdate, walk_in, wi_grp, walkin_flag


        nonlocal t_walkin_list
        nonlocal t_walkin_list_data

        if fdate == None:

            if not walkin_flag:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1) & (Res_line.gastnr == wi_int)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()
            else:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode)) & (((Segment.segmentcode == walk_in)) | ((Segment.segmentgrup == wi_grp) & (wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()

        elif fdate != None:

            if not walkin_flag:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.ankunft == fdate) & (Res_line.gastnr == wi_int) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag <= 2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()
            else:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode)) & (((Segment.segmentcode == walk_in)) | ((Segment.segmentgrup == wi_grp) & (wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.ankunft == fdate) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag <= 2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()


    def disp_arlist2():

        nonlocal t_walkin_list_data, wi_int, htparam, reservation, segment, zimkateg, res_line, guest
        nonlocal case_type, fdate, walk_in, wi_grp, walkin_flag


        nonlocal t_walkin_list
        nonlocal t_walkin_list_data

        if fdate == None:

            if not walkin_flag:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.gastnr == wi_int) & (Res_line.active_flag == 1)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()
            else:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode)) & (((Segment.segmentcode == walk_in)) | ((Segment.segmentgrup == wi_grp) & (wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.active_flag == 1)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()

        elif fdate != None:

            if not walkin_flag:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.ankunft == fdate) & (Res_line.gastnr == wi_int) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag <= 2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()
            else:

                res_line_obj_list = {}
                for res_line, reservation, segment, zimkateg in db_session.query(Res_line, Reservation, Segment, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,((Segment.segmentcode == Reservation.segmentcode)) & (((Segment.segmentcode == walk_in)) | ((Segment.segmentgrup == wi_grp) & (wi_grp != 0)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.ankunft == fdate) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (Res_line.active_flag <= 2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_walkin_list()


    def create_walkin_list():

        nonlocal t_walkin_list_data, wi_int, htparam, reservation, segment, zimkateg, res_line, guest
        nonlocal case_type, fdate, walk_in, wi_grp, walkin_flag


        nonlocal t_walkin_list
        nonlocal t_walkin_list_data

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
        t_walkin_list = T_walkin_list()
        t_walkin_list_data.append(t_walkin_list)

        buffer_copy(res_line, t_walkin_list)
        t_walkin_list.kurzbez = zimkateg.kurzbez
        t_walkin_list.bezeich = segment.bezeich
        t_walkin_list.res_address = guest.adresse1
        t_walkin_list.res_city = guest.wohnort + " " + guest.plz
        t_walkin_list.res_bemerk = reservation.bemerk


    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)],"paramgruppe": [(eq, 7)]})
    wi_int = htparam.finteger

    if case_type == 1:
        disp_arlist1()
    elif case_type == 2:
        disp_arlist2()

    return generate_output()