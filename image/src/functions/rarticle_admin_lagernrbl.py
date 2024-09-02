from functions.additional_functions import *
import decimal
from models import L_lager

def rarticle_admin_lagernrbl(h_lagernr:int, artnr:int):
    flag = 0
    l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_lager


        return {"flag": flag}


    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == h_lagernr)).first()

    if not l_lager and artnr != 0:
        flag = 1

    return generate_output()