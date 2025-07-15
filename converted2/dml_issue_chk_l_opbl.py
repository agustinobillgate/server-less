#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_ophis

def dml_issue_chk_l_opbl(lscheinnr:string, docu_nr:string):
    avail_l_op = False
    l_op = l_ophis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_op, l_op, l_ophis
        nonlocal lscheinnr, docu_nr

        return {"avail_l_op": avail_l_op}

    avail_l_op = True

    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"lscheinnr": [(eq, lscheinnr)]})

    if l_op:
        avail_l_op = False
    else:

        l_ophis = get_cache (L_ophis, {"op_art": [(eq, 1)],"lscheinnr": [(eq, lscheinnr)]})

        if l_ophis:
            avail_l_op = False

    return generate_output()