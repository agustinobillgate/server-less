from functions.additional_functions import *
import decimal
from models import L_artikel, L_bestand

def s_transform_stock_ohbl(curr_lager:int, s_artnr:int):
    stock_oh = 0
    description = ""
    price = 0
    l_artikel_artnr = 0
    l_artikel = l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, description, price, l_artikel_artnr, l_artikel, l_bestand


        return {"stock_oh": stock_oh, "description": description, "price": price, "l_artikel_artnr": l_artikel_artnr}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit
    price = l_artikel.vk_preis
    l_artikel_artnr = l_artikel.artnr

    return generate_output()