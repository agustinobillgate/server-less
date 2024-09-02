from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Htparam, Zimkateg, Zimmer, Outorder, Zimplan

def res_czinrbl(pvilanguage:int, ankunft:date, abreise:date, sharer:bool, resnr:int, reslinnr:int, rmcat:str, zinr:str):
    error_code = 0
    msg_str = ""
    lvcarea:str = "res_czinr"
    found:bool = False
    answer:bool = False
    resline_recid:int = 0
    ci_date:date = None
    from_date:date = None
    to_date:date = None
    accept_it:bool = False
    res_line = htparam = zimkateg = zimmer = outorder = zimplan = None

    resline = zimplan1 = None

    Resline = Res_line
    Zimplan1 = Zimplan

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, accept_it, res_line, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal resline, zimplan1


        nonlocal resline, zimplan1
        return {"error_code": error_code, "msg_str": msg_str}

    def check_roomplan_old():

        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, accept_it, res_line, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal resline, zimplan1


        nonlocal resline, zimplan1

        datum:date = None
        res_recid:int = 0
        Resline = Res_line
        Zimplan1 = Zimplan

        if from_date == to_date:

            if res_line:

                resline = db_session.query(Resline).filter(
                        (Resline._recid != res_line._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag == 1) &  (Resline.ankunft <= to_date) &  (Resline.abreise > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                        (Resline.resstatus <= 6) &  (Resline.active_flag == 1) &  (Resline.ankunft <= to_date) &  (Resline.abreise > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

            if resline:
                error_code = -3

            return

        if res_line:

            if res_line.active_flag == 1:

                resline = db_session.query(Resline).filter(
                        (Resline._recid != res_line._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag <= 1) &  (Resline.abreise >= from_date) &  (Resline.abreise <= to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                        (Resline._recid != res_line._recid) &  (Resline.active_flag == 0) &  (Resline.abreise >= from_date) &  (Resline.abreise <= to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                            (Resline._recid != res_line._recid) &  (Resline.active_flag == 1) &  (Resline.abreise > from_date) &  (Resline.abreise <= to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()
        else:

            resline = db_session.query(Resline).filter(
                    (Resline.active_flag == 0) &  (Resline.abreise >= from_date) &  (Resline.abreise <= to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

            if not resline:

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 1) &  (Resline.abreise > from_date) &  (Resline.abreise <= to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

        if resline:
            error_code = -3

            return

        if res_line:

            resline = db_session.query(Resline).filter(
                    (Resline._recid != res_line._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag <= 1) &  (Resline.to_date > Resline.ankunft) &  (Resline.to_date <= Resline.abreise) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower())).first()
        else:

            resline = db_session.query(Resline).filter(
                    (Resline.resstatus <= 6) &  (Resline.active_flag <= 1) &  (Resline.to_date > Resline.ankunft) &  (Resline.to_date <= Resline.abreise) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

        if resline:
            error_code = -3

            return

    def check_roomplan():

        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, accept_it, res_line, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal resline, zimplan1


        nonlocal resline, zimplan1

        datum:date = None
        res_recid:int = 0
        Resline = Res_line
        Zimplan1 = Zimplan

        if from_date == to_date:

            if res_line:

                resline = db_session.query(Resline).filter(
                        (Resline._recid != res_line._recid) &  (Resline.resstatus <= 6) &  (Resline.active_flag == 1) &  (Resline.ankunft <= to_date) &  (Resline.abreise > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                        (Resline.resstatus <= 6) &  (Resline.active_flag == 1) &  (Resline.ankunft <= to_date) &  (Resline.abreise > to_date) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.l_zuordnung[2] == 0)).first()

            if resline:
                error_code = -3

            return

        if res_line:

            if res_line.active_flag == 0 or res_line.active_flag == 2:

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 1) &  (Resline.resstatus == 6) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.abreise > from_date)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                            (Resline.active_flag == 0) &  (Resline.resstatus <= 5) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.ankunft < to_date) &  (Resline.abreise > from_date) &  (Resline._recid != res_line._recid)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                            (Resline.active_flag == 0) &  (Resline.resstatus <= 5) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.from_date < Resline.abreise) &  (Resline.to_date > Resline.ankunft) &  (Resline._recid != res_line._recid)).first()

                if resline:
                    error_code = -3

            elif res_line.active_flag == 1:

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 1) &  (Resline.resstatus == 6) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline._recid != res_line._recid)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                            (Resline.active_flag == 0) &  (Resline.resstatus <= 5) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.ankunft < to_date)).first()

                if resline:
                    error_code = -3
        else:

            resline = db_session.query(Resline).filter(
                    (Resline.active_flag == 1) &  (Resline.resstatus == 6) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.abreise > from_date)).first()

            if not resline:

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 0) &  (Resline.resstatus <= 5) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.ankunft < to_date) &  (Resline.abreise > from_date)).first()

            if not resline:

                resline = db_session.query(Resline).filter(
                        (Resline.active_flag == 0) &  (Resline.resstatus <= 5) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.from_date < Resline.abreise) &  (Resline.to_date > Resline.ankunft)).first()

            if resline:
                error_code = -3


    if resnr > 0:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if res_line and res_line.active_flag == 1:
        from_date = ci_date
    else:
        from_date = ankunft
    to_date = abreise

    zimkateg = db_session.query(Zimkateg).filter(
            (func.lower(Zimkateg.kurzbez) == (rmcat).lower())).first()

    if not zimkateg:
        error_code = -7

        return generate_output()

    if sharer and res_line:

        resline = db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.reslinnr != reslinnr)).first()
        while None != resline and not found:

            if resline.ankunft <= ankunft and resline.abreise >= abreise:
                found = True

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()
                rmcat = zimkateg.kurzbez

                return generate_output()

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == resnr) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.reslinnr != reslinnr)).first()

        if not found and res_line.active_flag == 0:
            error_code = -1

            return generate_output()

        elif not found and res_line.active_flag == 1:

            resline = db_session.query(Resline).filter(
                    (Resline.resstatus == 6) &  (Resline.active_flag == 1) &  (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.abreise >= abreise) &  (Resline.zikatnr == zimkateg.zikatnr)).first()

            if resline:
                found = True
            else:
                error_code = -1

            return generate_output()

    elif res_line and res_line.(zinr).lower().lower()  != (zinr).lower()  and (res_line.resstatus <= 2 or res_line.resstatus == 5):

        resline = db_session.query(Resline).filter(
                (Resline.resnr == resnr) &  (Resline.resstatus == 13) &  (Resline.zinr == res_line.zinr)).first()

        if resline:
            error_code = -6

            return generate_output()

    if zinr == "":

        return generate_output()

    zimmer = db_session.query(Zimmer).filter(
            (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

    if not zimmer:
        error_code = -1

        return generate_output()

    if res_line and res_line.active_flag == 1 and not sharer and abreise == ci_date:

        resline = db_session.query(Resline).filter(
                (func.lower(Resline.(zinr).lower()) == (zinr).lower()) &  (Resline.resstatus == 6) &  (Resline._recid != res_line._recid)).first()

        if resline:
            error_code = -3

            return generate_output()

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.zikatnr == zimmer.zikatnr)).first()

    if zimkateg.kurzbez.lower()  != (rmcat).lower() :
        msg_str = "&W" + translateExtended ("Room Type changed to", lvcarea, "") + " " + zimkateg.kurzbez + "." + chr(10)

    if resnr > 0:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr != resnr) &  (not Outorder.to_date <= Outorder.gespstart) &  (not Outorder.from_date > Outorder.gespende)).first()
    else:

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == zimmer.zinr) &  (not Outorder.to_date <= Outorder.gespstart) &  (not Outorder.from_date > Outorder.gespende)).first()

    if outorder:

        if outorder.betriebsnr <= 1:
            error_code = -2
        else:
            error_code = -5

        return generate_output()
    check_roomplan()

    if error_code != 0:

        return generate_output()

    if res_line and ((res_line.active_flag == 0 and res_line.ankunft == ci_date) or res_line.active_flag == 1) and zimmer.zistatus >= 1 and zimmer.zistatus <= 2:

        if res_line.active_flag == 1:
            error_code = -4

            return generate_output()

    if error_code == 0:
        rmcat = zimkateg.kurzbez

    return generate_output()