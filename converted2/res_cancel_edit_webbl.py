#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Reservation, Fixleist, Reslin_queasy

def res_cancel_edit_webbl(res_mode:string, done:bool, inp_resno:int, tot_qty:int, reslinno:int, grpflag:bool):
    successflag = False
    delete_it:bool = False
    found:bool = False
    gastno:int = 0
    res_line = reservation = fixleist = reslin_queasy = None

    rline = None

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, delete_it, found, gastno, res_line, reservation, fixleist, reslin_queasy
        nonlocal res_mode, done, inp_resno, tot_qty, reslinno, grpflag
        nonlocal rline


        nonlocal rline

        return {"reslinno": reslinno, "grpflag": grpflag, "successflag": successflag}

    def cancel_edit():

        nonlocal successflag, delete_it, found, gastno, res_line, reservation, fixleist, reslin_queasy
        nonlocal res_mode, done, inp_resno, tot_qty, reslinno, grpflag
        nonlocal rline


        nonlocal rline

        if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()) and not done:

            res_line = get_cache (Res_line, {"resnr": [(eq, inp_resno)],"reslinnr": [(ne, reslinno)]})

            if not res_line:

                rline = db_session.query(Rline).filter(
                         (Rline.resnr == inp_resno) & (Rline.reslinnr == reslinno) & (Rline.resstatus == 12)).first()

                if rline:
                    gastno = rline.gastnr


                    db_session.delete(rline)
                    pass
                    found = True

                if found:

                    reservation = get_cache (Reservation, {"resnr": [(eq, inp_resno)]})
                    db_session.delete(reservation)
                    pass
                    delete_it = True

            if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower() :

                res_line = get_cache (Res_line, {"resnr": [(eq, inp_resno)],"reslinnr": [(eq, reslinno)],"resstatus": [(eq, 12)]})

                if res_line:
                    gastno = res_line.gastnr


                    db_session.delete(res_line)
                    pass
                    delete_it = True

            if delete_it:

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == inp_resno) & (Fixleist.reslinnr == reslinno)).order_by(Fixleist._recid).all():
                    db_session.delete(fixleist)

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, inp_resno)],"reslinnr": [(eq, reslinno)]})
                while None != reslin_queasy:
                    pass
                    db_session.delete(reslin_queasy)

                    curr_recid = reslin_queasy._recid
                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == inp_resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy._recid > curr_recid)).first()

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.resnr == inp_resno) & (Reslin_queasy.reslinnr == reslinno)).order_by(Reslin_queasy._recid).all():
                    db_session.delete(reslin_queasy)

                if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower() :

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "rate-prog")],"number1": [(eq, inp_resno)],"number2": [(eq, 0)],"char1": [(eq, "")],"reslinnr": [(eq, 1)]})

                    if reslin_queasy:
                        db_session.delete(reslin_queasy)

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "reschanges")],"resnr": [(eq, inp_resno)],"reslinnr": [(eq, reslinno)]})
                while None != reslin_queasy:
                    pass
                    db_session.delete(reslin_queasy)

                    curr_recid = reslin_queasy._recid
                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.resnr == inp_resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy._recid > curr_recid)).first()
                pass
                reslinno = reslinno - 1

        if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()) and done and (tot_qty > 1):

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == inp_resno) & (Res_line.gastnr == gastno)).order_by(Res_line._recid).all():
                res_line.grpflag = True
                pass

        if tot_qty > 1:
            grpflag = True
        successflag = True


    cancel_edit()

    return generate_output()