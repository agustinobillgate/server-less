#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def del_if_prefixcodebl(recid_param:int):
    parameters = None

    param_list = None

    param_list_data, Param_list = create_model_like(Parameters, {"recid_param":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal recid_param


        nonlocal param_list
        nonlocal param_list_data

        return {}

    # parameters = get_cache (Parameters, {"_recid": [(eq, recid_param)]})
    parameters = db_session.query(Parameters).filter(
             (Parameters._recid == recid_param)).with_for_update().first()

    if parameters:
        db_session.delete(parameters)

    return generate_output()