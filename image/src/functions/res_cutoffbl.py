from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Zimkateg, Res_line

def res_cutoffbl(guaranteed:bool, fr_date:date, to_date:date):
    t_rescutoff_list = []
    reservation = zimkateg = res_line = None

    t_rescutoff = None

    t_rescutoff_list, T_rescutoff = create_model("T_rescutoff", {"resnr":int, "gastnr":int, "rsname":str, "ankunft":date, "abreise":date, "zimmeranz":int, "arrangement":str, "zikatnr":int, "zipreis":decimal, "anztage":int, "erwachs":int, "kind1":int, "gratis":int, "resstatus":int, "kurzbez":str, "rsv_resnr":int, "grpflag":bool, "rsvname":str, "point_resnr":int, "resdat":date, "groupname":str, "cutoffdate":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_rescutoff_list, reservation, zimkateg, res_line


        nonlocal t_rescutoff
        nonlocal t_rescutoff_list
        return {"t-rescutoff": t_rescutoff_list}

    if guaranteed == False:

        res_line_obj_list = []
        for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (((Reservation.point_resnr > 0) &  (Res_line.ankunft == fr_date)) |  ((Reservation.point_resnr > 0) &  ((Res_line.ankunft - Reservation.point_resnr) >= fr_date) &  ((Res_line.ankunft - Reservation.point_resnr) <= to_date)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 3)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_rescutoff = T_rescutoff()
            t_rescutoff_list.append(t_rescutoff)

            t_rescutoff.resnr = res_line.resnr
            t_rescutoff.grpflag = reservation.grpflag
            t_rescutoff.rsvname = reservation.name
            t_rescutoff.rsname = res_line.name
            t_rescutoff.point_resnr = reservation.point_resnr
            t_rescutoff.cutoffdate = res_line.ankunft - reservation.point_resnr
            t_rescutoff.ankunft = res_line.ankunft
            t_rescutoff.abreise = res_line.abreise
            t_rescutoff.zimmeranz = res_line.zimmeranz
            t_rescutoff.kurzbez = zimkateg.kurzbez
            t_rescutoff.arrangement = res_line.arrangement
            t_rescutoff.zipreis = res_line.zipreis
            t_rescutoff.anztage = res_line.anztage
            t_rescutoff.erwachs = res_line.erwachs
            t_rescutoff.gratis = res_line.gratis
            t_rescutoff.kind1 = res_line.kind1
            t_rescutoff.resstatus = res_line.resstatus
            t_rescutoff.resdat = reservation.resdat
            t_rescutoff.groupname = reservation.groupname


    elif guaranteed :

        res_line_obj_list = []
        for res_line, reservation, zimkateg in db_session.query(Res_line, Reservation, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (((Reservation.point_resnr > 0) &  (Res_line.ankunft == fr_date)) |  ((Reservation.point_resnr > 0) &  ((Res_line.ankunft - Reservation.point_resnr) >= fr_date) &  ((Res_line.ankunft - Reservation.point_resnr) <= to_date)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 1)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_rescutoff = T_rescutoff()
            t_rescutoff_list.append(t_rescutoff)

            t_rescutoff.resnr = res_line.resnr
            t_rescutoff.grpflag = reservation.grpflag
            t_rescutoff.rsvname = reservation.name
            t_rescutoff.rsname = res_line.name
            t_rescutoff.point_resnr = reservation.point_resnr
            t_rescutoff.cutoffdate = res_line.ankunft - reservation.point_resnr
            t_rescutoff.ankunft = res_line.ankunft
            t_rescutoff.abreise = res_line.abreise
            t_rescutoff.zimmeranz = res_line.zimmeranz
            t_rescutoff.kurzbez = zimkateg.kurzbez
            t_rescutoff.arrangement = res_line.arrangement
            t_rescutoff.zipreis = res_line.zipreis
            t_rescutoff.anztage = res_line.anztage
            t_rescutoff.erwachs = res_line.erwachs
            t_rescutoff.gratis = res_line.gratis
            t_rescutoff.kind1 = res_line.kind1
            t_rescutoff.resstatus = res_line.resstatus
            t_rescutoff.resdat = reservation.resdat
            t_rescutoff.groupname = reservation.groupname


    return generate_output()