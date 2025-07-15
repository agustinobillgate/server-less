#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

def egsub_task_sub_codebl(curr_select:string, subtask_sub_code:string):

    prepare_cache ([Eg_subtask])

    avail_sub = False
    eg_subtask = None

    sub = None

    Sub = create_buffer("Sub",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_subtask
        nonlocal curr_select, subtask_sub_code
        nonlocal sub


        nonlocal sub

        return {"avail_sub": avail_sub}


    if curr_select.lower()  == ("chg").lower() :

        sub = get_cache (Eg_subtask, {"sub_code": [(eq, subtask_sub_code)],"_recid": [(ne, eg_subtask._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        sub = get_cache (Eg_subtask, {"sub_code": [(eq, subtask_sub_code)]})

    if sub:
        avail_sub = True

    return generate_output()