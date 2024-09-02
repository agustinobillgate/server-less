from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def chg_storerequest_gl_acctbl(acct:str):
    t_desc = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_desc, avail_gl_acct, gl_acct


        return {"t_desc": t_desc, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        t_desc = gl_acct.bezeich

    return generate_output()