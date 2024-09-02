from functions.additional_functions import *
import decimal
from models import History, Queasy

def grphtl_admin_btn_delartbl(rec_id:int, htlname_number:int):
    err_flag = 0
    history = queasy = None

    hist = None

    Hist = History

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, history, queasy
        nonlocal hist


        nonlocal hist
        return {"err_flag": err_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    hist = db_session.query(Hist).filter(
            (Hist.guestnrcom == htlname_number)).first()

    if hist:
        err_flag = 1

        return generate_output()
    else:

        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)

    return generate_output()