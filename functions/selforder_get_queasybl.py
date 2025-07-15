#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def selforder_get_queasybl(department:int, queasy_number:int):
    mess_result = ""
    output_list_data = []
    queasy = None

    output_list = None

    output_list_data, Output_list = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, output_list_data, queasy
        nonlocal department, queasy_number


        nonlocal output_list
        nonlocal output_list_data

        return {"mess_result": mess_result, "output-list": output_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"betriebsnr": [(eq, department)],"number2": [(eq, queasy_number)]})

    if queasy:
        mess_result = "0-Queasy Found!"
        output_list = Output_list()
        output_list_data.append(output_list)

        buffer_copy(queasy, output_list)
    else:
        mess_result = "0-Queasy Not Found!"

    return generate_output()