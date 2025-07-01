#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def update_if_prefixcodebl(curr_select:string, zone:string, bezeich:string, recid_param:int):
    param_list_list = []
    parameters = None

    param_list = None

    param_list_list, Param_list = create_model_like(Parameters, {"recid_param":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal param_list_list, parameters
        nonlocal curr_select, zone, bezeich, recid_param


        nonlocal param_list
        nonlocal param_list_list

        return {"param-list": param_list_list}

    def fill_new_parameters():

        nonlocal param_list_list, parameters
        nonlocal curr_select, zone, bezeich, recid_param


        nonlocal param_list
        nonlocal param_list_list


        parameters.progname = "interface"
        parameters.section = "prefix"
        parameters.varname = zone
        parameters.vstring = bezeich

    param_list_list.clear()

    if curr_select.lower()  == ("add").lower() :
        parameters = Parameters()
        db_session.add(parameters)

        fill_new_parameters()

    elif curr_select.lower()  == ("chg").lower() :

        parameters = get_cache (Parameters, {"_recid": [(eq, recid_param)]})

        if parameters:
            parameters.vstring = bezeich

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("interface").lower()) & (Parameters.section == ("prefix").lower()) & (Parameters.varname == (zone).lower())).order_by(Parameters.vstring).all():
        param_list = Param_list()
        param_list_list.append(param_list)

        buffer_copy(parameters, param_list)
        param_list.recid_param = parameters._recid

    return generate_output()