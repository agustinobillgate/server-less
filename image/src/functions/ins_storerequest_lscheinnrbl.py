from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def ins_storerequest_lscheinnrbl(casetype:int, lscheinnr:str):
    err = 0
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, l_ophdr


        return {"err": err}


    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "REQ")).first()

    if casetype == 1:

        l_ophdr = db_session.query(L_ophdr).first()
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr

        l_ophdr = db_session.query(L_ophdr).first()

    elif casetype == 2:

        if l_ophdr:
            err = 1

            return generate_output()