#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_bestand

def ins_storerequest_btn_help1bl(s_artnr:int, curr_lager:int):

    prepare_cache ([L_artikel, L_bestand])

    description = ""
    stock_oh = to_decimal("0.0")
    price = to_decimal("0.0")
    l_artikel = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, stock_oh, price, l_artikel, l_bestand
        nonlocal s_artnr, curr_lager

        return {"description": description, "stock_oh": stock_oh, "price": price}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")
    price =  to_decimal(l_artikel.vk_preis)

    return generate_output()