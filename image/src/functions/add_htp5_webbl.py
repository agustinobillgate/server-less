from functions.additional_functions import *
import decimal
from functions.add_htp5bl import add_htp5bl

def add_htp5_webbl():
    done_flag = False


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done_flag


        return {"done_flag": done_flag}

    get_output(add_htp5bl())
    done_flag = True

    return generate_output()