from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def ins_storerequest_check_glacctbl(t_fibu:str):
    avail_gl_acct = False
    gl_bezeich = ""
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, gl_bezeich, gl_acct


        return {"avail_gl_acct": avail_gl_acct, "gl_bezeich": gl_bezeich}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (t_fibu).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        gl_bezeich = gl_acct.bezeich

    return generate_output()