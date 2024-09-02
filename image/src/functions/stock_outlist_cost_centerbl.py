from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def stock_outlist_cost_centerbl(cost_center:str):
    fibukonto = ""
    bezeich = ""
    avail_gl_acct = False
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fibukonto, bezeich, avail_gl_acct, gl_acct


        return {"fibukonto": fibukonto, "bezeich": bezeich, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_center).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        fibukonto = gl_acct.fibukonto
        bezeich = gl_acct.bezeich

    return generate_output()