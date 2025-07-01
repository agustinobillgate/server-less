#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def dml_stockin_l_artbl(d_artnr:int):

    prepare_cache ([L_artikel])

    s_artnr = 0
    description = ""
    avail_l_artikel = False
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, description, avail_l_artikel, l_artikel
        nonlocal d_artnr

        return {"s_artnr": s_artnr, "description": description, "avail_l_artikel": avail_l_artikel}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, d_artnr)]})

    if l_artikel:
        avail_l_artikel = True
        s_artnr = l_artikel.artnr
        description = trim(l_artikel.bezeich) + " - " +\
                to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()