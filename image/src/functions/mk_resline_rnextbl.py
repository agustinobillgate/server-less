from functions.additional_functions import *
import decimal
from models import Res_line

def mk_resline_rnextbl(resnr:int, reslinnr:int, t_zipreis:decimal):
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line


        return {}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line:
        res_line.zipreis = t_zipreis

    return generate_output()