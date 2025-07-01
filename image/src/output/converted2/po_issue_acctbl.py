#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, L_op

def po_issue_acctbl(case_type:int, cost_acct:string, docu_nr:string, lief_nr:int, created:bool):
    fl_code = 0
    avail_gl_acct = False
    gl_acct = l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, avail_gl_acct, gl_acct, l_op
        nonlocal case_type, cost_acct, docu_nr, lief_nr, created

        return {"fl_code": fl_code, "avail_gl_acct": avail_gl_acct}


    if case_type == 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if not gl_acct:
            fl_code = 1

            return generate_output()

        if not created:

            l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"lscheinnr": [(eq, lscheinnr)],"docu_nr": [(ne, docu_nr)]})

            if l_op:
                fl_code = 3

                return generate_output()

    elif case_type == 2:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if not gl_acct:
            avail_gl_acct = False

            return generate_output()
        else:
            avail_gl_acct = True

    return generate_output()