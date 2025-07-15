#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

def eg_mksub_of_subtaskbl(subtask:string):
    fl_code = 0
    eg_subtask = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal subtask

        return {"fl_code": fl_code}


    eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, subtask)]})

    if eg_subtask:
        fl_code = 1

    return generate_output()