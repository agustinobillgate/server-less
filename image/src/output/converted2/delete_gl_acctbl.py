from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def delete_gl_acctbl(case_type:int, int1:int, char1:str):
    success_flag = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_acct
        nonlocal case_type, int1, char1

        return {"success_flag": success_flag}


    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                 (func.lower(Gl_acct.fibukonto) == (char1).lower())).first()

        if gl_acct:
            db_session.delete(gl_acct)
            pass
            success_flag = True

    return generate_output()