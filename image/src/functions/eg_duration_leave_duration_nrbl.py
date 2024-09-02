from functions.additional_functions import *
import decimal
from models import Eg_duration

def eg_duration_leave_duration_nrbl(curr_select:str, duration_duration_nr:int, rec_id:int):
    fl_code = False
    eg_duration = None

    queasy1 = None

    Queasy1 = Eg_duration

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_duration
        nonlocal queasy1


        nonlocal queasy1
        return {"fl_code": fl_code}


    eg_duration = db_session.query(Eg_duration).filter(
            (eg_Duration._recid == rec_id)).first()

    if curr_select.lower()  == "chg":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.Duration_nr == duration_duration_nr) &  (Queasy1._recid != eg_Duration._recid)).first()

    elif curr_select.lower()  == "add":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.Duration_nr == duration_duration_nr)).first()

    if queasy1:
        fl_code = True

    return generate_output()