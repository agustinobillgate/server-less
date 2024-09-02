from functions.additional_functions import *
import decimal
from models import L_bestand, Htparam

def dml_issue_return_qtybl(qty:decimal, s_artnr:int, curr_lager:int):
    rest = 0
    err_code = 0
    l_bestand = htparam = None

    l_oh = None

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, err_code, l_bestand, htparam
        nonlocal l_oh


        nonlocal l_oh
        return {"rest": rest, "err_code": err_code}


    if qty < 0:

        l_oh = db_session.query(L_oh).filter(
                (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == curr_lager)).first()

        if l_oh and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty) < 0:
            err_code = 1
            rest = (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty)

            return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 402)).first()

    if htparam.paramgruppe == 15:
        err_code = 2

        return generate_output()

    if not htparam.flogical:
        err_code = 3

        return generate_output()