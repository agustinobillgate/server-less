#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_bestand

def s_transform_stock_ohbl(curr_lager:int, s_artnr:int):

    prepare_cache ([L_artikel, L_bestand])

    stock_oh = to_decimal("0.0")
    description = ""
    price = to_decimal("0.0")
    l_artikel_artnr = 0
    l_artikel = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, description, price, l_artikel_artnr, l_artikel, l_bestand
        nonlocal curr_lager, s_artnr

        return {"stock_oh": stock_oh, "description": description, "price": price, "l_artikel_artnr": l_artikel_artnr}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit
    price =  to_decimal(l_artikel.vk_preis)
    l_artikel_artnr = l_artikel.artnr

    return generate_output()