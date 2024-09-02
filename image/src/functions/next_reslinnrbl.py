from functions.additional_functions import *
import decimal
from models import Res_line

def next_reslinnrbl(inp_resno:int):
    reslinno = 0
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal reslinno, res_line


        return {"reslinno": reslinno}


    for res_line in db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resno)).all():
        reslinno = res_line.reslinnr + 1
        break

    return generate_output()