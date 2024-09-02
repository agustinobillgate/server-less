from functions.additional_functions import *
import decimal
from functions.htpint import htpint

def prepare_check_outbl():
    integerflag = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal integerflag


        return {"integerflag": integerflag}

    integerflag = get_output(htpint(297))

    return generate_output()