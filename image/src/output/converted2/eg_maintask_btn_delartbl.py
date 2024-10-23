from functions.additional_functions import *
import decimal
from models import Eg_property, Eg_request, Eg_subtask, Queasy

def eg_maintask_btn_delartbl(maintask_number1:int, rec_id:int):
    fl_code = 0
    eg_property = eg_request = eg_subtask = queasy = None

    egprop = egreq = egsub = None

    Egprop = create_buffer("Egprop",Eg_property)
    Egreq = create_buffer("Egreq",Eg_request)
    Egsub = create_buffer("Egsub",Eg_subtask)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_property, eg_request, eg_subtask, queasy
        nonlocal maintask_number1, rec_id
        nonlocal egprop, egreq, egsub


        nonlocal egprop, egreq, egsub
        return {"fl_code": fl_code}


    egsub = db_session.query(Egsub).filter(
             (egSub.main_nr == maintask_number1)).first()

    egprop = db_session.query(Egprop).filter(
             (egProp.maintask == maintask_number1)).first()

    if egProp or egSub:
        fl_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).first()
    db_session.delete(queasy)

    return generate_output()