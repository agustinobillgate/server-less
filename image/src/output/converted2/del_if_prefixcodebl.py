from functions.additional_functions import *
import decimal
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

    parameters = db_session.query(Parameters).filter(
             (Parameters._recid == recid_param)).first()
    db_session.delete(parameters)

    return generate_output()