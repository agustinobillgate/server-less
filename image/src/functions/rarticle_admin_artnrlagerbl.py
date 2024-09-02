from functions.additional_functions import *
import decimal
from models import L_artikel

def rarticle_admin_artnrlagerbl(h_artnrlager:int):
    flag = 0
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_artikel


        return {"flag": flag}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == h_artnrlager)).first()

    if not l_artikel:
        flag = 1

    return generate_output()