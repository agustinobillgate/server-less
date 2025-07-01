#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import History, Queasy

def grphtl_admin_btn_delartbl(rec_id:int, htlname_number:int):
    err_flag = 0
    history = queasy = None

    hist = None

    Hist = create_buffer("Hist",History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, history, queasy
        nonlocal rec_id, htlname_number
        nonlocal hist


        nonlocal hist

        return {"err_flag": err_flag}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

    hist = db_session.query(Hist).filter(
             (Hist.guestnrcom == htlname_number)).first()

    if hist:
        err_flag = 1

        return generate_output()
    else:
        pass
        db_session.delete(queasy)

    return generate_output()