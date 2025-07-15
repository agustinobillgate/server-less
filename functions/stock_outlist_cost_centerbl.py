#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def stock_outlist_cost_centerbl(cost_center:string):

    prepare_cache ([Gl_acct])

    fibukonto = ""
    bezeich = ""
    avail_gl_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fibukonto, bezeich, avail_gl_acct, gl_acct
        nonlocal cost_center

        return {"fibukonto": fibukonto, "bezeich": bezeich, "avail_gl_acct": avail_gl_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_center)]})

    if gl_acct:
        avail_gl_acct = True
        fibukonto = gl_acct.fibukonto
        bezeich = gl_acct.bezeich

    return generate_output()