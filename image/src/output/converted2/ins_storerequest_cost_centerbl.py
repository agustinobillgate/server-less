#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def ins_storerequest_cost_centerbl(cost_center:string):

    prepare_cache ([Gl_acct])

    g_fibukonto = ""
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_fibukonto, gl_acct
        nonlocal cost_center

        return {"g_fibukonto": g_fibukonto}


    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.bezeich == (cost_center).lower()) & (Gl_acct.activeflag)).first()

    if not gl_acct or trim(cost_center) == "":

        return generate_output()
    g_fibukonto = gl_acct.fibukonto

    return generate_output()