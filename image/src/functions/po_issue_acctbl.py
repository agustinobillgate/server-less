from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, L_op

def po_issue_acctbl(case_type:int, cost_acct:str, docu_nr:str, lief_nr:int, created:bool):
    fl_code = 0
    avail_gl_acct = False
    gl_acct = l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, avail_gl_acct, gl_acct, l_op


        return {"fl_code": fl_code, "avail_gl_acct": avail_gl_acct}


    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

        if not gl_acct:
            fl_code = 1

            return generate_output()

        if not created:

            l_op = db_session.query(L_op).filter(
                    (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.lscheinnr == lscheinnr) &  (func.lower(L_op.(docu_nr).lower()) != (docu_nr).lower())).first()

            if l_op:
                fl_code = 3

                return generate_output()

    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

        if not gl_acct:
            avail_gl_acct = False

            return generate_output()
        else:
            avail_gl_acct = True

    return generate_output()