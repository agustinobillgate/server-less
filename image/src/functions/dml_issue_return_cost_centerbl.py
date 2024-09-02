from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def dml_issue_return_cost_centerbl(cost_center:str):
    cost_acct = ""
    avail_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, avail_acct, gl_acct


        return {"cost_acct": cost_acct, "avail_acct": avail_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.bezeich) == (cost_center).lower())).first()

    if not gl_acct:
        avail_acct = True

        return generate_output()
    else:
        cost_acct = gl_acct.fibukonto
        cost_center = gl_acct.bezeich

    return generate_output()