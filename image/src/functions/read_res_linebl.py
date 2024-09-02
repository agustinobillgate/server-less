from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Kontline, Guest, Zimmer, Reservation

t_res_line_list, T_res_line = create_model_like(Res_line)

def read_res_linebl(case_type:int, resno:int, reslinno:int, resstat:int, actflag:int, rmno:str, arrive:date, depart:date, gastno:int, kontigno:int, kontcode:str):
    t_res_line_list = []
    c_room:str = ""
    res_line = kontline = guest = zimmer = reservation = None

    t_res_line = rbuff = None

    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_list, c_room, res_line, kontline, guest, zimmer, reservation
        nonlocal rbuff

        nonlocal t_res_line, rbuff
        nonlocal t_res_line_list
        return {"t-res-line": t_res_line_list}

    def delete_procedure():

        nonlocal t_res_line_list, c_room, res_line, kontline, guest, zimmer, reservation
        nonlocal rbuff
        nonlocal t_res_line, rbuff
        nonlocal t_res_line_list

#     hHandle = THIS_PROCEDURE

    local_storage.debugging = local_storage.debugging + ",Case:" + str(case_type)
    
    if case_type == 1:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 2:

        if kontigno > 0:

            res_line_obj_list = []
            recs = (
                db_session.query(Res_line, Kontline)
                .join(Kontline,(Kontline.kontignr == Res_line.kontignr) & 
                                 (func.lower(Kontline.kontcode.lower()) == kontcode.lower()) &  
                                 (Kontline.kontstatus == 1))
                .filter(
                    (Res_line.kontignr > 0) &  
                    (Res_line.gastnr == gastno) &  
                    (Res_line.active_flag <= 2) &  
                    (Res_line.resstatus <= 6)
                ).all()
            )
            for res_line, kontline in recs:
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)


        elif kontigno < 0:

            res_line_obj_list = []
            for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) &  (func.lower(Kontline.kontcode.lower()) == (kontcode).lower()) &  (Kontline.kontstatus == 1)).filter(
                    (Res_line.kontignr < 0) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag < 2) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)

    elif case_type == 3:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == actflag)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 4:
        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) & 
                (Res_line.active_flag <= 1) &  
                (Res_line.resstatus != 12) &  
                (Res_line.l_zuordnung[2] == 0)
                ).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 5:

        if rmno != "":

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == actflag) &  (Res_line.resstatus == resstat) &  (Res_line.zinr == rmno) &  (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno)).first()
        else:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == actflag) &  (Res_line.resstatus == resstat) &  (Res_line.resnr == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 6:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno) &  (Res_line.resstatus == resstat) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 7:

        res_line = db_session.query(Res_line).filter(
                (Res_line.zinr == rmno) &  (Res_line.active_flag == actflag) &  (Res_line.resnr != resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 8:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno) &  (Res_line.active_flag <= actflag) &  (Res_line.zipreis > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 9:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.zinr == rmno) &  (Res_line.ankunft >= arrive) &  (Res_line.ankunft < depart) &  (Res_line.resnr != resno) &  (Res_line.resstatus != resstat)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 10:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.kontakt_nr == reslinno) &  (Res_line.l_zuordnung[2] == 1)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 11:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 12:

        if rmno > "":

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  (Res_line.resstatus != resstat) &  (Res_line.zinr == rmno) &  (Res_line.l_zuordnung[2] == 0)).first()
        else:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  (Res_line.resstatus != resstat) &  (Res_line.l_zuordnung[2] == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 13:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 14:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.gastnr == gastno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 15:

        res_line = db_session.query(Res_line).filter(
                (Res_line._recid == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 16:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno) &  (Res_line.active_flag <= actflag)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 17:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  ((Res_line.resstatus == 11) |  (Res_line.resstatus == 13))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 18:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.gastnr == gastno) &  (Res_line.active_flag <= 1)).all():

            if res_line:
                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)
    elif case_type == 19:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= actflag) &  (func.lower(Res_line.pin_code) == (kontcode).lower())).first()
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)
    elif case_type == 20:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.resstatus == resstat) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 21:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  (Res_line.resstatus != resstat)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 22:

        if actflag <= 1:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).first()
        else:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag == 2) &  ((Res_line.resstatus == 8) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 23:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.gastnr == gastno) &  (((Res_line.resstatus >= 1) &  (Res_line.resstatus <= 4)) |  (Res_line.resstatus == 11)) &  (Res_line.zimmeranz > 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 24:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 25:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.pin_code == rmno) &  (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 26:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.abreise == arrive) &  (Res_line.zinr == rmno) &  (Res_line.resstatus != 12)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 27:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.zinr == rmno) &  (Res_line.resstatus == 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 28:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (Res_line.zinr == rmno) &  ((Res_line.resnr != resno) &  (Res_line.reslinnr != reslinno))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 29:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus <= 6) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 30:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.kontakt_nr == reslinno) &  (Res_line.l_zuordnung[2] == 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 31:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno) &  (Res_line.resstatus == 11) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 32:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != resno) &  (Res_line.zinr == rmno) &  (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 33:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno) &  (Res_line.zinr == "") &  (Res_line.active_flag == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 34:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 6)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 35:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 36:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.gastnr == gastno) &  (((Res_line.resstatus >= 1) &  (Res_line.resstatus <= 5)) |  (Res_line.resstatus == 11)) &  (Res_line.zimmeranz > 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 37:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.zinr == rmno) &  (Res_line.abreise == arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 38:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 6) &  (Res_line.zinr == rmno)).first()

        if not res_line and resstat == 13:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (Res_line.zinr == rmno) &  (Res_line.l_zuordnung[2] == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 39:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (Res_line.zinr == rmno) &  (Res_line.l_zuordnung[2] == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 40:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.zinr == "")).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 41:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.zinr == rmno) &  (Res_line.resstatus == 13) &  (Res_line.abreise > arrive) &  (Res_line.zipreis == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 42:

        res_line_obj_list = []
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) &  (func.lower(Kontline.kontcode.lower()) == (kontcode).lower()) &  (Kontline.kontstatus == 1)).filter(
                (Res_line.kontignr > 0) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag <= 2) &  (Res_line.resstatus <= 6)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 43:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

        if not res_line:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (Res_line.l_zuordnung[2] == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 44:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.zinr == rmno) &  (Res_line.reslinnr != reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 45:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == actflag) &  (Res_line.l_zuordnung[2] == 1) &  (Res_line.kontakt_nr == reslinno)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 46:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= actflag) &  (((Res_line.ankunft == arrive)) |  ((Res_line.abreise == arrive))) &  (Res_line.zinr == rmno) &  (Res_line.betrieb_gast > 0) &  (Res_line.resnr != resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 47:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != resno) &  (Res_line.zinr == rmno) &  (Res_line.active_flag <= actflag) &  (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 48:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  ((Res_line.resstatus == 11) |  (Res_line.resstatus == 13)) &  (Res_line.zinr == rmno) &  (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 49:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == actflag) &  (Res_line.zinr != "") &  (Res_line.betrieb_gast == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 50:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.kontakt_nr == reslinno) &  (Res_line.l_zuordnung[2] == 1)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 51:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 52:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 53:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 54:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  (Res_line.zipreis > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 55:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.zinr == rmno) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.ankunft == arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 56:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.zinr == rmno)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 57:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == resstat) &  (Res_line.abreise == arrive) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 58:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resstatus == resstat) &  (Res_line.zinr == rmno) &  (Res_line.abreise == arrive) &  (Res_line.l_zuordnung[2] == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 59:

        res_line_obj_list = []
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) &  (func.lower(Kontline.kontcode.lower()) == (kontcode).lower()) &  (Kontline.kontstat == 1)).filter(
                (Res_line.kontignr < 0) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag < actflag) &  (Res_line.resstatus < resstat) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 60:

        res_line_obj_list = []
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) &  (func.lower(Kontline.kontcode.lower()) == (kontcode).lower()) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).filter(
                (Res_line.kontignr < 0) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag < actflag) &  (Res_line.resstatus < resstat) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 61:

        res_line_obj_list = []
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) &  (func.lower(Kontline.kontcode.lower()) == (kontcode).lower()) &  (Kontline.kontstat == 1)).filter(
                (Res_line.kontignr != 0) &  (Res_line.gastnr == gastno) &  (Res_line.active_flag < actflag) &  (Res_line.resstatus < resstat)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 62:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  ((Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 63:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno) &  (Res_line.resstatus == resstat) &  ((Res_line.betrieb_gastpay <= 2) |  (Res_line.betrieb_gastpay == 5))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 64:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr != reslinno) &  ((Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.l_zuordnung[2] == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 65:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag) &  ((Res_line.resstatus == 11) |  (Res_line.resstatus == 13)) &  ((Res_line.kontakt_nr == reslinno))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 66:

        res_line = db_session.query(Res_line).filter(
                (Res_line.gastnrmember == gastno) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 67:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr >= reslinno)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 68:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == depart)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 69:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr != resno) &  (Res_line.active_flag == actflag) &  (Res_line.l_zuordnung[4] == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 70:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 71:

        res_line = db_session.query(Res_line).filter(
                (Res_line.zinr == rmno) &  (Res_line.resstatus == resstat)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 72:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= actflag) &  (((Res_line.ankunft >= arrive) &  (Res_line.ankunft <= depart)) |  ((Res_line.abreise >= arrive) &  (Res_line.abreise <= depart)) |  ((Res_line.arrive >= Res_line.ankunft) &  (Res_line.arrive <= Res_line.abreise))) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 73:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.zinr == rmno) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.active_flag == actflag))).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 74:

        res_line = db_session.query(Res_line).filter(
                (Res_line.betriebsnr == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 75:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.zinr == rmno) &  (Res_line.resstatus != 12)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 76:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.l_zuordnung[2] == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 77:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.l_zuordnung[4] == reslinno) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (Res_line.resnr != resno)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 78:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  ((Res_line.active_flag == actflag) |  (Res_line.resstatus == resstat))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 79:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 80:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.resstatus != resstat) &  (Res_line.l_zuordnung[2] == 0)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 81:

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (get_month(Guest.geburtdatum1) == get_month(get_current_date())) &  (get_day(Guest.geburtdatum1) == get_day(get_current_date()))).filter(
                (Res_line.active_flag <= actflag) &  (Res_line.resstatus != resstat)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 82:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.resstatus == resstat)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 83:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.zinr == rmno) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.resnr != resno) &  (Res_line.reslinnr != reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 84:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr != resno) &  (Res_line.active_flag == 1) &  (Res_line.l_zuordnung[1] == 0) &  (Res_line.l_zuordnung[4] == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 85:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag == actflag) &  (Res_line.resstatus != resstat)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 86:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == actflag) &  (Res_line.resstatus == resstat) &  (Res_line.resnr == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 87:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus >= 6) &  (Res_line.resstatus <= 8) &  (Res_line.betriebsnr != 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 88:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.gastnrmember == gastno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 89:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resnr != resno) &  (Res_line.resstatus != 12) &  (not Res_line.abreise <= arrive) &  (not Res_line.ankunft > depart) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 90:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (not Res_line.abreise <= arrive) &  (not Res_line.ankunft > depart) &  (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 91:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus >= 6) &  (Res_line.resstatus <= 8) &  (Res_line.gratis == 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 91:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= actflag)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 92:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.zinr == rmno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 93:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if not res_line:

            if arrive > depart:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == rmno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.ankunft <= depart) &  (Res_line.abreise > depart)).first()
            else:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == rmno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.ankunft <= depart) &  (Res_line.abreise >= depart)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 94:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 13)).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 95:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if not res_line:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.zinr == rmno) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.active_flag >= 1) &  (Res_line.active_flag <= 2) &  (Res_line.ankunft <= arrive) &  (Res_line.abreise > arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 96:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (to_int(Res_line.code) == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 99:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 100:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 101:
        zimmer = db_session.query(Zimmer).filter((Zimmer.zinr == rmno)).first()
        if zimmer:
            rbuff = db_session.query(Rbuff).filter( (Rbuff.zinr == rmno) &  (Rbuff.active_flag == 1)).first()
            if rbuff:

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.resnr == rbuff.resnr) &  
                        (Res_line.active_flag == 1) &  
                        ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))
                        ).all():

                    t_res_line = query(t_res_line_list, filters=(lambda t_res_line :t_res_line.zinr == res_line.zinr), first=True)

                    if not t_res_line:
                        t_res_line = T_res_line()
                        t_res_line_list.append(t_res_line)

                        buffer_copy(res_line, t_res_line)

        else:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.activeflag == 0) &  (Reservation.groupname == rmno)).first()

            if reservation:

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))).all():

                    t_res_line = query(t_res_line_list, filters=(lambda t_res_line :t_res_line.zinr == res_line.zinr), first=True)

                    if not t_res_line:
                        t_res_line = T_res_line()
                        t_res_line_list.append(t_res_line)

                        buffer_copy(res_line, t_res_line)


    return generate_output()