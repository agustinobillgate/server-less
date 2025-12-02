#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

maintask_data, Maintask = create_model_like(Queasy)

def eg_maintask_btn_exitbl(maintask_data:[Maintask], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

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

        return {"fl_code": fl_code}

    def fill_new_queasy():

        nonlocal fl_code, queasy
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal maintask, queasy1


        queasy.key = 133
        queasy.number1 = maintask.number1
        queasy.number2 = maintask.number2
        queasy.char1 = maintask.char1


    maintask = query(maintask_data, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        queasy = db_session.query(Queasy).filter(Queasy._recid == rec_id).with_for_update().first()

        queasy1 = get_cache (Queasy, {"number1": [(eq, maintask.number1)],"deci2": [(eq, 0)],"key": [(eq, 133)],"_recid": [(ne, queasy._recid)]})

        if queasy1:
            fl_code = 1
        else:

            queasy1 = get_cache (Queasy, {"char1": [(eq, maintask.char1)],"deci2": [(eq, 0)],"key": [(eq, 133)],"_recid": [(ne, queasy._recid)]})

            if queasy1:
                fl_code = 2
            else:
                pass
                queasy.number1 = maintask.number1
                queasy.number2 = maintask.number2
                queasy.char1 = maintask.char1
                pass
                fl_code = 3

    return generate_output()