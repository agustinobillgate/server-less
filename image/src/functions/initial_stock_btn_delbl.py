from functions.additional_functions import *
import decimal
from models import L_bestand, L_artikel

def initial_stock_btn_delbl(best_list_artnr:int, best_list_lager_nr:int, best_list_anz_anf_best:decimal, best_list_val_anf_best:decimal):
    l_bestand = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_bestand, l_artikel


        return {}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == best_list_artnr) &  (L_bestand.lager_nr == 0)).first()
    l_bestand.anz_anf_best = l_bestand.anz_anf_best -
    best_list_anz_anf_best
    l_bestand.val_anf_best = l_bestand.val_anf_best -
    best_list_val_anf_best

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == l_bestand.artnr)).first()

    if l_bestand.anz_anf_best != 0:
        l_artikel.vk_preis = l_bestand.val_anf_best / l_bestand.anz_anf_best
    else:
        l_artikel.vk_preis = 0

    l_artikel = db_session.query(L_artikel).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == best_list_artnr) &  (L_bestand.lager_nr == best_list_lager_nr)).first()
    db_session.delete(l_bestand)

    return generate_output()