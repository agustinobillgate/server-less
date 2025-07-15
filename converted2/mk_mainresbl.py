from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Reservation

def mk_mainresbl(case_type:int, int1:int, int2:int, char1:str, char2:str, deci1:decimal):
    res_line = reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, reservation
        nonlocal case_type, int1, int2, char1, char2, deci1


        return {}


    if case_type == 1:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == int1)).first()
        while None != res_line:
            res_line.grpflag = True

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == int1)).filter(Res_line._recid > curr_recid).first()

    if case_type == 2:

        for reservation in db_session.query(Reservation).filter(
                 (func.lower(Reservation.name) == (char1).lower()) & (Reservation.gastnr == int1) & (Reservation.activeflag == 0)).order_by(Reservation._recid).all():
            reservation.segmentcode = int2

    if case_type == 3:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == int1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.reserve_dec != 0)).order_by(Res_line._recid).all():
            res_line.reserve_dec =  to_decimal("0")

    if case_type == 4:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == int1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.reserve_dec == 0)).order_by(Res_line._recid).all():
            res_line.reserve_dec =  to_decimal(deci1)

    if case_type == 5:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == int1) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0) & ((Res_line.l_zuordnung[inc_value(4)] == 0) | (Res_line.l_zuordnung[inc_value(4)] == int1))).order_by(Res_line._recid).all():
            res_line.l_zuordnung[1] = 0

    return generate_output()