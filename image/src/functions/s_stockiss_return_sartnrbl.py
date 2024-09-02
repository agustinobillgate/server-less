from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def s_stockiss_return_sartnrbl(fibu:str):
    avail_gl = False
    cost_acct = ""
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, cost_acct, gl_acct


        return {"avail_gl": avail_gl, "cost_acct": cost_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()

    if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
        cost_acct = gl_acct.fibukonto
        avail_gl = True

    return generate_output()