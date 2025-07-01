#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_piacct, Gl_acct, Htparam

def mk_gcpi_check1abl(pvilanguage:int, pay_acctno:string):

    prepare_cache ([Gc_piacct, Htparam])

    gc_piacct_bezeich = ""
    p_558 = None
    msg_str = ""
    lvcarea:string = "mk-gcPI"
    gc_piacct = gl_acct = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_piacct_bezeich, p_558, msg_str, lvcarea, gc_piacct, gl_acct, htparam
        nonlocal pvilanguage, pay_acctno

        return {"gc_piacct_bezeich": gc_piacct_bezeich, "p_558": p_558, "msg_str": msg_str}


    if pay_acctno != "":

        gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, pay_acctno)]})

        if not gc_piacct:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("PI Payment Account Number not found.", lvcarea, "")

            return generate_output()
        else:
            gc_piacct_bezeich = gc_piacct.bezeich

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pay_acctno)]})

        if not gl_acct:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("GL Account Number not found.", lvcarea, "")

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    p_558 = htparam.fdate

    return generate_output()