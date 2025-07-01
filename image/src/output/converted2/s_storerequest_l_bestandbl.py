#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_bestand, L_op

def s_storerequest_l_bestandbl(curr_lager:int, s_artnr:int, transdate:date):

    prepare_cache ([L_bestand])

    avail_l_bestand = False
    avail_l_op = False
    stock_oh = to_decimal("0.0")
    l_bestand = l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_bestand, avail_l_op, stock_oh, l_bestand, l_op
        nonlocal curr_lager, s_artnr, transdate

        return {"avail_l_bestand": avail_l_bestand, "avail_l_op": avail_l_op, "stock_oh": stock_oh}


    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

    if l_bestand:
        avail_l_bestand = True
        stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

        l_op = db_session.query(L_op).filter(
                 (L_op.artnr == s_artnr) & (L_op.datum == transdate) & ((L_op.op_art == 13) | (L_op.op_art == 14)) & (substring(L_op.lscheinnr, 3, (length(L_op.lscheinnr) - 3)) == substring(lscheinnr, 3, (length(lscheinnr) - 3)))).first()

        if l_op:
            avail_l_op = True

    return generate_output()