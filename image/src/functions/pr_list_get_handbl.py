from functions.additional_functions import *
import decimal
from models import L_bestand

def pr_list_get_handbl(artnr:int):
    soh = 0
    l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal soh, l_bestand


        return {"soh": soh}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == artnr)).first()

    if l_bestand:
        soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    return generate_output()