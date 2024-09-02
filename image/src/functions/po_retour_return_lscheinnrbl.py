from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def po_retour_return_lscheinnrbl(lscheinnr:str, docu_nr:str):
    err_code = 0
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_ophdr


        return {"err_code": err_code}


    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI") &  (func.lower(L_ophdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if not l_ophdr:
        err_code = 1

        return generate_output()