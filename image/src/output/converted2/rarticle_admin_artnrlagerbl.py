#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def rarticle_admin_artnrlagerbl(h_artnrlager:int):
    flag = 0
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_artikel
        nonlocal h_artnrlager

        return {"flag": flag}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artnrlager)]})

    if not l_artikel:
        flag = 1

    return generate_output()