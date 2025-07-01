#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Reservation, Res_line

def res_vouchernobl(case_type:int, voucherno:string, fname:string, tname:string):

    prepare_cache ([Reservation, Res_line])

    t_res_voucherno_list = []
    t_part_resline_list = []
    reservation = res_line = None

    t_res_voucherno = t_part_resline = None

    t_res_voucherno_list, T_res_voucherno = create_model("T_res_voucherno", {"name":string, "vesrdepot":string, "resnr":int, "activeflag":int})
    t_part_resline_list, T_part_resline = create_model("T_part_resline", {"zimmer_wunsch":string, "gastnr":int, "name":string, "resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_voucherno_list, t_part_resline_list, reservation, res_line
        nonlocal case_type, voucherno, fname, tname


        nonlocal t_res_voucherno, t_part_resline
        nonlocal t_res_voucherno_list, t_part_resline_list

        return {"t-res-voucherno": t_res_voucherno_list, "t-part-resline": t_part_resline_list}


    if case_type == 1:

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.activeflag == 0) & (Reservation.vesrdepot == voucherno)).order_by(Reservation._recid).all():
            t_res_voucherno = T_res_voucherno()
            t_res_voucherno_list.append(t_res_voucherno)

            t_res_voucherno.name = reservation.name
            t_res_voucherno.vesrdepot = reservation.vesrdepot
            t_res_voucherno.resnr = reservation.resnr
            t_res_voucherno.activeflag = reservation.activeflag


    elif case_type == 2:

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.activeflag == 0) & (Reservation.name >= (fname).lower()) & (Reservation.name <= (tname).lower()) & (matches(Reservation.vesrdepot,("*" + voucherno + "*")))).order_by(Reservation._recid).all():
            t_res_voucherno = T_res_voucherno()
            t_res_voucherno_list.append(t_res_voucherno)

            t_res_voucherno.name = reservation.name
            t_res_voucherno.vesrdepot = reservation.vesrdepot
            t_res_voucherno.resnr = reservation.resnr
            t_res_voucherno.activeflag = reservation.activeflag


    elif case_type == 3:

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.activeflag == 0) & (matches(Reservation.vesrdepot,("*" + voucherno + "*")))).order_by(Reservation._recid).all():
            t_res_voucherno = T_res_voucherno()
            t_res_voucherno_list.append(t_res_voucherno)

            t_res_voucherno.name = reservation.name
            t_res_voucherno.vesrdepot = reservation.vesrdepot
            t_res_voucherno.resnr = reservation.resnr
            t_res_voucherno.activeflag = reservation.activeflag


    elif case_type == 4:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (matches(Res_line.zimmer_wunsch,("*VOUCHER*")))).order_by(Res_line._recid).all():
            t_part_resline = T_part_resline()
            t_part_resline_list.append(t_part_resline)

            t_part_resline.zimmer_wunsch = res_line.zimmer_wunsch
            t_part_resline.gastnr = res_line.gastnr
            t_part_resline.name = res_line.name
            t_part_resline.resnr = res_line.resnr

    return generate_output()