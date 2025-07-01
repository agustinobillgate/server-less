#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate

def prepare_res_cancelledbl():
    finteger = 0
    fdate = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal finteger, fdate

        return {"finteger": finteger, "fdate": fdate}

    finteger = get_output(htpint(297))
    fdate = get_output(htpdate(87))

    return generate_output()