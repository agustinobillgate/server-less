from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_op

def s_stockin_return_lscheinnrbl(lscheinnr:str):
    err_code = 0
    l_op = None

    l_op1 = None

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_op
        nonlocal l_op1


        nonlocal l_op1
        return {"err_code": err_code}


    l_op1 = db_session.query(L_op1).filter(
            (L_op1.op_art == 1) &  (L_op1.loeschflag <= 1) &  (func.lower(L_op1.(lscheinnr).lower()) == (lscheinnr).lower())).first()

    if l_op1:
        err_code = 1

        return generate_output()