#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand

def initial_stock_check_l_bestandbl(l_artikel_artnr:int, curr_lager:int):

    prepare_cache ([L_bestand])

    do_it = False
    l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, l_bestand
        nonlocal l_artikel_artnr, curr_lager

        return {"do_it": do_it}


    l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel_artnr)],"lager_nr": [(eq, curr_lager)]})

    if l_bestand and (l_bestand.anz_anf_best != 0 or l_bestand.anz_eingang != 0 or l_bestand.anz_ausgang != 0):
        do_it = True

    return generate_output()