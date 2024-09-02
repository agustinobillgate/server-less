from functions.additional_functions import *
import decimal
from models import L_artikel, L_bestand

def ins_storerequest_btn_help1bl(s_artnr:int, curr_lager:int):
    description = ""
    stock_oh = 0
    price = 0
    l_artikel = l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, stock_oh, price, l_artikel, l_bestand


        return {"description": description, "stock_oh": stock_oh, "price": price}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0
    price = l_artikel.vk_preis

    return generate_output()