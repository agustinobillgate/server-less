from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Reslin_queasy

def flag_replistbl(s_resnr:int, s_reslinnr:int, s_ind:int, s_done:bool, s_recid:int):
    reslin_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal reslin_queasy


        return {}


    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == s_resnr) &  (Reslin_queasy.reslinnr == s_reslinnr) &  (Reslin_queasy._recid == s_recid)).first()

    if reslin_queasy:

        reslin_queasy = db_session.query(Reslin_queasy).first()

        if s_ind == 1:
            reslin_queasy.deci1 = to_int(s_done)

        elif s_ind == 2:
            reslin_queasy.deci2 = to_int(s_done)

        elif s_ind == 3:
            reslin_queasy.deci3 = to_int(s_done)

        reslin_queasy = db_session.query(Reslin_queasy).first()

    return generate_output()