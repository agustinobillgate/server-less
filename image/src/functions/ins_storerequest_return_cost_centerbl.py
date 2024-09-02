from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def ins_storerequest_return_cost_centerbl(cost_center:str):
    avail_glacct = False
    gl_acct_fibukonto = ""
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_glacct, gl_acct_fibukonto, gl_acct


        return {"avail_glacct": avail_glacct, "gl_acct_fibukonto": gl_acct_fibukonto}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.bezeich) == (cost_center).lower()) &  (Gl_acct.activeflag)).first()

    if not gl_acct or trim(cost_center) == "":
        avail_glacct = False
    else:
        gl_acct_fibukonto = gl_acct.fibukonto

    return generate_output()