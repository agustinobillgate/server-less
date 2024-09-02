from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def s_storerequest_new_lscheinnrbl(lscheinnr:str, s:str, recid_l_ophdr:int):
    i:int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal l_ophdr1


        nonlocal l_ophdr1
        return {}


    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == recid_l_ophdr)).first()

    l_ophdr1 = db_session.query(L_ophdr1).filter(
            (func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "REQ")).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "REQ")).first()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.docu_nr = lscheinnr
    l_ophdr.lscheinnr = lscheinnr
    l_ophdr.op_typ = "REQ"

    l_ophdr = db_session.query(L_ophdr).first()


    return generate_output()