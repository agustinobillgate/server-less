from functions.additional_functions import *
import decimal
from models import L_bestand

def s_stockout_l_bestandbl(curr_lager:int, s_artnr:int):
    stock_oh = 0
    avail_l_bestand = False
    l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_oh, avail_l_bestand, l_bestand


        return {"stock_oh": stock_oh, "avail_l_bestand": avail_l_bestand}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        avail_l_bestand = True
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    return generate_output()