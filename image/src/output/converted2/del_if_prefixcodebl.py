#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def del_if_prefixcodebl(recid_param:int):
    parameters = None

    param_list = None

    param_list_list, Param_list = create_model_like(Parameters, {"recid_param":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal recid_param


        nonlocal param_list
        nonlocal param_list_list

        return {}

    parameters = get_cache (Parameters, {"_recid": [(eq, recid_param)]})

    if parameters:
        pass
        db_session.delete(parameters)
        pass

    return generate_output()