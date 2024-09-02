from functions.additional_functions import *
import decimal
from models import L_bestand

def s_stockins_return_qtybl(curr_lager:int, s_artnr:int, qty:decimal):
    err_code = 0
    rest = 0
    l_bestand = None

    l_oh = None

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, rest, l_bestand
        nonlocal l_oh


        nonlocal l_oh
        return {"err_code": err_code, "rest": rest}


    l_oh = db_session.query(L_oh).filter(
            (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == curr_lager)).first()

    if l_oh and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty) < 0:
        err_code = 1
        rest = (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty)

        return generate_output()