#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Htparam

def po_issue_btn_helpbl(cost_acct:string):

    prepare_cache ([Gl_acct, Htparam])

    cost_center = ""
    jobnr = 0
    flag = 0
    avail_glacct = False
    gl_acct = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_center, jobnr, flag, avail_glacct, gl_acct, htparam
        nonlocal cost_acct

        return {"cost_center": cost_center, "jobnr": jobnr, "flag": flag, "avail_glacct": avail_glacct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

    if gl_acct:
        avail_glacct = True
        cost_center = gl_acct.bezeich
        jobnr = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 933)]})

        if gl_acct.main_nr == htparam.finteger and gl_acct.main_nr != 0:
            flag = 1

        return generate_output()

    return generate_output()