#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Htparam

def s_stockiss_gl_acctbl(acct:string):

    prepare_cache ([Gl_acct, Htparam])

    avail_gl_acct = False
    a_bez = ""
    a_main_nr = 0
    p_933 = 0
    gl_acct = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_acct, a_bez, a_main_nr, p_933, gl_acct, htparam
        nonlocal acct

        return {"avail_gl_acct": avail_gl_acct, "a_bez": a_bez, "a_main_nr": a_main_nr, "p_933": p_933}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})

    if gl_acct:
        avail_gl_acct = True
        a_bez = gl_acct.bezeich
        a_main_nr = gl_acct.main_nr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 933)]})
        p_933 = htparam.finteger

    return generate_output()