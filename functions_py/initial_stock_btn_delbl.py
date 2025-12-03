#using conversion tools version: 1.0.0.119

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


    # l_bestand = get_cache (L_bestand, {"artnr": [(eq, best_list_artnr)],"lager_nr": [(eq, 0)]})
    l_bestand = db_session.query(L_bestand).filter(
        L_bestand.artnr == best_list_artnr,
        L_bestand.lager_nr == 0
    ).with_for_update().first()

    l_bestand.anz_anf_best =  to_decimal(l_bestand.anz_anf_best) - best_list_anz_anf_best
    l_bestand.val_anf_best =  to_decimal(l_bestand.val_anf_best) - best_list_val_anf_best

    l_artikel = db_session.query(L_artikel).filter(
        L_artikel.artnr == l_bestand.artnr
    ).with_for_update().first()

    if l_bestand.anz_anf_best != 0:
        l_artikel.vk_preis =  to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)
    else:
        l_artikel.vk_preis =  to_decimal("0")

    l_bestand = db_session.query(L_bestand).filter(
        L_bestand.artnr == best_list_artnr,
        L_bestand.lager_nr == best_list_lager_nr
    ).with_for_update().first()

    db_session.delete(l_bestand)

    return generate_output()