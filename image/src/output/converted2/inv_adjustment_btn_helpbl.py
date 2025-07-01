#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def inv_adjustment_btn_helpbl(cost_acct:string):

    prepare_cache ([Gl_acct])

    avail_gl_acct = False
    a_bez = ""
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, a_bez, gl_acct
        nonlocal cost_acct

        return {"avail_gl_acct": avail_gl_acct, "a_bez": a_bez}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich

    return generate_output()