from functions.additional_functions import *
import decimal
from models import L_bestand

def s_stockiss_return_qtybl(s_artnr:int, curr_lager:int, qty:decimal):
    rest = 0
    avail_l_oh = False
    l_bestand = None

    l_oh = None

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, avail_l_oh, l_bestand
        nonlocal l_oh


        nonlocal l_oh
        return {"rest": rest, "avail_l_oh": avail_l_oh}


    l_oh = db_session.query(L_oh).filter(
            (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == curr_lager)).first()

    if l_oh and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty) < 0:
        avail_l_oh = True
        rest = (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang + qty)

        return generate_output()