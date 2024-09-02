from functions.additional_functions import *
import decimal
from models import L_artikel

def dml_stockin_l_artbl(d_artnr:int):
    s_artnr = 0
    description = ""
    avail_l_artikel = False
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, description, avail_l_artikel, l_artikel


        return {"s_artnr": s_artnr, "description": description, "avail_l_artikel": avail_l_artikel}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == d_artnr)).first()

    if l_artikel:
        avail_l_artikel = True
        s_artnr = l_artikel.artnr
        description = trim(l_artikel.bezeich) + " - " +\
                to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()