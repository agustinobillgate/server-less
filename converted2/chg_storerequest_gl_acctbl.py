#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def chg_storerequest_gl_acctbl(acct:string):

    prepare_cache ([Gl_acct])

    t_desc = ""
    avail_gl_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_desc, avail_gl_acct, gl_acct
        nonlocal acct

        return {"t_desc": t_desc, "avail_gl_acct": avail_gl_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})

    if gl_acct:
        avail_gl_acct = True
        t_desc = gl_acct.bezeich

    return generate_output()