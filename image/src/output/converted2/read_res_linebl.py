#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Kontline, Guest, Zimmer, Reservation

def read_res_linebl(case_type:int, resno:int, reslinno:int, resstat:int, actflag:int, rmno:string, arrive:date, depart:date, gastno:int, kontigno:int, kontcode:string):

    prepare_cache ([Res_line, Reservation])

    t_res_line_list = []
    delichr4:string = ""
    rmnopattern:string = ""
    c_room:string = ""
    res_line = kontline = guest = zimmer = reservation = None

    t_res_line = rbuff = None

    t_res_line_list, T_res_line = create_model_like(Res_line)

    Rbuff = create_buffer("Rbuff",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_line_list, delichr4, rmnopattern, c_room, res_line, kontline, guest, zimmer, reservation
        nonlocal case_type, resno, reslinno, resstat, actflag, rmno, arrive, depart, gastno, kontigno, kontcode
        nonlocal rbuff


        nonlocal t_res_line, rbuff
        nonlocal t_res_line_list

        return {"t-res-line": t_res_line_list}


    delichr4 = chr_unicode(4)

    if case_type == 1:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

            if length(t_res_line.bemerk) == 1:
                t_res_line.bemerk = ""

            if t_res_line.bemerk.lower()  == None or t_res_line.bemerk.lower()  == ("\\u0000").lower()  or t_res_line.bemerk.lower()  == chr_unicode(4):
                t_res_line.bemerk = ""

            elif matches(t_res_line.bemerk,r"*\\u0000*"):
                t_res_line.bemerk = replace_str(t_res_line.bemerk, "\\u0000", "")

            elif matches(t_res_line.bemerk,r"*" + chr_unicode(4) + r"*"):
                t_res_line.bemerk = replace_str(t_res_line.bemerk, chr_unicode(4) , "")
    elif case_type == 2:

        if kontigno > 0:

            res_line_obj_list = {}
            for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                     (Res_line.kontignr > 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag <= 2) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)


        elif kontigno < 0:

            res_line_obj_list = {}
            for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                     (Res_line.kontignr < 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag < 2) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)

    elif case_type == 3:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, actflag)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 4:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 5:

        if rmno != "":

            res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"resstatus": [(eq, resstat)],"zinr": [(eq, rmno)],"resnr": [(eq, resno)],"reslinnr": [(ne, reslinno)]})
        else:

            res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"resstatus": [(eq, resstat)],"resnr": [(eq, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 6:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(ne, reslinno)],"resstatus": [(eq, resstat)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 7:

        res_line = get_cache (Res_line, {"zinr": [(eq, rmno)],"active_flag": [(eq, actflag)],"resnr": [(ne, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 8:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(ne, reslinno)],"active_flag": [(le, actflag)],"zipreis": [(gt, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 9:

        res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"zinr": [(eq, rmno)],"ankunft": [(ge, arrive),(lt, depart)],"resnr": [(ne, resno)],"resstatus": [(ne, resstat)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 10:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= 1) & (Res_line.kontakt_nr == reslinno) & (Res_line.l_zuordnung[inc_value(2)] == 1)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 11:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 12:

        if rmno > "":

            res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(le, actflag)],"resstatus": [(ne, resstat)],"zinr": [(eq, rmno)],"l_zuordnung[2]": [(eq, 0)]})
        else:

            res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(le, actflag)],"resstatus": [(ne, resstat)],"l_zuordnung[2]": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 13:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 14:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnr == gastno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)

    elif case_type == 15:

        res_line = get_cache (Res_line, {"_recid": [(eq, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 16:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"active_flag": [(le, actflag)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 17:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= actflag) & ((Res_line.resstatus == 11) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 18:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnr == gastno) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():

            if res_line:
                t_res_line = T_res_line()
                t_res_line_list.append(t_res_line)

                buffer_copy(res_line, t_res_line)
    elif case_type == 19:

        res_line = get_cache (Res_line, {"active_flag": [(le, actflag)],"pin_code": [(eq, kontcode)]})
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)
    elif case_type == 20:

        res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"resstatus": [(eq, resstat)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 21:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(le, actflag)],"resstatus": [(ne, resstat)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 22:

        if actflag <= 1:

            res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(le, actflag)],"resstatus": [(ne, 8),(ne, 9),(ne, 10),(ne, 12)]})
        else:

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.active_flag == 2) & ((Res_line.resstatus == 8) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 23:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.gastnr == gastno) & (((Res_line.resstatus >= 1) & (Res_line.resstatus <= 4)) | (Res_line.resstatus == 11)) & (Res_line.zimmeranz > 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 24:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 25:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.pin_code == rmno) & (Res_line.resnr == resno) & (Res_line.reslinnr == reslinno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 26:

        res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"abreise": [(eq, arrive)],"zinr": [(eq, rmno)],"resstatus": [(ne, 12)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 27:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rmno)],"resstatus": [(eq, 1)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 28:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, rmno)],"resnr": [(ne, resno)],"reslinnr": [(ne, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 29:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"resstatus": [(le, 6)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 30:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"kontakt_nr": [(eq, reslinno)],"l_zuordnung[2]": [(eq, 1)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 31:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(ne, reslinno)],"resstatus": [(eq, 11)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 32:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr != resno) & (Res_line.zinr == rmno) & (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 33:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"zinr": [(eq, "")],"active_flag": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 34:

        res_line = get_cache (Res_line, {"resstatus": [(eq, 6)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 35:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 36:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.gastnr == gastno) & (((Res_line.resstatus >= 1) & (Res_line.resstatus <= 5)) | (Res_line.resstatus == 11)) & (Res_line.zimmeranz > 1)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 37:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, rmno)],"abreise": [(eq, arrive)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 38:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 6)],"zinr": [(eq, rmno)]})

        if not res_line and resstat == 13:

            res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 13)],"zinr": [(eq, rmno)],"l_zuordnung[2]": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 39:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 13)],"zinr": [(eq, rmno)],"l_zuordnung[2]": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 40:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, "")]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 41:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rmno)],"resstatus": [(eq, 13)],"abreise": [(gt, arrive)],"zipreis": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 42:

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr > 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag <= 2) & (Res_line.resstatus <= 6)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 43:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

        if not res_line:

            res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, 1)],"resstatus": [(eq, 13)],"l_zuordnung[2]": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 44:

        res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"zinr": [(eq, rmno)],"reslinnr": [(ne, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 45:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag == actflag) & (Res_line.l_zuordnung[inc_value(2)] == 1) & (Res_line.kontakt_nr == reslinno)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 46:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag <= actflag) & (((Res_line.ankunft == arrive)) | ((Res_line.abreise == arrive))) & (Res_line.zinr == rmno) & (Res_line.betrieb_gast > 0) & (Res_line.resnr != resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 47:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr != resno) & (Res_line.zinr == rmno) & (Res_line.active_flag <= actflag) & (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 48:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & ((Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & (Res_line.zinr == rmno) & (Res_line.betrieb_gast > 0)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 49:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag == actflag) & (Res_line.zinr != "") & (Res_line.betrieb_gast == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 50:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.kontakt_nr == reslinno) & (Res_line.l_zuordnung[inc_value(2)] == 1)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 51:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, 1)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 52:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"resstatus": [(ne, 9),(ne, 10)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 53:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 8))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 54:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(le, actflag)],"zipreis": [(gt, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 55:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.zinr == rmno) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.ankunft == arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 56:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.zinr == rmno)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 57:

        res_line = get_cache (Res_line, {"resstatus": [(eq, resstat)],"abreise": [(eq, arrive)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 58:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == resstat) & (Res_line.zinr == rmno) & (Res_line.abreise == arrive) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 59:

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr < 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag < actflag) & (Res_line.resstatus < resstat) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 60:

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr < 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag < actflag) & (Res_line.resstatus < resstat) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 61:

        res_line_obj_list = {}
        for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1)).filter(
                 (Res_line.kontignr != 0) & (Res_line.gastnr == gastno) & (Res_line.active_flag < actflag) & (Res_line.resstatus < resstat)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 62:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & ((Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 63:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr != reslinno) & (Res_line.resstatus == resstat) & ((Res_line.betrieb_gastpay <= 2) | (Res_line.betrieb_gastpay == 5))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 64:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr != reslinno) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 65:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= actflag) & ((Res_line.resstatus == 11) | (Res_line.resstatus == 13)) & ((Res_line.kontakt_nr == reslinno))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 66:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.gastnrmember == gastno) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 67:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr >= reslinno)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 68:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == actflag) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == depart)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 69:

        res_line = get_cache (Res_line, {"resnr": [(ne, resno)],"active_flag": [(eq, actflag)],"l_zuordnung[4]": [(eq, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 70:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 71:

        res_line = get_cache (Res_line, {"zinr": [(eq, rmno)],"resstatus": [(eq, resstat)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 72:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag <= actflag) & (((Res_line.ankunft >= arrive) & (Res_line.ankunft <= depart)) | ((Res_line.abreise >= arrive) & (Res_line.abreise <= depart)) | ((arrive >= Res_line.ankunft) & (arrive <= Res_line.abreise))) & (Res_line.zinr == rmno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 73:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.zinr == rmno) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.active_flag == actflag))).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 74:

        res_line = get_cache (Res_line, {"betriebsnr": [(eq, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 75:

        res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"zinr": [(eq, rmno)],"resstatus": [(ne, 12)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 76:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 77:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.l_zuordnung[inc_value(4)] == reslinno) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.resnr != resno)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 78:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & ((Res_line.active_flag == actflag) | (Res_line.resstatus == resstat))).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 79:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == arrive)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 80:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == actflag) & (Res_line.resstatus != resstat) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 81:

        res_line_obj_list = {}
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (get_month(Guest.geburtdatum1) == get_month(get_current_date())) & (get_day(Guest.geburtdatum1) == get_day(get_current_date()))).filter(
                 (Res_line.active_flag <= actflag) & (Res_line.resstatus != resstat)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 82:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == actflag) & (Res_line.resstatus == resstat)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 83:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, rmno)],"l_zuordnung[2]": [(eq, 0)],"resnr": [(ne, resno)],"reslinnr": [(ne, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 84:

        res_line = get_cache (Res_line, {"resnr": [(ne, resno)],"active_flag": [(eq, 1)],"l_zuordnung[1]": [(eq, 0)],"l_zuordnung[4]": [(eq, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 85:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, actflag)],"resstatus": [(ne, resstat)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 86:

        res_line = get_cache (Res_line, {"active_flag": [(eq, actflag)],"resstatus": [(eq, resstat)],"resnr": [(eq, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 87:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"resstatus": [(ge, 6),(le, 8)],"betriebsnr": [(ne, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 88:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"gastnrmember": [(eq, gastno)],"resstatus": [(ne, 9),(ne, 10),(ne, 12)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 89:

        res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resnr": [(ne, resno)],"resstatus": [(ne, 12)],"abreise": [(le, arrive)],"ankunft": [(gt, depart)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 90:

        res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"abreise": [(le, arrive)],"ankunft": [(gt, depart)],"zinr": [(eq, rmno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 91:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"resstatus": [(ge, 6),(le, 8)],"gratis": [(eq, 0)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 91:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= actflag)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 92:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rmno)],"resstatus": [(ne, 9),(ne, 10),(ne, 12)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 93:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if not res_line:

            if arrive > depart:

                res_line = get_cache (Res_line, {"zinr": [(eq, rmno)],"resstatus": [(ne, 12),(ne, 9),(ne, 10)],"ankunft": [(le, depart)],"abreise": [(gt, depart)]})
            else:

                res_line = get_cache (Res_line, {"zinr": [(eq, rmno)],"resstatus": [(ne, 12),(ne, 9),(ne, 10)],"ankunft": [(le, depart)],"abreise": [(ge, depart)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 94:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).order_by(Res_line._recid).all():
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 95:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if not res_line:

            res_line = get_cache (Res_line, {"zinr": [(eq, rmno)],"resstatus": [(ne, 12),(ne, 9),(ne, 10)],"active_flag": [(ge, 1),(le, 2)],"ankunft": [(le, arrive)],"abreise": [(gt, arrive)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 96:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (to_int(Res_line.code) == resno)).first()

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 99:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 100:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)]})

        if res_line:
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            buffer_copy(res_line, t_res_line)
    elif case_type == 101:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})

        if zimmer:

            rbuff = get_cache (Res_line, {"zinr": [(eq, rmno)],"active_flag": [(eq, 1)]})

            if rbuff:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == rbuff.resnr) & (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line.zinr, Res_line.resstatus).all():

                    t_res_line = query(t_res_line_list, filters=(lambda t_res_line: t_res_line.zinr == res_line.zinr), first=True)

                    if not t_res_line:
                        t_res_line = T_res_line()
                        t_res_line_list.append(t_res_line)

                        buffer_copy(res_line, t_res_line)

        else:
            rmnopattern = "*" + rmno + "*"

            reservation = db_session.query(Reservation).filter(
                     (Reservation.activeflag == 0) & (matches(Reservation.groupname,rmnopattern))).first()

            if reservation:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == reservation.resnr) & (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line.zinr, Res_line.resstatus).all():

                    t_res_line = query(t_res_line_list, filters=(lambda t_res_line: t_res_line.zinr == res_line.zinr), first=True)

                    if not t_res_line:
                        t_res_line = T_res_line()
                        t_res_line_list.append(t_res_line)

                        buffer_copy(res_line, t_res_line)

    return generate_output()