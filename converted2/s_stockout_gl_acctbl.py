#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def s_stockout_gl_acctbl(cost_acct:string):
    avail_gl_acct = False
    err = 0
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, err, gl_acct
        nonlocal cost_acct

        return {"avail_gl_acct": avail_gl_acct, "err": err}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if not gl_acct:
        avail_gl_acct = False
    else:
        avail_gl_acct = True

    return generate_output()