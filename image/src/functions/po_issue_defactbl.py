from functions.additional_functions import *
import decimal
from models import Gl_acct, L_artikel

def po_issue_defactbl(stornogrund:str, s_artnr:int):
    avail_gl = False
    cost_acct = ""
    gl_acct = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, cost_acct, gl_acct, l_artikel


        return {"avail_gl": avail_gl, "cost_acct": cost_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == trim(stornogrund))).first()

    if gl_acct:
        cost_acct = gl_acct.fibukonto
        avail_gl = True
    else:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()

        if l_artikel:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

            if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
                cost_acct = gl_acct.fibukonto
                avail_gl = True

    return generate_output()