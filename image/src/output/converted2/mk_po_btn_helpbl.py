#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def mk_po_btn_helpbl(acct:string):
    cost_acct = ""
    avail_gl_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, avail_gl_acct, gl_acct
        nonlocal acct

        return {"cost_acct": cost_acct, "avail_gl_acct": avail_gl_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})

    if gl_acct:
        cost_acct = acct
        avail_gl_acct = True

    return generate_output()