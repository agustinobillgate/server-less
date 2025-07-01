#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

def rarticle_admin_lagernrbl(h_lagernr:int, artnr:int):
    flag = 0
    l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_lager
        nonlocal h_lagernr, artnr

        return {"flag": flag}


    l_lager = get_cache (L_lager, {"lager_nr": [(eq, h_lagernr)]})

    if not l_lager and artnr != 0:
        flag = 1

    return generate_output()