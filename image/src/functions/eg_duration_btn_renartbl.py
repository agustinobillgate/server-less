from functions.additional_functions import *
import decimal
from models import Eg_subtask

def eg_duration_btn_renartbl(duration_nr:int):
    fl_code = False
    eg_subtask = None

    egsub = None

    Egsub = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal egsub


        nonlocal egsub
        return {"fl_code": fl_code}


    egsub = db_session.query(Egsub).filter(
            (egSub.dur_nr == duration_nr)).first()

    if egSub:
        fl_code = True

    return generate_output()