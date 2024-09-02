from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, L_bestand

def s_stockiss_curr_artnrbl(fibu:str, curr_lager:int, s_artnr:int):
    avail_gl = False
    stock_oh = 0
    cost_acct = ""
    gl_acct = l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl, stock_oh, cost_acct, gl_acct, l_bestand


        return {"avail_gl": avail_gl, "stock_oh": stock_oh, "cost_acct": cost_acct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()

    if gl_acct and (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):
        cost_acct = gl_acct.fibukonto
        avail_gl = True

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0

    return generate_output()