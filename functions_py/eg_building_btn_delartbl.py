#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

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

    # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).with_for_update().first()
    pass
    db_session.delete(queasy)
    db_session.refresh(queasy,with_for_update=True)

    return generate_output()
