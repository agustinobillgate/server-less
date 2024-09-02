from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def read_parametersbl(case_type:int, char1:str, char2:str, char3:str, int1:int):
    t_parameters_list = []
    parameters = None

    t_parameters = None

    t_parameters_list, T_parameters = create_model_like(Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_parameters_list, parameters


        nonlocal t_parameters
        nonlocal t_parameters_list
        return {"t-parameters": t_parameters_list}

    if case_type == 1:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == (char1).lower()) &  (func.lower(Parameters.section) == (char2).lower()) &  (func.lower(Parameters.varname) > (char3).lower())).first()

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 2:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == (char1).lower()) &  (func.lower(Parameters.section) == (char2).lower()) &  (func.lower(Parameters.varname) == (char3).lower())).first()

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 3:

        parameters = db_session.query(Parameters).filter(
                (Parameters._recid == int1)).first()

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 4:

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == (char1).lower()) &  (func.lower(Parameters.section) == (char2).lower()) &  (func.lower(Parameters.varname) > (char3).lower())).all():
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    elif case_type == 5:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == (char1).lower()) &  (func.lower(Parameters.section) == (char2).lower()) &  (to_int(Parameters.varname) == to_int(char3))).first()

        if parameters:
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)

    return generate_output()