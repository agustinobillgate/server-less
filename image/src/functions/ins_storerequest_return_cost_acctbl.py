from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def ins_storerequest_return_cost_acctbl(cost_acct:str):
    err_flag = 0
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, gl_acct


        return {"err_flag": err_flag}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if not gl_acct:
        err_flag = 1

        return generate_output()

    if gl_acct and gl_acct.acc_type != 2 and gl_acct.acc_type != 5:
        err_flag = 2

        return generate_output()