#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ts_restinv_tischnrbl(curr_dept:int):
    avail_queasy = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_queasy, queasy
        nonlocal curr_dept

        return {"avail_queasy": avail_queasy}


    queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)]})

    if queasy:
        avail_queasy = True

    return generate_output()