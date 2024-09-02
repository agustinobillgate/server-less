from functions.additional_functions import *
import decimal
from models import Eg_location, Queasy

def eg_building_btn_delartbl(build_number1:int, rec_id:int):
    fl_code = 0
    eg_location = queasy = None

    egbuilding = None

    Egbuilding = Eg_location

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_location, queasy
        nonlocal egbuilding


        nonlocal egbuilding
        return {"fl_code": fl_code}


    egbuilding = db_session.query(Egbuilding).filter(
            (Egbuilding.building == build_number1)).first()

    if egbuilding:
        fl_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    queasy = db_session.query(Queasy).first()
    db_session.delete(queasy)

    return generate_output()