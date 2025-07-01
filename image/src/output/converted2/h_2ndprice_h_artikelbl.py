#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def h_2ndprice_h_artikelbl(dept:int):
    avail_h_artikel = False
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_artikel, h_artikel
        nonlocal dept

        return {"avail_h_artikel": avail_h_artikel}


    h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)]})

    if h_artikel:
        avail_h_artikel = True

    return generate_output()