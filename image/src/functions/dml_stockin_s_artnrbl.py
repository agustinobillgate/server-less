from functions.additional_functions import *
import decimal
from models import L_artikel, L_bestand

def dml_stockin_s_artnrbl(s_artnr:int, curr_lager:int):
    stock_oh = 0
    description = ""
    l_artikel = l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, description, l_artikel, l_bestand


        return {"stock_oh": stock_oh, "description": description}


    l_artikel = db_session.query(L_artikel).filter(
            (l_artikel.artnr == s_artnr)).first()

    l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0
    description = trim(l_artikel.bezeich) + " - " +\
            to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()