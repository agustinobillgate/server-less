from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Reservation, Res_line

def expiredid_countbl(aswaittime:int):
    expired_id = 0
    user_name = False
    server_time:int = 0
    server_date:date = None
    bediener = reservation = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal expired_id, user_name, server_time, server_date, bediener, reservation, res_line


        return {"expired_id": expired_id, "user_name": user_name}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username) == "Wi_Guest")).first()

    if bediener:
        expired_id = 0
        user_name = True

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.depositbez == 0)).filter(
                ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.cancelled_id == bediener.userinit) &  (Res_line.betrieb_gast == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            server_time = get_current_time_in_seconds() - res_line.ankzeit
            server_date = get_current_date()

            if (server_time > aswaittime or res_line.ankunft != server_date):
                expired_id = expired_id + 1

    return generate_output()