from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Reslin_queasy

def mk_resline_avail_argt_linebl(resnr:int, reslinnr:int):
    avail_argt = False
    reslin_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_argt, reslin_queasy
        nonlocal resnr, reslinnr


        return {"avail_argt": avail_argt}


    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr)).first()

    if reslin_queasy:
        avail_argt = True

    return generate_output()