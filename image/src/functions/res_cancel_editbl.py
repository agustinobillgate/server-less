from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Reservation, Fixleist, Reslin_queasy

def res_cancel_editbl(res_mode:str, done:bool, inp_resno:int, tot_qty:int, reslinno:int, grpflag:bool):
    successflag = False
    delete_it:bool = False
    gastno:int = 0
    res_line = reservation = fixleist = reslin_queasy = None

    rline = None

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, delete_it, gastno, res_line, reservation, fixleist, reslin_queasy
        nonlocal rline


        nonlocal rline
        return {"successflag": successflag}

    def cancel_edit():

        nonlocal successflag, delete_it, gastno, res_line, reservation, fixleist, reslin_queasy
        nonlocal rline


        nonlocal rline

        if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci") and not done:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == inp_resno) &  (Res_line.reslinnr != reslinno)).first()

            if not res_line:

                rline = db_session.query(Rline).filter(
                        (Rline.resnr == inp_resno) &  (Rline.reslinnr == reslinno)).first()
                gastno = rline.gastnr


                db_session.delete(rline)


                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == inp_resno)).first()
                db_session.delete(reservation)

                delete_it = True

        if res_mode.lower()  == "new" or res_mode.lower()  == "insert":

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == inp_resno) &  (Res_line.reslinnr == reslinno)).first()

            if res_line:
                gastno = res_line.gastnr


                db_session.delete(res_line)

                delete_it = True

        if delete_it:

            for fixleist in db_session.query(Fixleist).filter(
                    (Fixleist.resnr == inp_resno) &  (Fixleist.reslinnr == reslinno)).all():
                db_session.delete(fixleist)

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == inp_resno) &  (Reslin_queasy.reslinnr == reslinno)).first()
            while None != reslin_queasy:

                reslin_queasy = db_session.query(Reslin_queasy).first()
                db_session.delete(reslin_queasy)

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == inp_resno) &  (Reslin_queasy.reslinnr == reslinno)).first()

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == inp_resno) &  (Reslin_queasy.reslinnr == reslinno)).all():
                db_session.delete(reslin_queasy)

            if res_mode.lower()  == "new" or res_mode.lower()  == "qci":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "rate_prog") &  (Reslin_queasy.number1 == inp_resno) &  (Reslin_queasy.number2 == 0) &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.reslinnr == 1)).first()

                if reslin_queasy:
                    db_session.delete(reslin_queasy)
            reslinno = reslinno - 1

    cancel_edit()

    if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci") and done and (tot_qty > 1):

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resno) &  (Res_line.gastnr == gastno)).all():
            res_line.grpflag = True


    if tot_qty > 1:
        grpflag = True
    successflag = True

    return generate_output()