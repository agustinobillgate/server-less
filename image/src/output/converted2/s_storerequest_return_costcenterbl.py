#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def s_storerequest_return_costcenterbl(cost_center:string):

    prepare_cache ([Gl_acct])

    a_fibu = ""
    avail_gl_acct = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_fibu, avail_gl_acct, gl_acct
        nonlocal cost_center

        return {"a_fibu": a_fibu, "avail_gl_acct": avail_gl_acct}


    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.bezeich == (cost_center).lower()) & (Gl_acct.activeflag)).first()

    if gl_acct:
        a_fibu = gl_acct.fibukonto
        avail_gl_acct = True

    return generate_output()