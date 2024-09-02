from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Reslin_queasy, Res_line

def argt_frate_copybl(s_recid:int):
    done = False
    reslin_queasy = res_line = None

    r_queasy = rline = None

    R_queasy = Reslin_queasy
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, reslin_queasy, res_line
        nonlocal r_queasy, rline


        nonlocal r_queasy, rline
        return {"done": done}


    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (to_int(Reslin_queasy._recid) == s_recid)).first()

    if not reslin_queasy:

        return generate_output()

    for rline in db_session.query(Rline).filter(
                (Rline.resnr == reslin_queasy.resnr) &  (Rline.active_flag <= 1) &  (Rline.resstatus != 12) &  (Rline.reslinnr != reslin_queasy.reslinnr) &  (Rline.zipreis > 0)).all():

        r_queasy = db_session.query(R_queasy).filter(
                    (func.lower(R_queasy.key) == "fargt_line") &  (R_queasy.number1 == reslin_queasy.number1) &  (R_queasy.number2 == reslin_queasy.number2) &  (R_queasy.number3 == reslin_queasy.number3) &  (R_queasy.resnr == rline.resnr) &  (R_queasy.reslinnr == rline.reslinnr)).first()

        if not r_queasy:
            r_queasy = R_queasy()
            db_session.add(r_queasy)

            r_queasy.reslinnr = rline.reslinnr


        buffer_copy(reslin_queasy, r_queasy,except_fields=["reslin_queasy.reslinnr"])

        r_queasy = db_session.query(R_queasy).first()

    done = True

    return generate_output()