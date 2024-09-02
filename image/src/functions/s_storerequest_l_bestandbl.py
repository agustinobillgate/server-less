from functions.additional_functions import *
import decimal
from datetime import date
from models import L_bestand, L_op

def s_storerequest_l_bestandbl(curr_lager:int, s_artnr:int, transdate:date):
    avail_l_bestand = False
    avail_l_op = False
    stock_oh = 0
    l_bestand = l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_bestand, avail_l_op, stock_oh, l_bestand, l_op


        return {"avail_l_bestand": avail_l_bestand, "avail_l_op": avail_l_op, "stock_oh": stock_oh}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

    if l_bestand:
        avail_l_bestand = True
        stock_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

        l_op = db_session.query(L_op).filter(
                (L_op.artnr == s_artnr) &  (L_op.datum == transdate) &  ((L_op.op_art == 13) |  (L_op.op_art == 14)) &  (substring(L_op.lscheinnr, 3, (len(L_op.lscheinnr) - 3)) == substring(lscheinnr, 3, (len(lscheinnr) - 3)))).first()

        if l_op:
            avail_l_op = True

    return generate_output()