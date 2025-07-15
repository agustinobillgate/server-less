#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def next_reslinnrbl(inp_resno:int):

    prepare_cache ([Res_line])

    reslinno = 1
    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal reslinno, res_line
        nonlocal inp_resno

        return {"reslinno": reslinno}


    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == inp_resno)).order_by(Res_line.reslinnr.desc()).yield_per(100):
        reslinno = res_line.reslinnr + 1
        break

    return generate_output()