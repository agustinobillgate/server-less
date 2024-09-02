from functions.additional_functions import *
import decimal
from models import Queasy

def selforder_get_queasybl(department:int, queasy_number:int):
    mess_result = ""
    output_list_list = []
    queasy = None

    output_list = None

    output_list_list, Output_list = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, output_list_list, queasy


        nonlocal output_list
        nonlocal output_list_list
        return {"mess_result": mess_result, "output-list": output_list_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.betriebsnr == department) &  (Queasy.number2 == queasy_number)).first()

    if queasy:
        mess_result = "0_Queasy Found!"
        output_list = Output_list()
        output_list_list.append(output_list)

        buffer_copy(queasy, output_list)
    else:
        mess_result = "0_Queasy Not Found!"

    return generate_output()