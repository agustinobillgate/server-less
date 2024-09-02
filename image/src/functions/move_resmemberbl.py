from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Htparam, Master, Bill, Reservation, Counters, Gentable, Reslin_queasy, Res_history, Fixleist

def move_resmemberbl(case_type:int, resno:int, sorttype:int, newresno:int, r_list:[R_list]):
    done = False
    ci_date:date = None
    res_line = htparam = master = bill = reservation = counters = gentable = reslin_queasy = res_history = fixleist = None

    r_list = rbuff = msbuff = mbill = mbuff = rline = mainres = None

    r_list_list, R_list = create_model_like(Res_line, {"select_flag":bool})

    Rbuff = R_list
    rbuff_list = r_list_list

    Msbuff = Master
    Mbill = Bill
    Mbuff = Reservation
    Rline = Res_line
    Mainres = Reservation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal rbuff, msbuff, mbill, mbuff, rline, mainres


        nonlocal r_list, rbuff, msbuff, mbill, mbuff, rline, mainres
        nonlocal r_list_list
        return {"done": done, "r-list": r_list_list}

    def mk_r_list():

        nonlocal done, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal rbuff, msbuff, mbill, mbuff, rline, mainres


        nonlocal r_list, rbuff, msbuff, mbill, mbuff, rline, mainres
        nonlocal r_list_list

        if sorttype == 1:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.resstatus <= 5)).all():
                r_list = R_list()
                r_list_list.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 2:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.resstatus == 6)).all():
                r_list = R_list()
                r_list_list.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 3:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.resstatus <= 5) &  (Res_line.ankunft == ci_date)).all():
                r_list = R_list()
                r_list_list.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 4:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 11) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 13)).all():
                r_list = R_list()
                r_list_list.append(r_list)

                buffer_copy(res_line, r_list)


    def update_it():

        nonlocal done, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal rbuff, msbuff, mbill, mbuff, rline, mainres


        nonlocal r_list, rbuff, msbuff, mbill, mbuff, rline, mainres
        nonlocal r_list_list


        Rbuff = R_list
        Msbuff = Master
        Mbill = Bill
        Mbuff = Reservation
        Rline = Res_line
        Mainres = Reservation

        if newresno == 0:

            mainres = db_session.query(Mainres).first()

            if not mainres:
                newresno = 1
            else:
                newresno = mainres.resnr + 1

        for rline in db_session.query(Rline).all():

            if newresno <= rline.resnr:
                newresno = rline.resnr + 1
            break

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()
        mbuff = Mbuff()
        db_session.add(mbuff)

        buffer_copy(reservation, mbuff,except_fields=["resnr","depositgef","limitdate","limitdate2","depositbez","depositbez2","zahldatum","zahldatum2","zahlkonto","zahlkonto2","bestat_datum"])
        mbuff.resnr = newresno

        mbuff = db_session.query(Mbuff).first()

        master = db_session.query(Master).filter(
                    (Master.resnr == resno)).first()

        if master:

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
            counters.counter = counters.counter + 1

            counters = db_session.query(Counters).first()
            msbuff = Msbuff()
            db_session.add(msbuff)

            buffer_copy(master, msbuff,except_fields=["resnr","rechnr"])
            msbuff.rechnr = counters.counter
            msbuff.resnr = newresno

            msbuff = db_session.query(Msbuff).first()

            bill = db_session.query(Bill).filter(
                        (Bill.resnr == resno) &  (Bill.reslinnr == 0)).first()

            if bill:
                mbill = Mbill()
                db_session.add(mbill)

                buffer_copy(bill, mbill,except_fields=["resnr","rechnr","saldo"])
                mbill.rechnr = counters.counter
                mbill.resnr = newresno
                mbill.saldo = 0

                mbill = db_session.query(Mbill).first()

        for rbuff in query(rbuff_list, filters=(lambda rbuff :rbuff.select_flag)):

            res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == rbuff.resnr) &  (Res_line.reslinnr == rbuff.reslinnr)).first()

            if res_line.resstatus == 6:

                for bill in db_session.query(Bill).filter(
                            (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).all():

                    rline = db_session.query(Rline).filter(
                                (Rline.resnr == bill.resnr) &  (Rline.reslinnr == bill.reslinnr) &  (Rline.resstatus == 12)).first()

                    if rline:
                        rline.resnr = newresno


                    bill.resnr = newresno

            gentable = db_session.query(Gentable).filter(
                        (func.lower(Gentable.key) == "reservation") &  (Gentable.number1 == res_line.resnr) &  (Gentable.number2 == res_line.reslinnr)).first()

            if gentable:
                gentable.number1 = newresno

            for rline in db_session.query(Rline).filter(
                        (Rline.resnr == rbuff.resnr) &  ((Rline.resstatus == 11) |  (Rline.resstatus == 13)) &  (Rline.kontakt_nr == res_line.reslinnr)).all():
                rline.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "resChanges") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                reslin_queasy.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                        (func.lower(Res_history.action) == "Remark") &  (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr)).all():
                res_history.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                        (func.lower(Res_history.action) == "Pickup") &  (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr)).all():
                res_history.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                        (func.lower(Res_history.action) == "Drop") &  (Res_history.resnr == res_line.resnr) &  (Res_history.reslinnr == res_line.reslinnr)).all():
                res_history.resnr = newresno

            for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                fixleist.resnr = newresno
            res_line.resnr = newresno

            res_line = db_session.query(Res_line).first()
        done = True


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if case_type == 1:
        mk_r_list()
    else:
        update_it()

    return generate_output()