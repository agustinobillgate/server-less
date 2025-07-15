#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Parameters

def po_issue_check_acctbl(case_type:int, cost_acct:string):

    prepare_cache ([Gl_acct])

    avail_gl_acct = False
    fl_code = 0
    gl_acct = parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, fl_code, gl_acct, parameters
        nonlocal case_type, cost_acct

        return {"avail_gl_acct": avail_gl_acct, "fl_code": fl_code}


    if case_type == 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if not gl_acct:
            fl_code = 1

            return generate_output()

        if gl_acct:

            parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, gl_acct.fibukonto)]})

            if not parameters:
                fl_code = 2

                return generate_output()

    elif case_type == 2:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if not gl_acct:

            return generate_output()
        else:
            avail_gl_acct = True

    return generate_output()