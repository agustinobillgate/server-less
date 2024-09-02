from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Prtable, Guest_pr, Res_line, Reslin_queasy

def prtable_admin3bl(nr:int):
    enable_it = False
    prtable = guest_pr = res_line = reslin_queasy = None

    prtable1 = None

    Prtable1 = Prtable

    db_session = local_storage.db_session

    def generate_output():
        nonlocal enable_it, prtable, guest_pr, res_line, reslin_queasy
        nonlocal prtable1


        nonlocal prtable1
        return {"enable_it": enable_it}


    prtable1 = db_session.query(Prtable1).filter(
            (Prtable1.nr == nr) &  (Prtable1.prcode != "")).first()
    while None != prtable1 and enable_it:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.code == prtable1.prcode)).first()

        if guest_pr:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.gastnr == guest_pr.gastnr) &  (Res_line.active_flag <= 1) &  (Res_line.reserve_int == prtable1.marknr)).first()
            while None != res_line and enable_it:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if not reslin_queasy:
                    enable_it = False

                res_line = db_session.query(Res_line).filter(
                        (Res_line.gastnr == guest_pr.gastnr) &  (Res_line.active_flag <= 1) &  (Res_line.reserve_int == prtable1.marknr)).first()

        prtable1 = db_session.query(Prtable1).filter(
                (Prtable1.nr == nr) &  (Prtable1.prcode != "")).first()

    return generate_output()