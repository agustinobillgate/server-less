from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate

def prepare_group_cobl():
    htpint = 0
    ci_datum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpint, ci_datum


        return {"htpint": htpint, "ci_datum": ci_datum}

    htpint = get_output(htpint(297))
    ci_datum = get_output(htpdate(87))

    return generate_output()