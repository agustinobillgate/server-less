#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate

def prepare_res_voucherbl():
    fint = 0
    to_date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fint, to_date

        return {"fint": fint, "to_date": to_date}

    fint = get_output(htpint(297))
    to_date = get_output(htpdate(87))

    return generate_output()