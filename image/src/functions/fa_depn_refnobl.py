from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_jouhdr

def fa_depn_refnobl(refno:str):
    err_no = 0
    gl_jouhdr = None

    gl_jouhdr1 = None

    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, gl_jouhdr
        nonlocal gl_jouhdr1


        nonlocal gl_jouhdr1
        return {"err_no": err_no}


    gl_jouhdr1 = db_session.query(Gl_jouhdr1).filter(
            (func.lower(Gl_jouhdr1.(refno).lower()) == (refno).lower()) &  (Gl_jouhdr1.jtype == 7)).first()

    if gl_jouhdr1:
        err_no = 1

    return generate_output()