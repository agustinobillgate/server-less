from functions.additional_functions import *
import decimal
from models import Queasy

def ts_restinv_tischnrbl(curr_dept:int):
    avail_queasy = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_queasy, queasy


        return {"avail_queasy": avail_queasy}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 31) &  (Queasy.number1 == curr_dept)).first()

    if queasy:
        avail_queasy = True

    return generate_output()