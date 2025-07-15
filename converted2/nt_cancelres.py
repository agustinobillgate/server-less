from functions.additional_functions import *
import decimal
from datetime import date
from functions.del_resline import del_resline
from models import Htparam, Reservation, Res_line

def nt_cancelres():
    ci_date:date = None
    del_mainres:bool = False
    htparam = reservation = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, del_mainres, htparam, reservation, res_line

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    res_line_obj_list = []
    for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.point_resnr > 0) & ((ci_date + Reservation.point_resnr) > Res_line.ankunft) & (Reservation.depositbez == 0) & (Reservation.depositbez2 == 0)).filter(
             (Res_line.active_flag == 0) & (Res_line.resstatus == 3)).order_by(Res_line.resnr).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        del_mainres = get_output(del_resline("cancel", res_line.resnr, res_line.reslinnr))

    return generate_output()