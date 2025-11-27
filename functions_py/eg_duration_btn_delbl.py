#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask, Eg_duration

def eg_duration_btn_delbl(duration_nr:int, rec_id:int):
    fl_code = 0
    eg_subtask = eg_duration = None

    egsub = None

    Egsub = create_buffer("Egsub",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask, eg_duration
        nonlocal duration_nr, rec_id
        nonlocal egsub


        nonlocal egsub

        return {"fl_code": fl_code}


    egsub = db_session.query(Egsub).filter(
             (Egsub.dur_nr == duration_nr)).first()

    if egsub:
        fl_code = 1

        return generate_output()

    # eg_duration = get_cache (Eg_duration, {"_recid": [(eq, rec_id)]})
    eg_duration = db_session.query(Eg_duration).filter(
             (Eg_duration._recid == rec_id)).with_for_update().first()

    if eg_duration:
        pass
        db_session.delete(eg_duration)
        # pass
        db_session.refresh(eg_duration,with_for_update=True)

    return generate_output()
