from functions.additional_functions import *
import decimal
from models import L_artikel

def s_transform_l_artbl(s_artnr:int):
    description = ""
    bezeich = ""
    l_artikel_artnr = 0
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, bezeich, l_artikel_artnr, l_artikel


        return {"description": description, "bezeich": bezeich, "l_artikel_artnr": l_artikel_artnr}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit
    bezeich = l_artikel.bezeich
    l_artikel_artnr = l_artikel.artnr

    return generate_output()