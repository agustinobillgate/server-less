from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def eg_maintask_charbl(curr_select:str, maintask_char1:str):
    avail_queasy = False
    queasy = None

    queasy1 = None

    Queasy1 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_queasy, queasy
        nonlocal queasy1


        nonlocal queasy1
        return {"avail_queasy": avail_queasy}


    if curr_select.lower()  == "chg":

        queasy1 = db_session.query(Queasy1).filter(
                (func.lower(Queasy1.char1) == (maintask_char1).lower()) &  (Queasy1.number2 == 0) &  (Queasy1.deci2 == 0) &  (Queasy1.key == 133) &  (Queasy1._recid != queasy._recid)).first()

    elif curr_select.lower()  == "add":

        queasy1 = db_session.query(Queasy1).filter(
                (func.lower(Queasy1.char1) == (maintask_char1).lower()) &  (Queasy1.number2 == 0) &  (Queasy1.deci2 == 0) &  (Queasy1.key == 133)).first()

    return generate_output()