from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_subtask

def eg_mksub_btn_ok_webbl(deptnr:int, mainnr:int, subtask:str, user_init:str, bezeich:str, days:str, hours:str, minutes:str):
    fl_code = 0
    eg_subtask = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask


        return {"fl_code": fl_code}


    eg_subtask = db_session.query(Eg_subtask).filter(
            (Eg_subtask.main_nr == mainnr) &  (func.lower(Eg_subtask.(bezeich).lower()) == (bezeich).lower())).first()

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
        eg_subtask.create_DATE = get_current_date()
        eg_subtask.create_TIME = get_current_time_in_seconds()
        eg_subtask.create_by = user_init
        eg_subtask.sourceForm = "1"

    return generate_output()