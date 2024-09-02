from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr, Gl_acct

def ins_storerequest_btn_help2bl(lscheinnr:str, cost_acct:str):
    cost_center = ""
    avail_gl_acct = False
    l_ophdr = gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_center, avail_gl_acct, l_ophdr, gl_acct


        return {"cost_center": cost_center, "avail_gl_acct": avail_gl_acct}


    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "REQ")).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if gl_acct:
        cost_center = gl_acct.bezeich
        avail_gl_acct = True

    return generate_output()