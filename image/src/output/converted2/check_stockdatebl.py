#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr

def check_stockdatebl(billdate:date):
    err_code = 0
    gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_jouhdr
        nonlocal billdate

        return {"err_code": err_code}


    gl_jouhdr = get_cache (Gl_jouhdr, {"jtype": [(eq, 6)],"datum": [(ge, billdate)]})

    if gl_jouhdr:
        err_code = 1

    return generate_output()