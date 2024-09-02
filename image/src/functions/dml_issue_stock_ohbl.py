from functions.additional_functions import *
import decimal
from models import L_artikel, L_bestand

def dml_issue_stock_ohbl(curr_lager:int, s_artnr:int):
    stock_oh = 0
    l_art_bezeich = ""
    l_art_masseinheit = ""
    l_artikel = l_bestand = None

    l_art = None

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, l_art_bezeich, l_art_masseinheit, l_artikel, l_bestand
        nonlocal l_art


        nonlocal l_art
        return {"stock_oh": stock_oh, "l_art_bezeich": l_art_bezeich, "l_art_masseinheit": l_art_masseinheit}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0

    l_art = db_session.query(L_art).filter(
            (L_art.artnr == s_artnr)).first()

    l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0
    l_art_bezeich = l_art.bezeich
    l_art_masseinheit = l_art.masseinheit

    return generate_output()