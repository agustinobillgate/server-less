from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic

def prepare_calls_listbl():
    logic_flag = False


    db_session = local_storage.db_session

    def generate_output():
        nonlocal logic_flag


        return {"logic_flag": logic_flag}

    logic_flag = get_output(htplogic(307))

    return generate_output()