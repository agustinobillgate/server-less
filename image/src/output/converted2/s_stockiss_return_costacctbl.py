#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Parameters

def s_stockiss_return_costacctbl(cost_acct:string):

    prepare_cache ([Gl_acct])

    err_code = 0
    gl_acct = parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct, parameters
        nonlocal cost_acct

        return {"err_code": err_code}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if not gl_acct:
        err_code = 1

        return generate_output()

    if gl_acct:

        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, gl_acct.fibukonto)]})

        if not parameters:
            err_code = 2

            return generate_output()

    return generate_output()