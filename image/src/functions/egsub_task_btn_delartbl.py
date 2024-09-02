from functions.additional_functions import *
import decimal
from models import Eg_subtask

def egsub_task_btn_delartbl(rec_id:int):
    eg_subtask = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_subtask


        return {}


    eg_subtask = db_session.query(Eg_subtask).filter(
            (Eg_subtask._recid == rec_id)).first()

    eg_subtask = db_session.query(Eg_subtask).first()
    db_session.delete(eg_subtask)


    return generate_output()