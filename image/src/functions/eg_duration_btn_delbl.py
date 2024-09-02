from functions.additional_functions import *
import decimal
from models import Eg_subtask, Eg_duration

def eg_duration_btn_delbl(duration_nr:int, rec_id:int):
    fl_code = 0
    eg_subtask = eg_duration = None

    egsub = None

    Egsub = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask, eg_duration
        nonlocal egsub


        nonlocal egsub
        return {"fl_code": fl_code}


    egsub = db_session.query(Egsub).filter(
            (egSub.dur_nr == duration_nr)).first()

    if egSub:
        fl_code = 1

        return generate_output()

    eg_duration = db_session.query(Eg_duration).filter(
            (eg_Duration._recid == rec_id)).first()

    eg_duration = db_session.query(Eg_duration).first()
    db_session.delete(eg_duration)


    return generate_output()