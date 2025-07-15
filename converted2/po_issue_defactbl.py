#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, L_artikel

def po_issue_defactbl(stornogrund:string, s_artnr:int):

    prepare_cache ([Gl_acct, L_artikel])

    avail_gl = False
    cost_acct = ""
    gl_acct = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, cost_acct, gl_acct, l_artikel
        nonlocal stornogrund, s_artnr

        return {"avail_gl": avail_gl, "cost_acct": cost_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, trim(stornogrund))]})

    if gl_acct:
        cost_acct = gl_acct.fibukonto
        avail_gl = True
    else:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

        if l_artikel:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
                cost_acct = gl_acct.fibukonto
                avail_gl = True

    return generate_output()