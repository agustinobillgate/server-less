#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint

def prepare_check_outbl():
    integerflag = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal integerflag

        return {"integerflag": integerflag}

    integerflag = get_output(htpint(297))

    return generate_output()