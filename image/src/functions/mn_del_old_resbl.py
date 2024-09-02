from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Bill, Gentable, Archieve, Fixleist, Reslin_queasy, Res_history, Mast_art, Reservation, Master

def mn_del_old_resbl():
    i = 0
    j = 0
    k = 0
    ci_date:date = None
    htparam = res_line = bill = gentable = archieve = fixleist = reslin_queasy = res_history = mast_art = reservation = master = None

    reslist = None

    reslist_list, Reslist = create_model("Reslist", {"resnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_list
        return {"i": i, "j": j, "k": k}

    def del_old_res():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_list

        anz:int = 0
        delete_it:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 162)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        res_line = db_session.query(Res_line).filter(
                ((Res_line.resstatus == 8) |  (Res_line.resstatus == 12)) &  (Res_line.active_flag == 2) &  (Res_line.abreise < (ci_date - anz))).first()
        while None != res_line:

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == 0) &  (Bill.flag == 0)).first()
            delete_it = not (None != bill)

            if delete_it:
                i = i + 1

                reslist = query(reslist_list, filters=(lambda reslist :reslist.resnr == res_line.resnr), first=True)

                if not reslist:
                    reslist = Reslist()
                    reslist_list.append(reslist)

                    reslist.resnr = res_line.resnr

                gentable = db_session.query(Gentable).filter(
                            (func.lower(Gentable.key) == "reservation") &  (Gentable.number1 == res_line.resnr) &  (Gentable.number2 == res_line.reslinnr)).first()

                if gentable:
                    db_session.delete(gentable)

                archieve = db_session.query(Archieve).filter(
                            (func.lower(Archieve.key) == "send_sign_rc") &  (Archieve.num1 == res_line.resnr) &  (Archieve.num2 == res_line.reslinnr) &  (Archieve.num3 == res_line.gastnrmember)).first()

                if archieve:
                    db_session.delete(archieve)

                for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(fixleist)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "ResChanges") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():

                    res_history = db_session.query(Res_history).filter(
                                (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr) &  (Res_history.datum == reslin_queasy.date2) &  (Res_history.zeit == reslin_queasy.number2)).first()

                    if res_history:
                        db_session.delete(res_history)
                    db_session.delete(reslin_queasy)

                for res_history in db_session.query(Res_history).filter(
                            (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr) &  (Res_history.datum >= res_line.ankunft) &  (Res_history.zeit >= 0)).all():
                    db_session.delete(res_history)

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()

                if reslin_queasy:
                    db_session.delete(reslin_queasy)

                for mast_art in db_session.query(Mast_art).filter(
                            (Mast_art.resnr == res_line.resnr) &  (Mast_art.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(mast_art)

                for res_history in db_session.query(Res_history).filter(
                            (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr) &  (Res_history.datum >= res_line.ankunft) &  (Res_history.datum <= res_line.abreise) &  (Res_history.zeit == 0) &  (func.lower(Res_history.action) == "N/A")).all():
                    db_session.delete(res_history)

                res_line = db_session.query(Res_line).first()
                db_session.delete(res_line)


            res_line = db_session.query(Res_line).filter(
                    ((Res_line.resstatus == 8) |  (Res_line.resstatus == 12)) &  (Res_line.active_flag == 2) &  (Res_line.abreise < (ci_date - anz))).first()

        for reslist in query(reslist_list):

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslist.resnr)).first()

            if not res_line:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "rate_prog") &  (Reslin_queasy.number1 == reslist.resnr) &  (Reslin_queasy.number2 == 0) &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.reslinnr == 1)).first()

                if reslin_queasy:
                    db_session.delete(reslin_queasy)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == reslist.resnr)).first()
                db_session.delete(reservation)

                master = db_session.query(Master).filter(
                        (Master.resnr == reslist.resnr)).first()

                if master:
                    db_session.delete(master)
            reslist_list.remove(reslist)
        del_old_resline()
        del_mal_mainres()

    def del_old_resline():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_list

        anz:int = 0
        anz1:int = 0
        delete_it:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 260)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        res_line = db_session.query(Res_line).filter(
                ((Res_line.resstatus == 10) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 99)) &  (Res_line.active_flag == 2) &  (Res_line.ankunft < (ci_date - anz))).first()
        while None != res_line:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()
            delete_it = not (None != reservation and reservation.zahldatum != None)

            if delete_it:

                if res_line.resstatus == 10:
                    j = j + 1

                if res_line.resstatus == 9:
                    k = k + 1

                reslist = query(reslist_list, filters=(lambda reslist :reslist.resnr == res_line.resnr), first=True)

                if not reslist:
                    reslist = Reslist()
                    reslist_list.append(reslist)

                    reslist.resnr = res_line.resnr

                for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(fixleist)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "ResChanges") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    db_session.delete(reslin_queasy)

                res_line = db_session.query(Res_line).first()
                db_session.delete(res_line)


            res_line = db_session.query(Res_line).filter(
                    ((Res_line.resstatus == 10) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 99)) &  (Res_line.active_flag == 2) &  (Res_line.ankunft < (ci_date - anz))).first()

        for reslist in query(reslist_list):

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslist.resnr)).first()

            if not res_line:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == reslist.resnr)).first()
                db_session.delete(reservation)
            reslist_list.remove(reslist)

    def del_mal_mainres():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_list

        reservation = db_session.query(Reservation).filter(
                (Reservation.activeflag == 0)).first()
        while None != reservation:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reservation.resnr)).first()

            if not res_line:

                reservation = db_session.query(Reservation).first()
                db_session.delete(reservation)

            reservation = db_session.query(Reservation).filter(
                    (Reservation.activeflag == 0)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.activeflag == 1)).first()
        while None != reservation:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reservation.resnr)).first()

            if not res_line:

                reservation = db_session.query(Reservation).first()
                db_session.delete(reservation)

            reservation = db_session.query(Reservation).filter(
                    (Reservation.activeflag == 1)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_res()

    return generate_output()