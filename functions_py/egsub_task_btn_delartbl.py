#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

def egsub_task_btn_delartbl(rec_id:int):
    eg_subtask = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_subtask
        nonlocal rec_id

        return {}


    # eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})
    eg_subtask = db_session.query(Eg_subtask).filter(
             (Eg_subtask._recid == rec_id)).with_for_update().first()
    # pass
    if eg_subtask:
        db_session.delete(eg_subtask)
        # pass
    db_session.refresh(eg_subtask,with_for_update=True)

    return generate_output()