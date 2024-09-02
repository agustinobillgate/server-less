from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Parameters

def s_stockiss_return_costacctbl(cost_acct:str):
    err_code = 0
    gl_acct = parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct, parameters


        return {"err_code": err_code}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if not gl_acct:
        err_code = 1

        return generate_output()

    if gl_acct:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Alloc") &  (Parameters.varname > "") &  (Parameters.vstring == gl_acct.fibukonto)).first()

        if not parameters:
            err_code = 2

            return generate_output()