#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def ins_storerequest_return_cost_centerbl(cost_center:string):

    prepare_cache ([Gl_acct])

    avail_glacct = True
    gl_acct_fibukonto = ""
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_glacct, gl_acct_fibukonto, gl_acct
        nonlocal cost_center

        return {"avail_glacct": avail_glacct, "gl_acct_fibukonto": gl_acct_fibukonto}


    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.bezeich == (cost_center).lower()) & (Gl_acct.activeflag)).first()

    if not gl_acct or trim(cost_center) == "":
        avail_glacct = False
    else:
        gl_acct_fibukonto = gl_acct.fibukonto

    return generate_output()