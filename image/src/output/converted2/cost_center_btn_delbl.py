#using conversion tools version: 1.0.0.111

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


    parameters = get_cache (Parameters, {"_recid": [(eq, rec_id)]})

    if parameters:
        pass
        db_session.delete(parameters)
        pass

    return generate_output()