from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def s_storerequest_return_costcenterbl(cost_center:str):
    a_fibu = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_fibu, avail_gl_acct, gl_acct


        return {"a_fibu": a_fibu, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.bezeich) == (cost_center).lower()) &  (Gl_acct.activeflag)).first()

    if gl_acct:
        a_fibu = gl_acct.fibukonto
        avail_gl_acct = True

    return generate_output()