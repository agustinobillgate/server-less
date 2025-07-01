#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
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