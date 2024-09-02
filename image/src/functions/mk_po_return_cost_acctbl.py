from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def mk_po_return_cost_acctbl(cost_acct:str):
    err_code = 0
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct


        return {"err_code": err_code}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if not gl_acct:
        err_code = 1

        return generate_output()

    if gl_acct and gl_acct.acc_type != 2 and gl_acct.acc_type != 3 and gl_acct.acc_type != 5:
        err_code = 2

        return generate_output()