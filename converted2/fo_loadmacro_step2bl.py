#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

t_parameters_data, T_parameters = create_model_like(Parameters)

def fo_loadmacro_step2bl(t_parameters_data:[T_parameters]):
    parameters = None

    t_parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters


        nonlocal t_parameters

        return {}

    for t_parameters in query(t_parameters_data):
        parameters = Parameters()
        db_session.add(parameters)

        buffer_copy(t_parameters, parameters)

    return generate_output()