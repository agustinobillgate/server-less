#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def dml_issue_return_lscheinnrbl(lscheinnr:string):
    err_code = False
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_ophdr
        nonlocal lscheinnr

        return {"err_code": err_code}


    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")]})

    if l_ophdr:
        err_code = True

    return generate_output()