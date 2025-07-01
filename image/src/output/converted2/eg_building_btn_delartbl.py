#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Queasy

def eg_building_btn_delartbl(build_number1:int, rec_id:int):
    fl_code = 0
    eg_location = queasy = None

    egbuilding = None

    Egbuilding = create_buffer("Egbuilding",Eg_location)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_location, queasy
        nonlocal build_number1, rec_id
        nonlocal egbuilding


        nonlocal egbuilding

        return {"fl_code": fl_code}


    egbuilding = db_session.query(Egbuilding).filter(
             (Egbuilding.building == build_number1)).first()

    if egbuilding:
        fl_code = 1

        return generate_output()

    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(queasy)

    return generate_output()