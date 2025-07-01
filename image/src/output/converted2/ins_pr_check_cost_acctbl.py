#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def ins_pr_check_cost_acctbl(pvilanguage:int, cost_acct:string):

    prepare_cache ([Gl_acct])

    msg_str = ""
    lvcarea:string = "ins-pr"
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_acct
        nonlocal pvilanguage, cost_acct

        return {"msg_str": msg_str}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if not gl_acct:
        msg_str = translateExtended ("Account Number incorrect.", lvcarea, "")

    if gl_acct and gl_acct.acc_type == 1:
        msg_str = translateExtended ("Wrong Type of Account Number.", lvcarea, "")

    return generate_output()