#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Reslin_queasy, Res_line

def argt_frate_copybl(s_recid:int):

    prepare_cache ([Reslin_queasy, Res_line])

    done = False
    reslin_queasy = res_line = None

    r_queasy = rline = None

    R_queasy = create_buffer("R_queasy",Reslin_queasy)
    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, reslin_queasy, res_line
        nonlocal s_recid
        nonlocal r_queasy, rline


        nonlocal r_queasy, rline

        return {"done": done}


    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (to_int(Reslin_queasy._recid) == s_recid)).first()

    if not reslin_queasy:

        return generate_output()

    for rline in db_session.query(Rline).filter(
                 (Rline.resnr == reslin_queasy.resnr) & (Rline.active_flag <= 1) & (Rline.resstatus != 12) & (Rline.reslinnr != reslin_queasy.reslinnr) & (Rline.zipreis > 0)).order_by(Rline._recid).all():

        r_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"number1": [(eq, reslin_queasy.number1)],"number2": [(eq, reslin_queasy.number2)],"number3": [(eq, reslin_queasy.number3)],"resnr": [(eq, rline.resnr)],"reslinnr": [(eq, rline.reslinnr)]})

        if not r_queasy:
            r_queasy = Reslin_queasy()
            db_session.add(r_queasy)

            r_queasy.reslinnr = rline.reslinnr


        buffer_copy(reslin_queasy, r_queasy,except_fields=["reslin_queasy.reslinnr"])
        pass
    done = True

    return generate_output()