from functions.additional_functions import *
import decimal
from models import Queasy

def egcategory_catnumbl(curr_select:str, category_number1:int, rec_id:int):
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


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    if curr_select.lower()  == "chg":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.number1 == category_number1 and Queasy1.number2 == 0 and Queasy1.deci2 == 0 and Queasy1.key == 132) &  (Queasy1._recid != queasy._recid)).first()

    elif curr_select.lower()  == "add":

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.number1 == category_number1 and Queasy1.number2 == 0 and Queasy1.deci2 == 0 and Queasy1.key == 132)).first()

    if queasy1:
        avail_queasy = True

    return generate_output()