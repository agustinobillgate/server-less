#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_bestand

def dml_issue_stock_ohbl(curr_lager:int, s_artnr:int):

    prepare_cache ([L_artikel, L_bestand])

    stock_oh = to_decimal("0.0")
    l_art_bezeich = ""
    l_art_masseinheit = ""
    l_artikel = l_bestand = None

    l_art = None

    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, l_art_bezeich, l_art_masseinheit, l_artikel, l_bestand
        nonlocal curr_lager, s_artnr
        nonlocal l_art


        nonlocal l_art

        return {"stock_oh": stock_oh, "l_art_bezeich": l_art_bezeich, "l_art_masseinheit": l_art_masseinheit}


    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")

    l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")
    l_art_bezeich = l_art.bezeich
    l_art_masseinheit = l_art.masseinheit

    return generate_output()