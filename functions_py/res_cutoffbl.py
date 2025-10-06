#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rd, 6/10/2025
# data di point_resnr selalu 0
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Zimkateg, Res_line

def res_cutoffbl(guaranteed:bool, fr_date:date, to_date:date):

    prepare_cache ([Reservation, Zimkateg, Res_line])

    t_rescutoff_data = []
    reservation = zimkateg = res_line = None

    t_rescutoff = None

    t_rescutoff_data, T_rescutoff = create_model("T_rescutoff", {"resnr":int, "gastnr":int, "rsname":string, "ankunft":date, "abreise":date, "zimmeranz":int, "arrangement":string, "zikatnr":int, "zipreis":Decimal, "anztage":int, "erwachs":int, "kind1":int, "gratis":int, "resstatus":int, "kurzbez":string, "rsv_resnr":int, "grpflag":bool, "rsvname":string, "point_resnr":int, "resdat":date, "groupname":string, "cutoffdate":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_rescutoff_data, reservation, zimkateg, res_line
        nonlocal guaranteed, fr_date, to_date


        nonlocal t_rescutoff
        nonlocal t_rescutoff_data

        return {"t-rescutoff": t_rescutoff_data}

    if guaranteed == False:

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        zimkateg = Zimkateg()
        # for res_line.resnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.arrangement, res_line.zipreis, res_line.anztage, \
        #     res_line.erwachs, res_line.gratis, res_line.kind1, res_line.resstatus, res_line._recid, reservation.grpflag, reservation.name, \
        #         reservation.point_resnr, reservation.resdat, reservation.groupname, reservation._recid, zimkateg.kurzbez, zimkateg._recid \
        #         in db_session.query(Res_line.resnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.arrangement, \
        #                             Res_line.zipreis, Res_line.anztage, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.resstatus, \
        #                                 Res_line._recid, Reservation.grpflag, Reservation.name, Reservation.point_resnr, Reservation.resdat, \
        #                                     Reservation.groupname, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid)   \
        #         .join(Reservation,(Reservation.resnr == Res_line.resnr) & ((
        #                                                                     # (Reservation.point_resnr > 0) & 
        #                                                                     (Res_line.ankunft == fr_date)) | ((Reservation.point_resnr > 0) & 
        #                                                                     ((Res_line.ankunft - Reservation.point_resnr) >= fr_date) & 
        #                                                                     ((Res_line.ankunft - Reservation.point_resnr) <= to_date)))) \
        #         .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr))  \
        #         .filter(
        #          (Res_line.active_flag == 0) & (Res_line.resstatus == 3))   \
        #         .order_by(Reservation.point_resnr, Res_line.ankunft, Reservation.name, Reservation.resnr).all():

        for res_line in db_session.query(Res_line).filter(Res_line.active_flag == 0, Res_line.resstatus == 3).order_by(Res_line.ankunft, Res_line._recid).all():
            

            reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()
            if not reservation:
                continue

            # if not reservation.point_resnr or reservation.point_resnr <= 0:
            #     continue
            if not ((res_line.ankunft == fr_date) or (((res_line.ankunft - timedelta(days=reservation.point_resnr)) >= fr_date) and ((res_line.ankunft - timedelta(days=reservation.point_resnr)) <= to_date))):
                continue


            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            zimkateg = db_session.query(Zimkateg).filter(Zimkateg.zikatnr == res_line.zikatnr).first()
            if not zimkateg:
                continue

            t_rescutoff = T_rescutoff()
            t_rescutoff_data.append(t_rescutoff)

            t_rescutoff.resnr = res_line.resnr
            t_rescutoff.grpflag = reservation.grpflag
            t_rescutoff.rsvname = reservation.name
            t_rescutoff.rsname = res_line.name
            t_rescutoff.point_resnr = reservation.point_resnr
            t_rescutoff.cutoffdate = res_line.ankunft - timedelta(days=reservation.point_resnr)
            t_rescutoff.ankunft = res_line.ankunft
            t_rescutoff.abreise = res_line.abreise
            t_rescutoff.zimmeranz = res_line.zimmeranz
            t_rescutoff.kurzbez = zimkateg.kurzbez
            t_rescutoff.arrangement = res_line.arrangement
            t_rescutoff.zipreis =  to_decimal(res_line.zipreis)
            t_rescutoff.anztage = res_line.anztage
            t_rescutoff.erwachs = res_line.erwachs
            t_rescutoff.gratis = res_line.gratis
            t_rescutoff.kind1 = res_line.kind1
            t_rescutoff.resstatus = res_line.resstatus
            t_rescutoff.resdat = reservation.resdat
            t_rescutoff.groupname = reservation.groupname


    elif guaranteed :

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        zimkateg = Zimkateg()
        # for res_line.resnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.arrangement, res_line.zipreis, res_line.anztage, \
        #     res_line.erwachs, res_line.gratis, res_line.kind1, res_line.resstatus, res_line._recid, reservation.grpflag, reservation.name, \
        #         reservation.point_resnr, reservation.resdat, reservation.groupname, reservation._recid, zimkateg.kurzbez, zimkateg._recid \
        #         in db_session.query(Res_line.resnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.arrangement, Res_line.zipreis, \
        #                             Res_line.anztage, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.resstatus, Res_line._recid, Reservation.grpflag, \
        #                             Reservation.name, Reservation.point_resnr, Reservation.resdat, Reservation.groupname, Reservation._recid, Zimkateg.kurzbez, \
        #                             Zimkateg._recid)    \
        #             .join(Reservation,(Reservation.resnr == Res_line.resnr) & 
        #                   (( 
        #                     # (Reservation.point_resnr > 0) &
        #                     (Res_line.ankunft == fr_date)) | ((Reservation.point_resnr > 0) & 
        #                                                       ((Res_line.ankunft - Reservation.point_resnr) >= fr_date) & 
        #                                                       ((Res_line.ankunft - Reservation.point_resnr) <= to_date))))  \
        #             .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
        #                 (Res_line.active_flag == 0) & 
        #                 (Res_line.resstatus == 1)).order_by(Reservation.point_resnr, Res_line.ankunft, Reservation.name, Reservation.resnr).all():
        for res_line in db_session.query(Res_line).filter(Res_line.active_flag == 0, Res_line.resstatus == 1).order_by(Res_line.ankunft, Res_line._recid).all():
            
            reservation = db_session.query(Reservation).filter(Reservation.resnr == res_line.resnr).first()
            if not reservation:
                continue
            # if not reservation.point_resnr or reservation.point_resnr <= 0:
            #     continue
            if not ((res_line.ankunft == fr_date) or (((res_line.ankunft - timedelta(days=reservation.point_resnr)) >= fr_date) and ((res_line.ankunft - timedelta(days=reservation.point_resnr)) <= to_date))):
                continue

            zimkateg = db_session.query(Zimkateg).filter(Zimkateg.zikatnr == res_line.zikatnr).first()
            if not zimkateg:
                continue

            t_rescutoff = T_rescutoff()
            t_rescutoff_data.append(t_rescutoff)

            t_rescutoff.resnr = res_line.resnr
            t_rescutoff.grpflag = reservation.grpflag
            t_rescutoff.rsvname = reservation.name
            t_rescutoff.rsname = res_line.name
            t_rescutoff.point_resnr = reservation.point_resnr
            t_rescutoff.cutoffdate = res_line.ankunft - timedelta(days=reservation.point_resnr)
            t_rescutoff.ankunft = res_line.ankunft
            t_rescutoff.abreise = res_line.abreise
            t_rescutoff.zimmeranz = res_line.zimmeranz
            t_rescutoff.kurzbez = zimkateg.kurzbez
            t_rescutoff.arrangement = res_line.arrangement
            t_rescutoff.zipreis =  to_decimal(res_line.zipreis)
            t_rescutoff.anztage = res_line.anztage
            t_rescutoff.erwachs = res_line.erwachs
            t_rescutoff.gratis = res_line.gratis
            t_rescutoff.kind1 = res_line.kind1
            t_rescutoff.resstatus = res_line.resstatus
            t_rescutoff.resdat = reservation.resdat
            t_rescutoff.groupname = reservation.groupname


    t_rescutoff_data.sort(
        key=lambda x: (
            x.point_resnr or 0,
            x.ankunft,
            (x.rsvname or "")
        )
    )
        
        


    return generate_output()