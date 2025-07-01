#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def s_stockiss_return_sartnrbl(fibu:string):

    prepare_cache ([Gl_acct])

    avail_gl = False
    cost_acct = "00000000000000"
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, cost_acct, gl_acct
        nonlocal fibu

        return {"avail_gl": avail_gl, "cost_acct": cost_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

    if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
        cost_acct = gl_acct.fibukonto
        avail_gl = True

    return generate_output()