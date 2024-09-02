from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate

def prepare_checked_outbl():
    finteger = 0
    ci_date = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal finteger, ci_date


        return {"finteger": finteger, "ci_date": ci_date}

    finteger = get_output(htpint(297))
    ci_date = get_output(htpdate(87))

    return generate_output()