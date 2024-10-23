from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def gl_acct_admin_if_foundbl(fibukonto:str):
    success_flag = False
    i:int = 0
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i, gl_acct
        nonlocal fibukonto


        return {"success_flag": success_flag}


    gl_acct = db_session.query(Gl_acct).filter(
             (func.lower(Gl_acct.fibukonto) == (fibukonto).lower())).first()

    if gl_acct:
        for i in range(1,12 + 1) :

            if gl_acct.budget[i - 1] > 0:
                gl_acct.budget[i - 1] = - gl_acct.budget[i - 1]

            if gl_acct.ly_budget[i - 1] > 0:
                gl_acct.ly_budget[i - 1] = - gl_acct.ly_budget[i - 1]

            if gl_acct.debit[i - 1] > 0:
                gl_acct.debit[i - 1] = - gl_acct.debit[i - 1]
        success_flag = True

    return generate_output()