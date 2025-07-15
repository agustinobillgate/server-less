#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, L_artikel

def initial_stock_btn_delbl(best_list_artnr:int, best_list_lager_nr:int, best_list_anz_anf_best:Decimal, best_list_val_anf_best:Decimal):

    prepare_cache ([L_artikel])

    l_bestand = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_bestand, l_artikel
        nonlocal best_list_artnr, best_list_lager_nr, best_list_anz_anf_best, best_list_val_anf_best

        return {}


    l_bestand = get_cache (L_bestand, {"artnr": [(eq, best_list_artnr)],"lager_nr": [(eq, 0)]})
    l_bestand.anz_anf_best =  to_decimal(l_bestand.anz_anf_best) -
    best_list_anz_anf_best
    l_bestand.val_anf_best =  to_decimal(l_bestand.val_anf_best) -
    best_list_val_anf_best

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

    if l_bestand.anz_anf_best != 0:
        l_artikel.vk_preis =  to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)
    else:
        l_artikel.vk_preis =  to_decimal("0")
    pass

    l_bestand = get_cache (L_bestand, {"artnr": [(eq, best_list_artnr)],"lager_nr": [(eq, best_list_lager_nr)]})
    db_session.delete(l_bestand)

    return generate_output()