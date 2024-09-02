from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Htparam, Reservation, Zimkateg, Guest, Res_line, History, Segment, Reslin_queasy, Guestseg

def res_cancelled_1bl(case_type:int, show_rate:bool, curr_rmtype:str, do_it:bool, gname:str, tname:str, res_status:int, fdate:date, tdate:date, kart:int):
    tot_rm = 0
    tot_pax = 0
    tot_ch1 = 0
    tot_com = 0
    tot_nite = 0
    tot_rm_reactive = 0
    tot_pax_reactive = 0
    tot_ch1_reactive = 0
    tot_com_reactive = 0
    tot_nite_reactive = 0
    res_cancelled_list_list = []
    vip_nr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = reservation = zimkateg = guest = res_line = history = segment = reslin_queasy = guestseg = None

    res_cancelled_list = buff_rline = None

    res_cancelled_list_list, Res_cancelled_list = create_model("Res_cancelled_list", {"resnr":int, "columnr":int, "reslinnr":int, "gastnr":int, "rsv_gastnr":int, "zinr":str, "name":str, "rsv_name":str, "ankunft":date, "bemerk":str, "rsv_bemerk":str, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":str, "erwachs":int, "kind1":int, "gratis":int, "arrangement":str, "zipreis":decimal, "betrieb_gastpay":int, "cancelled":date, "cancelled_id":str, "resdat":date, "vesrdepot2":str, "address":str, "city":str, "res_resnr":int, "groupname":str, "flag":int, "vip":str, "nat":str, "rate_code":str, "segment":str, "sp_req":str, "usr_id":str, "vesrdepot":str, "firma":str})

    Buff_rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list
        return {"tot_rm": tot_rm, "tot_pax": tot_pax, "tot_ch1": tot_ch1, "tot_com": tot_com, "tot_nite": tot_nite, "tot_rm_reactive": tot_rm_reactive, "tot_pax_reactive": tot_pax_reactive, "tot_ch1_reactive": tot_ch1_reactive, "tot_com_reactive": tot_com_reactive, "tot_nite_reactive": tot_nite_reactive, "res-cancelled-list": res_cancelled_list_list}

    def disp_noshow():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if show_rate:
            disp_noshow1()
        else:
            disp_noshow2()

    def disp_noshowc():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if show_rate:
            disp_noshowc1()
        else:
            disp_noshowc2()

    def disp_noshow1():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if do_it:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshow1_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshow1_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.active_flag == 2)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*"))).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()

    def disp_noshow2():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if do_it:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshow2_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshow2_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()

    def disp_noshowc1():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if do_it:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshowc1_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.active_flag == 2) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshowc1_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.active_flag == 2) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()

    def disp_noshowc2():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if do_it:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshowc2_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if re.match(".*-ALL-.*",curr_rmtype):
                disp_noshowc2_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = []
                            for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                    (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                                if res_line._recid in res_line_obj_list:
                                    continue
                                else:
                                    res_line_obj_list.append(res_line._recid)


                                assign_it()

                            history_obj_list = []
                            for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr) &  (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                                    (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                                if history._recid in history_obj_list:
                                    continue
                                else:
                                    history_obj_list.append(history._recid)

                                res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()

    def disp_noshow1_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshow1_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*"))).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshow2_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshow2_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.ankunft >= fdate) &  (Res_line.ankunft <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshowc1_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.active_flag == 2) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshowc1_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.active_flag == 2) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshowc2_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr) &  (Guest.karteityp == kart)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def disp_noshowc2_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.cancelled >= fdate) &  (Res_line.cancelled <= tdate) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == "*" and substring(gname, len(gname) - 1, 1) == "*":

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (Res_line.name.op("~")(gname)) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  ((Res_line.betrieb_gastpay != 3) &  (Res_line.betrieb_gastpay != 99)) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, zimkateg, guest in db_session.query(Res_line, Reservation, Zimkateg, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.resstatus == 9) &  (Res_line.betrieb_gastpay == 3) &  (Res_line.active_flag == 2) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        assign_it()

                    history_obj_list = []
                    for history, res_line, reservation, zimkateg, guest in db_session.query(History, Res_line, Reservation, Zimkateg, Guest).join(Res_line,(Res_line.resnr == History.resnr) &  (Res_line.reslinnr == History.reslinnr) &  (func.lower(Res_line.name) >= (gname).lower()) &  (func.lower(Res_line.name) <= (tname).lower()) &  (Res_line.l_zuordnung[2] == 0)).join(Reservation,(Reservation.resnr == res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Guest,(Guest.gastnr == res_line.gastnr)).filter(
                            (History.bemerk.op("~")(".*reactive by.*")) &  (History.ankunft >= fdate) &  (History.ankunft <= tdate)).all():
                        if history._recid in history_obj_list:
                            continue
                        else:
                            history_obj_list.append(history._recid)

                        res_cancelled_list = query(res_cancelled_list_list, filters=(lambda res_cancelled_list :res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()

    def assign_it():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        loopi:int = 0
        str:str = ""
        found_mainguest:bool = False
        Buff_rline = Res_line

        for buff_rline in db_session.query(Buff_rline).filter(
                (Buff_rline.resnr == res_line.resnr) &  (Buff_rline.betrieb_gastpay == 1) &  (Buff_rline.l_zuordnung[2] == 0) &  (Buff_rline.resstatus == res_line.resstatus)).all():
            found_mainguest = True
            break

        if found_mainguest:

            if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or res_line.betrieb_gastpay == 11 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                pass
            else:
                tot_rm = tot_rm + res_line.zimmeranz
                tot_nite = tot_nite + (res_line.abreise - res_line.ankunft) * res_line.zimmeranz


        else:
            tot_rm = tot_rm + res_line.zimmeranz
            tot_nite = tot_nite + (res_line.abreise - res_line.ankunft) * res_line.zimmeranz


        tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
        tot_ch1 = tot_ch1 + res_line.kind1 * res_line.zimmeranz
        tot_com = tot_com + res_line.gratis * res_line.zimmeranz


        res_cancelled_list = Res_cancelled_list()
        res_cancelled_list_list.append(res_cancelled_list)

        res_cancelled_list.resnr = res_line.resnr
        res_cancelled_list.reslinnr = res_line.reslinnr
        res_cancelled_list.gastnr = res_line.gastnr
        res_cancelled_list.rsv_gastnr = reservation.gastnr
        res_cancelled_list.zinr = res_line.zinr
        res_cancelled_list.name = res_line.name
        res_cancelled_list.rsv_name = reservation.name
        res_cancelled_list.ankunft = res_line.ankunft
        res_cancelled_list.bemerk = res_line.bemerk
        res_cancelled_list.rsv_bemerk = reservation.bemerk
        res_cancelled_list.anztage = res_line.anztage
        res_cancelled_list.abreise = res_line.abreise
        res_cancelled_list.zimmeranz = res_line.zimmeranz
        res_cancelled_list.kurzbez = zimkateg.kurzbez
        res_cancelled_list.erwachs = res_line.erwachs
        res_cancelled_list.kind1 = res_line.kind1
        res_cancelled_list.gratis = res_line.gratis
        res_cancelled_list.arrangement = res_line.arrangement
        res_cancelled_list.zipreis = res_line.zipreis
        res_cancelled_list.betrieb_gastpay = res_line.betrieb_gastpay
        res_cancelled_list.cancelled = res_line.cancelled
        res_cancelled_list.cancelled_id = res_line.cancelled_id
        res_cancelled_list.resdat = reservation.resdat
        res_cancelled_list.vesrdepot2 = reservation.vesrdepot2
        res_cancelled_list.address = guest.adresse1
        res_cancelled_list.city = guest.wohnort + " " + guest.plz
        res_cancelled_list.res_resnr = reservation.resnr
        res_cancelled_list.groupname = reservation.groupname
        res_cancelled_list.vesrdepot = reservation.vesrdepot
        res_cancelled_list.firma = guest.name + ", " + guest.anredefirma

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == reservation.segmentcode)).first()

        if segment:
            res_cancelled_list.segment = entry(0, segment.bezeich, "$$0")
        res_cancelled_list.usr_id = reservation.useridanlage


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == "$CODE$":
                res_cancelled_list.rate_code = substring(str, 6)
                return

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

        if reslin_queasy:
            res_cancelled_list.sp_req = reslin_queasy.char3 + "," + res_cancelled_list.sp_req

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode)).first()

            if segment:
                res_cancelled_list.vip = segment.bezeich


        res_cancelled_list.nat = guest.nation1

    def assign_it_reactive():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_list, vip_nr, htparam, reservation, zimkateg, guest, res_line, history, segment, reslin_queasy, guestseg
        nonlocal buff_rline


        nonlocal res_cancelled_list, buff_rline
        nonlocal res_cancelled_list_list

        night:int = 0
        loopi:int = 0
        str:str = ""
        found_mainguest:bool = False
        Buff_rline = Res_line

        for buff_rline in db_session.query(Buff_rline).filter(
                (Buff_rline.resnr == res_line.resnr) &  (Buff_rline.betrieb_gastpay == 1) &  (Buff_rline.l_zuordnung[2] == 0) &  (Buff_rline.resstatus == res_line.resstatus)).all():
            found_mainguest = True
            break

        if res_line.abreise == res_line.ankunft:
            night = 1
        else:
            night = res_line.abreise - res_line.ankunft

        if found_mainguest:

            if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or res_line.betrieb_gastpay == 11 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                pass
            else:
                tot_rm_reactive = tot_rm_reactive + res_line.zimmeranz
                tot_nite_reactive = tot_nite_reactive + night * res_line.zimmeranz


        else:
            tot_rm_reactive = tot_rm_reactive + res_line.zimmeranz
            tot_nite_reactive = tot_nite_reactive + night * res_line.zimmeranz


        tot_pax_reactive = tot_pax_reactive + res_line.erwachs * res_line.zimmeranz
        tot_ch1_reactive = tot_ch1_reactive + res_line.kind1 * res_line.zimmeranz
        tot_com_reactive = tot_com_reactive + res_line.gratis * res_line.zimmeranz


        res_cancelled_list = Res_cancelled_list()
        res_cancelled_list_list.append(res_cancelled_list)

        res_cancelled_list.resnr = res_line.resnr
        res_cancelled_list.columnr = res_line.storno_nr
        res_cancelled_list.reslinnr = res_line.reslinnr
        res_cancelled_list.gastnr = res_line.gastnr
        res_cancelled_list.rsv_gastnr = reservation.gastnr
        res_cancelled_list.zinr = res_line.zinr
        res_cancelled_list.name = res_line.name
        res_cancelled_list.rsv_name = reservation.name
        res_cancelled_list.ankunft = res_line.ankunft
        res_cancelled_list.bemerk = res_line.bemerk
        res_cancelled_list.rsv_bemerk = reservation.bemerk
        res_cancelled_list.anztage = res_line.anztage
        res_cancelled_list.abreise = res_line.abreise
        res_cancelled_list.zimmeranz = res_line.zimmeranz
        res_cancelled_list.kurzbez = zimkateg.kurzbez
        res_cancelled_list.erwachs = res_line.erwachs
        res_cancelled_list.kind1 = res_line.kind1
        res_cancelled_list.gratis = res_line.gratis
        res_cancelled_list.arrangement = res_line.arrangement
        res_cancelled_list.zipreis = res_line.zipreis
        res_cancelled_list.betrieb_gastpay = res_line.betrieb_gastpay
        res_cancelled_list.cancelled = res_line.cancelled
        res_cancelled_list.cancelled_id = res_line.cancelled_id
        res_cancelled_list.resdat = reservation.resdat
        res_cancelled_list.vesrdepot2 = reservation.vesrdepot2
        res_cancelled_list.address = guest.adresse1
        res_cancelled_list.city = guest.wohnort + " " + guest.plz
        res_cancelled_list.res_resnr = reservation.resnr
        res_cancelled_list.groupname = reservation.groupname
        res_cancelled_list.flag = 1
        res_cancelled_list.vesrdepot = reservation.vesrdepot
        res_cancelled_list.firma = guest.name + ", " + guest.anredefirma

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == reservation.segmentcode)).first()

        if segment:
            res_cancelled_list.segment = entry(0, segment.bezeich, "$$0")
        res_cancelled_list.usr_id = reservation.useridanlage


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == "$CODE$":
                res_cancelled_list.rate_code = substring(str, 6)
                return

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

        if reslin_queasy:
            res_cancelled_list.sp_req = reslin_queasy.char3 + "," + res_cancelled_list.sp_req

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode)).first()

            if segment:
                res_cancelled_list.vip = segment.bezeich


        res_cancelled_list.nat = guest.nation1

    if case_type == 1:
        disp_noshow()

    elif case_type == 2:
        disp_noshowc()

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

    return generate_output()