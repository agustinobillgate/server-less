#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def cost_center_btn_delbl(rec_id:int):
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal rec_id

        return {}


    # parameters = get_cache (Parameters, {"_recid": [(eq, rec_id)]})
    parameters = db_session.query(Parameters).filter(
             (Parameters._recid == rec_id)).with_for_update().first()

    if parameters:
        pass
        db_session.delete(parameters)
        pass

    return generate_output()