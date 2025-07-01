#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept

def rarticle_admin_artnrrezeptbl(h_artnrrezept:int, artnr:int):
    flag = 0
    h_rezept = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_rezept
        nonlocal h_artnrrezept, artnr

        return {"flag": flag}


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artnrrezept)]})

    if not h_rezept and artnr != 0:
        flag = 1

    return generate_output()