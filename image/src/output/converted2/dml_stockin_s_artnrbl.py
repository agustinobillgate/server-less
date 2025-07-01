#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_bestand

def dml_stockin_s_artnrbl(s_artnr:int, curr_lager:int):

    prepare_cache ([L_artikel, L_bestand])

    stock_oh = to_decimal("0.0")
    description = ""
    l_artikel = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, description, l_artikel, l_bestand
        nonlocal s_artnr, curr_lager

        return {"stock_oh": stock_oh, "description": description}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")
    description = trim(l_artikel.bezeich) + " - " +\
            to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()