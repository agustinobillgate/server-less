#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

def eg_duration_btn_renartbl(duration_nr:int):
    fl_code = False
    eg_subtask = None

    egsub = None

    Egsub = create_buffer("Egsub",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal duration_nr
        nonlocal egsub


        nonlocal egsub

        return {"fl_code": fl_code}


    egsub = db_session.query(Egsub).filter(
             (egSub.dur_nr == duration_nr)).first()

    if egSub:
        fl_code = True

    return generate_output()