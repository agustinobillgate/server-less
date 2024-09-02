from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Parameters

def po_issue_check_acctbl(case_type:int, cost_acct:str):
    avail_gl_acct = False
    fl_code = 0
    gl_acct = parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, fl_code, gl_acct, parameters


        return {"avail_gl_acct": avail_gl_acct, "fl_code": fl_code}


    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

        if not gl_acct:
            fl_code = 1

            return generate_output()

        if gl_acct:

            parameters = db_session.query(Parameters).filter(
                    (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Alloc") &  (Parameters.varname > "") &  (Parameters.vstring == gl_acct.fibukonto)).first()

            if not parameters:
                fl_code = 2

                return generate_output()

    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

        if not gl_acct:

            return generate_output()
        else:
            avail_gl_acct = True

    return generate_output()