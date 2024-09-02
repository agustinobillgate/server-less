from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def dml_stockin_l_ophdrbl(lscheinnr:str):
    avail_l_ophdr = False
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_ophdr, l_ophdr


        return {"avail_l_ophdr": avail_l_ophdr}


    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

    if l_ophdr:
        avail_l_ophdr = True

    return generate_output()