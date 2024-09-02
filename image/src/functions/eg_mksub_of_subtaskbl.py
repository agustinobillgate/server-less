from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_subtask

def eg_mksub_of_subtaskbl(subtask:str):
    fl_code = 0
    eg_subtask = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_subtask


        return {"fl_code": fl_code}


    eg_subtask = db_session.query(Eg_subtask).filter(
            (func.lower(Eg_subtask.sub_code) == (subtask).lower())).first()

    if eg_subtask:
        fl_code = 1

    return generate_output()