#using conversion tools version: 1.0.0.119

# =============================
# Rulita, 03-11-2025 | 36D1D2
# - New compile program 
# =============================
# Rd, 26/11/2025, with_for_update
#------------------------------

# ==============================================
# Rulita, 04-12-2025
# Fixing input param var typo anknuft -> ankuft
# Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Queasy, Htparam, Zimkateg, Zimmer, Outorder, Zimplan

def res_czinrbl(pvilanguage:int, ankuft:date, abreise:date, sharer:bool, resnr:int, reslinnr:int, rmcat:string, zinr:string):

    prepare_cache ([Queasy, Htparam, Zimkateg, Zimmer, Outorder])

    error_code = 0
    msg_str = ""
    lvcarea:string = "res-czinr"
    found:bool = False
    answer:bool = False
    resline_recid:int = 0
    ci_date:date = None
    from_date:date = None
    to_date:date = None
    count_q359:int = 0
    timestamp_str:string = ""
    accept_it:bool = False
    res_line = queasy = htparam = zimkateg = zimmer = outorder = zimplan = None

    resline = buf_q359 = None

    Resline = create_buffer("Resline",Res_line)
    Buf_q359 = create_buffer("Buf_q359",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, count_q359, timestamp_str, accept_it, res_line, queasy, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal pvilanguage, ankuft, abreise, sharer, resnr, reslinnr, rmcat, zinr
        nonlocal resline, buf_q359


        nonlocal resline, buf_q359

        return {"rmcat": rmcat, "error_code": error_code, "msg_str": msg_str}


    def check_roomplan_old():

        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, count_q359, timestamp_str, accept_it, res_line, queasy, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal pvilanguage, ankuft, abreise, sharer, resnr, reslinnr, rmcat, zinr
        nonlocal resline, buf_q359


        nonlocal resline, buf_q359

        resline = None
        zimplan1 = None
        datum:date = None
        res_recid:int = 0
        Resline =  create_buffer("Resline",Res_line)
        Zimplan1 =  create_buffer("Zimplan1",Zimplan)

        if from_date == to_date:

            if res_line:

                resline = db_session.query(Resline).filter(
                         (Resline._recid != res_line._recid) & (Resline.resstatus <= 6) & (Resline.active_flag == 1) & (Resline.ankunft <= to_date) & (Resline.abreise > to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                         (Resline.resstatus <= 6) & (Resline.active_flag == 1) & (Resline.ankunft <= to_date) & (Resline.abreise > to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

            if resline:
                error_code = -3

            return

        if res_line:

            if res_line.active_flag == 1:

                resline = db_session.query(Resline).filter(
                         (Resline._recid != res_line._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (Resline.abreise >= from_date) & (Resline.abreise <= to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                         (Resline._recid != res_line._recid) & (Resline.active_flag == 0) & (Resline.abreise >= from_date) & (Resline.abreise <= to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline._recid != res_line._recid) & (Resline.active_flag == 1) & (Resline.abreise > from_date) & (Resline.abreise <= to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
                else:

                    resline = db_session.query(Resline).filter(
                            (Resline.active_flag == 0) & (Resline.abreise >= from_date) & (Resline.abreise <= to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 1) & (Resline.abreise > from_date) & (Resline.abreise <= to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

        if resline:
            error_code = -3

            return

        if res_line:

            resline = db_session.query(Resline).filter(
                     (Resline._recid != res_line._recid) & (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (to_date > Resline.ankunft) & (to_date <= Resline.abreise) & (Resline.zinr == (zinr).lower())).first()
        else:

            resline = db_session.query(Resline).filter(
                        (Resline.resstatus <= 6) & (Resline.active_flag <= 1) & (to_date > Resline.ankunft) & (to_date <= Resline.abreise) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

        if resline:
            error_code = -3

            return


    def check_roomplan():

        nonlocal error_code, msg_str, lvcarea, found, answer, resline_recid, ci_date, from_date, to_date, count_q359, timestamp_str, accept_it, res_line, queasy, htparam, zimkateg, zimmer, outorder, zimplan
        nonlocal pvilanguage, ankuft, abreise, sharer, resnr, reslinnr, rmcat, zinr
        nonlocal resline, buf_q359


        nonlocal resline, buf_q359

        resline = None
        zimplan1 = None
        datum:date = None
        res_recid:int = 0
        Resline =  create_buffer("Resline",Res_line)
        Zimplan1 =  create_buffer("Zimplan1",Zimplan)

        if from_date == to_date:

            if res_line:

                resline = db_session.query(Resline).filter(
                         (Resline._recid != res_line._recid) & (Resline.resstatus <= 6) & (Resline.active_flag == 1) & (Resline.ankunft <= to_date) & (Resline.abreise > to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
            else:

                resline = db_session.query(Resline).filter(
                         (Resline.resstatus <= 6) & (Resline.active_flag == 1) & (Resline.ankunft <= to_date) & (Resline.abreise > to_date) & (Resline.zinr == (zinr).lower()) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()

            if resline:
                error_code = -3

            return

        if res_line:

            if res_line.active_flag == 0 or res_line.active_flag == 2:

                resline = db_session.query(Resline).filter(
                         (Resline.active_flag == 1) & (Resline.resstatus == 6) & (Resline.zinr == (zinr).lower()) & (Resline.abreise > from_date)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 0) & (Resline.resstatus <= 5) & (Resline.zinr == (zinr).lower()) & (Resline.ankunft < to_date) & (Resline.abreise > from_date) & (Resline._recid != res_line._recid)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 0) & (Resline.resstatus <= 5) & (Resline.zinr == (zinr).lower()) & (Resline.abreise > from_date) & (Resline.ankunft < to_date) & (Resline._recid != res_line._recid)).first()

                if resline:
                    error_code = -3

            elif res_line.active_flag == 1:

                resline = db_session.query(Resline).filter(
                         (Resline.active_flag == 1) & (Resline.resstatus == 6) & (Resline.zinr == (zinr).lower()) & (Resline._recid != res_line._recid)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 0) & (Resline.resstatus <= 5) & (Resline.zinr == (zinr).lower()) & (Resline.ankunft < to_date)).first()

                if resline:
                    error_code = -3
            else:

                resline = db_session.query(Resline).filter(
                         (Resline.active_flag == 1) & (Resline.resstatus == 6) & (Resline.zinr == (zinr).lower()) & (Resline.abreise > from_date)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 0) & (Resline.resstatus <= 5) & (Resline.zinr == (zinr).lower()) & (Resline.ankunft < to_date) & (Resline.abreise > from_date)).first()

                if not resline:

                    resline = db_session.query(Resline).filter(
                             (Resline.active_flag == 0) & (Resline.resstatus <= 5) & (Resline.zinr == (zinr).lower()) & (Resline.abreise > from_date) & (Resline.ankunft < to_date)).first()

                if resline:
                    error_code = -3

    if resnr > 0:

        # res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    # htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if res_line and res_line.active_flag == 1:
        from_date = ci_date
    else:
        from_date = ankuft

    to_date = abreise

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 359) & (Queasy.number3 == 1) & (Queasy.char1 == (zinr).lower())).order_by(Queasy.char3).all():
        count_q359 = count_q359 + 1

    if count_q359 > 1:

        # buf_q359 = get_cache (Queasy, {"number3": [(eq, 1)],"number1": [(eq, resnr)],"number2": [(eq, reslinnr)],"char1": [(eq, zinr)]})
        buf_q359 = db_session.query(Queasy).filter(
                 (Queasy.number3 == 1) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr) & (Queasy.char1 == (zinr).lower())).first()

        if buf_q359:
            timestamp_str = buf_q359.char3

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 359) & (Queasy.number3 == 1) & ((Queasy.number1 != resnr) | (Queasy.number2 != reslinnr)) & (Queasy.char1 == (zinr).lower()) & not_ (Queasy.date2 <= ankuft) & not_ (Queasy.date1 >= abreise)).order_by(Queasy.char3.desc()).all():

            if queasy.char3.lower()  > (timestamp_str).lower() :
                error_code = -8
                msg_str = translateExtended ("This room is currently locked for Reservation Number: ", lvcarea, "") + to_string(queasy.number1) + "/" + to_string(queasy.number2, "999") + translateExtended (" - By User: ", lvcarea, "") + queasy.char2 + chr_unicode(10) + translateExtended ("Please select another room.", lvcarea, "")

                return generate_output()

    # zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmcat)]})
    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.kurzbez == (rmcat).lower())).first()

    if not zimkateg:
        error_code = -7

        return generate_output()

    if sharer and res_line:

        resline = db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.zinr == (zinr).lower()) & (Resline.reslinnr != reslinnr)).first()
        while None != resline and not found:

            if resline.ankunft <= ankuft and resline.abreise >= abreise:
                found = True

                # zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})
                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zinr == (zinr).lower())).first()

                # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.zikatnr == zimmer.zikatnr)).first()
                
                rmcat = zimkateg.kurzbez

                return generate_output()

            curr_recid = resline._recid
            resline = db_session.query(Resline).filter(
                     (Resline.resnr == resnr) & (Resline.zinr == (zinr).lower()) & (Resline.reslinnr != reslinnr) & (Resline._recid > curr_recid)).first()

        if not found and res_line.active_flag == 0:
            error_code = -1

            return generate_output()

        elif not found and res_line.active_flag == 1:

            resline = db_session.query(Resline).filter(
                     (Resline.resstatus == 6) & (Resline.active_flag == 1) & (Resline.zinr == (zinr).lower()) & (Resline.abreise >= abreise) & (Resline.zikatnr == zimkateg.zikatnr)).first()

            if resline:
                found = True
            else:
                error_code = -1

            return generate_output()

    elif res_line and res_line.zinr.lower()  != (zinr).lower()  and (res_line.resstatus <= 2 or res_line.resstatus == 5):

        resline = db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.resstatus == 13) & (Resline.zinr == res_line.zinr)).first()

        if resline:
            error_code = -6

            return generate_output()

    if zinr == "":

        return generate_output()

    # zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})
    zimmer = db_session.query(Zimmer).filter(
             (Zimmer.zinr == (zinr).lower())).first()

    if not zimmer:
        error_code = -1

        return generate_output()

    if res_line and res_line.active_flag == 1 and not sharer and abreise == ci_date:

        resline = db_session.query(Resline).filter(
                 (Resline.zinr == (zinr).lower()) & (Resline.resstatus == 6) & (Resline._recid != res_line._recid)).first()

        if resline:
            error_code = -3

            return generate_output()

    # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == zimmer.zikatnr)).first()

    if zimkateg.kurzbez.lower()  != (rmcat).lower() :
        msg_str = "&W" + translateExtended ("Room Type changed to", lvcarea, "") + " " + zimkateg.kurzbez + "." + chr_unicode(10)

    if resnr > 0:
        # outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(ne, resnr)],"gespstart": [(ge, to_date)],"gespende": [(lt, from_date)]})
        outorder = db_session.query(Outorder).filter(
                 (Outorder.zinr == zimmer.zinr) & (Outorder.betriebsnr != resnr) & (Outorder.gespstart >= to_date) & (Outorder.gespende < from_date)).first()
    else:

        # outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(ge, to_date)],"gespende": [(lt, from_date)]})
        outorder = db_session.query(Outorder).filter(
                 (Outorder.zinr == zimmer.zinr) & (Outorder.gespstart >= to_date) & (Outorder.gespende < from_date)).first()

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

    # queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, resnr)],"number2": [(eq, reslinnr)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 359) & (Queasy.number3 == 1) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr)).with_for_update().first()

    if queasy:
        db_session.refresh(queasy,with_for_update=True)
        db_session.delete(queasy)
        db_session.flush()
        pass

    return generate_output()