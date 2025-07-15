#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Htparam, Master, Bill, Reservation, Counters, Gentable, Reslin_queasy, Res_history, Fixleist

r_list_data, R_list = create_model_like(Res_line, {"select_flag":bool})

def move_resmemberbl(case_type:int, resno:int, sorttype:int, newresno:int, r_list_data:[R_list]):

    prepare_cache ([Res_line, Htparam, Master, Bill, Reservation, Counters, Gentable, Reslin_queasy, Res_history, Fixleist])

    done = False
    r_list_data = []
    ci_date:date = None
    res_line = htparam = master = bill = reservation = counters = gentable = reslin_queasy = res_history = fixleist = None

    r_list = rbuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, r_list_data, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal case_type, resno, sorttype, newresno


        nonlocal r_list, rbuff

        return {"done": done, "r-list": r_list_data}

    def mk_r_list():

        nonlocal done, r_list_data, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal case_type, resno, sorttype, newresno


        nonlocal r_list, rbuff

        if sorttype == 1:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.resstatus <= 5)).order_by(Res_line._recid).all():
                r_list = R_list()
                r_list_data.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 2:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.resstatus == 6)).order_by(Res_line._recid).all():
                r_list = R_list()
                r_list_data.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 3:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.resstatus <= 5) & (Res_line.ankunft == ci_date)).order_by(Res_line._recid).all():
                r_list = R_list()
                r_list_data.append(r_list)

                buffer_copy(res_line, r_list)


        elif sorttype == 4:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13)).order_by(Res_line._recid).all():
                r_list = R_list()
                r_list_data.append(r_list)

                buffer_copy(res_line, r_list)

    def update_it():

        nonlocal done, r_list_data, ci_date, res_line, htparam, master, bill, reservation, counters, gentable, reslin_queasy, res_history, fixleist
        nonlocal case_type, resno, sorttype, newresno


        nonlocal r_list, rbuff

        msbuff = None
        mbill = None
        mbuff = None
        rline = None
        mainres = None
        Rbuff = R_list
        rbuff_data = r_list_data
        Msbuff =  create_buffer("Msbuff",Master)
        Mbill =  create_buffer("Mbill",Bill)
        Mbuff =  create_buffer("Mbuff",Reservation)
        Rline =  create_buffer("Rline",Res_line)
        Mainres =  create_buffer("Mainres",Reservation)

        if newresno == 0:

            mainres = db_session.query(Mainres).first()

            if not mainres:
                newresno = 1
            else:
                newresno = mainres.resnr + 1

        for rline in db_session.query(Rline).order_by(Rline.resnr.desc()).yield_per(100):

            if newresno <= rline.resnr:
                newresno = rline.resnr + 1
            break

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
        mbuff = Reservation()
        db_session.add(mbuff)

        buffer_copy(reservation, mbuff,except_fields=["resnr","depositgef","limitdate","limitdate2","depositbez","depositbez2","zahldatum","zahldatum2","zahlkonto","zahlkonto2","bestat_datum"])
        mbuff.resnr = newresno


        pass

        master = get_cache (Master, {"resnr": [(eq, resno)]})

        if master:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            pass
            msbuff = Master()
            db_session.add(msbuff)

            buffer_copy(master, msbuff,except_fields=["resnr","rechnr"])
            msbuff.rechnr = counters.counter
            msbuff.resnr = newresno


            pass

            bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, 0)]})

            if bill:
                mbill = Bill()
                db_session.add(mbill)

                buffer_copy(bill, mbill,except_fields=["resnr","rechnr","saldo"])
                mbill.rechnr = counters.counter
                mbill.resnr = newresno
                mbill.saldo =  to_decimal("0")


                pass

        for rbuff in query(rbuff_data, filters=(lambda rbuff: rbuff.select_flag)):

            res_line = get_cache (Res_line, {"resnr": [(eq, rbuff.resnr)],"reslinnr": [(eq, rbuff.reslinnr)]})

            if res_line.resstatus == 6:

                for bill in db_session.query(Bill).filter(
                             (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr)).order_by(Bill._recid).all():

                    rline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)],"resstatus": [(eq, 12)]})

                    if rline:
                        rline.resnr = newresno


                    bill.resnr = newresno

            gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

            if gentable:
                gentable.number1 = newresno

            for rline in db_session.query(Rline).filter(
                         (Rline.resnr == rbuff.resnr) & ((Rline.resstatus == 11) | (Rline.resstatus == 13)) & (Rline.kontakt_nr == res_line.reslinnr)).order_by(Rline._recid).all():
                rline.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("resChanges").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                reslin_queasy.resnr = newresno

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                reslin_queasy.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                         (Res_history.action == ("Remark").lower()) & (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr)).order_by(Res_history._recid).all():
                res_history.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                         (Res_history.action == ("Pickup").lower()) & (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr)).order_by(Res_history._recid).all():
                res_history.resnr = newresno

            for res_history in db_session.query(Res_history).filter(
                         (Res_history.action == ("Drop").lower()) & (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr)).order_by(Res_history._recid).all():
                res_history.resnr = newresno

            for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                fixleist.resnr = newresno
            res_line.resnr = newresno


            pass
        done = True


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if case_type == 1:
        mk_r_list()
    else:
        update_it()

    return generate_output()