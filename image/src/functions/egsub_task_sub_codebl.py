from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_subtask

def egsub_task_sub_codebl(curr_select:str, subtask_sub_code:str):
    avail_sub = False
    eg_subtask = None

    sub = None

    Sub = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_subtask
        nonlocal sub


        nonlocal sub
        return {"avail_sub": avail_sub}


    if curr_select.lower()  == "chg":

        sub = db_session.query(Sub).filter(
                (func.lower(Sub.sub_code) == (subtask_sub_code).lower()) &  (Sub._recid != eg_subtask._recid)).first()

    elif curr_select.lower()  == "add":

        sub = db_session.query(Sub).filter(
                (func.lower(Sub.sub_code) == (subtask_sub_code).lower())).first()

    if sub:
        avail_sub = True

    return generate_output()