from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_op

def po_issue_chk_l_opbl(lscheinnr:str, docu_nr:str):
    avail_l_op = False
    l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_op, l_op


        return {"avail_l_op": avail_l_op}


    l_op = db_session.query(L_op).filter(
            (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_op.(docu_nr).lower()) != (docu_nr).lower())).first()

    if l_op:
        avail_l_op = True

    return generate_output()