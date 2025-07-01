#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def gl_acct_admin_if_foundbl(fibukonto:string):

    prepare_cache ([Gl_acct])

    success_flag = False
    i:int = 0
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i, gl_acct
        nonlocal fibukonto

        return {"success_flag": success_flag}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

    if gl_acct:
        for i in range(1,12 + 1) :

            if gl_acct.budget[i - 1] > 0:
                gl_acct.budget[i - 1] = - gl_acct.budget[i - 1]

            if gl_acct.ly_budget[i - 1] > 0:
                gl_acct.ly_budget[i - 1] = - gl_acct.ly_budget[i - 1]

            if gl_acct.debit[i - 1] > 0:
                gl_acct.debit[i - 1] = - gl_acct.debit[i - 1]
        success_flag = True

    return generate_output()