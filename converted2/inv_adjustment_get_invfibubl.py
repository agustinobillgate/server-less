#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Gl_acct

def inv_adjustment_get_invfibubl(artnr:int):

    prepare_cache ([L_artikel, Gl_acct])

    fibukonto = ""
    cost_alloc = ""
    flag = False
    l_artikel = gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fibukonto, cost_alloc, flag, l_artikel, gl_acct
        nonlocal artnr

        return {"fibukonto": fibukonto, "cost_alloc": cost_alloc, "flag": flag}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

    if l_artikel:

        if l_artikel.fibukonto.lower()  != ("00000000").lower()  and l_artikel.fibukonto.lower()  != ("0000000000").lower()  and l_artikel.fibukonto.lower()  != "" and not matches(l_artikel.fibukonto.lower() ,r"* *"):
            fibukonto = l_artikel.fibukonto

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct:
                cost_alloc = gl_acct.bezeich
            flag = True

        elif l_artikel.fibukonto == "" or l_artikel.fibukonto == " ":
            fibukonto = "00000000"

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct:
                cost_alloc = gl_acct.bezeich
            flag = True

    return generate_output()