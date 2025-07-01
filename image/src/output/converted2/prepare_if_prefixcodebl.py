#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def prepare_if_prefixcodebl(zone:string):
    param_list_list = []
    parameters = None

    param_list = None

    param_list_list, Param_list = create_model_like(Parameters, {"recid_param":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal param_list_list, parameters
        nonlocal zone


        nonlocal param_list
        nonlocal param_list_list

        return {"param-list": param_list_list}

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("interface").lower()) & (Parameters.section == ("prefix").lower()) & (Parameters.varname == (zone).lower())).order_by(Parameters.vstring).all():
        param_list = Param_list()
        param_list_list.append(param_list)

        buffer_copy(parameters, param_list)
        param_list.recid_param = parameters._recid

    return generate_output()