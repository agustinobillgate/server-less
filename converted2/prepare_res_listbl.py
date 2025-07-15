#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htplogic import htplogic
from functions.htpdate import htpdate

def prepare_res_listbl():
    integerflag = 0
    new_contrate = False
    ci_date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal integerflag, new_contrate, ci_date

        return {"integerflag": integerflag, "new_contrate": new_contrate, "ci_date": ci_date}

    integerflag = get_output(htpint(297))
    new_contrate = get_output(htplogic(550))
    ci_date = get_output(htpdate(87))

    return generate_output()