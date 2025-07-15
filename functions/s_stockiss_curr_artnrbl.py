#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, L_bestand

def s_stockiss_curr_artnrbl(fibu:string, curr_lager:int, s_artnr:int):

    prepare_cache ([Gl_acct, L_bestand])

    avail_gl = False
    stock_oh = to_decimal("0.0")
    cost_acct = ""
    gl_acct = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, stock_oh, cost_acct, gl_acct, l_bestand
        nonlocal fibu, curr_lager, s_artnr

        return {"avail_gl": avail_gl, "stock_oh": stock_oh, "cost_acct": cost_acct}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

    if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
        cost_acct = gl_acct.fibukonto
        avail_gl = True

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")

    return generate_output()