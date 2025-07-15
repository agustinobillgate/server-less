#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location

def eg_building_btn_renartbl(build_number1:int):
    fl_code = 0
    eg_location = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_location
        nonlocal build_number1

        return {"fl_code": fl_code}


    eg_location = get_cache (Eg_location, {"building": [(eq, build_number1)]})

    if eg_location:
        fl_code = 1

    return generate_output()