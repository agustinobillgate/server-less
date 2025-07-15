#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Outorder, Zimkateg, Queasy, Htparam, Res_line, Res_history, Zimmer, Bediener

t_outorder_data, T_outorder = create_model_like(Outorder)

def hk_ooo1bl(case_type:int, t_outorder_data:[T_outorder], from_date:date, to_date:date, service_flag:bool, zinr:string, user_nr:int, reason:string, dept:int, user_init:string):

    prepare_cache ([Zimkateg, Queasy, Htparam, Res_line, Res_history, Zimmer, Bediener])

    msg_int = 0
    resno = 0
    resname = ""
    ankunft = None
    abreise = None
    ooo_list_ind = 0
    cat_flag:bool = False
    roomnr:int = 0
    datum:date = None
    do_it:bool = True
    i:int = 0
    zistatus:int = 0
    ci_date:date = None
    outorder = zimkateg = queasy = htparam = res_line = res_history = zimmer = bediener = None

    t_outorder = zbuff = qsy = obuff = None

    Zbuff = create_buffer("Zbuff",Zimkateg)
    Qsy = create_buffer("Qsy",Queasy)
    Obuff = create_buffer("Obuff",Outorder)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_int, resno, resname, ankunft, abreise, ooo_list_ind, cat_flag, roomnr, datum, do_it, i, zistatus, ci_date, outorder, zimkateg, queasy, htparam, res_line, res_history, zimmer, bediener
        nonlocal case_type, from_date, to_date, service_flag, zinr, user_nr, reason, dept, user_init
        nonlocal zbuff, qsy, obuff


        nonlocal t_outorder, zbuff, qsy, obuff

        return {"msg_int": msg_int, "resno": resno, "resname": resname, "ankunft": ankunft, "abreise": abreise, "ooo_list_ind": ooo_list_ind}

    def chg_ooo():

        nonlocal msg_int, resno, resname, ankunft, abreise, ooo_list_ind, cat_flag, roomnr, datum, do_it, i, zistatus, ci_date, outorder, zimkateg, queasy, htparam, res_line, res_history, zimmer, bediener
        nonlocal case_type, from_date, to_date, service_flag, zinr, user_nr, reason, dept, user_init
        nonlocal zbuff, qsy, obuff


        nonlocal t_outorder, zbuff, qsy, obuff

        t_outorder = query(t_outorder_data, first=True)

        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 1) | (Res_line.resstatus == 2)) & (((Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)) | (((Res_line.abreise - 1) >= from_date) & (Res_line.abreise <= to_date)) | ((from_date >= Res_line.ankunft) & (from_date <= (Res_line.abreise - 1)))) & (Res_line.zinr == (zinr).lower())).first()

        if res_line:
            resno = res_line.resnr
            resname = res_line.name
            ankunft = res_line.ankunft
            abreise = res_line.abreise


            msg_int = 1

            return

        if from_date != to_date and service_flag:
            msg_int = 2

            return

        obuff = db_session.query(Obuff).filter(
                 (Obuff.zinr == t_outorder.zinr) & not_ (Obuff.gespstart > to_date) & not_ (Obuff.gespende < from_date) & ((Obuff.zinr != t_outorder.zinr) & (Obuff.gespstart != t_outorder.gespstart))).first()

        if obuff:
            msg_int = 3

            return

        if not service_flag and ((t_outorder.gespstart != from_date) or (t_outorder.gespende != to_date)):
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = user_nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "O-O-O Room " + zinr +\
                    " " + to_string(t_outorder.gespstart) +\
                    "-" + to_string(t_outorder.gespende) +\
                    " Changed To " + to_string(from_date) + "-" + to_string(to_date)
            res_history.action = "HouseKeeping"


            pass
            pass

        outorder = get_cache (Outorder, {"zinr": [(eq, t_outorder.zinr)],"betriebsnr": [(eq, t_outorder.betriebsnr)],"gespstart": [(eq, t_outorder.gespstart)],"gespende": [(eq, t_outorder.gespende)]})
        outorder.gespstart = from_date
        outorder.gespende = to_date
        outorder.gespgrund = reason + "$" + user_init


        outorder.betriebsnr = dept

        if service_flag:
            outorder.betriebsnr = outorder.betriebsnr + 3

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr
        for datum in date_range(outorder.gespstart,outorder.gespende) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")],"logi1": [(eq, False)],"logi2": [(eq, False)]})

            if queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass
        for datum in date_range(from_date,to_date) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")],"logi1": [(eq, False)],"logi2": [(eq, False)]})

            if queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Change to OOO - Room : " + zimmer.zinr
        res_history.action = "Log Availability"


        pass
        pass
        zimmer.bediener_nr_stat = user_nr

        if ci_date >= from_date and ci_date <= to_date:
            zistatus = 6


        else:
            zistatus = 2

        if zistatus == 0 or zistatus == 1 or zistatus == 2:

            res_line = get_cache (Res_line, {"zinr": [(eq, zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

            if res_line:

                if res_line.abreise == ci_date:
                    zimmer.zistatus = 3
                else:

                    if zimmer.zistatus == 4:
                        zimmer.zistatus = 4
                    else:
                        zimmer.zistatus = 5
                zimmer.bediener_nr_stat = 0
            else:

                if zimmer and zimmer.sleeping:
                    zimmer.zistatus = 2

        elif zistatus == 3:

            res_line = get_cache (Res_line, {"zinr": [(eq, zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

            if res_line and res_line.abreise > ci_date:
                zimmer.zistatus = 5
                zimmer.bediener_nr_stat = 0

            elif not res_line:
                zimmer.zistatus = 1
                zimmer.bediener_nr_stat = 0

        elif zistatus == 4 or zistatus == 5:

            res_line = get_cache (Res_line, {"zinr": [(eq, zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

            if res_line and res_line.abreise == ci_date:
                zimmer.zistatus = 3
                zimmer.bediener_nr_stat = 0

            elif not res_line:
                zimmer.zistatus = 1
                zimmer.bediener_nr_stat = 0

        if zistatus == 6:

            res_line = db_session.query(Res_line).filter(
                     (Res_line.zinr == (zinr).lower()) & (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

            if res_line:

                if res_line.abreise == ci_date:
                    zimmer.zistatus = 3
                else:
                    zimmer.zistatus = 5
                zimmer.bediener_nr_stat = 0

                obuff = db_session.query(Obuff).filter(
                         (Obuff.zinr == (zinr).lower()) & (Obuff.gespstart < res_line.abreise)).first()

                if obuff:
                    db_session.delete(obuff)
            else:

                obuff = db_session.query(Obuff).filter(
                         (Obuff.zinr == (zinr).lower()) & (Obuff.gespstart <= ci_date) & (Obuff.gespende >= ci_date)).first()

                if not obuff:
                    zimmer.bediener_nr_stat = 0
                    zimmer.zistatus = 2


                else:

                    if zimmer and zimmer.sleeping:
                        zimmer.zistatus = 6
        pass
        pass

        zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})
        ooo_list_ind = outorder.betriebsnr + 1

        if (ooo_list_ind + 1) >= 6:
            ooo_list_ind = 3


    def chg_om():

        nonlocal msg_int, resno, resname, ankunft, abreise, ooo_list_ind, cat_flag, roomnr, datum, do_it, i, zistatus, ci_date, outorder, zimkateg, queasy, htparam, res_line, res_history, zimmer, bediener
        nonlocal case_type, from_date, to_date, service_flag, zinr, user_nr, reason, dept, user_init
        nonlocal zbuff, qsy, obuff


        nonlocal t_outorder, zbuff, qsy, obuff

        t_outorder = query(t_outorder_data, first=True)

        if t_outorder.betriebsnr > 2:

            res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resnr": [(ne, t_outorder.betriebsnr)],"resstatus": [(ne, 12)],"abreise": [(le, from_date)],"ankunft": [(gt, to_date)],"zinr": [(eq, zinr)]})
        else:

            res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"abreise": [(le, from_date)],"ankunft": [(gt, to_date)],"zinr": [(eq, zinr)]})

        if res_line:
            do_it = False
            resno = res_line.resnr
            resname = res_line.name
            ankunft = res_line.ankunft
            abreise = res_line.abreise
            msg_int = 1

            return

        if do_it:

            obuff = db_session.query(Obuff).filter(
                     (Obuff.zinr == outorder.zinr) & not_ (Obuff.gespstart > to_date) & not_ (Obuff.gespende < from_date) & (Obuff._recid != outorder._recid)).first()

            if obuff:
                msg_int = 2
                do_it = False

        if do_it:

            outorder = get_cache (Outorder, {"zinr": [(eq, t_outorder.zinr)]})


            outorder.gespstart = from_date
            outorder.gespende = to_date
            outorder.gespgrund = reason + "$" + user_init

            zimmer = get_cache (Zimmer, {"zinr": [(eq, t_outorder.zinr)]})
            zimmer.bediener_nr_stat = user_nr
            pass
            pass
        else:
            msg_int = 3


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if case_type == 1:
        chg_ooo()

    elif case_type == 2:
        chg_om()

    return generate_output()