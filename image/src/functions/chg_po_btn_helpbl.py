from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def chg_po_btn_helpbl(acct:str):
    cost_acct = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, avail_gl_acct, gl_acct


        return {"cost_acct": cost_acct, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

    if gl_acct:
        cost_acct = acct
        avail_gl_acct = True

    return generate_output()