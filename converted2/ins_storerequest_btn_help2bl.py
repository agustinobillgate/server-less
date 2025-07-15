#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr, Gl_acct

def ins_storerequest_btn_help2bl(lscheinnr:string, cost_acct:string):

    prepare_cache ([Gl_acct])

    cost_center = ""
    avail_gl_acct = False
    l_ophdr = gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_center, avail_gl_acct, l_ophdr, gl_acct
        nonlocal lscheinnr, cost_acct

        return {"cost_center": cost_center, "avail_gl_acct": avail_gl_acct}


    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "req")]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if gl_acct:
        cost_center = gl_acct.bezeich
        avail_gl_acct = True

    return generate_output()