#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op

def s_stockout_ret_sartnrbl(s_artnr:int, transdate:date):
    avail_l_op = False
    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_op, l_op
        nonlocal s_artnr, transdate

        return {"avail_l_op": avail_l_op}


    l_op = db_session.query(L_op).filter(
             (L_op.artnr == s_artnr) & (L_op.datum == transdate) & ((L_op.op_art == 3) | (L_op.op_art == 4)) & (substring(L_op.lscheinnr, 3, (length(L_op.lscheinnr) - 3)) == substring(lscheinnr, 3, (length(lscheinnr) - 3)))).first()

    if l_op:
        avail_l_op = True

    return generate_output()