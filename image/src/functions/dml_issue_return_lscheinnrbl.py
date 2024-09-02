from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def dml_issue_return_lscheinnrbl(lscheinnr:str):
    err_code = False
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_ophdr


        return {"err_code": err_code}


    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

    if l_ophdr:
        err_code = True

    return generate_output()