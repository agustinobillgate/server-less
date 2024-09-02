from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_op

def po_stockin_mi_allbl(lscheinnr:str, docu_nr:str):
    fl_code = 0
    l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, l_op


        return {"fl_code": fl_code}


    l_op = db_session.query(L_op).filter(
            (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_op.(docu_nr).lower()) != (docu_nr).lower())).first()

    if l_op:
        fl_code = 1

        return generate_output()