from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def mk_pr_read_glacctbl(acct:str):
    err_code = 0
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct


        return {"err_code": err_code}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

    if gl_acct.acc_type == 1:
        err_code = 1

    return generate_output()