from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def ins_storerequest_cost_centerbl(cost_center:str):
    g_fibukonto = ""
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_fibukonto, gl_acct


        return {"g_fibukonto": g_fibukonto}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.bezeich) == (cost_center).lower()) &  (Gl_acct.activeflag)).first()

    if not gl_acct or trim(cost_center) == "":

        return generate_output()
    g_fibukonto = gl_acct.fibukonto

    return generate_output()