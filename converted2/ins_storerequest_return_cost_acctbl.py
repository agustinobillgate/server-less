#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def ins_storerequest_return_cost_acctbl(cost_acct:string):

    prepare_cache ([Gl_acct])

    err_flag = 0
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, gl_acct
        nonlocal cost_acct

        return {"err_flag": err_flag}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if not gl_acct:
        err_flag = 1

        return generate_output()

    if gl_acct and gl_acct.acc_type != 2 and gl_acct.acc_type != 5:
        err_flag = 2

        return generate_output()

    return generate_output()