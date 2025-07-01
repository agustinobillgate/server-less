#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def s_transform_l_artbl(s_artnr:int):

    prepare_cache ([L_artikel])

    description = ""
    bezeich = ""
    l_artikel_artnr = 0
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, bezeich, l_artikel_artnr, l_artikel
        nonlocal s_artnr

        return {"description": description, "bezeich": bezeich, "l_artikel_artnr": l_artikel_artnr}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    description = l_artikel.bezeich + " - " + l_artikel.masseinheit
    bezeich = l_artikel.bezeich
    l_artikel_artnr = l_artikel.artnr

    return generate_output()