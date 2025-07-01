#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def mk_pr_returnbl(fibu:string):

    prepare_cache ([Gl_acct])

    err_code = 0
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct
        nonlocal fibu

        return {"err_code": err_code}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

    if not gl_acct:
        err_code = 1

        return generate_output()

    if gl_acct and gl_acct.acc_type == 1:
        err_code = 2

        return generate_output()

    return generate_output()