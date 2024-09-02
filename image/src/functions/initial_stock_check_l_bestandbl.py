from functions.additional_functions import *
import decimal
from models import L_bestand

def initial_stock_check_l_bestandbl(l_artikel_artnr:int, curr_lager:int):
    do_it = False
    l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, l_bestand


        return {"do_it": do_it}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == l_artikel_artnr) &  (L_bestand.lager_nr == curr_lager)).first()

    if l_bestand and (l_bestand.anz_anf_best != 0 or l_bestand.anz_eingang != 0 or l_bestand.anz_ausgang != 0):
        do_it = True

    return generate_output()