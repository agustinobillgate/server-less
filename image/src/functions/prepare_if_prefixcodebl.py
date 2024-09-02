from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def prepare_if_prefixcodebl(zone:str):
    param_list_list = []
    parameters = None

    param_list = None

    param_list_list, Param_list = create_model_like(Parameters, {"recid_param":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal param_list_list, parameters


        nonlocal param_list
        nonlocal param_list_list
        return {"param-list": param_list_list}

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "interface") &  (func.lower(Parameters.section) == "prefix") &  (func.lower(Parameters.varname) == (zone).lower())).all():
        param_list = Param_list()
        param_list_list.append(param_list)

        buffer_copy(parameters, param_list)
        param_list.recid_param = parameters._recid

    return generate_output()