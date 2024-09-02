from functions.additional_functions import *
import decimal
from datetime import date
from models import Gc_piacct, Gl_acct, Htparam

def mk_gcpi_check1abl(pvilanguage:int, pay_acctno:str):
    gc_piacct_bezeich = ""
    p_558 = None
    msg_str = ""
    lvcarea:str = "mk_gcPI"
    gc_piacct = gl_acct = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_piacct_bezeich, p_558, msg_str, lvcarea, gc_piacct, gl_acct, htparam


        return {"gc_piacct_bezeich": gc_piacct_bezeich, "p_558": p_558, "msg_str": msg_str}


    if pay_acctno != "":

        gc_piacct = db_session.query(Gc_piacct).filter(
                (gc_PIacct.fibukonto == pay_acctno)).first()

        if not gc_PIacct:
            msg_str = msg_str + chr(2) + translateExtended ("PI Payment Account Number not found.", lvcarea, "")

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == pay_acctno)).first()

        if not gl_acct:
            msg_str = msg_str + chr(2) + translateExtended ("GL Account Number not found.", lvcarea, "")

            return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    p_558 = htparam.fdate
    gc_piacct_bezeich = gc_PIacct.bezeich

    return generate_output()