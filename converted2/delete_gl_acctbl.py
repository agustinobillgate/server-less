#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def delete_gl_acctbl(case_type:int, int1:int, char1:string):
    success_flag = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_acct
        nonlocal case_type, int1, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, char1)]})

        if gl_acct:
            db_session.delete(gl_acct)
            pass
            success_flag = True

    return generate_output()