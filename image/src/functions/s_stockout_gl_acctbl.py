from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def s_stockout_gl_acctbl(cost_acct:str):
    avail_gl_acct = False
    err = 0
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, err, gl_acct


        return {"avail_gl_acct": avail_gl_acct, "err": err}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if not gl_acct:
        avail_gl_acct = False
    else:
        avail_gl_acct = True

    return generate_output()