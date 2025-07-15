#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand

def s_stockout_l_bestandbl(curr_lager:int, s_artnr:int):

    prepare_cache ([L_bestand])

    stock_oh = to_decimal("0.0")
    avail_l_bestand = False
    l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, avail_l_bestand, l_bestand
        nonlocal curr_lager, s_artnr

        return {"stock_oh": stock_oh, "avail_l_bestand": avail_l_bestand}


    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        avail_l_bestand = True
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    return generate_output()