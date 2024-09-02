from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def dml_issue_curr_select_costbl(cost_acct:str):
    a_bez = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_bez, avail_gl_acct, gl_acct


        return {"a_bez": a_bez, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich

    return generate_output()