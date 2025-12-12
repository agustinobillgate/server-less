#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Bill, Gentable, Archieve, Fixleist, Reslin_queasy, Res_history, Mast_art, Reservation, Master

def mn_del_old_resbl():

    prepare_cache ([Htparam])

    i = 0
    j = 0
    k = 0
    ci_date:date = None
    htparam = res_line = bill = gentable = archieve = fixleist = reslin_queasy = res_history = mast_art = reservation = master = None

    reslist = None

    reslist_data, Reslist = create_model("Reslist", {"resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_data

        return {"i": i, "j": j, "k": k}

    def del_old_res():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_data

        anz:int = 0
        delete_it:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 162)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 8) | (Res_line.resstatus == 12)) & (Res_line.active_flag == 2) & (Res_line.abreise < (ci_date - timedelta(days=anz)))).with_for_update().first()
        while None != res_line:

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)],"flag": [(eq, 0)]})
            delete_it = not (None != bill)

            if delete_it:
                i = i + 1

                reslist = query(reslist_data, filters=(lambda reslist: reslist.resnr == res_line.resnr), first=True)

                if not reslist:
                    reslist = Reslist()
                    reslist_data.append(reslist)

                    reslist.resnr = res_line.resnr

                # gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})
                gentable = db_session.query(Gentable).filter(
                         (Gentable.key == ("reservation").lower()) & (Gentable.number1 == res_line.resnr) & (Gentable.number2 == res_line.reslinnr)).with_for_update().first()

                if gentable:
                    db_session.delete(gentable)

                # archieve = get_cache (Archieve, {"key": [(eq, "send-sign-rc")],"num1": [(eq, res_line.resnr)],"num2": [(eq, res_line.reslinnr)],"num3": [(eq, res_line.gastnrmember)]})
                archieve = db_session.query(Archieve).filter(
                         (Archieve.key == ("send-sign-rc").lower()) & (Archieve.num1 == res_line.resnr) & (Archieve.num2 == res_line.reslinnr) & (Archieve.num3 == res_line.gastnrmember)).with_for_update().first()

                if archieve:
                    db_session.delete(archieve)

                for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).with_for_update().all():
                    db_session.delete(fixleist)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():

                    # res_history = get_cache (Res_history, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"datum": [(eq, reslin_queasy.date2)],"zeit": [(eq, reslin_queasy.number2)]})
                    res_history = db_session.query(Res_history).filter(
                             (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr) & (Res_history.datum == reslin_queasy.date2) & (Res_history.zeit == reslin_queasy.number2)).with_for_update().first()

                    if res_history:
                        db_session.delete(res_history)
                    db_session.delete(reslin_queasy)

                for res_history in db_session.query(Res_history).filter(
                             (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr) & (Res_history.datum >= res_line.ankunft) & (Res_history.zeit >= 0)).order_by(Res_history._recid).with_for_update().all():
                    db_session.delete(res_history)

                # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"betriebsnr": [(eq, 0)]})
                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.betriebsnr == 0)).with_for_update().first()

                if reslin_queasy:
                    db_session.delete(reslin_queasy)

                for mast_art in db_session.query(Mast_art).filter(
                             (Mast_art.resnr == res_line.resnr) & (Mast_art.reslinnr == res_line.reslinnr)).order_by(Mast_art._recid).with_for_update().all():
                    db_session.delete(mast_art)

                for res_history in db_session.query(Res_history).filter(
                             (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr) & (Res_history.datum >= res_line.ankunft) & (Res_history.datum <= res_line.abreise) & (Res_history.zeit == 0) & (Res_history.action == ("N/A").lower())).order_by(Res_history._recid).with_for_update().all():
                    db_session.delete(res_history)
                pass
                db_session.delete(res_line)

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     ((Res_line.resstatus == 8) | (Res_line.resstatus == 12)) & (Res_line.active_flag == 2) & (Res_line.abreise < (ci_date - timedelta(days=anz))) & (Res_line._recid > curr_recid)).first()

        for reslist in query(reslist_data):

            res_line = get_cache (Res_line, {"resnr": [(eq, reslist.resnr)]})

            if not res_line:

                # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "rate-prog")],"number1": [(eq, reslist.resnr)],"number2": [(eq, 0)],"char1": [(eq, "")],"reslinnr": [(eq, 1)]})
                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("rate-prog").lower()) & (Reslin_queasy.number1 == reslist.resnr) & (Reslin_queasy.number2 == 0) & (Reslin_queasy.char1 == "") & (Reslin_queasy.reslinnr == 1)).with_for_update().first()

                if reslin_queasy:
                    db_session.delete(reslin_queasy)

                # reservation = get_cache (Reservation, {"resnr": [(eq, reslist.resnr)]})
                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == reslist.resnr)).with_for_update().first()
                db_session.delete(reservation)

                # master = get_cache (Master, {"resnr": [(eq, reslist.resnr)]})
                master = db_session.query(Master).filter(
                         (Master.resnr == reslist.resnr)).with_for_update().first()

                if master:
                    db_session.delete(master)
            reslist_data.remove(reslist)
        del_old_resline()
        del_mal_mainres()


    def del_old_resline():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_data

        anz:int = 0
        anz1:int = 0
        delete_it:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 260)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        res_line = db_session.query(Res_line).filter(
                 ((Res_line.resstatus == 10) | (Res_line.resstatus == 9) | (Res_line.resstatus == 99)) & (Res_line.active_flag == 2) & (Res_line.ankunft < (ci_date - timedelta(days=anz)))).first()
        while None != res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            delete_it = not (None != reservation and reservation.zahldatum != None)

            if delete_it:

                if res_line.resstatus == 10:
                    j = j + 1

                if res_line.resstatus == 9:
                    k = k + 1

                reslist = query(reslist_data, filters=(lambda reslist: reslist.resnr == res_line.resnr), first=True)

                if not reslist:
                    reslist = Reslist()
                    reslist_data.append(reslist)

                    reslist.resnr = res_line.resnr

                for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).with_for_update().all():
                    db_session.delete(fixleist)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():
                    db_session.delete(reslin_queasy)

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).with_for_update().all():
                    db_session.delete(reslin_queasy)
                pass
                db_session.delete(res_line)

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     ((Res_line.resstatus == 10) | (Res_line.resstatus == 9) | (Res_line.resstatus == 99)) & (Res_line.active_flag == 2) & (Res_line.ankunft < (ci_date - timedelta(days=anz))) & (Res_line._recid > curr_recid)).first()

        for reslist in query(reslist_data):

            res_line = get_cache (Res_line, {"resnr": [(eq, reslist.resnr)]})

            if not res_line:

                # reservation = get_cache (Reservation, {"resnr": [(eq, reslist.resnr)]})
                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == reslist.resnr)).with_for_update().first()
                db_session.delete(reservation)
            reslist_data.remove(reslist)


    def del_mal_mainres():

        nonlocal i, j, k, ci_date, htparam, res_line, bill, gentable, archieve, fixleist, reslin_queasy, res_history, mast_art, reservation, master


        nonlocal reslist
        nonlocal reslist_data

        # reservation = get_cache (Reservation, {"activeflag": [(eq, 0)]})
        reservation = db_session.query(Reservation).filter(
                 (Reservation.activeflag == 1)).with_for_update().first()
        while None != reservation:

            res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)]})

            if not res_line:
                pass
                db_session.delete(reservation)

            curr_recid = reservation._recid
            reservation = db_session.query(Reservation).filter(
                     (Reservation.activeflag == 0) & (Reservation._recid > curr_recid)).first()

        # reservation = get_cache (Reservation, {"activeflag": [(eq, 1)]})
        reservation = db_session.query(Reservation).filter((Reservation.activeflag == 1)).with_for_update().first()
        while None != reservation:

            res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)]})

            if not res_line:
                pass
                db_session.delete(reservation)

            curr_recid = reservation._recid
            reservation = db_session.query(Reservation).filter(
                     (Reservation.activeflag == 1) & (Reservation._recid > curr_recid)).first()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_res()

    return generate_output()