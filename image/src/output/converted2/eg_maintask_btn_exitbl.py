from functions.additional_functions import *
import decimal
from models import Queasy

maintask_list, Maintask = create_model_like(Queasy)

def eg_maintask_btn_exitbl(maintask_list:[Maintask], case_type:int, rec_id:int):
    fl_code = 0
    queasy = None

    maintask = queasy1 = None

    Queasy1 = create_buffer("Queasy1",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal maintask, queasy1
        nonlocal maintask_list
        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal maintask, queasy1
        nonlocal maintask_list


        queasy.key = 133
        queasy.number1 = maintask.number1
        queasy.number2 = maintask.number2
        queasy.char1 = maintask.char1


    maintask = query(maintask_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == rec_id)).first()

        queasy1 = db_session.query(Queasy1).filter(
                 (Queasy1.number1 == maintask.number1 and Queasy1.deci2 == 0 and Queasy1.key == 133) & (Queasy1._recid != queasy._recid)).first()

        if queasy1:
            fl_code = 1
        else:

            queasy1 = db_session.query(Queasy1).filter(
                     (Queasy1.char1 == maintask.char1 and Queasy1.deci2 == 0 and Queasy1.key == 133) & (Queasy1._recid != queasy._recid)).first()

            if queasy1:
                fl_code = 2
            else:
                queasy.number1 = maintask.number1
                queasy.number2 = maintask.number2
                queasy.char1 = maintask.char1
                fl_code = 3

    return generate_output()