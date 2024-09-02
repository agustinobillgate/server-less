from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr

def check_stockdatebl(billdate:date):
    err_code = 0
    gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_jouhdr


        return {"err_code": err_code}


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jtype == 6) &  (Gl_jouhdr.datum >= billdate)).first()

    if gl_jouhdr:
        err_code = 1

    return generate_output()