#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request, Eg_subtask, Eg_property

def eg_maintask_btn_renartbl(maintask_number1:int):

    prepare_cache ([Eg_request])

    fl_code = 0
    eg_request = eg_subtask = eg_property = None

    egreq = egsub = egprop = None

    Egreq = create_buffer("Egreq",Eg_request)
    Egsub = create_buffer("Egsub",Eg_subtask)
    Egprop = create_buffer("Egprop",Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_request, eg_subtask, eg_property
        nonlocal maintask_number1
        nonlocal egreq, egsub, egprop


        nonlocal egreq, egsub, egprop

        return {"fl_code": fl_code}


    egreq = get_cache (Eg_request, {"maintask": [(eq, maintask_number1)]})

    egsub = db_session.query(Egsub).filter(
             (egSub.main_nr == maintask_number1)).first()

    egprop = db_session.query(Egprop).filter(
             (Egprop.maintask == maintask_number1)).first()

    if egprop or egreq or egSub:
        fl_code = 1

    return generate_output()