#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def s_storerequest_glacctbl(acct:string):

    prepare_cache ([Gl_acct])

    a_bez = ""
    a_fibu = ""
    avail_gl_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_bez, a_fibu, avail_gl_acct, gl_acct
        nonlocal acct

        return {"a_bez": a_bez, "a_fibu": a_fibu, "avail_gl_acct": avail_gl_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich
        a_fibu = gl_acct.fibukonto

    return generate_output()