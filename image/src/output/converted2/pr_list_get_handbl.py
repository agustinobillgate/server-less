#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand

def pr_list_get_handbl(artnr:int):

    prepare_cache ([L_bestand])

    soh = to_decimal("0.0")
    l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal soh, l_bestand
        nonlocal artnr

        return {"soh": soh}


    l_bestand = get_cache (L_bestand, {"artnr": [(eq, artnr)]})

    if l_bestand:
        soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    return generate_output()