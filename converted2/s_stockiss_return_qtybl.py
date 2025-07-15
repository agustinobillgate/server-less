#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand

def s_stockiss_return_qtybl(s_artnr:int, curr_lager:int, qty:Decimal):
    rest = to_decimal("0.0")
    avail_l_oh = False
    l_bestand = None

    l_oh = None

    L_oh = create_buffer("L_oh",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, avail_l_oh, l_bestand
        nonlocal s_artnr, curr_lager, qty
        nonlocal l_oh


        nonlocal l_oh

        return {"rest": rest, "avail_l_oh": avail_l_oh}


    l_oh = db_session.query(L_oh).filter(
             (L_oh.artnr == s_artnr) & (L_oh.lager_nr == curr_lager)).first()

    if l_oh and (anz_anf_best + anz_eingang - anz_ausgang + qty) < 0:
        avail_l_oh = True
        rest = ( to_decimal(anz_anf_best) + to_decimal(anz_eingang) - to_decimal(anz_ausgang) + to_decimal(qty))

        return generate_output()

    return generate_output()