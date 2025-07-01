#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask

def eg_mksub_btn_ok_webbl(deptnr:int, mainnr:int, subtask:string, user_init:string, bezeich:string, days:string, hours:string, minutes:string):

    prepare_cache ([Eg_subtask])

    fl_code = 0
    eg_subtask = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask
        nonlocal deptnr, mainnr, subtask, user_init, bezeich, days, hours, minutes

        return {"fl_code": fl_code}


    eg_subtask = get_cache (Eg_subtask, {"main_nr": [(eq, mainnr)],"bezeich": [(eq, bezeich)]})

    if eg_subtask:
        fl_code = 1

        return generate_output()
    else:
        eg_subtask = Eg_subtask()
        db_session.add(eg_subtask)

        eg_subtask.dept_nr = deptnr
        eg_subtask.main_nr = mainnr
        eg_subtask.reserve_char = days + ";" + hours + ";" + minutes
        eg_subtask.sub_code = subtask
        eg_subtask.bezeich = bezeich
        eg_subtask.create_date = get_current_date()
        eg_subtask.create_time = get_current_time_in_seconds()
        eg_subtask.create_by = user_init
        eg_subtask.sourceform = "1"

    return generate_output()