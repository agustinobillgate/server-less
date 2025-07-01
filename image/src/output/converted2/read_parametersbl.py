#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def read_parametersbl(case_type:int, char1:string, char2:string, char3:string, int1:int):
    t_parameters_list = []
    parameters = None

    t_parameters = None

    t_parameters_list, T_parameters = create_model_like(Parameters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_parameters_list, parameters
        nonlocal case_type, char1, char2, char3, int1


        nonlocal t_parameters
        nonlocal t_parameters_list

        return {"t-parameters": t_parameters_list}

    if case_type == 1:

        parameters = get_cache (Parameters, {"progname": [(eq, char1)],"section": [(eq, char2)],"varname": [(gt, char3)]})

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 2:

        parameters = get_cache (Parameters, {"progname": [(eq, char1)],"section": [(eq, char2)],"varname": [(eq, char3)]})

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 3:

        parameters = get_cache (Parameters, {"_recid": [(eq, int1)]})

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 4:

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == (char1).lower()) & (Parameters.section == (char2).lower()) & (Parameters.varname > (char3).lower())).order_by(Parameters._recid).all():
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 5:

        parameters = db_session.query(Parameters).filter(
                 (Parameters.progname == (char1).lower()) & (Parameters.section == (char2).lower()) & (to_int(Parameters.varname) == to_int(char3))).first()

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)

    return generate_output()