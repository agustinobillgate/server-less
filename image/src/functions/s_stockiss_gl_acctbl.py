from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Htparam

def s_stockiss_gl_acctbl(acct:str):
    avail_gl_acct = False
    a_bez = ""
    a_main_nr = 0
    p_933 = 0
    gl_acct = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, a_bez, a_main_nr, p_933, gl_acct, htparam


        return {"avail_gl_acct": avail_gl_acct, "a_bez": a_bez, "a_main_nr": a_main_nr, "p_933": p_933}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich
        a_main_nr = gl_acct.main_nr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 933)).first()
        p_933 = htparam.finteger

    return generate_output()