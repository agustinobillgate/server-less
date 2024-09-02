from functions.additional_functions import *
import decimal
from models import L_bestand

def s_stockin_return_sartnrbl(curr_lager:int, s_artnr:int):
    stock_oh = 0
    l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, l_bestand


        return {"stock_oh": stock_oh}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
    else:
        stock_oh = 0

    return generate_output()