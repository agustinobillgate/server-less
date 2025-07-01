#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def ins_storerequest_check_glacctbl(t_fibu:string):

    prepare_cache ([Gl_acct])

    avail_gl_acct = False
    gl_bezeich = ""
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, gl_bezeich, gl_acct
        nonlocal t_fibu

        return {"avail_gl_acct": avail_gl_acct, "gl_bezeich": gl_bezeich}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, t_fibu)]})

    if gl_acct:
        avail_gl_acct = True
        gl_bezeich = gl_acct.bezeich

    return generate_output()