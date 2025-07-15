#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Eg_request, Eg_subtask, Queasy

def eg_maintask_btn_delartbl(maintask_number1:int, rec_id:int):
    fl_code = 0
    eg_property = eg_request = eg_subtask = queasy = None

    eg_prop = eg_req = eg_sub = None

    Eg_prop = create_buffer("Eg_prop",Eg_property)
    Eg_req = create_buffer("Eg_req",Eg_request)
    Eg_sub = create_buffer("Eg_sub",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_property, eg_request, eg_subtask, queasy
        nonlocal maintask_number1, rec_id
        nonlocal eg_prop, eg_req, eg_sub


        nonlocal eg_prop, eg_req, eg_sub

        return {"fl_code": fl_code}


    eg_sub = db_session.query(Eg_sub).filter(
             (Eg_sub.main_nr == maintask_number1)).first()

    if eg_sub:

        eg_prop = db_session.query(Eg_prop).filter(
                 (Eg_prop.maintask == maintask_number1)).first()

        if eg_prop:
            fl_code = 1

            return generate_output()

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        if queasy:
            pass
            db_session.delete(queasy)

    return generate_output()