#using conversion tools version: 1.0.0.117

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


    eg_subtask = get_cache (Eg_subtask, {"_recid": [(eq, rec_id)]})
    pass
    if eg_subtask:
        db_session.delete(eg_subtask)
        pass

    return generate_output()