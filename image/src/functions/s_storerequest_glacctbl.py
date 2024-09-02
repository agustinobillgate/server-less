from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def s_storerequest_glacctbl(acct:str):
    a_bez = ""
    a_fibu = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_bez, a_fibu, avail_gl_acct, gl_acct


        return {"a_bez": a_bez, "a_fibu": a_fibu, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich
        a_fibu = gl_acct.fibukonto

    return generate_output()