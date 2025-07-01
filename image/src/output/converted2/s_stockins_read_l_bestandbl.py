#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand

def s_stockins_read_l_bestandbl(curr_lager:int, s_artnr:int):

    prepare_cache ([L_bestand])

    stock_oh = to_decimal("0.0")
    l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, l_bestand
        nonlocal curr_lager, s_artnr

        return {"stock_oh": stock_oh}


    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
    else:
        stock_oh =  to_decimal("0")

    return generate_output()