#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def dml_issue_return_cost_centerbl(cost_center:string):

    prepare_cache ([Gl_acct])

    cost_acct = ""
    avail_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, avail_acct, gl_acct
        nonlocal cost_center

        return {"cost_center": cost_center, "cost_acct": cost_acct, "avail_acct": avail_acct}


    gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, cost_center)]})

    if not gl_acct:
        avail_acct = True

        return generate_output()
    else:
        cost_acct = gl_acct.fibukonto
        cost_center = gl_acct.bezeich

    return generate_output()