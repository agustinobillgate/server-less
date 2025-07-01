#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Prtable, Guest_pr, Res_line, Reslin_queasy

def prtable_admin3bl(nr:int):

    prepare_cache ([Guest_pr])

    enable_it = True
    prtable = guest_pr = res_line = reslin_queasy = None

    prtable1 = None

    Prtable1 = create_buffer("Prtable1",Prtable)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal enable_it, prtable, guest_pr, res_line, reslin_queasy
        nonlocal nr
        nonlocal prtable1


        nonlocal prtable1

        return {"enable_it": enable_it}


    prtable1 = db_session.query(Prtable1).filter(
             (Prtable1.nr == nr) & (Prtable1.prcode != "")).first()
    while None != prtable1 and enable_it:

        guest_pr = get_cache (Guest_pr, {"code": [(eq, prtable1.prcode)]})

        if guest_pr:

            res_line = get_cache (Res_line, {"gastnr": [(eq, guest_pr.gastnr)],"active_flag": [(le, 1)],"reserve_int": [(eq, prtable1.marknr)]})
            while None != res_line and enable_it:

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if not reslin_queasy:
                    enable_it = False

                curr_recid = res_line._recid
                res_line = db_session.query(Res_line).filter(
                         (Res_line.gastnr == guest_pr.gastnr) & (Res_line.active_flag <= 1) & (Res_line.reserve_int == prtable1.marknr) & (Res_line._recid > curr_recid)).first()

        curr_recid = prtable1._recid
        prtable1 = db_session.query(Prtable1).filter(
                 (Prtable1.nr == nr) & (Prtable1.prcode != "") & (Prtable1._recid > curr_recid)).first()

    return generate_output()