from functions.additional_functions import *
import decimal
from models import Parameters

t_parameters_list, T_parameters = create_model_like(Parameters)

def fo_loadmacro_step2bl(t_parameters_list:[T_parameters]):
    parameters = None

    t_parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        nonlocal t_parameters
        nonlocal t_parameters_list
        return {}

    for t_parameters in query(t_parameters_list):
        parameters = Parameters()
        db_session.add(parameters)

        buffer_copy(t_parameters, parameters)

    return generate_output()