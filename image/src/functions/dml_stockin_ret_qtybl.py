from functions.additional_functions import *
import decimal
from models import L_bestand, Htparam

def dml_stockin_ret_qtybl(s_artnr:int, curr_lager:int, qty:decimal):
    rest = 0
    fl_code = 0
    htparam_paramgruppe = 0
    htparam_flogical = False
    l_bestand = htparam = None

    l_oh = None

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, fl_code, htparam_paramgruppe, htparam_flogical, l_bestand, htparam
        nonlocal l_oh


        nonlocal l_oh
        return {"rest": rest, "fl_code": fl_code, "htparam_paramgruppe": htparam_paramgruppe, "htparam_flogical": htparam_flogical}


    if qty < 0:

        l_oh = db_session.query(L_oh).filter(
                (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == curr_lager)).first()

        if l_oh and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty) < 0:
            rest = (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty)
            fl_code = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 402)).first()
    htparam_paramgruppe = htparam.paramgruppe
    htparam_flogical = htparam.flogical

    return generate_output()