#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op

def direct_autodeduct_check_outgoingbl(bill_date:date):
    avail_deduct = False
    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_deduct, l_op
        nonlocal bill_date

        return {"avail_deduct": avail_deduct}


    l_op = db_session.query(L_op).filter(
             (L_op.datum == bill_date) & (L_op.op_art == 3) & ((substring(L_op.lscheinnr, 0, 3)) == ("SAD").lower()) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).first()

    if l_op:
        avail_deduct = True

    return generate_output()