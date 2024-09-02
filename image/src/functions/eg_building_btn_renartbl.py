from functions.additional_functions import *
import decimal
from models import Eg_location

def eg_building_btn_renartbl(build_number1:int):
    fl_code = 0
    eg_location = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_location


        return {"fl_code": fl_code}


    eg_location = db_session.query(Eg_location).filter(
            (Eg_location.building == build_number1)).first()

    if eg_location:
        fl_code = 1

    return generate_output()