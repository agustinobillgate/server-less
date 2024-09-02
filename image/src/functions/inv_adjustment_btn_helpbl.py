from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def inv_adjustment_btn_helpbl(cost_acct:str):
    avail_gl_acct = False
    a_bez = ""
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, a_bez, gl_acct


        return {"avail_gl_acct": avail_gl_acct, "a_bez": a_bez}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich

    return generate_output()